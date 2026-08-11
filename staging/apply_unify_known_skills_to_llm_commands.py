#!/usr/bin/env python3
"""
apply_unify_known_skills_to_llm_commands.py

Single-source-of-truth fix for the skill list divergence.

After 960afa5 (canon balance_parentheses merge), src/helper.py has TWO skill
lists that disagree:
  LLM_COMMANDS (canon, used by starts_command_line/balance_parentheses): 15
    skills, including promote and demote (live in memory.metta, used when
    prompted, per Patrick's design).
  wrap_if_bare_command.known_skills (bare-command safety net): 13 skills,
    MISSING promote and demote.

The divergence means a bare (promote ...) or (demote ...) command is recognized
by the canon assembler but NOT by the safety net, so promote/demote do not
function identically on both paths. This is the B10 multiple-skill-source drift
the audit flagged.

This fix points known_skills at LLM_COMMANDS, making it the single source of
truth so all 15 skills (including promote/demote) are recognized on both paths.
One edit, one file.

Conventions (apply_task_state_step2_wiring.py template): dry-run default,
--apply, --reverse, exact-substring match (abort unless found exactly once,
both directions), code-aware paren counting, py_compile of simulated file,
action summary. No em dashes. OLD/NEW stored base64 for byte-exact matching.

Usage (run from repo root):
  python3 staging/apply_unify_known_skills_to_llm_commands.py
  python3 staging/apply_unify_known_skills_to_llm_commands.py --apply
  python3 staging/apply_unify_known_skills_to_llm_commands.py --reverse --apply
"""

import argparse
import base64
import py_compile
import sys
import tempfile
import os

HELPER = "src/helper.py"

_B = {
    'OLD': 'ICAgICMgS25vd24gc2tpbGxzIHJlZ2lzdHJ5ICgxMyBpdGVtcywgZnJvbSBwcm9tcHQgU0tJTExTIHNlY3Rpb24pCiAgICBrbm93bl9za2lsbHMgPSB7CiAgICAgICAgInJlbWVtYmVyIiwgInF1ZXJ5IiwgImVwaXNvZGVzIiwgInBpbiIsICJzaGVsbCIsCiAgICAgICAgInJlYWQtZmlsZSIsICJ3cml0ZS1maWxlIiwgImFwcGVuZC1maWxlIiwgInNlbmQiLAogICAgICAgICJzZWFyY2giLCAidGF2aWx5LXNlYXJjaCIsICJ0ZWNobmljYWwtYW5hbHlzaXMiLCAibWV0dGEiLAogICAgfQ==',
    'NEW': 'ICAgICMgS25vd24gc2tpbGxzIHJlZ2lzdHJ5OiBzaW5nbGUgc291cmNlIG9mIHRydXRoIGlzIExMTV9DT01NQU5EUyAodGhlIGNhbm9uCiAgICAjIHNldCB1c2VkIGJ5IGJhbGFuY2VfcGFyZW50aGVzZXMvc3RhcnRzX2NvbW1hbmRfbGluZSkuIFJlZmVyZW5jaW5nIGl0IGhlcmUKICAgICMga2VlcHMgdGhlIGJhcmUtY29tbWFuZCBzYWZldHkgbmV0IGluIGFncmVlbWVudCB3aXRoIHRoZSBhc3NlbWJsZXIsIHNvIGV2ZXJ5CiAgICAjIHNraWxsIChpbmNsdWRpbmcgcHJvbW90ZS9kZW1vdGUpIGlzIHJlY29nbml6ZWQgaWRlbnRpY2FsbHkgb24gYm90aCBwYXRocy4KICAgIGtub3duX3NraWxscyA9IExMTV9DT01NQU5EUw==',
}

def _d(k):
    return base64.b64decode(_B[k]).decode("utf-8")


def code_aware_paren_count(text):
    opens = closes = 0
    in_str = False
    esc = False
    in_comment = False
    for ch in text:
        if in_comment:
            if ch == "\n":
                in_comment = False
            continue
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "#":
            in_comment = True
        elif ch == "(":
            opens += 1
        elif ch == ")":
            closes += 1
    return opens, closes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    args = ap.parse_args()

    old, new = _d("OLD"), _d("NEW")
    a, b = (new, old) if args.reverse else (old, new)

    if not os.path.exists(HELPER):
        print("ABORT: %s not found. Run from repo root." % HELPER)
        sys.exit(1)
    before = open(HELPER, "r", encoding="utf-8").read()

    n = before.count(a)
    if n != 1:
        print("ABORT: target found %d times (need exactly 1). Direction=%s"
              % (n, "REVERSE" if args.reverse else "FORWARD"))
        sys.exit(1)
    after = before.replace(a, b, 1)

    ob, cb = code_aware_paren_count(before)
    no, nc = code_aware_paren_count(after)

    print("=" * 70)
    print("UNIFY known_skills -> LLM_COMMANDS (single source of truth)")
    print("=" * 70)
    print("file      : %s" % HELPER)
    print("direction : %s" % ("REVERSE" if args.reverse else "FORWARD"))
    print("mode      : %s" % ("APPLY (writing)" if args.apply else "DRY-RUN (no write)"))
    print("code-aware parens: opens %d->%d closes %d->%d  delta before=%d after=%d  %s"
          % (ob, no, cb, nc, ob - cb, no - nc,
             "OK" if (ob - cb) == (no - nc) else "NOTE inspect"))
    print()
    print("--- removing ---")
    print(a)
    print("--- inserting ---")
    print(b)
    print()

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tf:
        tf.write(after)
        tmp = tf.name
    try:
        py_compile.compile(tmp, doraise=True)
        print("py_compile of simulated %s: PASS" % HELPER)
    except py_compile.PyCompileError as e:
        print("py_compile of simulated %s: FAIL" % HELPER)
        print(e)
        os.unlink(tmp)
        sys.exit(1)
    os.unlink(tmp)
    print()

    if args.apply:
        with open(HELPER, "w", encoding="utf-8") as f:
            f.write(after)
        print(">>> WRITTEN. Next: rebuild --no-cache, restart.")
    else:
        print(">>> DRY-RUN only. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
