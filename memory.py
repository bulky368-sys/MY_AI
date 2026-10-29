"""
memory.py — Conversation Memory System
ইউজার যে টপিক নিয়ে কথা বলছে মনে রাখে
"""

import os
import json
import time

from config import BASE_DIR, MEMORY_MAX_TURNS, MEMORY_CONTEXT_TURNS

MEMORY_DIR = os.path.join(BASE_DIR, "memory")

# ============================================================
#  DIR
# ============================================================
def _ensure_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)

def _memory_path(user_id):
    safe = "".join(c for c in user_id if c.isalnum() or c in "-_") or "default"
    return os.path.join(MEMORY_DIR, f"{safe}.json")

# ============================================================
#  LOAD / SAVE
# ============================================================
def load_memory(user_id="default"):
    _ensure_dir()
    path = _memory_path(user_id)
    if not os.path.exists(path):
        return {"turns": [], "topic": "", "updated": 0}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"turns": [], "topic": "", "updated": 0}

def save_memory(user_id, memory):
    _ensure_dir()
    memory["updated"] = int(time.time())
    with open(_memory_path(user_id), "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# ============================================================
#  ADD TURN
# ============================================================
def add_turn(user_id, question, answer, topic=""):
    mem = load_memory(user_id)
    mem["turns"].append({
        "q": question,
        "a": answer,
        "t": int(time.time()),
    })
    if len(mem["turns"]) > MEMORY_MAX_TURNS:
        mem["turns"] = mem["turns"][-MEMORY_MAX_TURNS:]
    if topic:
        mem["topic"] = topic
    save_memory(user_id, mem)
    return mem

# ============================================================
#  GET CONTEXT
# ============================================================
def get_context(user_id="default", max_turns=None):
    max_turns = max_turns or MEMORY_CONTEXT_TURNS
    mem = load_memory(user_id)
    turns = mem.get("turns", [])[-max_turns:]
    if not turns:
        return ""
    lines = []
    for t in turns:
        lines.append(f"User: {t['q']}")
        lines.append(f"Assistant: {t['a']}")
    return "\n".join(lines)

def get_topic(user_id="default"):
    return load_memory(user_id).get("topic", "")

# ============================================================
#  CLEAR
# ============================================================
def clear_memory(user_id="default"):
    path = _memory_path(user_id)
    if os.path.exists(path):
        os.remove(path)
    return True

def memory_stats(user_id="default"):
    mem = load_memory(user_id)
    return {
        "turns": len(mem.get("turns", [])),
        "topic": mem.get("topic", ""),
        "updated": mem.get("updated", 0),
    }