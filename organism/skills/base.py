"""Skill framework — how the organism grows new capabilities.

A skill is a small, self-contained unit of behaviour. The organism discovers
skills at startup from two places:

  1. this built-in package (the "instinctive" skills it's born with), and
  2. the grown_skills directory on disk (skills it acquired during its life).

Because new skills can simply be *dropped in as files* — including files the
organism writes for itself — its codebase literally grows over time. That is
the "algorithmically growing codebase" made concrete and safe: every new
capability is an inspectable file you can read, edit, or delete.
"""
from __future__ import annotations

import importlib
import importlib.util
import pkgutil
from dataclasses import dataclass
from typing import Callable

from .. import config


@dataclass
class Context:
    """Everything a skill is handed when it runs."""
    memory: object          # MemoryStore
    args: str               # text after the command
    raw: str                # full raw input line


@dataclass
class Skill:
    name: str                       # the command word, e.g. "learn"
    help: str                       # one-line description
    run: Callable[[Context], str]   # the behaviour


_registry: dict[str, Skill] = {}


def register(skill: Skill) -> None:
    _registry[skill.name] = skill


def all_skills() -> dict[str, Skill]:
    return dict(_registry)


def get(name: str) -> Skill | None:
    return _registry.get(name)


def discover() -> None:
    """Load built-in skills, then any skills the organism has grown on disk."""
    _registry.clear()

    # 1. instinctive (built-in) skills
    import organism.skills as builtin_pkg
    for mod in pkgutil.iter_modules(builtin_pkg.__path__):
        if mod.name in {"base"}:
            continue
        module = importlib.import_module(f"organism.skills.{mod.name}")
        _maybe_register(module)

    # 2. grown skills loaded from disk
    config.ensure_dirs()
    for path in sorted(config.GROWN_SKILLS_DIR.glob("*.py")):
        if path.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"grown_{path.stem}", path)
        if not spec or not spec.loader:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            _maybe_register(module)
        except Exception as e:  # a broken grown skill must not kill the organism
            print(f"[skill load failed] {path.name}: {e}")


def _maybe_register(module) -> None:
    # A module may expose one or several skills via any module-level attribute
    # that is a Skill instance (e.g. SKILL, SKILL_LIST, ...).
    for value in vars(module).values():
        if isinstance(value, Skill):
            register(value)
