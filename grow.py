#!/usr/bin/env python3
"""Entry point — bring the organism to life.

Usage:
    python3 grow.py                 # interactive session (REPL)
    python3 grow.py "learn https://example.com"   # run a single command and exit
    echo "tell the sky is blue" | python3 grow.py # pipe commands in

Try, in order:
    obey always answer concisely
    tell my favourite language is python
    learn https://en.wikipedia.org/wiki/Cell_(biology)
    recall cell
    status
    grow weather report today's forecast
    what do you know about cells?
"""
from __future__ import annotations

import sys

from organism.agent import Organism

BANNER = """\
  ◍  organism seed — generation {gen}
  A small genome that grows into your AI agent. Type `help` for what I can do,
  `status` to see how much I've grown, or just ask me a question. Ctrl-D to sleep.
"""


def main(argv: list[str]) -> int:
    org = Organism()
    try:
        # One-shot mode: command passed as arguments.
        if len(argv) > 1:
            print(org.handle(" ".join(argv[1:])))
            return 0

        # Piped mode: read commands from stdin if it isn't a terminal.
        if not sys.stdin.isatty():
            for line in sys.stdin:
                out = org.handle(line)
                if out:
                    print(out)
            return 0

        # Interactive REPL.
        print(BANNER.format(gen=org.generation))
        while True:
            try:
                line = input("you › ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n…sleeping. My memory persists; I'll keep growing next time.")
                return 0
            if line in {"exit", "quit"}:
                print("…sleeping. My memory persists; I'll keep growing next time.")
                return 0
            out = org.handle(line)
            if out:
                print(out + "\n")
    finally:
        org.close()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
