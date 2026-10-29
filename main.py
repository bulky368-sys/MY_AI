import time
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import FLASK_HOST, FLASK_PORT
from brain import brain
from gemini_client import (
    generate_with_fallback,
    vision_with_fallback,
    get_status as gemini_status,
)
from translator import translate_to_user_language, cache_stats, clear_cache
from expander import expand
from language_detect import detect_language, detect_with_info
from data_loader import get_data_stats
from languages import total_languages
from memory import add_turn, get_context, clear_memory, memory_stats
from database import init_db, create_user, verify_user

app = Flask(__name__)

# CORS: Netlify বা অন্য যেকোনো ডোমেইন থেকে রিকোয়েস্ট অ্যালাও করবে
CORS(app, resources={r"/*": {"origins": "*"}})

init_db()

def _expand_lang(user_lang):
    if user_lang == "Bengali": return "Bengali"
    if user_lang == "Hindi": return "Hindi"
    return "English"

# ============================================================
#  AUTH ROUTES
# ============================================================
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(force=True, silent=True) or {}
    name, email, password = data.get("name"), data.get("email"), data.get("password")
    if not name or not email or not password:
        return jsonify({"error": "সব ঘর পূরণ করুন"}), 400
    if create_user(name, email, password):
        return jsonify({"message": "সফলভাবে অ্যাকাউন্ট তৈরি হয়েছে"})
    return jsonify({"error": "এই ইমেইল দিয়ে আগেই অ্যাকাউন্ট খোলা হয়েছে"}), 400

@app.route("/signin", methods=["POST"])
def signin():
    data = request.get_json(force=True, silent=True) or {}
    user = verify_user(data.get("email"), data.get("password"))
    if user:
        return jsonify({"message": "লগইন সফল", "user_id": str(user["id"]), "name": user["name"]})
    return jsonify({"error": "ইমেইল বা পাসওয়ার্ড ভুল"}), 401

# ============================================================
#  AI ROUTES
# ============================================================
@app.route("/ask", methods=["POST"])
def ask():
    t0 = time.time()
    body = request.get_json(force=True, silent=True) or {}
    question = (body.get("question") or "").strip()
    user_id = body.get("user_id", "default")

    if not question:
        return jsonify({"answer": "প্রশ্ন খালি।", "error": True}), 400

    user_lang = detect_language(question)
    local = brain.search(question)
    
    if local:
        answer, score = local
        source = f"local ({score:.2f})"
    else:
        context = get_context(user_id)
        prompt = (
            "Answer the following question clearly and in very simple language, "
            "like explaining to a 10-year-old child. Use short sentences.\n"
        )
        if context: prompt += f"\nPrevious conversation:\n{context}\n"
        prompt += f"\nQuestion: {question}"

        answer, src = generate_with_fallback(prompt)
        if not answer: answer = "দুঃখিত, এই মুহূর্তে উত্তর দিতে পারছি না।"
        source = src

    answer = expand(answer, question, language=_expand_lang(user_lang))
    answer = translate_to_user_language(answer, user_lang)
    add_turn(user_id, question, answer)

    return jsonify({
        "answer": answer, "source": source, "lang": user_lang,
        "time_ms": round((time.time() - t0) * 1000)
    })

@app.route("/ask_image", methods=["POST"])
def ask_image():
    t0 = time.time()
    body = request.get_json(force=True, silent=True) or {}
    image_b64 = body.get("image")
    question = (body.get("question") or "এই ছবিতে কী আছে?").strip()
    user_id = body.get("user_id", "default")
    mime = body.get("mime", "image/jpeg")

    if not image_b64:
        return jsonify({"answer": "ছবি পাওয়া যায়নি।", "error": True}), 400

    prompt = f"Describe this image and answer in simple language.\nQuestion: {question}"
    answer, source = vision_with_fallback(prompt, image_b64, mime)

    if not answer:
        return jsonify({"answer": "দুঃখিত, ছবিটি বুঝতে পারিনি।", "source": "none"})

    user_lang = detect_language(question)
    answer = expand(answer, question, language=_expand_lang(user_lang))
    answer = translate_to_user_language(answer, user_lang)
    add_turn(user_id, f"[ছবি] {question}", answer)

    return jsonify({
        "answer": answer, "source": source, "lang": user_lang,
        "time_ms": round((time.time() - t0) * 1000)
    })

@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        "brain": brain.stats(), "data": get_data_stats(),
        "gemini": gemini_status(), "cache": cache_stats(),
        "languages_supported": total_languages(),
    })

@app.route("/retrain", methods=["POST"])
def retrain():
    ok = brain.train(verbose=True)
    return jsonify({"trained": ok, "brain": brain.stats()})

@app.route("/reset_cache", methods=["POST"])
def reset_cache():
    clear_cache()
    return jsonify({"ok": True, "cache": cache_stats()})

@app.route("/")
def home():
    return jsonify({"status": "MY_AI Server is running ✅"})

# ============================================================
#  RUN
# ============================================================
if __name__ == "__main__":
    print("MY_AI Server চালু হচ্ছে...")
    brain.train(verbose=True)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False)