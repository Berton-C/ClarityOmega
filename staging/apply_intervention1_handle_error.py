#!/usr/bin/env python3
"""
apply_intervention1_handle_error.py

INTERVENTION 1, PIECE 1a -- Make command-execution errors ACTIONABLE.

PROBLEM (proven, not assumed):
  On a failed command, the runtime ALREADY produces a readable error term:
    (Error (syntax_error Parse error in form: <input>) none)   [parse path]
    (Error <eval-formal> <eval-context>)                       [eval path]
  but HandleError DISCARDS it. On the Error branch it appends only the generic
  constant ($msg $cmd) to &error and RETURNS change-state!'s value. So Clarity
  never sees what actually went wrong; she gets only
  "..._NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY".

CONSUMER TRACE (Discipline 6, done before this script):
  &error CONTENT is never surfaced to Clarity -- it is read only as an emptiness
  guard (gates $metta_cmds and soul-note-record). The path Clarity actually reads
  is the SINGLE/eval HandleError RETURN value -> COMMAND_RETURN -> $results ->
  &lastresults -> next prompt LAST_SKILL_USE_RESULTS. Therefore the fix must
  change HandleError's RETURN on the Error branch, not just the &error append.

THE FIX (two self-balanced, count-guarded edits to src/loop.metta HandleError):
  Edit A: append the readable detail to &error too (hygiene; harmless to guards
          which only check emptiness):
            (($msg $cmd))  ->  (($msg $cmd $a))
  Edit B: return the readable detail on the Error branch so the eval/SINGLE path
          surfaces it via COMMAND_RETURN -> &lastresults:
            (change-state! &error $new)
              -> (progn (change-state! &error $new) ($msg $cmd $a))

  Net paren delta: 0 (Edit A adds an atom; Edit B adds matched progn+tuple parens,
  +2 open / +2 close). Net line delta: 0 (both edits are in-place token changes).

  This lands on the eval/SINGLE path (where |- and argument errors live) and is
  robust to the uncaptured |- term -- it surfaces whatever eval produced. The
  parse/MULTI path surfacing is a separate follow-on (Piece 1b, $results gating),
  NOT in this script.

REVERSIBILITY: --reverse --apply restores the original two forms exactly.
USAGE:
  python3 apply_intervention1_handle_error.py                 # dry-run (default)
  python3 apply_intervention1_handle_error.py --apply         # write
  python3 apply_intervention1_handle_error.py --reverse --apply
"""

import argparse
import sys
import datetime
from pathlib import Path

TARGET = Path("src/loop.metta")
BACKUP = Path("src/loop.metta.bak.intervention1_handleerror")
LOGDIR = Path("shared_files")

# --- Edit A: the &error append tuple ---
A_OLD = '(($msg $cmd))'
A_NEW = '(($msg $cmd $a))'

# --- Edit B: the Error-branch return (wrap change-state! in progn, return detail) ---
B_OLD = '(progn (change-state! &error $new) ($msg $cmd $a))'  # post-state (for reverse detection)
B_NEW = '(progn (change-state! &error $new) ($msg $cmd $a))'
B_ORIG = '(change-state! &error $new)'
B_WRAPPED = '(progn (change-state! &error $new) ($msg $cmd $a))'


def code_aware_paren_count(text: str):
    """Count parens outside of double-quoted strings."""
    opens = closes = 0
    in_str = False
    esc = False
    for ch in text:
        if esc:
            esc = False
            continue
        if ch == '\\':
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == '(':
            opens += 1
        elif ch == ')':
            closes += 1
    return opens, closes


