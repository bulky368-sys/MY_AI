"""
config.py — সব settings এক জায়গায়
"""

import os
from dotenv import load_dotenv

# .env ফাইল থেকে API Key লোড করবে
load_dotenv()

# ============================================================
#  GEMINI API KEYS (Environment Variable থেকে লোড হবে)
# ============================================================
# .env ফাইল থেকে স্ট্রিং আকারে পড়বে এবং কমা (,) দিয়ে আলাদা করবে
_gemini_str = os.getenv("GEMINI_API_KEYS", "")
GEMINI_API_KEYS = [k.strip() for k in _gemini_str.split(",") if k.strip()]

# ============================================================
#  DEEPSEEK API KEY (Environment Variable থেকে লোড হবে)
# ============================================================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-flash"     # টেক্সট + ভিশন দুটোই

# ============================================================
#  MODEL SETTINGS
# ============================================================
GEMINI_MODEL_NAME = "gemini-2.0-flash"
SIMILARITY_THRESHOLD = 0.45
GEMINI_MAX_RETRIES = 3

# ============================================================
#  PATHS
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_DIR = os.path.join(BASE_DIR, "memory")

# ============================================================
#  FLASK (Render এর জন্য PORT ডাইনামিক করা হলো)
# ============================================================
PORT = int(os.getenv("PORT", 5000))
FLASK_HOST = "0.0.0.0"
FLASK_PORT = PORT
FLASK_DEBUG = False

# ============================================================
#  SIMPLE LANGUAGE
# ============================================================
SIMPLE_LANGUAGE_ENABLED = True
SIMPLE_LANGUAGE_TARGET = "10-year-old child"

# ============================================================
#  TRANSLATION
# ============================================================
DEFAULT_LANGUAGE = "English"
TRANSLATE_CACHE_SIZE = 500

# ============================================================
#  MEMORY SYSTEM
# ============================================================
MEMORY_MAX_TURNS = 6
MEMORY_CONTEXT_TURNS = 2

# ============================================================
#  IMAGE
# ============================================================
MAX_IMAGE_SIZE_MB = 8
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]