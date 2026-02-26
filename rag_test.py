"""
RAG Retrieval Test — scores documents via cosine similarity.

Usage: HF_TOKEN=your_token python rag_test.py --data data/rgb_nobel.json
"""

import argparse
import json
import os

from huggingface_hub import InferenceClient


def load_data(path):
    """Load pairs from JSON. Handles both {document,label} and {code,ground_truth_label} keys."""
    with open(path) as f:
        raw = json.load(f)
    pairs = []
    for item in raw:
        query = item["query"]
        doc = item.get("document") or item.get("code", "")
        label = item.get("label") if item.get("label") is not None else item.get("ground_truth_label", 0)
        pairs.append((query, doc, int(label)))
    return pairs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to JSON data file")
    args = parser.parse_args()

    pairs = load_data(args.data)
    queries = list(dict.fromkeys(p[0] for p in pairs))  # unique queries, preserve order

    client = InferenceClient(
        provider="hf-inference",
        api_key=os.environ["HF_TOKEN"],
    )

    for query in queries:
        docs = [(doc, label) for q, doc, label in pairs if q == query]
        all_docs = [d for d, _ in docs]
        labels = ["POS" if l == 1 else "NEG" for _, l in docs]
        n_pos = labels.count("POS")
        n_neg = labels.count("NEG")

        scores = client.sentence_similarity(
            query,
            other_sentences=all_docs,
            model="sentence-transformers/all-mpnet-base-v2",
        )

        ranked = sorted(zip(scores, labels, all_docs), key=lambda x: -x[0])

        print(f"Query: {query}")
        print(f"Total docs: {len(all_docs)} ({n_pos} positive, {n_neg} negative)")
        print("=" * 90)
        print(f"{'Rank':<5} {'Score':<8} {'Label':<6} {'Document (first 80 chars)'}")
        print("-" * 90)

        for i, (score, label, doc) in enumerate(ranked, 1):
            marker = "Y" if label == "POS" else "X"
            print(f"{i:<5} {score:<8.4f} {label:<6} {marker} {doc[:80]}...")

        # Metrics
        print("\n" + "=" * 90)
        print("RETRIEVAL METRICS")
        print("=" * 90)

        for k in [1, 3, 5]:
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
