import sqlite3
from pathlib import Path


class DatabaseManager:
    def __init__(self, db_path: str = "data/aetheros.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        cur = self.conn.cursor()
        # Basit kullanıcı, log ve istatistik tabloları
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric TEXT,
            value REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        self.conn.commit()

    def add_user(self, username: str, password: str):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def log_action(self, user_id: int, action: str):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO audit_logs (user_id, action) VALUES (?, ?)", (user_id, action))
        self.conn.commit()

    def add_statistic(self, metric: str, value: float):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO statistics (metric, value) VALUES (?, ?)", (metric, value))
        self.conn.commit()

    def close(self):
        self.conn.close()
        self.conn.close()
        self.conn.close()
