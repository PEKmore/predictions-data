# 🌱 organism — a seed that grows into your own AI agent

You asked for a small "genome" of code that — like an egg and sperm cell —
starts simple but **algorithmically grows** into something complex: an AI
agent that **learns from the internet** and **adheres to you**.

This is the honest, working version of that idea.

## First, the honest part (it makes the rest better)

A genome doesn't "wake up" into a mind on its own. It's a compact set of
instructions that grows complexity **only because it runs inside a rich
environment** — a cell, a body, a world. Code is the same. A small seed *can*
grow into something powerful, but the intelligence has to come from somewhere:

- **what it accumulates** — memory and data it gathers over its lifetime, and
- **what it reasons with** — either a model it talks to, or feedback over time.

No short program turns into AGI by itself; anyone who tells you otherwise is
selling science fiction. So this seed doesn't pretend to. Instead it gives you
the **real** mechanisms of growth, all of which genuinely work today.

## What actually grows here

| Biological idea        | What the code really does                                              |
|------------------------|------------------------------------------------------------------------|
| Genome → body          | A tiny seed builds its own `.organism/` body (memory, skills, logs).   |
| Growing complexity     | A persistent SQLite **memory** that accumulates knowledge across runs. |
| Learning from world    | **Polite web ingestion** (obeys `robots.txt`) digests pages → memory.  |
| Gaining new abilities  | A **skill system** the organism extends — it can *write new skills*.   |
| Loyalty / instinct     | **Standing directives** it adheres to on every decision.               |
| Generations            | A generation counter that ticks up each lifetime (each run).           |

The "intelligence" layer is pluggable: with an API key it reasons with Claude;
without one it falls back to a transparent, offline recall brain so it **runs
with zero setup**.

## Run it (no installation required)

```bash
python3 grow.py          # interactive session
```

Try this sequence:

```
obey always answer concisely          # a directive it will always adhere to
tell my favourite language is python  # teach it a fact
learn https://en.wikipedia.org/wiki/Cell_(biology)   # feed it the web
recall cell                           # search what it has grown
grow weather show today's forecast    # it writes itself a NEW skill, live
status                                # see how much it has grown
what do you know about cells?         # ask it a question
```

One-shot and piped modes also work:

```bash
python3 grow.py "tell the sky is blue"
echo "recall sky" | python3 grow.py
```

## Give it a real brain (optional)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...       # now it reasons with Claude
export ORGANISM_OWNER="your name"     # who it adheres to
python3 grow.py
```

Now answers are reasoned over its grown memory + your directives, instead of
plain recall.

## The "algorithmically growing codebase", literally

`grow <name> <description>` makes the organism **write a new Python skill file**
into `.organism/grown_skills/` and load it immediately — a new command without
a restart. Every grown skill is a plain, readable file you can inspect, edit, or
delete. The organism never runs hidden or obfuscated code: growth you can audit.

## Layout

```
grow.py                     # entry point — brings the organism to life
organism/
  agent.py                  # the loop tying memory + brain + skills together
  memory.py                 # persistent growing memory (SQLite + TF-IDF recall)
  learner.py                # digests text into fact-sized memories
  web.py                    # polite, robots.txt-respecting web ingestion
  brain.py                  # reasoning: Claude if available, else local recall
  config.py                 # all behaviour tunable via env vars
  skills/                   # instinctive (built-in) skills
    base.py                 # skill framework + auto-discovery
    learn_url.py  tell.py  recall.py  directive.py  grow_skill.py
.organism/                  # the body it grows at runtime (git-ignored)
```

## Where to take it next

- Replace the TF-IDF recall with vector embeddings for richer memory.
- Add a scheduler so it learns on a cadence (a real "metabolism").
- Let the Claude brain *author* the body of grown skills, then you review them.
- Add feedback (`good`/`bad` on answers) so it learns what you value.

It's a seed. You're the environment it grows in.
