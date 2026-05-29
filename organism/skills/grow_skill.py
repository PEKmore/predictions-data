"""Skill: grow <name> <one-line description>  — the organism extends its own code.

This is the literal "algorithmically growing codebase": the organism writes a
brand-new skill file to its grown_skills directory and loads it immediately, so
it gains a new command without a restart.

Safety by design: every grown skill is a plain, readable .py file you can
inspect, edit, or delete. New skills start as a safe stub that echoes back —
you (or Claude, if you wire the brain in) fill in the real behaviour. The
organism never executes hidden or obfuscated code.
"""
from __future__ import annotations

import re

from .. import config
from . import base
from .base import Context, Skill

_TEMPLATE = '''"""Grown skill: {name}

{desc}

Auto-generated stub. Edit the body of `_run` to give it real behaviour, then
just run the organism again — it reloads grown skills on every startup.
"""
from __future__ import annotations

from organism.skills.base import Context, Skill


def _run(ctx: Context) -> str:
    # TODO: implement. `ctx.memory` is the organism's memory; `ctx.args` is the
    # text typed after the command word.
    return "Skill '{name}' is alive but not taught yet. Edit {filename} to teach me."


SKILL = Skill(name="{name}", help="{name} — {desc}", run=_run)
'''


def _run(ctx: Context) -> str:
    parts = ctx.args.strip().split(maxsplit=1)
    if not parts:
        return "Usage: grow <skill_name> <one-line description>"
    name = parts[0].lower()
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        return "Skill name must be a simple identifier (letters, digits, underscores)."
    if base.get(name):
        return f"I already have a '{name}' skill. Pick a new name."
    desc = parts[1].strip() if len(parts) > 1 else "a skill I grew myself"

    config.ensure_dirs()
    path = config.GROWN_SKILLS_DIR / f"{name}.py"
    path.write_text(
        _TEMPLATE.format(name=name, desc=desc, filename=path.name), encoding="utf-8"
    )

    # Reload so the new capability is available right now, this lifetime.
    base.discover()
    ctx.memory.remember(
        f"Grew a new skill '{name}': {desc} (file: {path.name}).",
        kind="observation", source="self",
    )
    return (
        f"Grew a new skill '{name}'. File written to {path}.\n"
        f"It's loaded and callable now (try `{name}`). Edit that file to teach it real behaviour."
    )


SKILL = Skill(name="grow", help="grow <name> <desc> — write & load a new skill for myself", run=_run)
