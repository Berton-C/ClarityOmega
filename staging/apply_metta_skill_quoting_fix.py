#!/usr/bin/env python3
"""
apply_metta_skill_quoting_fix.py

Purpose
-------
Fix the dominant Clarity command-malformation loop driver.

The getSkills prompt teaches the metta skill argument UNQUOTED, as
(metta sexpression), while the metta skill sreads its argument and therefore
requires a quoted STRING. Every bare (metta (...)) call Clarity copies from the
example returns type_error string. This is verified at source: skills.metta line
57 is (sread $str); the prompt example at line 18 is bare; every other skill in
the prompt already names its argument _in_quotes; her own history line 236734
shows a quoted metta arg passing sread.

This script brings the metta teaching into line with that universal convention:
  - line 18 placeholder renamed: sexpression -> sexpression_in_quotes
  - the two |- examples are shown as the literal working call (metta "(|- ...)"),
    with the inner quotes authored as \\" per the existing in-repo pattern in
    src/utils.metta line 23.

Design constraints honored
--------------------------
  - PAREN-DELTA ZERO: only \\" characters are inserted and one placeholder is
    renamed. No ( or ) is added or removed. The script asserts the file's ( and
    ) counts are unchanged, and aborts if not.
  - Reversible: --reverse returns the file to the current fork state exactly.
  - Targets the live bytes by stable, ASCII-safe locator substrings, so it is
    robust to indentation and aborts safely if the expected text is not found
    exactly once.
  - No em dashes anywhere. ASCII-safe (the existing multiplication-sign chars in
    the target lines are preserved untouched; they are not part of any locator).

Usage (run from repo root)
---------------------------
  python3 staging/apply_metta_skill_quoting_fix.py            # dry-run (default)
  python3 staging/apply_metta_skill_quoting_fix.py --apply
  python3 staging/apply_metta_skill_quoting_fix.py --reverse  # dry-run of reverse
  python3 staging/apply_metta_skill_quoting_fix.py --reverse --apply

After --apply: rebuild --no-cache, then READ the live rendered prompt to confirm
\\" renders to Clarity as a single double-quote (not \\" and not _quote_). If it
renders wrong, run --reverse --apply and switch to the name-the-convention shape.
The rendered PREVIEW printed below assumes \\" -> " per the utils.metta precedent;
the live read is the confirmation.
"""

import argparse
import sys

TARGET = "src/skills.metta"

# Each edit: a stable locator substring present in BOTH states (used to find the
# unique line), plus the forward find/replace pair. ASCII-safe locators only.
EDITS = [
    {
        "name": "line18-placeholder",
        "locator": "Execute MeTTa expression",
        "old": "(metta sexpression)",
        "new": "(metta sexpression_in_quotes)",
    },
    {
        "name": "ex1-open-quote",
        "locator": "sam garfield) friend",
        "old": "(metta (|- ",
        "new": "(metta \\\"(|- ",
    },
    {
        "name": "ex1-close-quote",
        "locator": "garfield animal)",
        "old": "(stv 1.0 0.9))))",
        "new": "(stv 1.0 0.9)))\\\")",
    },
    {
        "name": "ex2-open-quote",
        "locator": "$1 elephant",
        "old": "(metta (|- ",
        "new": "(metta \\\"(|- ",
    },
    {
        "name": "ex2-close-quote",
        "locator": "tiger elephant) eat",
        "old": "(stv 1.0 0.9))))",
        "new": "(stv 1.0 0.9)))\\\")",
    },
]


def count_parens(text):
    return text.count("("), text.count(")")


def locate_unique(lines, locator):
    hits = [i for i, l in enumerate(lines) if locator in l]
    return hits


def render_preview(lines):
    """What Clarity sees for the metta block, assuming \\" renders as a single ".
    Strips the MeTTa element delimiters and converts the escape for display."""
    out = []
    grab = False
    for l in lines:
        if "Execute MeTTa expression" in l:
            grab = True
        if grab:
            s = l.strip()
            # strip outer MeTTa string-literal quotes if present
            if s.startswith('"'):
                s = s[1:]
            # drop trailing element close and any list close parens that belong
            # to the getSkills list, not to the displayed content
            s = s.rstrip()
            # convert the authored escape to the displayed quote
            s = s.replace('\\"', '"')
            out.append(s)
        if grab and "Additionally |-" in l:
            break
    return "\n".join(out)


def apply_edits(lines, reverse):
    changed = []
    for e in EDITS:
        find = e["new"] if reverse else e["old"]
        repl = e["old"] if reverse else e["new"]
        idxs = locate_unique(lines, e["locator"])
        if len(idxs) != 1:
            return None, "ABORT [%s]: locator '%s' matched %d lines (need 1)." % (
                e["name"], e["locator"], len(idxs))
        i = idxs[0]
        if find not in lines[i]:
            return None, (
                "ABORT [%s]: expected text not found on line %d. "
                "File may already be in the target state, or bytes differ.\n"
                "  line: %s" % (e["name"], i + 1, lines[i].rstrip()))
        if lines[i].count(find) != 1:
            return None, "ABORT [%s]: text '%s' is not unique on line %d." % (
                e["name"], find, i + 1)
        newline = lines[i].replace(find, repl)
        changed.append((i, lines[i], newline))
        lines[i] = newline
    return changed, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the change (default is dry-run)")
    ap.add_argument("--reverse", action="store_true", help="revert to current fork state")
    args = ap.parse_args()

    try:
        with open(TARGET, "r", encoding="utf-8") as f:
            original = f.read()
    except FileNotFoundError:
        print("ABORT: %s not found. Run from repo root." % TARGET)
        sys.exit(1)

    lines = original.split("\n")
    open_before, close_before = count_parens(original)

    changed, err = apply_edits(lines, args.reverse)
    if err:
        print(err)
        sys.exit(1)

    updated = "\n".join(lines)
    open_after, close_after = count_parens(updated)

    print("=" * 70)
    print("ACTION SUMMARY")
    print("=" * 70)
    print("target            : %s" % TARGET)
    print("direction         : %s" % ("REVERSE (back to fork state)" if args.reverse else "FORWARD (apply quoting fix)"))
    print("mode              : %s" % ("APPLY (writing)" if args.apply else "DRY-RUN (no write)"))
    print("edits             : %d" % len(changed))
    print("paren ( before/after : %d / %d" % (open_before, open_after))
    print("paren ) before/after : %d / %d" % (close_before, close_after))
    paren_ok = (open_before == open_after) and (close_before == close_after)
    print("paren-delta-zero  : %s" % ("PASS" if paren_ok else "FAIL"))
    print()

    print("-" * 70)
    print("SOURCE DIFF")
    print("-" * 70)
    for i, old, new in changed:
        print("line %d" % (i + 1))
        print("  - %s" % old.rstrip())
        print("  + %s" % new.rstrip())
    print()

    if not args.reverse:
        print("-" * 70)
        print("RENDERED PREVIEW (what Clarity sees, assuming \\\" renders as \")")
        print("(confirm against the live prompt after rebuild; see header note)")
        print("-" * 70)
        print(render_preview(lines))
        print()

    if not paren_ok:
        print("ABORT: paren counts changed. Not writing. Investigate before proceeding.")
        sys.exit(1)

    if args.apply:
        with open(TARGET, "w", encoding="utf-8") as f:
            f.write(updated)
        print(">>> WRITTEN. Next: rebuild --no-cache, then read the live rendered")
        print(">>> prompt to confirm \\\" renders as a single double-quote to Clarity.")
    else:
        print(">>> DRY-RUN only. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
