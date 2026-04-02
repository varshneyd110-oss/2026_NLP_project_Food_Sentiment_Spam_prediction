import sqlite3

conn = sqlite3.connect("predictions.db", check_same_thread=False)
cursor = conn.cursor()

def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review TEXT,
        sentiment TEXT,
        confidence REAL
    )
    """)
    conn.commit()

def save_prediction(review, sentiment, confidence):
    cursor.execute(
        "INSERT INTO predictions (review, sentiment, confidence) VALUES (?, ?, ?)",
        (review, sentiment, confidence)
    )
    conn.commit()

def get_all_predictions():
    return cursor.execute("SELECT * FROM predictions").fetchall()

def clear_history():
    cursor.execute("DELETE FROM predictions")
    conn.commit()


# 📦 Create Table
import sqlite3

# 📦 Create Table
def create_spam_table():
    conn = sqlite3.connect("spam.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spam_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Message TEXT,
        Prediction TEXT,
        Confidence REAL
    )
    """)

    conn.commit()
    conn.close()


# 💾 Save Prediction
def save_spam_prediction(Message, Prediction, Confidence):
    conn = sqlite3.connect("spam.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO spam_predictions (Message, Prediction, Confidence) VALUES (?, ?, ?)",
        (Message, Prediction, Confidence)
    )

    conn.commit()
    conn.close()


# 📊 Get All Data
def get_all_spam_predictions():
    conn = sqlite3.connect("spam.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM spam_predictions ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()
    return data


# 🗑️ Clear History
def clear_spam_history():
    conn = sqlite3.connect("spam.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM spam_predictions")

    conn.commit()
    conn.close()