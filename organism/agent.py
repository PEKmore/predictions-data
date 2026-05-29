"""The organism itself — the loop that ties memory, brain, and skills together.

Think of this as the cell that the genome (the seed code) builds. It is born
with instinctive skills, it feeds and grows memory, it adheres to its owner's
directives, and it can extend its own code. Each run increments a generation
counter so you can watch it grow over its lifetime.
"""
from __future__ import annotations

from . import brain, config
from .memory import MemoryStore
from .skills import base as skills


class Organism:
    def __init__(self) -> None:
        config.ensure_dirs()
        self.memory = MemoryStore(config.MEMORY_DB)
        skills.discover()
        gen = int(self.memory.get_state("generation", "0")) + 1
        self.memory.set_state("generation", str(gen))
        self.generation = gen

    # --- one turn of life -------------------------------------------------
    def handle(self, line: str) -> str:
        line = line.strip()
        if not line:
            return ""
        command, _, rest = line.partition(" ")
        command = command.lower()

        if command in {"help", "?"}:
            return self._help()
        if command == "status":
            return self._status()

        skill = skills.get(command)
        if skill:
            ctx = skills.Context(memory=self.memory, args=rest, raw=line)
            return skill.run(ctx)

        # Anything that isn't a known command is treated as a question for the brain.
        return brain.think(self.memory, line)

    # --- introspection ----------------------------------------------------
    def _help(self) -> str:
        lines = ["I grow as you teach me. Commands I currently know:"]
        for name, sk in sorted(skills.all_skills().items()):
            lines.append(f"  {sk.help}")
        lines.append("  status — show how much I've grown")
        lines.append("  help — this list")
        lines.append("")
        lines.append("Anything else you type, I treat as a question and reason about.")
        return "\n".join(lines)

    def _status(self) -> str:
        mode = "Claude brain" if brain.using_claude() else "local brain (offline)"
        return (
            f"Generation: {self.generation}\n"
            f"Memories held: {self.memory.count()}\n"
            f"Standing directives: {len(self.memory.directives())}\n"
            f"Skills known: {len(skills.all_skills())}\n"
            f"Reasoning mode: {mode}\n"
            f"Owner I adhere to: {config.OWNER}"
        )

    def close(self) -> None:
        self.memory.close()
