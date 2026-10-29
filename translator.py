"""
translator.py — ১০৫ ভাষায় translate করে
৩ layer:
  Layer 1: cache (আগে translate করা থাকলে)
  Layer 2: Gemini (grammar নিখুঁত)
  Layer 3: original text (fail হলে)
"""

from collections import OrderedDict

from config import TRANSLATE_CACHE_SIZE, SIMPLE_LANGUAGE_ENABLED
from languages import get_language_info, get_grammar_order
from gemini_client import gemini_generate


# ============================================================
#  CACHE (আগে translate করা মনে রাখে)
# ============================================================
_cache = OrderedDict()


def _cache_key(text, target_lang):
    return f"{target_lang}::{text}"


def _cache_get(text, target_lang):
    key = _cache_key(text, target_lang)
    if key in _cache:
        # LRU: শেষে সরাও
        _cache.move_to_end(key)
        return _cache[key]
    return None


def _cache_set(text, target_lang, translated):
    key = _cache_key(text, target_lang)
    _cache[key] = translated
    # সাইজ limit
    while len(_cache) > TRANSLATE_CACHE_SIZE:
        _cache.popitem(last=False)


def clear_cache():
    _cache.clear()


# ============================================================
#  SIMPLE LANGUAGE PROMPT
# ============================================================
def _simple_prompt_text():
    if SIMPLE_LANGUAGE_ENABLED:
        return (
            "Use very simple, easy-to-understand language, "
            "like explaining to a 10-year-old child. "
            "Use short sentences and common words."
        )
    return "Use clear and natural language."


# ============================================================
#  CORE: translate
# ============================================================
def translate(text, target_lang, use_cache=True):
    """
    text কে target_lang এ translate করে
    target_lang: "Bengali", "Hindi", "Arabic"...
    """
    if not text or not text.strip():
        return text

    # ইংরেজি → ইংরেজি, translate দরকার নেই
    if target_lang.lower() in ("english", "en"):
        return text

    # cache check
    if use_cache:
        cached = _cache_get(text, target_lang)
        if cached:
            return cached

    # ভাষার তথ্য
    info = get_language_info(target_lang)
    native = info["native"] if info else target_lang

    # Gemini prompt
    prompt = (
        f"Translate the following text into {target_lang} ({native}). "
        f"{_simple_prompt_text()} "
        f"Only return the translated text, nothing else. "
        f"Do not add quotes or explanations.\n\n"
        f"Text:\n{text}"
    )

    result = gemini_generate(prompt)

    if result:
        if use_cache:
            _cache_set(text, target_lang, result)
        return result

    # fail → original ফেরত
    print(f"[TRANSLATOR] translate fail ({target_lang}), original ফেরত")
    return text


# ============================================================
#  MULTI-LANGUAGE (একসাথে কয়েক ভাষায়)
# ============================================================
def translate_multi(text, target_langs):
    """
    একসাথে কয়েকটা ভাষায় translate
    return: {lang: translated_text}
    """
    results = {}
    for lang in target_langs:
        results[lang] = translate(text, lang)
    return results


# ============================================================
#  GRAMMAR-AWARE TRANSLATE (ভবিষ্যতে)
# ============================================================
def translate_with_grammar(text, target_lang):
    """
    grammar order মাথায় রেখে translate
    (Gemini কে grammar hint দেয়)
    """
    if not text or not text.strip():
        return text

    if target_lang.lower() in ("english", "en"):
        return text

    order = get_grammar_order(target_lang)
    info = get_language_info(target_lang)
    native = info["native"] if info else target_lang

    order_desc = {
        "SVO": "Subject-Verb-Object",
        "SOV": "Subject-Object-Verb",
        "VSO": "Verb-Subject-Object",
    }.get(order, "natural")

    prompt = (
        f"Translate the following text into {target_lang} ({native}). "
        f"Follow the natural {order_desc} sentence order of this language. "
        f"{_simple_prompt_text()} "
        f"Only return the translated text, nothing else.\n\n"
        f"Text:\n{text}"
    )

    result = gemini_generate(prompt)
    return result if result else text


# ============================================================
#  DETECT + TRANSLATE (একসাথে)
# ============================================================
def translate_to_user_language(text, user_lang):
    """
    user-এর ভাষায় translate (ইংরেজি হলে skip)
    """
    if user_lang.lower() in ("english", "en"):
        return text
    return translate(text, user_lang)


# ============================================================
#  CACHE STATS
# ============================================================
def cache_stats():
    return {
        "size": len(_cache),
        "max_size": TRANSLATE_CACHE_SIZE,
    }