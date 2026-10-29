"""
gemini_client.py — ১৮টা Gemini key rotation + DeepSeek fallback
Gemini সব key fail হলে DeepSeek try করে
"""

import time
import google.generativeai as genai
from config import (
    GEMINI_API_KEYS,
    GEMINI_MODEL_NAME,
    GEMINI_MAX_RETRIES,
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
)

# ============================================================
#  STATE
# ============================================================
_key_index = 0
_dead_keys = set()
_usage_count = {}
_last_error = None

# ============================================================
#  KEY VALIDATE
# ============================================================
def _key_looks_valid(key):
    if not key or not isinstance(key, str):
        return False
    if key.startswith("YOUR_KEY"):
        return False
    if len(key) < 20:
        return False
    if not (key.startswith("AIza") or key.startswith("AQ.")):
        return False
    return True

def _available_keys():
    return [
        (i, k) for i, k in enumerate(GEMINI_API_KEYS)
        if _key_looks_valid(k) and k not in _dead_keys
    ]

# ============================================================
#  GEMINI GENERATE (rotation)
# ============================================================
def gemini_generate(prompt, retries=None):
    global _key_index, _last_error
    retries = retries if retries is not None else GEMINI_MAX_RETRIES
    available = _available_keys()

    if not available:
        _last_error = "কোনো valid Gemini key নেই"
        print(f"[GEMINI] {_last_error}")
        return None

    n = len(available)
    total_attempts = min(n, retries * n)

    for attempt in range(total_attempts):
        idx_in_available = (_key_index + attempt) % n
        real_index, key = available[idx_in_available]

        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(GEMINI_MODEL_NAME)
            resp = model.generate_content(prompt)
            text = resp.text.strip() if resp and resp.text else ""

            if not text:
                raise ValueError("empty response")

            _key_index = (idx_in_available + 1) % n
            _usage_count[real_index] = _usage_count.get(real_index, 0) + 1
            return text

        except Exception as e:
            msg = str(e).lower()
            _last_error = str(e)
            print(f"[GEMINI] key #{real_index + 1} failed: {e}")

            if any(x in msg for x in (
                "api key", "invalid", "401", "403",
                "permission", "leaked", "revoked", "not valid"
            )):
                _dead_keys.add(key)
            elif any(x in msg for x in ("429", "quota", "rate limit", "resource exhausted")):
                _dead_keys.add(key)

            time.sleep(0.05)
            continue

    print(f"[GEMINI] সব key fail। শেষ error: {_last_error}")
    return None

# ============================================================
#  GEMINI VISION
# ============================================================
def gemini_vision(prompt, image_b64, mime="image/jpeg"):
    import base64
    import io
    from PIL import Image

    available = _available_keys()
    if not available:
        return None

    n = len(available)
    for attempt in range(n):
        idx_in_available = (_key_index + attempt) % n
        real_index, key = available[idx_in_available]
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(GEMINI_MODEL_NAME)
            img_bytes = base64.b64decode(image_b64)
            img = Image.open(io.BytesIO(img_bytes))
            resp = model.generate_content([prompt, img])
            if resp and resp.text:
                _usage_count[real_index] = _usage_count.get(real_index, 0) + 1
                return resp.text.strip()
        except Exception as e:
            print(f"[GEMINI VISION] key #{real_index + 1} fail: {e}")
            continue
    return None

# ============================================================
#  DEEPSEEK GENERATE
# ============================================================
def deepseek_generate(prompt, image_b64=None, image_mime="image/jpeg"):
    try:
        from openai import OpenAI
        if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY.startswith("YOUR_"):
            print("[DEEPSEEK] key নেই")
            return None

        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

        if image_b64:
            content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{image_mime};base64,{image_b64}"}},
            ]
        else:
            content = prompt

        resp = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[{"role": "user", "content": content}],
            temperature=0.7,
            max_tokens=2048,
        )
        text = resp.choices[0].message.content
        return text.strip() if text else None
    except Exception as e:
        print(f"[DEEPSEEK ERROR] {e}")
        return None

# ============================================================
#  GENERATE WITH FALLBACK
# ============================================================
def generate_with_fallback(prompt):
    r = gemini_generate(prompt)
    if r:
        return r, "gemini"
    print("[FALLBACK] Gemini fail → DeepSeek try")
    r = deepseek_generate(prompt)
    if r:
        return r, "deepseek"
    return None, "none"

def vision_with_fallback(prompt, image_b64, mime="image/jpeg"):
    r = gemini_vision(prompt, image_b64, mime)
    if r:
        return r, "gemini-vision"
    print("[FALLBACK] Gemini vision fail → DeepSeek vision")
    r = deepseek_generate(prompt, image_b64=image_b64, image_mime=mime)
    if r:
        return r, "deepseek-vision"
    return None, "none"

# ============================================================
#  STATUS
# ============================================================
def get_status():
    total = len(GEMINI_API_KEYS)
    valid = sum(1 for k in GEMINI_API_KEYS if _key_looks_valid(k))
    dead = len(_dead_keys)
    alive = max(0, valid - dead)

    return {
        "total_keys": total,
        "configured": valid,
        "dead": dead,
        "alive": alive,
        "usage": dict(_usage_count),
        "last_error": _last_error,
        "deepseek_configured": bool(
            DEEPSEEK_API_KEY and not DEEPSEEK_API_KEY.startswith("YOUR_")
        ),
    }

def reset_dead_keys():
    global _dead_keys
    _dead_keys = set()
    print("[GEMINI] সব dead key reset হয়েছে।")