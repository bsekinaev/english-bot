import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import os

def init_db():
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        translation TEXT NOT NULL,
        example TEXT,
        level TEXT,
        category TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        user_id INTEGER NOT NULL,
        word_id INTEGER NOT NULL,
        last_reviewed TEXT,
        next_review TEXT,
        correct_answers INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, word_id),
        FOREIGN KEY (word_id) REFERENCES words(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        registration_date TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def fill_initial_data():
    init_db()
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM words')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'words.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            words_data = json.load(f)
            
        for category, items in words_data.items():
            for item in items:
                cursor.execute(
                    'INSERT INTO words (word, translation, example, level, category) VALUES (?, ?, ?, ?, ?)',
                    (item['word'], item['translation'], item.get('example', ''), item.get('level', 'A1'), category)
                )
    except Exception as e:
        print(f"Error loading words: {e}")
    finally:
        conn.commit()
        conn.close()

def register_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)',
            (user_id, username, first_name, last_name, datetime.now().isoformat())
        )
        conn.commit()
    finally:
        conn.close()

def save_word(user_id, word, translation):
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO words (word, translation) VALUES (?, ?)',
            (word, translation)
        )
        word_id = cursor.lastrowid
        cursor.execute(
            'INSERT INTO user_progress (user_id, word_id, last_reviewed, next_review) VALUES (?, ?, ?, ?)',
            (user_id, word_id, datetime.now().isoformat(), (datetime.now() + timedelta(days=1)).isoformat())
        )
        conn.commit()
    except Exception as e:
        print(f"Error saving word: {e}")
    finally:
        conn.close()

def get_random_word(user_id):
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT w.id, w.word, w.translation, w.example 
        FROM words w
        LEFT JOIN user_progress up ON w.id = up.word_id AND up.user_id = ?
        WHERE up.word_id IS NULL OR up.next_review < CURRENT_TIMESTAMP
        ORDER BY RANDOM()
        LIMIT 1
        ''', (user_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def get_words_to_review(user_id):
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT w.word, w.translation 
        FROM words w
        JOIN user_progress up ON w.id = up.word_id
        WHERE up.user_id = ? AND up.next_review <= ?
        ORDER BY up.next_review ASC
        LIMIT 10
        ''', (user_id, datetime.now().isoformat()))
        return cursor.fetchall()
    finally:
        conn.close()

def mark_word_as_learned(user_id, word_id):
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT OR REPLACE INTO user_progress 
        (user_id, word_id, last_reviewed, next_review, correct_answers) 
        VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id, 
            word_id,
            datetime.now().isoformat(),
            (datetime.now() + timedelta(days=3)).isoformat(),
            1
        ))
        conn.commit()
    finally:
        conn.close()

def get_user_stats(user_id):
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    try:
        # Общее количество изученных слов
        cursor.execute('SELECT COUNT(*) FROM user_progress WHERE user_id = ?', (user_id,))
        total_words = cursor.fetchone()[0]
        
        # Количество правильных ответов
        cursor.execute('SELECT SUM(correct_answers) FROM user_progress WHERE user_id = ?', (user_id,))
        correct_answers = cursor.fetchone()[0] or 0
        
        # Процент правильных ответов
        accuracy = round((correct_answers / (total_words * 3)) * 100 if total_words > 0 else 0)
        
        return {
            'total_words': total_words,
            'correct_answers': correct_answers,
            'accuracy': accuracy
        }
    finally:
        conn.close()

def get_all_users():
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT user_id FROM users')
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()

# Инициализация при первом импорте
fill_initial_data()