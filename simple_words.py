"""
simple_words.py — কঠিন শব্দকে সহজ শব্দে বদলায়
AI সহজ ভাষায় কথা বলবে
"""

import re

# ============================================================
#  কঠিন শব্দ → সহজ শব্দ (বাংলা)
# ============================================================
SIMPLE_WORDS_BN = {
    # বিজ্ঞান
    "সালোকসংশ্লেষণ": "গাছের খাবার বানানোর প্রক্রিয়া",
    "জৈব রাসায়নিক": "জীবের রাসায়নিক",
    "অণু": "খুব ছোট কণা",
    "পরমাণু": "সবচেয়ে ছোট কণা",
    "কোষ": "জীবের ক্ষুদ্র একক",
    "শক্তি": "কাজ করার সামর্থ্য",
    "মাধ্যাকর্ষণ": "পৃথিবীর টান",
    "বায়ুমণ্ডল": "পৃথিবীর চারপাশের বাতাস",
    "উদ্ভিদ": "গাছপালা",
    "প্রাণী": "জীবজন্তু",
    "রাসায়নিক": "পদার্থের গুণ",
    "পদার্থ": "যা দিয়ে সবকিছু তৈরি",
    "তাপমাত্রা": "গরম-ঠান্ডার মাত্রা",
    "বাষ্পীভবন": "পানি থেকে বাষ্প হওয়া",
    "ঘনীভবন": "বাষ্প থেকে পানি হওয়া",
    "আবহাওয়া": "একদিনের বাতাসের অবস্থা",
    "জলবায়ু": "বহুদিনের আবহাওয়ার ধরন",
    "বাস্তুতন্ত্র": "জীব ও পরিবেশের সম্পর্ক",
    "জীববিজ্ঞান": "জীব নিয়ে পড়াশোনা",
    "রসায়ন": "পদার্থ নিয়ে পড়াশোনা",
    "পদার্থবিজ্ঞান": "শক্তি ও পদার্থ নিয়ে পড়াশোনা",

    # ইতিহাস
    "স্বাধীনতা": "আজাদি",
    "যুদ্ধ": "লড়াই",
    "শাসন": "রাজত্ব",
    "সাম্রাজ্য": "বড় রাজ্য",
    "বিপ্লব": "বড় পরিবর্তন",
    "চুক্তি": "সমঝোতা",
    "সংবিধান": "দেশের মূল আইন",
    "গণতন্ত্র": "জনগণের শাসন",
    "সভ্যতা": "উন্নত সমাজ",
    "ঔপনিবেশিক": "বিদেশি শাসন",
    "আন্দোলন": "দাবির জন্য লড়াই",
    "জাতীয়তাবাদ": "দেশপ্রেম",
    "অভ্যুত্থান": "হঠাৎ বড় পরিবর্তন",
    "শহীদ": "দেশের জন্য প্রাণ দেওয়া",
    "মুক্তিযুদ্ধ": "আজাদির যুদ্ধ",

    # সাধারণ
    "গুরুত্বপূর্ণ": "জরুরি",
    "প্রয়োজনীয়": "দরকারি",
    "সম্ভাবনা": "হতে পারে এমন",
    "সমস্যা": "অসুবিধা",
    "সমাধান": "প্রতিকার",
    "উদাহরণ": "নমুনা",
    "বিশ্লেষণ": "ভেঙে দেখা",
    "ব্যাখ্যা": "বুঝিয়ে বলা",
    "তথ্য": "খবর",
    "প্রযুক্তি": "কারিগরি",
    "কম্পিউটার": "গণকযন্ত্র",
    "ইন্টারনেট": "বিশ্বব্যাপী জাল",
    "যোগাযোগ": "সংযোগ",
    "পরিবহন": "যাতায়াত",
    "অর্থনীতি": "টাকা-পয়সার ব্যবস্থা",
    "শিক্ষা": "পড়াশোনা",
    "স্বাস্থ্য": "শরীরের ভালো অবস্থা",
    "চিকিৎসা": "রোগের চিকিৎসা",
    "ঔষধ": "ওষুধ",

    # কঠিন পদ
    "তথ্য প্রযুক্তি": "কম্পিউটার-ইন্টারনেট",
    "কৃত্রিম বুদ্ধিমত্তা": "যন্ত্রের বুদ্ধি",
    "মেশিন লার্নিং": "যন্ত্রের শেখা",
    "ডেটাবেস": "তথ্যের ভাণ্ডার",
    "অ্যালগরিদম": "ধাপে ধাপে সমাধান",
    "প্রোগ্রামিং": "যন্ত্রকে নির্দেশ দেওয়া",
    "সফটওয়্যার": "কম্পিউটারের প্রোগ্রাম",
    "হার্ডওয়্যার": "কম্পিউটারের যন্ত্রাংশ",
}

