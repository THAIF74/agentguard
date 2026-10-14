import hashlib
import json
import sqlite3
import time
from typing import Optional


GENESIS_HASH = "0" * 64


class AuditLog:
    def __init__(self, db_path: str = "audit.db"):
        self.db_path = db_path
        self._init()

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    tool TEXT NOT NULL,
                    args TEXT NOT NULL,
                    allowed INTEGER NOT NULL,
                    reason TEXT,
                    prev_hash TEXT NOT NULL,
                    entry_hash TEXT NOT NULL
                )
            """)

    def _last_hash(self, conn) -> str:
        row = conn.execute(
            "SELECT entry_hash FROM audit ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return row["entry_hash"] if row else GENESIS_HASH

    @staticmethod
    def _compute_hash(prev_hash, timestamp, tool, args_json, allowed, reason) -> str:
        payload = f"{prev_hash}|{timestamp}|{tool}|{args_json}|{int(allowed)}|{reason or ''}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def append(self, tool: str, args: dict, allowed: bool, reason: Optional[str] = None):
        args_json = json.dumps(args, sort_keys=True)
        ts = time.time()
        with self._conn() as conn:
            prev = self._last_hash(conn)
            entry_hash = self._compute_hash(prev, ts, tool, args_json, allowed, reason)
            conn.execute(
                "INSERT INTO audit (timestamp, tool, args, allowed, reason, prev_hash, entry_hash) "
                "VALUES (?,?,?,?,?,?,?)",
                (ts, tool, args_json, int(allowed), reason, prev, entry_hash),
            )

    def entries(self, limit: int = 100):
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM audit ORDER BY id ASC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    def verify(self):
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM audit ORDER BY id ASC").fetchall()

        prev = GENESIS_HASH
        for row in rows:
            expected = self._compute_hash(
                prev, row["timestamp"], row["tool"], row["args"],
                bool(row["allowed"]), row["reason"],
            )
            if row["prev_hash"] != prev:
                return False, f"Chain broken at id={row['id']}: prev_hash mismatch", row["id"]
            if row["entry_hash"] != expected:
                return False, f"Tampered entry at id={row['id']}: hash mismatch", row["id"]
            prev = row["entry_hash"]
        return True, f"OK - {len(rows)} entries verified", None