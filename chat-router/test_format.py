#!/usr/bin/env python3
"""Tests for to_chat_markdown. Run: python3 chat-router/test_format.py"""

import importlib.machinery
import importlib.util
import pathlib
import sys

spec = importlib.util.spec_from_loader(
    "chat_router",
    importlib.machinery.SourceFileLoader(
        "chat_router", str(pathlib.Path(__file__).parent / "bin" / "chat-router")
    ),
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
f = mod.to_chat_markdown

CASES = [
    # Markdown Chat renders natively is passed through untouched.
    ("**bold** _it_ `code` [l](https://e.com)", "**bold** _it_ `code` [l](https://e.com)"),
    ("## Heading\ntext", "## Heading\ntext"),
    ("- one\n  - nested\n1. first", "- one\n  - nested\n1. first"),
    ("> quoted", "> quoted"),
    # Tables are fenced, because Chat concatenates cells and eats the next line.
    ("| a | b |\n|---|---|\n| 1 | 2 |\nafter",
     "```\n| a | b |\n|---|---|\n| 1 | 2 |\n```\nafter"),
    ("intro\n\n| h |\n| - |\n| v |",
     "intro\n\n```\n| h |\n| - |\n| v |\n```"),
    # Horizontal rules are dropped; Chat swallows them anyway.
    ("above\n\n---\n\nbelow", "above\n\nbelow"),
    ("above\n***\nbelow", "above\nbelow"),
    # Content inside a fence is never rewritten.
    ("```\n| not | a table |\n|---|---|\n---\n```",
     "```\n| not | a table |\n|---|---|\n---\n```"),
    # A bullet list is not mistaken for a rule.
    ("- a\n- b", "- a\n- b"),
    ("", ""),
]


def main() -> int:
    failures = 0
    for src, want in CASES:
        got = f(src)
        if got != want:
            failures += 1
            print(f"FAIL\n  in:   {src!r}\n  want: {want!r}\n  got:  {got!r}")
    total = len(CASES)

    r = mod.resolve_name
    live = {"orchestrator": {}, "chat-router-test": {}, "e2e-solo-a": {}}
    NAME_CASES = [
        ("orchestrator", ("orchestrator", "")),
        ("Orchestrator.", ("orchestrator", "")),
        ("orch", ("orchestrator", "")),
        ("send to orchestrator: ship it", ("orchestrator", "send to : ship it")),
        ("chat-router-test", ("chat-router-test", "")),
        # Ambiguous or unknown must not guess.
        ("e2", (None, "")),
        ("nobody", (None, "")),
        ("", (None, "")),
        ("yes", (None, "")),
    ]
    for src, want in NAME_CASES:
        got = r(src, live)
        if got != want:
            failures += 1
            print(f"FAIL resolve_name\n  in:   {src!r}\n  want: {want!r}\n  got:  {got!r}")
    total += len(NAME_CASES)

    print(f"{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
