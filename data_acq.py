# === data_acq.py ===
import sqlite3
from init import db_name


def create_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lighting_events (
        timestamp TEXT,
        light_level INTEGER,
        motion_detected INTEGER,
        light_on INTEGER
    )''')
    conn.commit()
    conn.close()


def get_all_records():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM lighting_events")
    rows = c.fetchall()
    conn.close()
    return rows


def filter_records_by_light(threshold):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM lighting_events WHERE light_level < ?", (threshold,))
    rows = c.fetchall()
    conn.close()
    return rows