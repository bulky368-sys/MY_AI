"""
database.py — ইউজার অ্যাকাউন্ট সেভ করার জন্য SQLite ডেটাবেস
"""

import sqlite3
import hashlib
import os
from config import BASE_DIR

# ডেটাবেস ফাইলের পাথ
DB_PATH = os.path.join(BASE_DIR, "users.db")

def init_db():
    """ডেটাবেস এবং টেবিল তৈরি করে (যদি আগে থেকে না থাকে)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT UNIQUE,
                    password TEXT
                 )''')
    conn.commit()
    conn.close()

def hash_password(password):
    """পাসওয়ার্ড হ্যাশ (গোপন) করে"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(name, email, password):
    """নতুন ইউজার তৈরি করে"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, hash_password(password)))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # ইমেইল আগে থেকেই থাকলে এরর দিবে
        success = False 
    conn.close()
    return success

def verify_user(email, password):
    """লগইনের সময় ইউজার যাচাই করে"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    
    # পাসওয়ার্ড হ্যাশ মিলিয়ে দেখা
    if user and user[3] == hash_password(password):
        return {"id": user[0], "name": user[1], "email": user[2]}
    return None