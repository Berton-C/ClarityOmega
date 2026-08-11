#!/usr/bin/env python3
"""apply_release_gitignore_fix.py

Stops .gitignore from ignoring `.github/`, which silently prevented any GitHub
Actions workflow or pull-request template from ever being committed.

The current line 19 reads exactly `.github/`. This replaces it with a comment
explaining why it is no longer ignored, plus a narrower ignore for local
Actions-runner scratch. No other line is touched.

Default is DRY RUN (prints a diff, writes nothing):
  python3 staging/apply_release_gitignore_fix.py            # dry run
  python3 staging/apply_release_gitignore_fix.py --apply    # write
  python3 staging/apply_release_gitignore_fix.py --reverse  # exact inverse

Fails loud: if the anchor is missing or not unique, nothing is written.
Idempotent: re-running --apply on an already-applied file refuses.
"""
import argparse
import difflib
import sys

TARGET = ".gitignore"

FIND = "\n.github/\n"

REPL = (
    "\n"
    "# .github/ is intentionally NOT ignored: workflows and issue/PR templates\n"
    "# must be committed for CI to run. Ignoring it silently prevented every\n"
    "# workflow file from being added.\n"
    "# Local Actions-runner scratch only:\n"
    ".github/act/\n"
)


def read():
    try:
        with open(TARGET, encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        sys.exit("ABORT: " + TARGET + " not found (run from repo root)")


def forward(text):
    if REPL in text:
        sys.exit("ABORT: already applied. Use --reverse first to re-apply.")
    n = text.count(FIND)
    if n != 1:
        sys.exit(
            "ABORT: anchor found " + str(n) + " times (need exactly 1). "
            "The file has drifted; re-read it and update the anchor."
        )
    return text.replace(FIND, REPL, 1)


def backward(text):
    if REPL not in text:
        sys.exit("ABORT: not applied; nothing to reverse.")
    return text.replace(REPL, FIND, 1)


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--apply", action="store_true", help="write the change")
    g.add_argument("--reverse", action="store_true", help="undo the change")
    args = ap.parse_args()

    cur = read()
    new = backward(cur) if args.reverse else forward(cur)

    if not (args.apply or args.reverse):
        diff = "".join(difflib.unified_diff(
            cur.splitlines(keepends=True), new.splitlines(keepends=True),
            fromfile=TARGET + " (current)", tofile=TARGET + " (after)",
        ))
        print(diff if diff else "(no change)")
        print("\n[DRY RUN] nothing written. Use --apply to write.")
        return

    with open(TARGET, "w", encoding="utf-8") as fh:
        fh.write(new)
    print(("Reversed" if args.reverse else "Applied") + " -> " + TARGET)


if __name__ == "__main__":
    main()
