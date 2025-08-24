import sqlite3
from datetime import datetime

DB_NAME='water-tracker.db'

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS water_intake (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            intake_ml INTEGER NOT NULL,
            DATETIME TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_water_intake(user_id, intake_ml):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_today= datetime.today().strftime('%Y-%m-%d')
    cursor.execute('''
        INSERT INTO water_intake (user_id, intake_ml, DATETIME)
        VALUES (?, ?, ?)
    ''', (user_id, intake_ml, date_today))
    conn.commit()
    conn.close()

def get_intake_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT intake_ml, DATETIME FROM water_intake
        WHERE user_id = ?
        ORDER BY DATETIME DESC
    ''', (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

create_table()