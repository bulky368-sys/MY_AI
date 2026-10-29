"""
languages.py — পৃথিবীর ১০৫টা ভাষার তথ্য
প্রতিটা ভাষার: নাম, native নাম, grammar order, unicode range
"""

LANGUAGES = {
    # ---------- দক্ষিণ এশিয়া ----------
    "Bengali":    {"native": "বাংলা", "order": "SOV", "unicode": (0x0980, 0x09FF), "code": "bn"},
    "Hindi":      {"native": "हिन्दी", "order": "SOV", "unicode": (0x0900, 0x097F), "code": "hi"},
    "Urdu":       {"native": "اردو", "order": "SOV", "unicode": (0x0600, 0x06FF), "code": "ur"},
    "Punjabi":    {"native": "ਪੰਜਾਬੀ", "order": "SOV", "unicode": (0x0A00, 0x0A7F), "code": "pa"},
    "Gujarati":   {"native": "ગુજરાતી", "order": "SOV", "unicode": (0x0A80, 0x0AFF), "code": "gu"},
    "Marathi":    {"native": "मराठी", "order": "SOV", "unicode": (0x0900, 0x097F), "code": "mr"},
    "Tamil":      {"native": "தமிழ்", "order": "SOV", "unicode": (0x0B80, 0x0BFF), "code": "ta"},
    "Telugu":     {"native": "తెలుగు", "order": "SOV", "unicode": (0x0C00, 0x0C7F), "code": "te"},
    "Kannada":    {"native": "ಕನ್ನಡ", "order": "SOV", "unicode": (0x0C80, 0x0CFF), "code": "kn"},
    "Malayalam":  {"native": "മലയാളം", "order": "SOV", "unicode": (0x0D00, 0x0D7F), "code": "ml"},
    "Sinhala":    {"native": "සිංහල", "order": "SOV", "unicode": (0x0D80, 0x0DFF), "code": "si"},
    "Nepali":     {"native": "नेपाली", "order": "SOV", "unicode": (0x0900, 0x097F), "code": "ne"},
    "Odia":       {"native": "ଓଡ଼ିଆ", "order": "SOV", "unicode": (0x0B00, 0x0B7F), "code": "or"},
    "Assamese":   {"native": "অসমীয়া", "order": "SOV", "unicode": (0x0980, 0x09FF), "code": "as"},
    # ---------- ইউরোপ ----------
    "English":    {"native": "English", "order": "SVO", "unicode": None, "code": "en"},
    "French":     {"native": "Français", "order": "SVO", "unicode": None, "code": "fr"},
    "Spanish":    {"native": "Español", "order": "SVO", "unicode": None, "code": "es"},
    "Portuguese": {"native": "Português", "order": "SVO", "unicode": None, "code": "pt"},
    "Italian":    {"native": "Italiano", "order": "SVO", "unicode": None, "code": "it"},
    "German":     {"native": "Deutsch", "order": "SVO", "unicode": None, "code": "de"},
    "Dutch":      {"native": "Nederlands", "order": "SVO", "unicode": None, "code": "nl"},
    "Russian":    {"native": "Русский", "order": "SVO", "unicode": (0x0400, 0x04FF), "code": "ru"},
    "Ukrainian":  {"native": "Українська", "order": "SVO", "unicode": (0x0400, 0x04FF), "code": "uk"},
    "Polish":     {"native": "Polski", "order": "SVO", "unicode": None, "code": "pl"},
    "Czech":      {"native": "Čeština", "order": "SVO", "unicode": None, "code": "cs"},
    "Slovak":     {"native": "Slovenčina", "order": "SVO", "unicode": None, "code": "sk"},
    "Hungarian":  {"native": "Magyar", "order": "SVO", "unicode": None, "code": "hu"},
    "Romanian":   {"native": "Română", "order": "SVO", "unicode": None, "code": "ro"},
    "Bulgarian":  {"native": "Български", "order": "SVO", "unicode": (0x0400, 0x04FF), "code": "bg"},
    "Serbian":    {"native": "Српски", "order": "SVO", "unicode": (0x0400, 0x04FF), "code": "sr"},
    "Croatian":   {"native": "Hrvatski", "order": "SVO", "unicode": None, "code": "hr"},
    "Greek":      {"native": "Ελληνικά", "order": "SVO", "unicode": (0x0370, 0x03FF), "code": "el"},
    "Swedish":    {"native": "Svenska", "order": "SVO", "unicode": None, "code": "sv"},
    "Norwegian":  {"native": "Norsk", "order": "SVO", "unicode": None, "code": "no"},
    "Danish":     {"native": "Dansk", "order": "SVO", "unicode": None, "code": "da"},
    "Finnish":    {"native": "Suomi", "order": "SVO", "unicode": None, "code": "fi"},
    "Icelandic":  {"native": "Íslenska", "order": "SVO", "unicode": None, "code": "is"},
    "Irish":      {"native": "Gaeilge", "order": "VSO", "unicode": None, "code": "ga"},
    "Welsh":      {"native": "Cymraeg", "order": "VSO", "unicode": None, "code": "cy"},
    "Catalan":    {"native": "Català", "order": "SVO", "unicode": None, "code": "ca"},
    "Basque":     {"native": "Euskara", "order": "SOV", "unicode": None, "code": "eu"},
    "Albanian":   {"native": "Shqip", "order": "SVO", "unicode": None, "code": "sq"},
    "Macedonian": {"native": "Македонски", "order": "SVO", "unicode": (0x0400, 0x04FF), "code": "mk"},
    "Slovenian":  {"native": "Slovenščina", "order": "SVO", "unicode": None, "code": "sl"},
    "Estonian":   {"native": "Eesti", "order": "SVO", "unicode": None, "code": "et"},
    "Latvian":    {"native": "Latviešu", "order": "SVO", "unicode": None, "code": "lv"},
    "Lithuanian": {"native": "Lietuvių", "order": "SVO", "unicode": None, "code": "lt"},
    "Maltese":    {"native": "Malti", "order": "SVO", "unicode": None, "code": "mt"},
    # ---------- মধ্যপ্রাচ্য / আরবি ----------
    "Arabic":     {"native": "العربية", "order": "VSO", "unicode": (0x0600, 0x06FF), "code": "ar"},
    "Hebrew":     {"native": "עברית", "order": "SVO", "unicode": (0x0590, 0x05FF), "code": "he"},
    "Persian":    {"native": "فارسی", "order": "SOV", "unicode": (0x0600, 0x06FF), "code": "fa"},
    "Turkish":    {"native": "Türkçe", "order": "SOV", "unicode": None, "code": "tr"},
    "Kurdish":    {"native": "Kurdî", "order": "SOV", "unicode": (0x0600, 0x06FF), "code": "ku"},
    "Pashto":     {"native": "پښتو", "order": "SOV", "unicode": (0x0600, 0x06FF), "code": "ps"},
    "Azerbaijani":{"native": "Azərbaycan", "order": "SOV", "unicode": None, "code": "az"},
    "Armenian":   {"native": "Հայերեն", "order": "SVO", "unicode": (0x0530, 0x058F), "code": "hy"},
    "Georgian":   {"native": "ქართული", "order": "SVO", "unicode": (0x10A0, 0x10FF), "code": "ka"},
    # ---------- পূর্ব এশিয়া ----------
    "Chinese":    {"native": "中文", "order": "SVO", "unicode": (0x4E00, 0x9FFF), "code": "zh"},
    "Japanese":   {"native": "日本語", "order": "SOV", "unicode": (0x3040, 0x30FF), "code": "ja"},
    "Korean":     {"native": "한국어", "order": "SOV", "unicode": (0xAC00, 0xD7AF), "code": "ko"},
    "Vietnamese": {"native": "Tiếng Việt", "order": "SVO", "unicode": None, "code": "vi"},
    "Thai":       {"native": "ไทย", "order": "SVO", "unicode": (0x0E00, 0x0E7F), "code": "th"},
    "Lao":        {"native": "ລາວ", "order": "SVO", "unicode": (0x0E80, 0x0EFF), "code": "lo"},
    "Khmer":      {"native": "ខ្មែរ", "order": "SVO", "unicode": (0x1780, 0x17FF), "code": "km"},
    "Burmese":    {"native": "မြန်မာ", "order": "SOV", "unicode": (0x1000, 0x109F), "code": "my"},
    "Mongolian":  {"native": "Монгол", "order": "SOV", "unicode": (0x1800, 0x18AF), "code": "mn"},
    "Tibetan":    {"native": "བོད་སྐད", "order": "SOV", "unicode": (0x0F00, 0x0FFF), "code": "bo"},
    # ---------- দক্ষিণ-পূর্ব এশিয়া ----------
    "Indonesian": {"native": "Bahasa Indonesia", "order": "SVO", "unicode": None, "code": "id"},
    "Malay":      {"native": "Bahasa Melayu", "order": "SVO", "unicode": None, "code": "ms"},
    "Filipino":   {"native": "Filipino", "order": "VSO", "unicode": None, "code": "tl"},
    "Javanese":   {"native": "Basa Jawa", "order": "SVO", "unicode": None, "code": "jw"},
    "Sundanese":  {"native": "Basa Sunda", "order": "SVO", "unicode": None, "code": "su"},
    "Cebuano":    {"native": "Cebuano", "order": "VSO", "unicode": None, "code": "ceb"},
    # ---------- আফ্রিকা ----------
    "Swahili":    {"native": "Kiswahili", "order": "SVO", "unicode": None, "code": "sw"},
    "Amharic":    {"native": "አማርኛ", "order": "SOV", "unicode": (0x1200, 0x137F), "code": "am"},
    "Tigrinya":   {"native": "ትግርኛ", "order": "SOV", "unicode": (0x1200, 0x137F), "code": "ti"},
    "Somali":     {"native": "Soomaali", "order": "SVO", "unicode": None, "code": "so"},
    "Yoruba":     {"native": "Yorùbá", "order": "SVO", "unicode": None, "code": "yo"},
    "Igbo":       {"native": "Igbo", "order": "SVO", "unicode": None, "code": "ig"},
    "Hausa":      {"native": "Hausa", "order": "SVO", "unicode": None, "code": "ha"},
    "Zulu":       {"native": "isiZulu", "order": "SVO", "unicode": None, "code": "zu"},
    "Xhosa":      {"native": "isiXhosa", "order": "SVO", "unicode": None, "code": "xh"},
    "Afrikaans":  {"native": "Afrikaans", "order": "SVO", "unicode": None, "code": "af"},
    "Malagasy":   {"native": "Malagasy", "order": "VSO", "unicode": None, "code": "mg"},
    "Wolof":      {"native": "Wolof", "order": "SVO", "unicode": None, "code": "wo"},
    "Fula":       {"native": "Fulfulde", "order": "SVO", "unicode": None, "code": "ff"},
    "Oromo":      {"native": "Afaan Oromoo", "order": "SOV", "unicode": None, "code": "om"},
    "Shona":      {"native": "chiShona", "order": "SVO", "unicode": None, "code": "sn"},
    # ---------- মধ্য এশিয়া ----------
    "Kazakh":     {"native": "Қазақ", "order": "SOV", "unicode": (0x0400, 0x04FF), "code": "kk"},
    "Uzbek":      {"native": "Oʻzbek", "order": "SOV", "unicode": None, "code": "uz"},
    "Kyrgyz":     {"native": "Кыргыз", "order": "SOV", "unicode": (0x0400, 0x04FF), "code": "ky"},
    "Tajik":      {"native": "Тоҷикӣ", "order": "SOV", "unicode": (0x0400, 0x04FF), "code": "tg"},
    "Turkmen":    {"native": "Türkmen", "order": "SOV", "unicode": None, "code": "tk"},
    # ---------- প্রশান্ত মহাসাগরীয় / অন্যান্য ----------
    "Maori":      {"native": "Māori", "order": "VSO", "unicode": None, "code": "mi"},
    "Samoan":     {"native": "Gagana Sāmoa", "order": "VSO", "unicode": None, "code": "sm"},
    "Tongan":     {"native": "Lea Fakatonga","order": "VSO", "unicode": None, "code": "to"},
    "Fijian":     {"native": "Na Vosa Vakaviti", "order": "VSO", "unicode": None, "code": "fj"},
    "Hawaiian":   {"native": "ʻŌlelo Hawaiʻi","order": "VSO", "unicode": None, "code": "haw"},
    "Esperanto":  {"native": "Esperanto", "order": "SVO", "unicode": None, "code": "eo"},
    "Latin":      {"native": "Latina", "order": "SOV", "unicode": None, "code": "la"},
    "Maltese2":   {"native": "Malti", "order": "SVO", "unicode": None, "code": "mt"},
}


def get_language_info(lang_name):
    return LANGUAGES.get(lang_name, None)

def get_all_language_names():
    return list(LANGUAGES.keys())

def get_language_by_unicode(char):
    code = ord(char)
    for lang, info in LANGUAGES.items():
        rng = info.get("unicode")
        if rng and rng[0] <= code <= rng[1]:
            return lang
    return None

def detect_language_offline(text):
    counts = {}
    for ch in text:
        lang = get_language_by_unicode(ch)
        if lang:
            counts[lang] = counts.get(lang, 0) + 1
    if not counts:
        return "English"
    return max(counts, key=counts.get)

def get_grammar_order(lang_name):
    info = LANGUAGES.get(lang_name)
    return info["order"] if info else "SVO"

def total_languages():
    return len(LANGUAGES)