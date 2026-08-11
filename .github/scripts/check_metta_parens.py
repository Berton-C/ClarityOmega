#!/usr/bin/env python3
"""Check parenthesis balance in tracked .metta files.

Unbalanced parens are a recurring, high-cost failure in this project: a file
loads silently wrong rather than erroring cleanly. This catches it at PR time.

Ignores parens inside double-quoted strings and after a `;` line comment.
Skips staging/OLD/ (archived scratch, not loaded at runtime).
"""
import subprocess
import sys


def tracked_metta_files():
    out = subprocess.run(
        ["git", "ls-files", "*.metta"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    return [f for f in out if f and not f.startswith("staging/OLD/")]


def balance(path):
    """Return (depth, first_offending_line). depth 0 == balanced."""
    depth = 0
    offender = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            in_string = False
            i = 0
            while i < len(line):
                ch = line[i]
                if in_string:
                    if ch == "\\":
                        i += 2
                        continue
                    if ch == '"':
                        in_string = False
                elif ch == '"':
                    in_string = True
                elif ch == ";":
                    break  # rest of line is a comment
                elif ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth < 0 and offender is None:
                        offender = lineno
                i += 1
    return depth, offender


def main():
    files = tracked_metta_files()
    failures = []
    for path in files:
        try:
            depth, offender = balance(path)
        except OSError as exc:
            failures.append(f"{path}: unreadable ({exc})")
            continue
        if depth != 0:
            where = f" (first unmatched ')' at line {offender})" if offender else ""
            state = "unclosed '('" if depth > 0 else "extra ')'"
            failures.append(f"{path}: {state}, net depth {depth}{where}")

    print(f"Checked {len(files)} tracked .metta files.")
    if failures:
        print("\nPAREN BALANCE FAILURES:")
        for f in failures:
            print(f"  {f}")
        return 1
    print("All balanced.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
