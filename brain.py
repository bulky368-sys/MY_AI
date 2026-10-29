"""
brain.py — sklearn দিয়ে data/*.json train করে
প্রশ্নের সাথে সবচেয়ে মিলে যাওয়া উত্তর খোঁজে
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import SIMILARITY_THRESHOLD
from data_loader import load_all_data

# ============================================================
#  TEXT NORMALIZE
# ============================================================
def normalize(text):
    """ছোট হাতের, punctuation বাদ, extra space সরায়"""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ============================================================
#  BRAIN CLASS
# ============================================================
class Brain:
    def __init__(self):
        self.questions = []
        self.answers = []
        self.vectorizer = None
        self.matrix = None
        self.trained = False

    def train(self, verbose=True):
        """data/ থেকে data নিয়ে TF-IDF model train করে"""
        data = load_all_data(verbose=verbose)

        if not data:
            if verbose:
                print("[WARN] Brain: কোনো data নেই, train হয়নি।")
            self.trained = False
            return False

        self.questions = [normalize(q) for q in data.keys()]
        self.answers = list(data.values())

        # খালি প্রশ্ন বাদ
        filtered_q, filtered_a = [], []
        for q, a in zip(self.questions, self.answers):
            if q:
                filtered_q.append(q)
                filtered_a.append(a)

        if not filtered_q:
            self.trained = False
            return False

        self.questions = filtered_q
        self.answers = filtered_a

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words=None,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
        )
        self.matrix = self.vectorizer.fit_transform(self.questions)
        self.trained = True

        if verbose:
            print(f"[OK] Brain trained on {len(self.questions)} Q&A pairs.")
        return True

    def search(self, query, threshold=None):
        """সবচেয়ে মিলে যাওয়া উত্তর ফেরত দেয়, নাহলে None"""
        if not self.trained or not self.questions:
            return None

        threshold = threshold if threshold is not None else SIMILARITY_THRESHOLD

        q_norm = normalize(query)
        if not q_norm:
            return None

        try:
            q_vec = self.vectorizer.transform([q_norm])
            sims = cosine_similarity(q_vec, self.matrix).flatten()
            best_idx = int(sims.argmax())
            best_score = float(sims[best_idx])

            if best_score >= threshold:
                return self.answers[best_idx], best_score
            return None
        except Exception as e:
            print(f"[BRAIN ERROR] search: {e}")
            return None

    def stats(self):
        return {
            "trained": self.trained,
            "questions": len(self.questions),
            "vocabulary": len(self.vectorizer.vocabulary_) if self.vectorizer else 0,
        }

# ============================================================
#  GLOBAL INSTANCE
# ============================================================
brain = Brain()