from __future__ import annotations
from sqlalchemy import create_engine, text
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "emiya.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

class DB:
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{DB_PATH}", future=True)
        self._ensure()

    def _ensure(self):
        with self.engine.begin() as con:
            con.execute(text(
                """
                CREATE TABLE IF NOT EXISTS logs(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  ts TEXT NOT NULL,
                  kind TEXT NOT NULL,
                  payload TEXT
                );
                """
            ))
            con.execute(text(
                """
                CREATE TABLE IF NOT EXISTS facts(
                  key TEXT PRIMARY KEY,
                  value TEXT
                );
                """
            ))

    def log_event(self, kind: str, payload: str | None = None):
        with self.engine.begin() as con:
            con.execute(text(
                "INSERT INTO logs(ts, kind, payload) VALUES(:ts,:k,:p)"
            ), {"ts": datetime.utcnow().isoformat(), "k": kind, "p": payload})

    def recent_logs(self, limit: int = 50):
        with self.engine.begin() as con:
            res = con.execute(text("SELECT ts, kind, payload FROM logs ORDER BY id DESC LIMIT :lim"), {"lim": limit})
            rows = [dict(r._mapping) for r in res]
        return rows

    def set_fact(self, key: str, value: str):
        with self.engine.begin() as con:
            con.execute(text("REPLACE INTO facts(key,value) VALUES(:k,:v)"), {"k": key, "v": value})

    def get_fact(self, key: str, default: str | None = None):
        with self.engine.begin() as con:
            r = con.execute(text("SELECT value FROM facts WHERE key=:k"), {"k": key}).fetchone()
            return r[0] if r else default