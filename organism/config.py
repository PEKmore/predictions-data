"""Configuration for the organism.

Everything is overridable via environment variables so the seed can run in
different "environments" (a genome behaves differently depending on where it
grows). Sensible defaults mean it runs with zero setup.
"""
from __future__ import annotations

import os
from pathlib import Path

# Root where the organism keeps everything it grows: memory, generated skills,
# logs. This is the "body" the genome builds for itself.
ROOT = Path(os.environ.get("ORGANISM_HOME", Path(__file__).resolve().parent.parent / ".organism"))
MEMORY_DB = ROOT / "memory.db"
GROWN_SKILLS_DIR = ROOT / "grown_skills"
LOG_FILE = ROOT / "organism.log"

# The reasoning "brain". If an Anthropic API key is present the organism thinks
# with Claude; otherwise it falls back to a fully-local learner so it still runs.
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
BRAIN_MODEL = os.environ.get("ORGANISM_MODEL", "claude-opus-4-8")

# The owner. The organism "adheres to" this person above all else.
OWNER = os.environ.get("ORGANISM_OWNER", "the owner")

# Web manners. We are a polite citizen of the internet by default.
USER_AGENT = os.environ.get(
    "ORGANISM_USER_AGENT",
    "organism-seed/0.1 (+respectful learner; obeys robots.txt)",
)
CRAWL_DELAY_SECONDS = float(os.environ.get("ORGANISM_CRAWL_DELAY", "2.0"))
MAX_PAGE_BYTES = int(os.environ.get("ORGANISM_MAX_PAGE_BYTES", str(2_000_000)))
REQUEST_TIMEOUT = int(os.environ.get("ORGANISM_REQUEST_TIMEOUT", "15"))


def ensure_dirs() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    GROWN_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
