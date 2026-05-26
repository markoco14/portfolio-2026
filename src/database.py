import sqlite3
from pathlib import Path

DB_PATH = Path("markodevo.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    return conn

def init_db():
    conn = get_conn()
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.commit()
    conn.close()