def count_occurrences(text: str, needle: str) -> int:
    return text.count(needle)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    ap.add_argument("--reverse", action="store_true", help="reverse the edits")
    args = ap.parse_args()

    mode = ("REVERSE" if args.reverse else "FORWARD") + (" / APPLY" if args.apply else " / DRY-RUN")
    ts = datetime.datetime.now().strftime("%H%M%S")
    log_lines = []

    def out(s=""):
        print(s)
        log_lines.append(s)

    out("=" * 76)
    out("INTERVENTION 1 PIECE 1a -- HandleError surfaces command errors to Clarity")
    out(f"MODE: {mode}")
    out("=" * 76)

    if not TARGET.exists():
        out(f"ERROR: {TARGET} not found. Run from repo root.")
        return 1

    content = TARGET.read_text()
    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    pre_lines = len(content.splitlines())

    out("\n>>> PRE-EDIT STATE <<<")
    out(f"  Path: {TARGET}")
    out(f"  Line count: {pre_lines}")
    cpar = "OK" if pre_d == 0 else "FAIL"
    out(f"  Paren: opens={pre_o} closes={pre_c} delta={pre_d} ({cpar})")
    if pre_d != 0:
        out("  PAREN IMBALANCE pre-edit. Aborting.")
        return 1

    # ---- State checks + simulate ----
    if not args.reverse:
        # FORWARD: original forms present, new forms absent
        nA_old = count_occurrences(content, A_OLD)
        nA_new = count_occurrences(content, A_NEW)
        nB_orig = count_occurrences(content, B_ORIG)
        nB_wrapped = count_occurrences(content, B_WRAPPED)

        out("\n>>> FORWARD STATE CHECK <<<")
        out(f"  Edit A anchor '(($msg $cmd))'           count={nA_old} (need exactly 1)")
        out(f"  Edit A target '(($msg $cmd $a))'        count={nA_new} (need 0)")
        out(f"  Edit B anchor '(change-state! &error $new)' count={nB_orig} (need exactly 1)")
        out(f"  Edit B target progn-wrapped             count={nB_wrapped} (need 0)")

        if nA_old != 1 or nA_new != 0 or nB_orig != 1 or nB_wrapped != 0:
            out("  STATE CHECK FAILED. Anchors not in clean forward state. Aborting.")
            return 1

        simulated = content.replace(A_OLD, A_NEW, 1)
        # Edit B: replace the bare change-state! with the progn-wrapped form.
        # A_NEW now contains '($msg $cmd $a)'; ensure B replacement does not collide.
        simulated = simulated.replace(B_ORIG, B_WRAPPED, 1)
        expected_line_delta = 0

    else:
        # REVERSE: new forms present, restore originals
        nA_new = count_occurrences(content, A_NEW)
        nB_wrapped = count_occurrences(content, B_WRAPPED)

        out("\n>>> REVERSE STATE CHECK <<<")
        out(f"  Edit A target '(($msg $cmd $a))'        count={nA_new} (need exactly 1)")
        out(f"  Edit B wrapped progn form               count={nB_wrapped} (need exactly 1)")

        if nA_new != 1 or nB_wrapped != 1:
            out("  STATE CHECK FAILED. Not in clean applied state. Aborting.")
            return 1

        # Reverse Edit B first (it contains the $a tuple), then Edit A.
        simulated = content.replace(B_WRAPPED, B_ORIG, 1)
        simulated = simulated.replace(A_NEW, A_OLD, 1)
        expected_line_delta = 0

    # ---- Post-edit checks ----
    post_o, post_c = code_aware_paren_count(simulated)
    post_d = post_o - post_c
    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines

    out("\n>>> POST-EDIT (SIMULATED) CHECKS <<<")
    c5 = "OK" if post_d == 0 else "FAIL"
    out(f"  Paren post: opens={post_o} closes={post_c} delta={post_d} ({c5})")
    c6 = "OK" if (post_d - pre_d) == 0 else "FAIL"
    out(f"  Paren delta change: {post_d - pre_d} ({c6})")
    c7 = "OK" if line_delta == expected_line_delta else "FAIL"
    out(f"  Line delta: {line_delta} (expected {expected_line_delta}) ({c7})")

    if c5 != "OK" or c6 != "OK" or c7 != "OK":
        out("\n  POST-EDIT CHECK FAILED. Aborting; no disk write.")
        return 1

    # ---- Diff preview ----
    out("\n>>> DIFF PREVIEW (changed region) <<<")
    for i, (a, b) in enumerate(zip(content.splitlines(), simulated.splitlines())):
        if a != b:
            out(f"  L{i+1}-  {a.strip()}")
            out(f"  L{i+1}+  {b.strip()}")

    out("\n" + "=" * 76)
    out("ACTION SUMMARY")
    out("=" * 76)
    out(f"  File:            {TARGET}")
    out(f"  Edit A:          append readable detail to &error  (($msg $cmd)) -> (($msg $cmd $a))")
    out(f"  Edit B:          return detail on Error branch      change-state! -> (progn change-state! ($msg $cmd $a))")
    out(f"  Surfaces via:    SINGLE/eval path -> COMMAND_RETURN -> &lastresults -> next prompt")
    out(f"  Paren delta:     0   Line delta: {line_delta}")
    out(f"  Reversible:      yes (--reverse --apply)")
    out(f"  NOT in scope:    parse/MULTI path surfacing (Piece 1b, $results gating)")

    if not args.apply:
        out("\nDRY-RUN complete. All checks pass. Re-run with --apply to write.")
        _write_log(log_lines, ts, mode)
        return 0

    if not args.reverse:
        if BACKUP.exists():
            out(f"\nWARNING: backup {BACKUP} exists; overwriting.")
        BACKUP.write_text(content)
        out(f"\nBackup written: {BACKUP}")

    TARGET.write_text(simulated)
    out(f"WROTE: {TARGET}")
    _write_log(log_lines, ts, mode)
    return 0


def _write_log(log_lines, ts, mode):
    try:
        LOGDIR.mkdir(exist_ok=True)
        tag = "reverse" if "REVERSE" in mode else "forward"
        sub = "apply" if "APPLY" in mode else "dryrun"
        p = LOGDIR / f"apply_intervention1_handleerror_{tag}_{sub}_{ts}.log"
        p.write_text("\n".join(log_lines) + "\n")
        print(f"LOG WRITTEN: {p}")
    except Exception as e:
        print(f"(log write skipped: {e})")


if __name__ == "__main__":
    sys.exit(main())
