"""
language_detect.py — ১০৫ ভাষা detect করে
২ layer:
  Layer 1: unicode range (দ্রুত, offline, 0ms)
  Layer 2: Gemini (fallback, unicode না পেলে)
"""

from languages import (
    LANGUAGES,
    detect_language_offline,
    get_language_info,
)
from gemini_client import gemini_generate


# ============================================================
#  MAIN: detect
# ============================================================
def detect_language(text, use_gemini_fallback=True):
    """
    ভাষা detect করে (English নামে)
    ১) unicode দেখে চেষ্টা
    ২) না পেলে Gemini
    """
    if not text or not text.strip():
        return "English"

    # Layer 1: unicode (দ্রুত)
    offline = detect_language_offline(text)
    if offline != "English":
        return offline

    # ইংরেজি অক্ষর থাকলে English
    if _is_mostly_latin(text):
        return "English"

    # Layer 2: Gemini fallback
    if use_gemini_fallback:
        return _detect_with_gemini(text)

    return "English"


# ============================================================
#  LATIN CHECK (ইংরেজি অক্ষর)
# ============================================================
def _is_mostly_latin(text):
    """বেশিরভাগ অক্ষর ইংরেজি (A-Z) কিনা"""
    total = 0
    latin = 0
    for ch in text:
        if ch.isalpha():
            total += 1
            if "a" <= ch.lower() <= "z":
                latin += 1
    if total == 0:
        return True
    return (latin / total) > 0.7


# ============================================================
#  GEMINI DETECT (fallback)
# ============================================================
def _detect_with_gemini(text):
    """Gemini দিয়ে ভাষা detect"""
    prompt = (
        "What language is the following text written in? "
        "Reply with ONLY the English language name "
        "(for example: Bengali, Hindi, Arabic, French, Chinese, Japanese, English). "
        "Do not add any explanation or punctuation.\n\n"
        f"Text: {text}"
    )
    result = gemini_generate(prompt)
    if not result:
        return "English"

    lang = result.strip().split("\n")[0].strip(" .,:;")

    # আমাদের LANGUAGES এ আছে কিনা check
    if lang in LANGUAGES:
        return lang

    # alias ম্যাপ
    aliases = {
        "bangla": "Bengali",
        "farsi": "Persian",
        "mandarin": "Chinese",
        "castilian": "Spanish",
        "hindi": "Hindi",
        "urdu": "Urdu",
    }
    lang_lower = lang.lower()
    if lang_lower in aliases:
        return aliases[lang_lower]

    return lang if lang else "English"


# ============================================================
#  DETECT + INFO
# ============================================================
def detect_with_info(text):
    """
    ভাষা + তার তথ্য ফেরত দেয়
    return: {"language": "...", "native": "...", "order": "...", "code": "..."}
    """
    lang = detect_language(text)
    info = get_language_info(lang)

    if info:
        return {
            "language": lang,
            "native": info["native"],
            "order": info["order"],
            "code": info["code"],
        }
    return {
        "language": lang,
        "native": lang,
        "order": "SVO",
        "code": "unknown",
    }


# ============================================================
#  IS SUPPORTED?
# ============================================================
def is_supported(lang_name):
    """ভাষাটা আমাদের ১০৫ তালিকায় আছে কিনা"""
    return lang_name in LANGUAGES