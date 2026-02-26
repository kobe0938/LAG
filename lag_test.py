"""
LAG Test — scores documents via LLM-as-Judge P(YES) logprob.

Usage: OPENAI_API_KEY=your_key python lag_test.py --data data/rgb_nobel.json
"""

import argparse
import json
import math
import os

import requests

SYSTEM_PROMPT = "You are a document relevance judge. Given a query and a document, determine whether the document directly answers the query. Respond with only YES or NO."

USER_PROMPT_TEMPLATE = """Query: {query}

Document: {document}

Does this document directly answer the query? Respond with only YES or NO."""


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


def judge_document(query, document, api_key):
    """Ask the LLM YES/NO, return P(YES) from logprobs as the score."""
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(
                    query=query, document=document)},
            ],
            "temperature": 0,
            "max_tokens": 1,
            "logprobs": True,
            "top_logprobs": 5,
        },
    )
    response.raise_for_status()
    data = response.json()
    choice = data["choices"][0]
    token = choice["message"]["content"].strip()
    top_logprobs = choice["logprobs"]["content"][0]["top_logprobs"]

    # Find logprobs for YES and NO tokens (case-insensitive)
    yes_lp, no_lp = None, None
    for entry in top_logprobs:
        t = entry["token"].strip().upper()
        if t == "YES" and yes_lp is None:
            yes_lp = entry["logprob"]
        elif t == "NO" and no_lp is None:
            no_lp = entry["logprob"]

    # Compute P(YES) from logprobs via softmax over YES/NO
    if yes_lp is not None and no_lp is not None:
        score = 1.0 / (1.0 + math.exp(no_lp - yes_lp))
    elif yes_lp is not None:
        score = math.exp(yes_lp)
    elif no_lp is not None:
        score = 1.0 - math.exp(no_lp)
    else:
        score = 1.0 if token.upper() == "YES" else 0.0

    return score, token


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="Path to JSON data file")
    args = parser.parse_args()

    api_key = os.environ["OPENAI_API_KEY"]
    pairs = load_data(args.data)
    queries = list(dict.fromkeys(p[0] for p in pairs))

    for query in queries:
        docs = [(doc, label) for q, doc, label in pairs if q == query]
        all_docs = [d for d, _ in docs]
        labels = ["POS" if l == 1 else "NEG" for _, l in docs]
        n_pos = labels.count("POS")
        n_neg = labels.count("NEG")

        print(f"Query: {query}")
        print(f"Judging {len(all_docs)} documents ({n_pos} positive, {n_neg} negative)")
        print("=" * 110)

        results = []
        for i, (doc, label) in enumerate(zip(all_docs, labels)):
            print(f"  Judging doc {i+1}/{len(all_docs)} [{label}]...", end=" ", flush=True)
            score, token = judge_document(query, doc, api_key)
            print(f"P(YES)={score:.4f}  token={token}")
            results.append((score, label, doc, token))

        ranked = sorted(results, key=lambda x: -x[0])

        print("\n" + "=" * 110)
        print(f"{'Rank':<5} {'P(YES)':<10} {'Token':<6} {'Label':<6} {'Document (first 80 chars)'}")
        print("-" * 110)
        for i, (score, label, doc, token) in enumerate(ranked, 1):
            marker = "Y" if label == "POS" else "X"
            print(f"{i:<5} {score:<10.4f} {token:<6} {label:<6} {marker} {doc[:75]}...")

        # Metrics
        print("\n" + "=" * 110)
        print("RETRIEVAL METRICS (LLM-as-Judge)")
        print("=" * 110)

        for k in [1, 3, 5]:
            top_k_labels = [label for _, label, _, _ in ranked[:k]]
            precision = top_k_labels.count("POS") / k
            recall = top_k_labels.count("POS") / n_pos if n_pos else 0
            hit = 1 if "POS" in top_k_labels else 0
            print(f"  Precision@{k}: {precision:.2f}  |  Recall@{k}: {recall:.2f}  |  Hit@{k}: {hit}")

        for i, (_, label, _, _) in enumerate(ranked, 1):
            if label == "POS":
                print(f"  MRR: {1/i:.4f} (first positive doc at rank {i})")
                break

        neg_above = 0
        for _, label, _, _ in ranked:
            if label == "POS":
                break
            neg_above += 1
        print(f"\n  Negative docs ranked ABOVE first positive: {neg_above}")
        print(f"  -> {'RETRIEVAL FAILURE: noisy docs outrank correct docs!' if neg_above > 0 else 'Retrieval OK for this query'}")
        print()


if __name__ == "__main__":
    main()
