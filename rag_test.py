"""
RAG Retrieval Test — scores documents via cosine similarity.

Supports both inline documents and file_path-based data.
Usage: HF_TOKEN=your_token python rag_test.py --data data/openclaw_29106.json
"""

import argparse
import json
import math
import os

import numpy as np
from huggingface_hub import InferenceClient

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openclaw")


def load_data(path):
    with open(path) as f:
        raw = json.load(f)
    pairs = []
    for item in raw:
        query = item["query"]
        # Support both inline document and file_path
        if "file_path" in item and "document" not in item:
            fullpath = os.path.join(REPO, item["file_path"])
            with open(fullpath, "r", errors="replace") as f:
                doc = f.read()
            name = item["file_path"]
        else:
            doc = item.get("document") or item.get("code", "")
            name = doc[:80]
        label = item.get("label") if item.get("label") is not None else item.get("ground_truth_label", 0)
        pairs.append((query, doc, int(label), name))
    return pairs


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


def embed_batch(client, texts, model, batch_size=64):
    """Get embeddings in batches."""
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        result = client.feature_extraction(batch, model=model)
        # result is list of embeddings (each is list of floats)
        all_embeddings.extend(result)
        if (i + batch_size) % 256 == 0 or i + batch_size >= len(texts):
            print(f"  Embedded {min(i + batch_size, len(texts))}/{len(texts)}")
    return all_embeddings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to JSON data file")
    args = parser.parse_args()

    pairs = load_data(args.data)
    queries = list(dict.fromkeys(p[0] for p in pairs))

    client = InferenceClient(
        provider="hf-inference",
        api_key=os.environ["HF_TOKEN"],
    )
    model = "sentence-transformers/all-mpnet-base-v2"

    for query in queries:
        docs = [(doc, label, name) for q, doc, label, name in pairs if q == query]
        all_docs = [d for d, _, _ in docs]
        labels = ["POS" if l == 1 else "NEG" for _, l, _ in docs]
        names = [n for _, _, n in docs]
        n_pos = labels.count("POS")
        n_neg = labels.count("NEG")

        print(f"Query: {query[:120]}...")
        print(f"Total docs: {len(all_docs)} ({n_pos} positive, {n_neg} negative)")
        print("Embedding documents...")

        # Embed query
        q_emb = client.feature_extraction(query, model=model)

        # Embed all documents in batches
        doc_embs = embed_batch(client, all_docs, model)

        # Compute cosine similarity
        scores = [cosine_similarity(q_emb, d_emb) for d_emb in doc_embs]

        ranked = sorted(zip(scores, labels, names), key=lambda x: -x[0])

        print("=" * 100)
        print(f"{'Rank':<5} {'Score':<8} {'Label':<6} {'File'}")
        print("-" * 100)

        for i, (score, label, name) in enumerate(ranked[:50], 1):
            marker = "Y" if label == "POS" else " "
            print(f"{i:<5} {score:<8.4f} {label:<6} {marker} {name}")

        if len(ranked) > 50:
            print(f"  ... ({len(ranked) - 50} more documents not shown)")

        # Metrics
        print("\n" + "=" * 100)
        print("RETRIEVAL METRICS")
        print("=" * 100)

        for k in [1, 3, 5, 10, 20]:
            top_k_labels = [label for _, label, _ in ranked[:k]]
            precision = top_k_labels.count("POS") / k
            recall = top_k_labels.count("POS") / n_pos if n_pos else 0
            hit = 1 if "POS" in top_k_labels else 0
            print(f"  Precision@{k}: {precision:.2f}  |  Recall@{k}: {recall:.2f}  |  Hit@{k}: {hit}")

        for i, (_, label, _) in enumerate(ranked, 1):
            if label == "POS":
                print(f"  MRR: {1/i:.4f} (first positive doc at rank {i})")
                break

        neg_above = 0
        for _, label, _ in ranked:
            if label == "POS":
                break
            neg_above += 1
        print(f"\n  Negative docs ranked ABOVE first positive: {neg_above}")
        print(f"  -> {'RETRIEVAL FAILURE: noisy docs outrank correct docs!' if neg_above > 0 else 'Retrieval OK for this query'}")
        print()


if __name__ == "__main__":
    main()
