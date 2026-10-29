"""
expander.py — ছোট উত্তরকে বড় করে, সহজ ভাষায়
নিজের code দিয়ে (Gemini নয়)
"""

import re

from simple_words import make_simple
from languages import get_language_info


# ============================================================
#  MAIN: expand
# ============================================================
def expand(short_answer, question, language="Bengali"):
    """
    ছোট উত্তরকে বড় করে, সহজ ভাষায়
    """
    if not short_answer:
        return short_answer

    # ১) কঠিন শব্দ সহজ করি
    simplified = make_simple(short_answer, language)

    # ২) বাক্য ভেঙে দেখি
    sentences = _split_sentences(simplified)

    # ৩) অংশ যোগ করি
    parts = []

    # ভূমিকা
    parts.append(_intro(question, language))

    # মূল উত্তর
    parts.append(simplified)

    # খুব ছোট হলে একটু ব্যাখ্যা
    if len(sentences) <= 1:
        parts.append(_short_note(question, simplified, language))

    # উপসংহার
    parts.append(_outro(question, language))

    return "\n\n".join(p for p in parts if p)


# ============================================================
#  SENTENCE SPLIT
# ============================================================
def _split_sentences(text):
    """বাক্য ভাগ করে"""
    if not text:
        return []
    parts = re.split(r"(?<=[.!?।])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


# ============================================================
#  INTRO (ভূমিকা)
# ============================================================
def _intro(question, language):
    if language == "Bengali":
        return "সহজ করে বলি —"
    elif language == "Hindi":
        return "सरल शब्दों में कहें तो —"
    else:
        return "Simply put —"


# ============================================================
#  SHORT NOTE (খুব ছোট হলে)
# ============================================================
def _short_note(question, answer, language):
    if language == "Bengali":
        return (
            f"মানে, \"{question}\" এর মূল উত্তর হলো — {answer} "
            f"এটা মনে রাখলে সহজে বুঝতে পারবে।"
        )
    elif language == "Hindi":
        return (
            f"यानी, \"{question}\" का मुख्य उत्तर है — {answer} "
            f"इसे याद रखने से आसानी से समझ पाओगे।"
        )
    else:
        return (
            f"In short, the main answer to \"{question}\" is — {answer} "
            f"Remember this and you'll understand easily."
        )


# ============================================================
#  OUTRO (উপসংহার)
# ============================================================
def _outro(question, language):
    if language == "Bengali":
        return (
            f"আশা করি \"{question}\" সম্পর্কে পরিষ্কার ধারণা পেয়েছো। "
            f"আরও জানতে চাইলে নির্দিষ্ট অংশটি আবার জিজ্ঞেস করো।"
        )
    elif language == "Hindi":
        return (
            f"उम्मीद है \"{question}\" के बारे में साफ समझ मिली। "
            f"और जानना चाहो तो खास हिस्सा फिर से पूछो।"
        )
    else:
        return (
            f"I hope you now have a clear idea about \"{question}\". "
            f"If you want to know more, ask about a specific part again."
        )


# ============================================================
#  EXPAND WITHOUT QUESTION (শুধু বড় করা)
# ============================================================
def expand_only(text, language="Bengali"):
    """প্রশ্ন ছাড়া শুধু text বড় করে"""
    return expand(text, "এই বিষয়টি", language)


# ============================================================
#  ADD EXAMPLES (ভবিষ্যতে)
# ============================================================
def expand_with_example(short_answer, question, example, language="Bengali"):
    """উত্তর + উদাহরণ দিয়ে বড় করে"""
    base = expand(short_answer, question, language)
    if language == "Bengali":
        return f"{base}\n\nউদাহরণ: {example}"
    elif language == "Hindi":
        return f"{base}\n\nउदाहरण: {example}"
    else:
        return f"{base}\n\nExample: {example}"