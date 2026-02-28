"""
Label openclaw documents using OpenAI API (ground truth generation).
Reads file content from disk on the fly — never holds all docs in memory.

Usage: OPENAI_API_KEY=your_key python label_openclaw_data.py --data data/openclaw_29106.json
"""

import argparse
import json
import math
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openclaw")

SYSTEM_PROMPT = (
    "You are a codebase expert. Given a GitHub issue description and a source code file, "
    "determine whether modifying this file would be necessary or highly relevant to fixing "
    "the described issue. Respond with only YES or NO."
)

USER_PROMPT = """GitHub Issue:
{query}

Source File:
{document}

Is this file relevant to fixing the described issue? Respond with only YES or NO."""


def read_file(file_path):
    fullpath = os.path.join(REPO, file_path)
    with open(fullpath, "r", errors="replace") as f:
        content = f.read()
    return f"// FILE: {file_path}\n{content}"


def label_one(query, file_path, api_key):
    """Read file from disk, call OpenAI, return (label, score)."""
    document = read_file(file_path)
    if len(document) > 60000:
        document = document[:30000] + "\n\n... [truncated] ...\n\n" + document[-30000:]

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT.format(query=query, document=document)},
            ],
            "temperature": 0,
            "max_tokens": 1,
            "logprobs": True,
            "top_logprobs": 5,
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    choice = data["choices"][0]
    token = choice["message"]["content"].strip().upper()
    top_logprobs = choice["logprobs"]["content"][0]["top_logprobs"]

    yes_lp, no_lp = None, None
    for entry in top_logprobs:
        t = entry["token"].strip().upper()
        if t == "YES" and yes_lp is None:
            yes_lp = entry["logprob"]
        elif t == "NO" and no_lp is None:
            no_lp = entry["logprob"]

    if yes_lp is not None and no_lp is not None:
        score = 1.0 / (1.0 + math.exp(no_lp - yes_lp))
    elif yes_lp is not None:
        score = math.exp(yes_lp)
    elif no_lp is not None:
        score = 1.0 - math.exp(no_lp)
    else:
        score = 1.0 if token == "YES" else 0.0

    label = 1 if score >= 0.9 else 0
    return label, score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()

    api_key = os.environ["OPENAI_API_KEY"]

    # Index file is lightweight (~200KB), safe to load fully
    with open(args.data) as f:
        entries = json.load(f)

    todo = [(i, e) for i, e in enumerate(entries) if e["label"] is None]
    done = len(entries) - len(todo)
    query = entries[0]["query"]
    print(f"Total: {len(entries)}, already labeled: {done}, to label: {len(todo)}")

    if not todo:
        print("All labeled.")
        return

    t0 = time.time()
    completed = 0
    errors = 0

    for batch_start in range(0, len(todo), args.batch_size):
        batch = todo[batch_start:batch_start + args.batch_size]
        results = {}

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(label_one, query, entries[i]["file_path"], api_key): i
                for i, _ in batch
            }
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    label, score = future.result()
                    results[idx] = (label, score)
                except Exception as ex:
                    errors += 1
                    print(f"  ERROR {entries[idx]['file_path']}: {ex}")

        # Apply results
        for idx, (label, score) in results.items():
            entries[idx]["label"] = label
            entries[idx]["score"] = score

        # Checkpoint
        with open(args.data, "w") as f:
            json.dump(entries, f, indent=2)

        completed += len(batch)
        n_pos = sum(1 for e in entries if e.get("label") == 1)
        elapsed = time.time() - t0
        rate = completed / elapsed if elapsed > 0 else 0
        eta = (len(todo) - completed) / rate if rate > 0 else 0
        print(f"  [{completed}/{len(todo)}] {rate:.1f} docs/s, "
              f"ETA {eta:.0f}s, positives: {n_pos}, errors: {errors}")

    n_pos = sum(1 for e in entries if e.get("label") == 1)
    n_neg = sum(1 for e in entries if e.get("label") == 0)
    print(f"\nDone. Positives: {n_pos}, Negatives: {n_neg}, Errors: {errors}")
    print("Positive files:")
    for e in entries:
        if e.get("label") == 1:
            print(f"  {e['file_path']} (score={e.get('score', '?'):.4f})")


if __name__ == "__main__":
    main()
