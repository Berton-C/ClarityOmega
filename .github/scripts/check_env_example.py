#!/usr/bin/env python3
"""Verify .env.example documents every variable docker-compose.yml expects.

Prevents the failure where a new user copies .env.example, follows the README,
and the stack silently starts without a key it needed. Variables that supply
their own default in compose (${VAR:-default}) are not required.
"""
import os
import re
import sys

COMPOSE = "docker-compose.yml"
EXAMPLE = ".env.example"

# Interpolations compose resolves itself; not user-supplied configuration.
EXEMPT = {"PWD", "HOME", "USER"}


def compose_vars(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    required, defaulted = set(), set()
    for match in re.finditer(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(:-[^}]*)?\}", text):
        name, default = match.group(1), match.group(2)
        (defaulted if default else required).add(name)
    return required - EXEMPT, defaulted - EXEMPT


def example_vars(path):
    names = set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            # Accept commented-out optional entries: "# OPENAI_API_KEY="
            if line.startswith("#"):
                line = line.lstrip("#").strip()
            match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=", line)
            if match:
                names.add(match.group(1))
    return names


def main():
    for path in (COMPOSE, EXAMPLE):
        if not os.path.exists(path):
            print(f"ERROR: {path} not found.")
            return 1

    required, defaulted = compose_vars(COMPOSE)
    documented = example_vars(EXAMPLE)

    missing = sorted(required - documented)
    undocumented_defaults = sorted(defaulted - documented)

    print(f"{COMPOSE}: {len(required)} required, {len(defaulted)} with defaults.")
    print(f"{EXAMPLE}: {len(documented)} documented.")

    if missing:
        print("\nERROR: required by docker-compose.yml but absent from .env.example:")
        for name in missing:
            print(f"  {name}")
        return 1

    if undocumented_defaults:
        print("\nNote (not fatal): compose supplies defaults for these, and they")
        print("are not in .env.example. Document them if a user should override:")
        for name in undocumented_defaults:
            print(f"  {name}")

    print("\n.env.example covers all required variables.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
