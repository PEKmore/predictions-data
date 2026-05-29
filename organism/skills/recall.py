"""Skill: recall <query>  — search memory directly (no reasoning layer)."""
from __future__ import annotations

from .base import Context, Skill


def _run(ctx: Context) -> str:
    query = ctx.args.strip()
    if not query:
        return "Usage: recall <query>"
    hits = ctx.memory.recall(query, limit=8)
    if not hits:
        return "Nothing relevant in memory yet."
    lines = [f"Top {len(hits)} memories for '{query}':"]
    for m in hits:
        lines.append(f"  [{m.score:.2f}] ({m.kind}) {m.content}")
    return "\n".join(lines)


SKILL = Skill(name="recall", help="recall <query> — search my memory", run=_run)
