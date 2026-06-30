#!/usr/bin/env python3
"""
apply_intervention2_bar_working_form.py

Malformation doc Intervention 2: resolve the |- prompt/runtime contradiction.
The prompt instructs |- as if its derivation is displayable. It is not: |-
computes a compound result that the metta display path (repr/atom_string)
refuses (the marshalling doc's B5 boundary throw). The documented resolution is
to DOCUMENT THE WORKING FORM: |- computes a value you must capture with
add-atom, then read back with match. Never expect a displayed derivation.

Two edit targets (both confirmed at source):
  1. soul/idle_goal_prompt.py  lines 354 and 360  (the genesis directive strings)
  2. src/skills.metta           after line 25       (the skill-prompt |- block)

Conventions: dry-run default, --apply, --reverse, exact-byte targeting via
unique substrings (aborts safely if not found exactly once), action summary,
no em dashes, reversible to the current state.

Usage (run from repo root):
  python3 staging/apply_intervention2_bar_working_form.py
  python3 staging/apply_intervention2_bar_working_form.py --apply
  python3 staging/apply_intervention2_bar_working_form.py --reverse
  python3 staging/apply_intervention2_bar_working_form.py --reverse --apply
"""

import argparse
import sys

# (path, old_exact, new_exact). old must occur exactly once per file.
EDITS = [
    # --- genesis directive: ACTION line (idle_goal_prompt.py line 354) ---
    (
        "soul/idle_goal_prompt.py",
        "        lines.append('ACTION: Use (metta (|- atom1 atom2)) to test what NAL derives.')",
        "        lines.append('ACTION: |- computes a value it does NOT display. Capture it: (metta \"(add-atom &self (|- atom1 atom2))\") then read it back with (metta \"(match &self $x $x)\"). Do not expect a visible derivation from a bare (metta (|- ...)).')",
    ),
    # --- genesis directive: PROTOCOL step 2 (idle_goal_prompt.py line 360) ---
    (
        "soul/idle_goal_prompt.py",
        "    lines.append('2. Feed two atoms from different domains to NAL: (metta (|- atom1 atom2))')",
        "    lines.append('2. Feed two atoms to NAL and CAPTURE the result with add-atom (it is not displayable): (metta \"(add-atom &self (|- atom1 atom2))\")')",
    ),
    # --- skill prompt: add the capture note after the |- revision line (skills.metta line 25) ---
    (
        "src/skills.metta",
        "    \"Additionally |- also works for revision, to merge evidence even when the term of both premises is the same.\"))",
        "    \"Additionally |- also works for revision, to merge evidence even when the term of both premises is the same.\"\n    \"IMPORTANT: |- computes a compound value that is NOT displayable. To keep a derivation, capture it: (metta \\\"(add-atom &self (|- premise1 premise2))\\\") then read it back with (metta \\\"(match &self $x $x)\\\"). A bare (metta (|- ...)) that expects a visible result will fail at the display boundary.\"))",
    ),
]


def count_parens(t):
    return t.count("("), t.count(")")


def process(reverse):
    summaries = []
    files_text = {}
    for path, old, new in EDITS:
        a, b = (new, old) if reverse else (old, new)
        if path not in files_text:
            try:
                files_text[path] = open(path, "r", encoding="utf-8").read()
            except FileNotFoundError:
                return None, "ABORT: %s not found. Run from repo root." % path
        text = files_text[path]
        n = text.count(a)
        if n != 1:
            return None, ("ABORT [%s]: target text found %d times (need 1).\n"
                          "  looking for: %s" % (path, n, a[:80]))
        files_text[path] = text.replace(a, b)
        summaries.append((path, a, b))
    return (files_text, summaries), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    args = ap.parse_args()

    # capture before-state paren counts per file
    before = {}
    for path, _, _ in EDITS:
        if path not in before:
            try:
                before[path] = count_parens(open(path, "r", encoding="utf-8").read())
            except FileNotFoundError:
                print("ABORT: %s not found. Run from repo root." % path)
                sys.exit(1)

    res, err = process(args.reverse)
    if err:
        print(err)
        sys.exit(1)
    files_text, summaries = res

    print("=" * 70)
    print("ACTION SUMMARY  (Intervention 2: document |- working form)")
    print("=" * 70)
    print("direction : %s" % ("REVERSE" if args.reverse else "FORWARD"))
    print("mode      : %s" % ("APPLY (writing)" if args.apply else "DRY-RUN (no write)"))
    print("edits     : %d across %d file(s)" % (len(summaries), len(files_text)))
    print()

    all_ok = True
    for path in files_text:
        ob, cb = before[path]
        oa, ca = count_parens(files_text[path])
        ok = (ob == oa) and (cb == ca)
        all_ok = all_ok and ok
        print("%s  paren ( %d->%d  ) %d->%d  balance:%s" % (
            path, ob, oa, cb, ca, "PASS" if ok else "NOTE(text-added)"))
    print("(paren balance may shift because we ADD prose inside string literals;")
    print(" what matters is the file stays structurally valid, verified at rebuild)")
    print()

    print("-" * 70)
    print("EDITS")
    print("-" * 70)
    for path, a, b in summaries:
        print("FILE %s" % path)
        print("  - %s" % a.strip()[:200])
        print("  + %s" % b.strip()[:200])
        print()

    if args.apply:
        for path, text in files_text.items():
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        print(">>> WRITTEN to %d file(s). Next: rebuild --no-cache, restart." % len(files_text))
    else:
        print(">>> DRY-RUN only. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
