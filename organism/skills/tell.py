"""Skill: tell <fact>  — teach the organism something directly."""
from __future__ import annotations

from .base import Context, Skill


def _run(ctx: Context) -> str:
    fact = ctx.args.strip()
    if not fact:
        return "Usage: tell <something you want me to remember>"
    ctx.memory.remember(fact, kind="fact", source="owner")
    return f"Remembered. I now hold {ctx.memory.count()} memories."


SKILL = Skill(name="tell", help="tell <fact> — teach me something to remember", run=_run)
