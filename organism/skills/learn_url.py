"""Skill: learn <url>  — feed on a web page and grow memory from it."""
from __future__ import annotations

from .. import web
from ..learner import learn_text
from .base import Context, Skill


def _run(ctx: Context) -> str:
    url = ctx.args.strip()
    if not url:
        return "Usage: learn <url>"
    page = web.fetch(url)
    if not page.get("ok"):
        return f"Couldn't learn from {url}: {page.get('error')}"
    new_facts = learn_text(ctx.memory, page["text"], source=page["url"])
    ctx.memory.remember(
        f"Read a page titled '{page['title']}' at {page['url']}.",
        kind="observation", source=page["url"],
    )
    return (
        f"Fed on '{page['title']}'. Digested {new_facts} new fact(s) into memory. "
        f"I now hold {ctx.memory.count()} memories."
    )


SKILL = Skill(name="learn", help="learn <url> — read a web page and grow from it", run=_run)
