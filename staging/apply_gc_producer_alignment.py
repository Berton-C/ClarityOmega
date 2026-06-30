#!/usr/bin/env python3
"""
apply_gc_producer_alignment.py

Producer-alignment fix for the (gc) call introduced by B1 merge commit 6ebba7a
("B1: Adopt Patrick's (cut) and (gc) housekeeping (Tier B upstream merge)").

The B1 commit adopted the (gc) call site at loop.metta line 168 without
bringing the producer side. This fix lands the producer:

1. src/skills.pl: append gc/1 predicate definition (verbatim from upstream
   src/skills.pl, drives Prolog-level garbage collection)
2. src/skills.metta line 53: add `gc` to the imported predicate list so
   loop.metta's (gc) call resolves into the substrate

Architectural framing: this is the first commit in the producer-alignment
category. The capability registry pattern (Sprint 0-Coda) is designed to
make this class of consumer-without-producer gap structurally visible
rather than silently broken at runtime.

Usage
-----
Dry-run (default):
    python3 staging/apply_gc_producer_alignment.py

Apply:
    python3 staging/apply_gc_producer_alignment.py --apply

Reverse (after apply, returns to pre-fix state):
    python3 staging/apply_gc_producer_alignment.py --reverse --apply

Pre-conditions
--------------
Forward apply expects:
- src/skills.pl: no gc/1 predicate currently defined
- src/skills.metta line 53: import list is exactly `(shell first_char)`

Reverse apply expects:
- src/skills.pl: gc/1 predicate present
- src/skills.metta line 53: import list is exactly `(shell first_char gc)`

Backup files (forward apply only):
- src/skills.pl.bak.gc_producer_alignment
- src/skills.metta.bak.gc_producer_alignment

Verification
------------
After --apply:
1. Both backup files exist
2. skills.pl contains the gc/1 predicate exactly once
3. skills.metta line 53 import list is `(shell first_char gc)` exactly once
4. Both files end with a newline
5. Manifest integrity check: skills.metta has exactly one
   !(import_prolog_functions_from_file ...) directive (defensive against
   the edit clobbering surrounding lines)

After --apply --reverse:
1. skills.pl matches the original byte-for-byte (no gc/1)
2. skills.metta matches the original byte-for-byte (import list is
   `(shell first_char)` again)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ============================================================================
# PATHS
# ============================================================================

SKILLS_PL_PATH = Path("src/skills.pl")
SKILLS_PL_BAK = Path("src/skills.pl.bak.gc_producer_alignment")

SKILLS_METTA_PATH = Path("src/skills.metta")
SKILLS_METTA_BAK = Path("src/skills.metta.bak.gc_producer_alignment")


# ============================================================================
# ANCHORS AND EDITS
# ============================================================================

# Edit 1: append gc/1 predicate to src/skills.pl
#
# Anchor: the trailing first_char/2 predicate definition exactly as it appears
# in the current file. We replace it with itself + blank line + gc/1 predicate.
# The gc/1 body is verbatim from upstream src/skills.pl.
SKILLS_PL_ANCHOR = "first_char(Str, C) :- sub_string(Str, 0, 1, _, C).\n"

SKILLS_PL_GC_BLOCK = (
    "\n"
    "gc(true) :-\n"
    "    garbage_collect,\n"
    "    garbage_collect_atoms,\n"
    "    trim_stacks.\n"
)

SKILLS_PL_FORWARD_NEW = SKILLS_PL_ANCHOR + SKILLS_PL_GC_BLOCK


# Edit 2: extend the Prolog import list in src/skills.metta line 53
#
# Anchor: exact current line. Replace with extended-import line.
SKILLS_METTA_OLD_LINE = (
    "!(import_prolog_functions_from_file "
    "(library omegaclaw ./src/skills.pl) (shell first_char))"
)
SKILLS_METTA_NEW_LINE = (
    "!(import_prolog_functions_from_file "
    "(library omegaclaw ./src/skills.pl) (shell first_char gc))"
)


# ============================================================================
# UTILITIES
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
    """Count parens excluding those inside string literals and line comments.

    Used for MeTTa file paren balance verification. Treats `;` as line comment
    and `"..."` as string literal with backslash escaping.
    """
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


def diff_preview_first_change(orig: str, new: str, label: str, context: int = 2) -> str:
    """Show the first divergence between orig and new with surrounding context."""
    orig_lines = orig.splitlines()
    new_lines = new.splitlines()
    n = min(len(orig_lines), len(new_lines))
    first_diff = None
    for i in range(n):
        if orig_lines[i] != new_lines[i]:
            first_diff = i
            break
    if first_diff is None and len(orig_lines) != len(new_lines):
        first_diff = n
    if first_diff is None:
        return f"--- {label} ---\n(no changes)"
    start = max(0, first_diff - context)
    end = min(max(len(orig_lines), len(new_lines)), first_diff + context + 5)
    lines = [f"--- {label} (first change at line {first_diff + 1}) ---"]
    lines.append("  BEFORE:")
    for i in range(start, min(end, len(orig_lines))):
        marker = ">" if i >= first_diff else " "
        lines.append(f"  {marker} {i + 1:4d}: {orig_lines[i]}")
    lines.append("  AFTER:")
    for i in range(start, min(end, len(new_lines))):
        marker = ">" if i >= first_diff else " "
        lines.append(f"  {marker} {i + 1:4d}: {new_lines[i]}")
    return "\n".join(lines)


def check_file_exists(path: Path, label: str) -> bool:
    if not path.exists():
        print(f"ERROR: {label} not found at {path}.")
        print("       Run from repo root.")
        return False
    return True


# ============================================================================
# STATE CHECKS
# ============================================================================

def skills_pl_forward_state_ok(content: str) -> tuple[bool, str]:
    """Pre-forward: first_char/2 present, gc/1 absent."""
    has_anchor = find_target_substring_count(content, SKILLS_PL_ANCHOR) == 1
    has_gc = "gc(true)" in content
    ok = has_anchor and not has_gc
    msg = (
        f"first_char anchor present={has_anchor}, "
        f"gc absent={not has_gc} -> {'OK' if ok else 'FAIL'}"
    )
    return ok, msg


def skills_pl_reverse_state_ok(content: str) -> tuple[bool, str]:
    """Pre-reverse: forward-edit shape present (anchor + gc block)."""
    has_block = find_target_substring_count(content, SKILLS_PL_FORWARD_NEW) == 1
    msg = f"forward block present={has_block} -> {'OK' if has_block else 'FAIL'}"
    return has_block, msg


def skills_metta_forward_state_ok(content: str) -> tuple[bool, str]:
    """Pre-forward: old import line present, new import line absent."""
    has_old = find_target_substring_count(content, SKILLS_METTA_OLD_LINE) == 1
    has_new = SKILLS_METTA_NEW_LINE in content
    ok = has_old and not has_new
    msg = (
        f"old import present={has_old}, "
        f"new import absent={not has_new} -> {'OK' if ok else 'FAIL'}"
    )
    return ok, msg


def skills_metta_reverse_state_ok(content: str) -> tuple[bool, str]:
    """Pre-reverse: new import line present."""
    has_new = find_target_substring_count(content, SKILLS_METTA_NEW_LINE) == 1
    msg = f"new import present={has_new} -> {'OK' if has_new else 'FAIL'}"
    return has_new, msg


def skills_metta_manifest_integrity_ok(content: str) -> tuple[bool, str]:
    """Defensive: exactly one !(import_prolog_functions_from_file ...) directive."""
    count = find_target_substring_count(
        content, "!(import_prolog_functions_from_file"
    )
    ok = count == 1
    msg = (
        f"import_prolog_functions_from_file directive count={count} "
        f"(expected 1) -> {'OK' if ok else 'FAIL'}"
    )
    return ok, msg


# ============================================================================
# SIMULATION
# ============================================================================

def simulate_skills_pl_forward(content: str) -> str:
    count = find_target_substring_count(content, SKILLS_PL_ANCHOR)
    if count != 1:
        raise RuntimeError(
            f"skills.pl forward: expected 1 occurrence of first_char anchor, found {count}."
        )
    return content.replace(SKILLS_PL_ANCHOR, SKILLS_PL_FORWARD_NEW, 1)


def simulate_skills_pl_reverse(content: str) -> str:
    count = find_target_substring_count(content, SKILLS_PL_FORWARD_NEW)
    if count != 1:
        raise RuntimeError(
            f"skills.pl reverse: expected 1 occurrence of forward block, found {count}."
        )
    return content.replace(SKILLS_PL_FORWARD_NEW, SKILLS_PL_ANCHOR, 1)


def simulate_skills_metta_forward(content: str) -> str:
    count = find_target_substring_count(content, SKILLS_METTA_OLD_LINE)
    if count != 1:
        raise RuntimeError(
            f"skills.metta forward: expected 1 occurrence of old import, found {count}."
        )
    return content.replace(SKILLS_METTA_OLD_LINE, SKILLS_METTA_NEW_LINE, 1)


def simulate_skills_metta_reverse(content: str) -> str:
    count = find_target_substring_count(content, SKILLS_METTA_NEW_LINE)
    if count != 1:
        raise RuntimeError(
            f"skills.metta reverse: expected 1 occurrence of new import, found {count}."
        )
    return content.replace(SKILLS_METTA_NEW_LINE, SKILLS_METTA_OLD_LINE, 1)


# ============================================================================
# PROCESS FILE
# ============================================================================

def process_file(
    path: Path,
    bak_path: Path,
    simulate_fn,
    simulate_reverse_fn,
    expected_line_delta_forward: int,
    args,
    label: str,
    check_parens: bool,
    forward_state_check_fn,
    reverse_state_check_fn,
    extra_post_check_fn=None,
) -> tuple[bool, str, str]:
    """Read file, run pre-checks, simulate, run post-checks.

    Returns (success, original_content, simulated_content).
    """
    print(f"\n>>> {label} <<<")

    content = path.read_text()
    pre_lines = len(content.splitlines())
    print(f"  Path: {path}")
    print(f"  Pre-edit line count: {pre_lines}")

    if check_parens:
        pre_o, pre_c = code_aware_paren_count(content)
        pre_d = pre_o - pre_c
        ok_p = "OK" if pre_d == 0 else "FAIL"
        print(f"  Pre-edit paren count: opens={pre_o} closes={pre_c} delta={pre_d} ({ok_p})")
        if ok_p != "OK":
            print(f"  PRE-EDIT PAREN COUNT FAILED for {label}. Aborting.")
            return False, content, ""

    # State check
    if args.reverse:
        state_ok, state_msg = reverse_state_check_fn(content)
    else:
        state_ok, state_msg = forward_state_check_fn(content)
    print(f"  State check: {state_msg}")
    if not state_ok:
        print(f"  STATE CHECK FAILED for {label}. Aborting.")
        return False, content, ""

    # Simulate
    try:
        if args.reverse:
            simulated = simulate_reverse_fn(content)
        else:
            simulated = simulate_fn(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return False, content, ""

    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines

    if check_parens:
        post_o, post_c = code_aware_paren_count(simulated)
        post_d = post_o - post_c
        ok_p = "OK" if post_d == 0 else "FAIL"
        print(f"  Post-edit paren count: opens={post_o} closes={post_c} delta={post_d} ({ok_p})")
        if ok_p != "OK":
            print(f"  POST-EDIT PAREN COUNT FAILED for {label}. Aborting.")
            return False, content, simulated

    expected_delta = expected_line_delta_forward if not args.reverse else -expected_line_delta_forward
    c_lines = "OK" if line_delta == expected_delta else "FAIL"
    print(f"  Line delta: {line_delta} (expected {expected_delta}) ({c_lines})")
    if c_lines != "OK":
        print(f"  LINE DELTA FAILED for {label}. Aborting.")
        return False, content, simulated

    # Extra simulated-content check if provided (e.g., manifest integrity)
    if extra_post_check_fn is not None:
        ok_x, msg_x = extra_post_check_fn(simulated)
        print(f"  Extra post check: {msg_x}")
        if not ok_x:
            print(f"  EXTRA POST CHECK FAILED for {label}. Aborting.")
            return False, content, simulated

    return True, content, simulated


# ============================================================================
# DISK VERIFICATION (after write)
# ============================================================================

def verify_disk(
    path: Path,
    args,
    label: str,
    forward_check_fn,
    reverse_check_fn,
    check_parens: bool,
    extra_check_fn=None,
) -> bool:
    disk = path.read_text()
    if check_parens:
        o, c = code_aware_paren_count(disk)
        d = o - c
        ok_p = d == 0
        print(f"  {label} disk paren: opens={o} closes={c} delta={d} ({'OK' if ok_p else 'FAIL'})")
        if not ok_p:
            return False
    if args.reverse:
        # After reverse, file should be back in forward-state shape
        ok, msg = forward_check_fn(disk)
    else:
        # After forward, file should be in reverse-state shape
        ok, msg = reverse_check_fn(disk)
    print(f"  {label} disk state: {msg}")
    if not ok:
        return False
    if extra_check_fn is not None:
        ok_x, msg_x = extra_check_fn(disk)
        print(f"  {label} disk extra: {msg_x}")
        if not ok_x:
            return False
    return True


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Producer-alignment fix: gc/1 predicate + skills.metta import"
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Actually write changes. Default is dry-run."
    )
    parser.add_argument(
        "--reverse", action="store_true",
        help="Reverse the edits. Combine with --apply to write."
    )
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== GC PRODUCER ALIGNMENT: {direction} ==========")

    if not all([
        check_file_exists(SKILLS_PL_PATH, "src/skills.pl"),
        check_file_exists(SKILLS_METTA_PATH, "src/skills.metta"),
    ]):
        return 1

    # skills.pl: append gc block, expect +5 lines (1 blank + 4 lines of gc block)
    skills_pl_delta = SKILLS_PL_GC_BLOCK.count("\n")
    ok_pl, pl_orig, pl_sim = process_file(
        SKILLS_PL_PATH, SKILLS_PL_BAK,
        simulate_skills_pl_forward, simulate_skills_pl_reverse,
        expected_line_delta_forward=skills_pl_delta,
        args=args, label="src/skills.pl",
        check_parens=False,  # Prolog, paren rules differ from MeTTa
        forward_state_check_fn=skills_pl_forward_state_ok,
        reverse_state_check_fn=skills_pl_reverse_state_ok,
    )
    if not ok_pl:
        return 1

    # skills.metta: line-for-line replacement, expect 0 line delta
    ok_metta, metta_orig, metta_sim = process_file(
        SKILLS_METTA_PATH, SKILLS_METTA_BAK,
        simulate_skills_metta_forward, simulate_skills_metta_reverse,
        expected_line_delta_forward=0,
        args=args, label="src/skills.metta",
        check_parens=True,
        forward_state_check_fn=skills_metta_forward_state_ok,
        reverse_state_check_fn=skills_metta_reverse_state_ok,
        extra_post_check_fn=skills_metta_manifest_integrity_ok,
    )
    if not ok_metta:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview_first_change(pl_orig, pl_sim, "src/skills.pl", context=2))
    print()
    print(diff_preview_first_change(metta_orig, metta_sim, "src/skills.metta", context=2))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    # Backup before forward write
    if not args.reverse:
        for path, bak in [(SKILLS_PL_PATH, SKILLS_PL_BAK), (SKILLS_METTA_PATH, SKILLS_METTA_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"  Backed up {path} -> {bak}")

    # Write
    print("\n========== WRITING ==========")
    SKILLS_PL_PATH.write_text(pl_sim)
    print(f"  Wrote {SKILLS_PL_PATH}")
    SKILLS_METTA_PATH.write_text(metta_sim)
    print(f"  Wrote {SKILLS_METTA_PATH}")

    # Verify disk state matches expected
    print("\n========== DISK VERIFICATION ==========")
    pl_disk_ok = verify_disk(
        SKILLS_PL_PATH, args, "src/skills.pl",
        skills_pl_forward_state_ok, skills_pl_reverse_state_ok,
        check_parens=False,
    )
    metta_disk_ok = verify_disk(
        SKILLS_METTA_PATH, args, "src/skills.metta",
        skills_metta_forward_state_ok, skills_metta_reverse_state_ok,
        check_parens=True,
        extra_check_fn=skills_metta_manifest_integrity_ok,
    )

    if not (pl_disk_ok and metta_disk_ok):
        print("\n========== DISK VERIFICATION FAILED ==========")
        print("Files may be in an inconsistent state. Inspect backups:")
        print(f"  {SKILLS_PL_BAK}")
        print(f"  {SKILLS_METTA_BAK}")
        return 1

    print(f"\n========== {direction} COMPLETE ==========")
    if not args.reverse:
        print("Backups preserved:")
        print(f"  {SKILLS_PL_BAK}")
        print(f"  {SKILLS_METTA_BAK}")
        print("\nNext: rebuild container and verify (gc) call no longer silently fails.")
        print("  docker compose build --no-cache mettaclaw")
        print("  docker compose up -d mettaclaw")
        print("  docker logs clarity_omega 2>&1 | head -50")
    else:
        print("Reverse complete. Original state restored.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
