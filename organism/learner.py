"""Learning — turning raw input (web pages, files, chat) into stored knowledge.

The organism "digests" text into discrete, sentence-sized facts that get
written to long-term memory. This is deliberately simple and transparent: no
black boxes, just splitting, cleaning, and de-duplicating. Over many feedings
the memory grows, and recall gets richer — that is the learning.
"""
from __future__ import annotations

import re

from .memory import MemoryStore

_SENTENCE = re.compile(r"(?<=[.!?])\s+")
_WS = re.compile(r"\s+")


def _clean(text: str) -> str:
    return _WS.sub(" ", text).strip()


def to_facts(text: str, min_len: int = 25, max_len: int = 400) -> list[str]:
    """Break a blob of text into fact-sized, useful sentences."""
    facts: list[str] = []
    for raw_line in text.split("\n"):
        line = _clean(raw_line)
        if not line:
            continue
        for sentence in _SENTENCE.split(line):
            s = sentence.strip()
            # Keep things that look like real statements, drop nav/boilerplate.
            if min_len <= len(s) <= max_len and any(c.isalpha() for c in s):
                facts.append(s)
    # Preserve order but drop duplicates within this batch.
    seen: set[str] = set()
    unique = []
    for f in facts:
        key = f.lower()
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def learn_text(memory: MemoryStore, text: str, source: str) -> int:
    """Digest free text into memory. Returns the number of new facts stored."""
    facts = to_facts(text)
    return memory.remember_many(facts, kind="fact", source=source)
