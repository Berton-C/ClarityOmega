#!/usr/bin/env python3
"""
apply_detection_coverage_fix1.py

SURFACE C DETECTION-COVERAGE FIX 1 -- tag the 8 bare-headed constitutional atoms.

PROBLEM (proven by detection_surface_harness + Clarity's enumeration):
  The soul-mutation gate detects soul mutations via membership tagging
  (soul-ns-member HEAD). All ~119 tagged heads are soul-prefixed; ZERO bare heads
  are tagged. But 8 constitutional atom families are stored under BARE heads in
  soul_kernel.metta, so a mutation to any of them passes the gate UNGATED --
  including (priority ...), the alignment anchor.

  The 8 (verified 8/8 present in live kernel by harness Section B):
    priority, irreversible-skill, tension-vector, threatens,
    person-state-type, irreversible-weight, task-context-field, operation-risk

DILIGENCE DONE before this script:
  - Harness Section B: all 8 verified present in soul_kernel.metta.
  - Harness Section D: all 8 writers are BOOT-CONSTRUCTION in soul_kernel.metta;
    ZERO runtime writers -> tagging does NOT over-gate per-cycle work.
  - Boot-path read: the soul-mutation gate lives in the per-cycle let*, NOT in
    the (if (== $k 1) (progn (initLoop)(initMemory)(initSoulSeeds)...)) boot
    branch -> tagging does NOT gate the kernel's own boot construction.

THE FIX (additive append to soul/soul_namespace_membership_seed.metta):
  Add 8 lines, one (soul-ns-member HEAD) per bare constitutional head, in the
  same form as the existing 119 tags. Pure additions; no existing line changes.

NOT IN SCOPE: the general untagged-fallback (Fix 2) -- DEFERRED per Clarity
  (needs careful &self-scoping; separate iteration).

REVERSIBILITY: --reverse --apply removes exactly the 8 added lines.
USAGE:
  python3 apply_detection_coverage_fix1.py                 # dry-run (default)
  python3 apply_detection_coverage_fix1.py --apply         # write
  python3 apply_detection_coverage_fix1.py --reverse --apply
"""

import argparse
import sys
import datetime
from pathlib import Path

TARGET = Path("soul/soul_namespace_membership_seed.metta")
BACKUP = Path("soul/soul_namespace_membership_seed.metta.bak.detection_coverage_fix1")
LOGDIR = Path("shared_files")

# The 8 bare constitutional heads (harness-verified). Order per Clarity's enumeration.
HEADS = [
    "priority",
    "irreversible-skill",
    "tension-vector",
    "threatens",
    "person-state-type",
    "irreversible-weight",
    "task-context-field",
    "operation-risk",
]

# Block marker so the addition is self-identifying and cleanly reversible.
BLOCK_HEADER = ";; Surface C detection-coverage Fix 1: tag bare-headed constitutional atoms"
BLOCK_FOOTER = ";; end Surface C detection-coverage Fix 1"


def tag_line(head: str) -> str:
    return f"!(add-atom &self (soul-ns-member {head}))"


def build_block() -> str:
    lines = [BLOCK_HEADER]
    lines += [tag_line(h) for h in HEADS]
    lines.append(BLOCK_FOOTER)
    return "\n".join(lines)


