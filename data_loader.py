"""
data_loader.py — data/ folder এর json পড়ে, validate করে
"""

import os
import json
import glob
from config import DATA_DIR

# ============================================================
#  LOAD ALL DATA
# ============================================================
def load_all_data(verbose=True):
    """
    data/ folder এর সব .json পড়ে একটা dict বানায়
    format: {"question": "answer"}
    """
    all_data = {}
    files = glob.glob(os.path.join(DATA_DIR, "*.json"))

    if not files:
        if verbose:
            print(f"[WARN] {DATA_DIR} এ কোনো json নেই।")
        return all_data

    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = json.load(f)

            if not isinstance(content, dict):
                if verbose:
                    print(f"[WARN] {os.path.basename(filepath)}: dict না, বাদ দেওয়া হলো")
                continue

            # validate each entry
            valid = {}
            for q, a in content.items():
                if isinstance(q, str) and isinstance(a, str) and q.strip() and a.strip():
                    valid[q.strip()] = a.strip()
                else:
                    if verbose:
                        print(f"[WARN] invalid entry: {q!r} → {type(a).__name__}")

            all_data.update(valid)
            if verbose:
                print(f"[OK] {os.path.basename(filepath)}: {len(valid)} entry")

        except json.JSONDecodeError as e:
            if verbose:
                print(f"[ERROR] {os.path.basename(filepath)}: JSON ভাঙা — {e}")
        except Exception as e:
            if verbose:
                print(f"[ERROR] {filepath}: {e}")

    return all_data

# ============================================================
#  STATS
# ============================================================
def get_data_stats():
    """data/ এর পরিসংখ্যান"""
    files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    stats = {"files": [], "total_entries": 0}

    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = json.load(f)
            count = len(content) if isinstance(content, dict) else 0
            stats["files"].append({
                "name": os.path.basename(filepath),
                "entries": count,
            })
            stats["total_entries"] += count
        except Exception:
            stats["files"].append({
                "name": os.path.basename(filepath),
                "entries": 0,
                "error": True,
            })

    return stats