# ============================================================
#  কঠিন শব্দ → সহজ শব্দ (ইংরেজি)
# ============================================================
SIMPLE_WORDS_EN = {
    "photosynthesis": "how plants make food using sunlight",
    "biochemical": "chemical in living things",
    "molecule": "very small particle",
    "atom": "smallest particle",
    "cell": "tiny unit of life",
    "energy": "ability to do work",
    "gravity": "the pull of the Earth",
    "atmosphere": "air around the Earth",
    "organism": "living thing",
    "temperature": "how hot or cold something is",
    "evaporation": "water turning into vapor",
    "condensation": "vapor turning into water",
    "ecosystem": "living things and their environment",
    "biology": "study of living things",
    "chemistry": "study of substances",
    "physics": "study of matter and energy",
    "dna": "the instruction book of life",
    "electricity": "flow of electric charge",
    "independence": "freedom",
    "war": "fight between countries",
    "empire": "large kingdom",
    "revolution": "big change",
    "treaty": "peace agreement",
    "constitution": "main law of a country",
    "democracy": "rule by the people",
    "civilization": "advanced society",
    "colonial": "foreign rule",
    "movement": "campaign for change",
    "nationalism": "love for one's country",
    "martyr": "person who dies for a cause",
    "important": "needed",
    "necessary": "needed",
    "possibility": "chance of happening",
    "problem": "difficulty",
    "solution": "answer to a problem",
    "example": "sample",
    "analysis": "breaking down to understand",
    "explanation": "clear description",
    "information": "facts and knowledge",
    "technology": "tools and machines",
    "computer": "thinking machine",
    "internet": "worldwide network",
    "communication": "sharing information",
    "transport": "moving things",
    "economy": "money system",
    "education": "learning",
    "health": "wellness of body",
    "medicine": "treatment for illness",
    "artificial intelligence": "machine thinking",
    "machine learning": "machines learning from data",
    "database": "storage of information",
    "algorithm": "step-by-step method",
    "programming": "giving instructions to machines",
    "software": "computer programs",
    "hardware": "computer parts",
}

# ============================================================
#  FUNCTION
# ============================================================
def _replace_ci(text, old, new):
    """Case-insensitive replace"""
    return re.sub(re.escape(old), new, text, flags=re.IGNORECASE)

def simplify_text(text, language="Bengali"):
    """কঠিন শব্দকে সহজ শব্দে বদলায়"""
    if not text:
        return text
    mapping = SIMPLE_WORDS_BN if language == "Bengali" else SIMPLE_WORDS_EN
    simplified = text
    for hard, easy in mapping.items():
        if language == "English":
            simplified = _replace_ci(simplified, hard, easy)
        else:
            simplified = simplified.replace(hard, easy)
    return simplified

def simplify_sentence_structure(text):
    """বাক্যকে ছোট ছোট ভাগে ভাঙে"""
    if not text:
        return text
    sentences = re.split(r"(?<=[.!?])\s+", text)
    simplified = []
    for s in sentences:
        s = s.strip()
        if not s: continue
        words = s.split()
        if len(words) > 25:
            mid = len(words) // 2
            simplified.append(" ".join(words[:mid]) + "।")
            simplified.append(" ".join(words[mid:]))
        else:
            simplified.append(s)
    return " ".join(simplified)

def make_simple(text, language="Bengali", split_sentences=True):
    """পুরো process: শব্দ বদল + বাক্য ভাঙা"""
    text = simplify_text(text, language)
    if split_sentences:
        text = simplify_sentence_structure(text)
    return text