"""Persistent, growing memory — the part of the organism that actually grows.

Backed by SQLite (stdlib, zero deps) so knowledge survives across runs and
accumulates over a lifetime. Retrieval uses a pure-Python TF-IDF cosine search
so the organism can recall relevant memories without any external service.
"""
from __future__ import annotations

import math
import re
import sqlite3
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

_WORD = re.compile(r"[a-z0-9]+")
# A few extremely common words carry little signal for retrieval.
_STOP = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for",
    "is", "are", "was", "were", "be", "it", "this", "that", "with", "as",
    "at", "by", "from", "i", "you", "he", "she", "they", "we",
}


def _tokenize(text: str) -> list[str]:
    return [w for w in _WORD.findall(text.lower()) if w not in _STOP and len(w) > 1]


@dataclass
class Memory:
    id: int
    kind: str
    content: str
    source: str
    created_at: float
    score: float = 0.0


class MemoryStore:
    """The organism's long-term memory. Append-only knowledge that grows."""

    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(db_path))
        self.db.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                kind       TEXT NOT NULL,        -- fact | observation | directive | conversation
                content    TEXT NOT NULL,
                source     TEXT DEFAULT '',
                created_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS state (
                key   TEXT PRIMARY KEY,
                value TEXT
            );
            """
        )
        self.db.commit()

    # --- growth -----------------------------------------------------------
    def remember(self, content: str, kind: str = "fact", source: str = "") -> int:
        content = content.strip()
        if not content:
            return -1
        # Avoid storing exact duplicates so memory grows in knowledge, not noise.
        existing = self.db.execute(
            "SELECT id FROM memories WHERE content = ? AND kind = ?", (content, kind)
        ).fetchone()
        if existing:
            return int(existing["id"])
        cur = self.db.execute(
            "INSERT INTO memories (kind, content, source, created_at) VALUES (?,?,?,?)",
            (kind, content, source, time.time()),
        )
        self.db.commit()
        return int(cur.lastrowid)

    def remember_many(self, contents: Iterable[str], kind: str = "fact", source: str = "") -> int:
        return sum(1 for c in contents if self.remember(c, kind, source) != -1)

    # --- recall (TF-IDF cosine over the whole corpus) ---------------------
    def recall(self, query: str, limit: int = 5) -> list[Memory]:
        rows = self.db.execute(
            "SELECT id, kind, content, source, created_at FROM memories"
        ).fetchall()
        if not rows:
            return []

        docs = [_tokenize(r["content"]) for r in rows]
        n_docs = len(docs)
        df: Counter[str] = Counter()
        for d in docs:
            df.update(set(d))
        idf = {w: math.log((n_docs + 1) / (c + 1)) + 1 for w, c in df.items()}

        q_tokens = _tokenize(query)
        if not q_tokens:
            return []
        q_tf = Counter(q_tokens)
        q_vec = {w: tf * idf.get(w, 0.0) for w, tf in q_tf.items()}
        q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0

        scored: list[Memory] = []
        for row, tokens in zip(rows, docs):
            if not tokens:
                continue
            tf = Counter(tokens)
            dot = 0.0
            d_norm_sq = 0.0
            for w, t in tf.items():
                w_idf = idf.get(w, 0.0)
                val = t * w_idf
                d_norm_sq += val * val
                if w in q_vec:
                    dot += val * q_vec[w]
            d_norm = math.sqrt(d_norm_sq) or 1.0
            score = dot / (q_norm * d_norm)
            if score > 0:
                scored.append(
                    Memory(
                        id=row["id"], kind=row["kind"], content=row["content"],
                        source=row["source"], created_at=row["created_at"], score=score,
                    )
                )
        scored.sort(key=lambda m: m.score, reverse=True)
        return scored[:limit]

    def directives(self) -> list[str]:
        rows = self.db.execute(
            "SELECT content FROM memories WHERE kind='directive' ORDER BY created_at"
        ).fetchall()
        return [r["content"] for r in rows]

    def count(self) -> int:
        return int(self.db.execute("SELECT COUNT(*) AS c FROM memories").fetchone()["c"])

    # --- generic state (generation counter, etc.) -------------------------
    def get_state(self, key: str, default: str = "") -> str:
        row = self.db.execute("SELECT value FROM state WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default

    def set_state(self, key: str, value: str) -> None:
        self.db.execute(
            "INSERT INTO state (key, value) VALUES (?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        self.db.commit()

    def close(self) -> None:
        self.db.close()
