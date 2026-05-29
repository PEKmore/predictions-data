"""Skill: obey <directive>  — set a standing instruction the organism adheres to.

Directives are the "adhering to you" mechanism: they are stored with the
highest priority and are injected into every reasoning step, so they shape all
future behaviour. List them with `directives`.
"""
from __future__ import annotations

from .base import Context, Skill


def _run_obey(ctx: Context) -> str:
    directive = ctx.args.strip()
    if not directive:
        return "Usage: obey <a standing instruction you want me to always follow>"
    ctx.memory.remember(directive, kind="directive", source="owner")
    return f"Understood. I will adhere to: \"{directive}\""


def _run_list(ctx: Context) -> str:
    ds = ctx.memory.directives()
    if not ds:
        return "You haven't given me any standing directives yet. Use `obey <instruction>`."
    return "Standing directives I adhere to:\n" + "\n".join(f"  {i+1}. {d}" for i, d in enumerate(ds))


# Discovery registers every module-level Skill instance, so both are picked up.
SKILL = Skill(name="obey", help="obey <instruction> — give me a standing directive", run=_run_obey)
SKILL_LIST = Skill(name="directives", help="directives — list my standing instructions", run=_run_list)
