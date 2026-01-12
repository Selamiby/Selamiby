"""Auto-generated Database Manager"""

import sqlite3
from typing import List, Dict, Any


class DatabaseManager:
    def __init__(self, db_path: str = "nexus.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def execute(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return [dict(row) for row in cursor.fetchall()]

    def create_table(self, table_name: str, columns: Dict[str, str]):
        cols = ", ".join([f"{k} {v}" for k, v in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})"
        self.execute(query)
