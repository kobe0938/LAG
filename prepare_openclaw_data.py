"""
Collect all source files from the openclaw repo into a lightweight index.
Output: data/openclaw_29106.json — list of {query, file_path, label: null}
No inline document content — scripts read from disk on the fly.
"""

import json
import os

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openclaw")
EXTENSIONS = {".ts", ".js", ".tsx", ".jsx", ".mjs", ".cjs"}
SKIP = {"node_modules", ".git", ".venv"}

QUERY = """Gateway delivery-recovery replays already-delivered messages after restart. Users get duplicates from days ago.
Summary
After restarting the gateway, the delivery-recovery system re-sends messages that were already successfully delivered in previous sessions. Recipients see duplicate messages that were originally sent days or weeks earlier.
Steps to Reproduce
1. Have agents running normally with delivery history
2. Restart the gateway (e.g. openclaw gateway restart)
3. Delivery recovery runs and reports messages as "recovered"
4. Channel receives duplicate copies of old messages that were already delivered
Expected Behavior
Delivery recovery should only re-send messages that were genuinely not delivered. Already-acknowledged deliveries should be skipped.
Actual Behavior
The recovery system re-delivers messages regardless of prior delivery status. From today's logs: Delivery recovery complete: 7 recovered — but those 7 messages had already been received by the user previously (some ~1 week old).
Notes
It looks like ackDelivery() removes the queue file on success, but if the gateway is restarted between delivery and ack (or the ack write is interrupted), the file persists and gets replayed indefinitely on every subsequent restart. A delivery ID check or a "delivered" marker in the queue entry before replaying would prevent this.
Workaround
None currently — duplicates arrive silently with no user-visible warning.
Environment
* OpenClaw: 2026.2.26
* macOS 26.2 (arm64)"""


def main():
    entries = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for fname in files:
            ext = os.path.splitext(fname)[1]
            if ext not in EXTENSIONS or fname.endswith(".d.ts"):
                continue
            fullpath = os.path.join(root, fname)
            relpath = os.path.relpath(fullpath, REPO)
            entries.append({"query": QUERY, "file_path": relpath, "label": None})

    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "openclaw_29106.json")
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, "w") as f:
        json.dump(entries, f, indent=2)
    size_kb = os.path.getsize(outpath) / 1024
    print(f"Found {len(entries)} files, saved index to {outpath} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