def code_aware_paren_count(text: str):
    opens = closes = 0
    in_str = False
    esc = False
    for ch in text:
        if esc:
            esc = False
            continue
        if ch == "\\":
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == "(":
            opens += 1
        elif ch == ")":
            closes += 1
    return opens, closes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    ap.add_argument("--reverse", action="store_true", help="reverse the edit")
    args = ap.parse_args()

    mode = ("REVERSE" if args.reverse else "FORWARD") + (" / APPLY" if args.apply else " / DRY-RUN")
    ts = datetime.datetime.now().strftime("%H%M%S")
    log_lines = []

    def out(s=""):
        print(s)
        log_lines.append(s)

    out("=" * 76)
    out("SURFACE C DETECTION-COVERAGE FIX 1 -- tag 8 bare constitutional heads")
    out(f"MODE: {mode}")
    out("=" * 76)

    if not TARGET.exists():
        out(f"ERROR: {TARGET} not found. Run from repo root.")
        return 1

    content = TARGET.read_text()
    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    pre_lines = len(content.splitlines())
    block = build_block()
    # each tag line is balanced: !(add-atom &self (soul-ns-member HEAD)) = 2 opens, 2 closes
    block_o, block_c = code_aware_paren_count(block)

    out("\n>>> PRE-EDIT STATE <<<")
    out(f"  Path: {TARGET}")
    out(f"  Line count: {pre_lines}")
    cpar = "OK" if pre_d == 0 else "FAIL"
    out(f"  Paren: opens={pre_o} closes={pre_c} delta={pre_d} ({cpar})")
    out(f"  Block parens: opens={block_o} closes={block_c} (balanced: {block_o == block_c})")
    if pre_d != 0:
        out("  PAREN IMBALANCE pre-edit. Aborting.")
        return 1

    # Count existing tags for each head (to verify forward = absent, reverse = present)
    per_head_counts = {h: content.count(f"(soul-ns-member {h})") for h in HEADS}

    if not args.reverse:
        out("\n>>> FORWARD STATE CHECK <<<")
        already = [h for h, n in per_head_counts.items() if n > 0]
        block_present = BLOCK_HEADER in content
        for h in HEADS:
            out(f"  tag '(soul-ns-member {h})' present: {per_head_counts[h]} (need 0)")
        out(f"  Fix-1 block already present: {block_present} (need False)")
        if already:
            out(f"  STATE CHECK FAILED. These heads already tagged: {already}. Aborting.")
            return 1
        if block_present:
            out("  STATE CHECK FAILED. Fix-1 block already present. Aborting.")
            return 1
        # Append the block at end of file (with a leading blank line for separation)
        sep = "" if content.endswith("\n") else "\n"
        simulated = content + sep + "\n" + block + "\n"
        expected_line_delta = len(block.splitlines()) + 1  # block lines + 1 blank separator
    else:
        out("\n>>> REVERSE STATE CHECK <<<")
        block_present = BLOCK_HEADER in content and BLOCK_FOOTER in content
        out(f"  Fix-1 block present: {block_present} (need True)")
        for h in HEADS:
            out(f"  tag '(soul-ns-member {h})' present: {per_head_counts[h]} (need >=1)")
        if not block_present:
            out("  STATE CHECK FAILED. Fix-1 block not present. Aborting.")
            return 1
        # Remove the block (and the blank separator line immediately before it)
        start = content.index(BLOCK_HEADER)
        end = content.index(BLOCK_FOOTER) + len(BLOCK_FOOTER)
        # consume trailing newline after footer if present
        if end < len(content) and content[end] == "\n":
            end += 1
        # consume one blank separator line before the header if present
        pre = content[:start]
        if pre.endswith("\n\n"):
            pre = pre[:-1]
        simulated = pre + content[end:]
        expected_line_delta = -(len(block.splitlines()) + 1)

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

    out("\n>>> BLOCK TO " + ("REMOVE" if args.reverse else "ADD") + " <<<")
    for ln in block.splitlines():
        out(f"  {'-' if args.reverse else '+'} {ln}")

    out("\n" + "=" * 76)
    out("ACTION SUMMARY")
    out("=" * 76)
    out(f"  File:        {TARGET}")
    out(f"  Heads tagged: {len(HEADS)} ({', '.join(HEADS)})")
    out(f"  Paren delta:  0   Line delta: {line_delta}")
    out(f"  Reversible:   yes (--reverse --apply)")
    out(f"  NOT in scope: Fix 2 general untagged-fallback (deferred per Clarity)")

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
        p = LOGDIR / f"apply_detection_coverage_fix1_{tag}_{sub}_{ts}.log"
        p.write_text("\n".join(log_lines) + "\n")
        print(f"LOG WRITTEN: {p}")
    except Exception as e:
        print(f"(log write skipped: {e})")


if __name__ == "__main__":
    sys.exit(main())
