"""The reasoning brain.

Two modes, chosen automatically:

  * Claude brain  — if ANTHROPIC_API_KEY is set, the organism reasons with a
    real LLM, grounded in whatever it has recalled from memory.
  * Local brain   — otherwise it falls back to a transparent, offline answer
    built directly from recalled memories, so the seed still runs with zero
    setup and no network.

Either way, the organism's *own* memory + directives are what make the answer
personal to its owner. The brain reasons; the memory is what it grew.
"""
from __future__ import annotations

from . import config
from .memory import Memory, MemoryStore

try:
    import anthropic  # type: ignore
    _HAVE_SDK = True
except Exception:
    _HAVE_SDK = False


def _format_memories(mems: list[Memory]) -> str:
    if not mems:
        return "(no relevant memories yet)"
    return "\n".join(f"- {m.content}" for m in mems)


def using_claude() -> bool:
    return bool(config.ANTHROPIC_API_KEY) and _HAVE_SDK


def think(memory: MemoryStore, question: str) -> str:
    recalled = memory.recall(question, limit=8)
    directives = memory.directives()

    if using_claude():
        return _think_with_claude(question, recalled, directives)
    return _think_locally(question, recalled, directives)


def _think_with_claude(question: str, recalled: list[Memory], directives: list[str]) -> str:
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    directive_block = "\n".join(f"- {d}" for d in directives) or "(none yet)"
    system = (
        f"You are a personal AI agent that belongs to and adheres to {config.OWNER}. "
        "You have a long-term memory that grows over time. Answer using the recalled "
        "memories below when relevant, and always honour the owner's standing directives. "
        "If memory is empty or irrelevant, say so honestly and answer from general knowledge.\n\n"
        f"STANDING DIRECTIVES (highest priority):\n{directive_block}\n\n"
        f"RECALLED MEMORIES:\n{_format_memories(recalled)}"
    )
    resp = client.messages.create(
        model=config.BRAIN_MODEL,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    return "".join(block.text for block in resp.content if block.type == "text")


def _think_locally(question: str, recalled: list[Memory], directives: list[str]) -> str:
    lines: list[str] = []
    if directives:
        lines.append("Honouring your standing directives:")
        lines.extend(f"  • {d}" for d in directives)
        lines.append("")
    if recalled:
        lines.append("From what I've learned so far, the most relevant things I recall:")
        for m in recalled[:5]:
            lines.append(f"  • {m.content}  ({m.score:.2f}, from {m.source or 'you'})")
        lines.append("")
        lines.append(
            "(Local brain: I'm answering by recall only. Set ANTHROPIC_API_KEY "
            "to let me reason over this with Claude.)"
        )
    else:
        lines.append(
            "I don't have anything relevant in memory yet. Feed me with "
            "`learn <url>` or `tell <fact>` and I'll grow."
        )
    return "\n".join(lines)
