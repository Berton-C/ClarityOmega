#!/usr/bin/env python3
"""
Apply script: guard path-scope-score against the F30 raw-marshalling crash
(soul/output_verdict.metta, live line 48).

Purpose
-------
Clarity flagged path-scope-score during her review of the norm-metta-arg
guard: it passes an LLM-derived path RAW to py-call, no repr, no guard.
Probe 2026-07-04 confirmed the defect is the fatal class: an
unbound-variable-carrying path (e.g. (foo $u), or a bare unbound var) kills
py_call uncaught (janus:py_call/3 Arguments are not sufficiently
instantiated, exit 2) inside the per-cycle gate walk, the same position
that made the norm-metta-arg throw fatal.

Production reachability is established, not hypothetical: she emits
variables in malformed commands despite the format contract (all-session
evidence); sread parses $x as a REAL unbound MeTTa variable; and
output-cmd-path extracts the first argument of any (write-file ...) or
(append-file ...) straight into this call.

Guarded-shape probe (2026-07-04, throwaway container, host soul/ mounted):
  bound soul path      -> 1  (correct scoring undisturbed)
  ()  (no-arg extract) -> 4  (str-coerces, fail-safe)
  (foo $u) [the killer]-> 4  (caught, exit 0)
  bare unbound $v      -> 4  (caught, exit 0)

The one edit
------------
Edit G: replace the one-line path-scope-score definition with the guarded
version. The catch converts the janus throw to an (Error ...) term; the
Error branch returns 4 (system scope, maximum caution) per the file's own
default-safe-on-failure constraint: no silent PROCEED, and an
uninspectable path is treated as widest scope. Execution-side is already
safe (file-command eval sits inside the B4 catch), so this mirrors the
norm-metta-arg logic: gate inspects safely, execution fails safely.

Pattern grounds: catch-in-let-bind (probe-proven executing, this session);
case-on-(Error $a $b) (HandleError production precedent, loop.metta;
norm-metta-arg guard precedent in this same file).

Net change
----------
- soul/output_verdict.metta: OLD 1 line -> NEW 16 lines (+15)
- Paren delta: 0 (balanced both sides; verified by code-aware count)

Deployment
----------
soul/ is BIND-MOUNTED. NO REBUILD. Apply, then restart:
  docker compose up -d --force-recreate clarityclaw

Usage
-----
Dry-run (default):
    python3 staging/apply_guard_path_scope_score_f30.py

Apply:
    python3 staging/apply_guard_path_scope_score_f30.py --apply

Reverse (after apply):
    python3 staging/apply_guard_path_scope_score_f30.py --reverse --apply

Pre-conditions
--------------
- Run from repo root
- soul/output_verdict.metta line 48 matches the live-verified OLD block
  (in-container grep 2026-07-04; the state check enforces exactly-once)

Backup file (forward apply only):
- soul/output_verdict.metta.bak.path_scope_guard
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

TARGET_PATH = Path("soul/output_verdict.metta")
TARGET_BAK = Path("soul/output_verdict.metta.bak.path_scope_guard")

# ============================================================================
# EDIT G: guard path-scope-score
# ============================================================================

G_OLD = "(= (path-scope-score $path) (py-call (soul_governance.path_scope $path)))"

G_NEW = ''';; CRASH GUARD (2026-07-04): raw py-call marshalling of an unbound-carrying
;; path kills py_call uncaught (janus instantiation error, exit 2) inside
;; the per-cycle gate walk (F30 class; probe-proven on (foo $u) and bare $v).
;; Production-reachable: contract-violating variables in her file commands
;; parse via sread as real unbound vars; output-cmd-path extracts them here.
;; The catch converts the throw; the Error branch returns 4 (system scope,
;; maximum caution) per this file\'s default-safe-on-failure constraint: no
;; silent PROCEED, and an uninspectable path is treated as widest scope.
;; Guarded-shape probe 2026-07-04: bound soul path still scores 1; () scores
;; 4 via str-coercion; (foo $u) and bare $v return 4 with exit 0.
;; Flagged by Clarity in her norm-metta-arg guard review (same defect class).
(= (path-scope-score $path)
   (let $s (catch (py-call (soul_governance.path_scope $path)))
        (case $s
          (((Error $e $d) 4)
           ($else $s)))))'''

EXPECTED_LINE_DELTA_FORWARD = G_NEW.count("\n") - G_OLD.count("\n")

NEW_MARKER = "(catch (py-call (soul_governance.path_scope"

# ============================================================================
# HELPERS
# ============================================================================

def find_target_substring_count(text: str, target: str) -> int:
    count = 0
    start = 0
    while True:
        idx = text.find(target, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count


def code_aware_paren_count(text: str) -> tuple[int, int]:
    """Count parens excluding string literals and ; line comments (metta)."""
    opens = 0
    closes = 0
    in_string = False
    escape = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == ";":
                while i < n and text[i] != "\n":
                    i += 1
                continue
            elif ch == "(":
                opens += 1
            elif ch == ")":
                closes += 1
        i += 1
    return opens, closes


# ============================================================================
# SIMULATION
# ============================================================================

def simulate_forward(content: str) -> str:
    if find_target_substring_count(content, G_OLD) != 1:
        raise RuntimeError("edit G forward: OLD definition not found exactly once.")
    return content.replace(G_OLD, G_NEW, 1)


def simulate_reverse(content: str) -> str:
    if find_target_substring_count(content, G_NEW) != 1:
        raise RuntimeError("edit G reverse: NEW block not found exactly once.")
    return content.replace(G_NEW, G_OLD, 1)


# ============================================================================
# STATE CHECK PREDICATES
# ============================================================================

def forward_state_ok(content: str) -> tuple[bool, str]:
    g = find_target_substring_count(content, G_OLD) == 1
    new_absent = NEW_MARKER not in content
    ok = g and new_absent
    msg = f"anchor present={g}, guard absent={new_absent} -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def reverse_state_ok(content: str) -> tuple[bool, str]:
    g = find_target_substring_count(content, G_NEW) == 1
    msg = f"new block present={g} -> {'OK' if g else 'FAIL'}"
    return g, msg


# ============================================================================
# DIFF PREVIEW
# ============================================================================

def diff_preview_first_change(old: str, new: str, label: str, context: int = 3) -> str:
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    differ_start = None
    for i in range(min(len(old_lines), len(new_lines))):
        if old_lines[i] != new_lines[i]:
            differ_start = i
            break
    if differ_start is None:
        if len(old_lines) == len(new_lines):
            return f"--- {label}: NO CHANGES DETECTED ---"
        differ_start = min(len(old_lines), len(new_lines))
    differ_end_old = len(old_lines) - 1
    differ_end_new = len(new_lines) - 1
    while differ_end_old > differ_start and differ_end_new > differ_start:
        if old_lines[differ_end_old] == new_lines[differ_end_new]:
            differ_end_old -= 1
            differ_end_new -= 1
        else:
            break
    out = [f"--- {label} (lines {differ_start + 1} to {max(differ_end_old, differ_end_new) + 1}) ---"]
    start = max(0, differ_start - context)
    for i in range(start, differ_start):
        if i < len(old_lines):
            out.append(f"  {old_lines[i]}")
    for i in range(differ_start, differ_end_old + 1):
        if i < len(old_lines):
            out.append(f"- {old_lines[i]}")
    for i in range(differ_start, differ_end_new + 1):
        if i < len(new_lines):
            out.append(f"+ {new_lines[i]}")
    end_old = min(len(old_lines), differ_end_old + 1 + context)
    for i in range(differ_end_old + 1, end_old):
        out.append(f"  {old_lines[i]}")
    return "\n".join(out)


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guard path-scope-score against the F30 raw-marshalling crash"
    )
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edit. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== PATH-SCOPE-SCORE F30 GUARD: {direction} ==========")

    if not TARGET_PATH.exists():
        print(f"ERROR: {TARGET_PATH} not found. Run from repo root.")
        return 1

    content = TARGET_PATH.read_text()
    pre_lines = len(content.splitlines())
    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c

    print(f"\n>>> {TARGET_PATH} <<<")
    print(f"  Pre-edit line count: {pre_lines}")
    print(f"  Pre-edit paren count: opens={pre_o} closes={pre_c} delta={pre_d} ({'OK' if pre_d == 0 else 'FAIL'})")
    if pre_d != 0:
        print("  PAREN COUNT FAILED. Aborting.")
        return 1

    if args.reverse:
        state_ok, state_msg = reverse_state_ok(content)
    else:
        state_ok, state_msg = forward_state_ok(content)
    print(f"  State check: {state_msg}")
    if not state_ok:
        print("  STATE CHECK FAILED. Aborting.")
        return 1

    try:
        simulated = simulate_reverse(content) if args.reverse else simulate_forward(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return 1

    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines
    expected_delta = -EXPECTED_LINE_DELTA_FORWARD if args.reverse else EXPECTED_LINE_DELTA_FORWARD
    c_lines = "OK" if line_delta == expected_delta else "FAIL"
    print(f"  Line delta: {line_delta} (expected {expected_delta}) ({c_lines})")
    if c_lines != "OK":
        print("  LINE DELTA FAILED. Aborting.")
        return 1

    post_o, post_c = code_aware_paren_count(simulated)
    post_d = post_o - post_c
    print(f"  Post-edit paren count: opens={post_o} closes={post_c} delta={post_d} ({'OK' if post_d == 0 else 'FAIL'})")
    if post_d != 0:
        print("  POST-EDIT PAREN COUNT FAILED. Aborting.")
        return 1

    print("\n========== DIFF PREVIEW ==========")
    print(diff_preview_first_change(content, simulated, "output_verdict.metta", context=2))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        if TARGET_BAK.exists():
            print(f"WARNING: backup {TARGET_BAK} exists; overwriting.")
        TARGET_BAK.write_text(content)
        print(f"Backup written: {TARGET_BAK}")

    print("\n========== WRITING ==========")
    TARGET_PATH.write_text(simulated)
    print(f"Wrote: {TARGET_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    disk = TARGET_PATH.read_text()
    do, dc = code_aware_paren_count(disk)
    dd = do - dc
    print(f"  disk paren: opens={do} closes={dc} delta={dd} ({'OK' if dd == 0 else 'FAIL'})")
    if args.reverse:
        ok, msg = forward_state_ok(disk)
    else:
        ok, msg = reverse_state_ok(disk)
    print(f"  disk state: {msg}")
    if dd != 0 or not ok:
        print("\nDISK VERIFICATION FAILED. File may be in inconsistent state.")
        if not args.reverse:
            print(f"Restore:  cp {TARGET_BAK} {TARGET_PATH}")
        return 1

    print("\n========== PATH-SCOPE-SCORE F30 GUARD COMPLETE ==========")
    print("Edit applied. All checks pass.")
    if not args.reverse:
        print("\nNext: soul/ is bind-mounted, NO rebuild. Restart:")
        print("  docker compose up -d --force-recreate clarityclaw")
    return 0


if __name__ == "__main__":
    sys.exit(main())
