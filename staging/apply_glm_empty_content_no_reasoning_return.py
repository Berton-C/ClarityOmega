#!/usr/bin/env python3
"""
Apply script: GLM empty-content fix. Stops returning reasoning_content as
the response; adds a per-call boundary diagnostic.

Purpose
-------
On some heavy-reasoning cycles GLM returns empty message.content with the
deliberation in message.reasoning_content. GlmProvider.chat (lib_llm_ext.py)
fell back to returning reasoning_content as the response. The canon
balance_parentheses line splitter then executed every draft (send ...) line
inside her deliberation. History proof (2026-07-04): the 13:28:08 entry is
ONE batch, THREE send commands, first token ((Let "me carefully analyze..."
which is reasoning captured as a pseudo-command. The Mattermost duplicate
bursts and reasoning walls follow from this mechanism.

This script lands the fix plus the instrumentation that makes it
falsifiable. Two edits in one file. All or none.

The two edits
-------------
Edit D: class docstring accuracy (lines ~106-108)
  Anchor: the three docstring lines describing the old fallback
  Replacement: five lines describing the new print-only behavior

Edit F: the chat() fallback block (lines ~136-141)
  Anchor: the six-line block from msg assignment through return
  Replacement: 21 lines: same content extraction, plus reasoning
  extraction, plus one diagnostic print per call
  (content_len / reasoning_len / fallback_would_have_fired), plus the
  empty-content branch that prints reasoning labeled for visibility and
  returns "" instead of returning the reasoning as the response.

Falsifiability (why the diagnostic ships with the fix)
------------------------------------------------------
M1 true (fallback was the dump source): dumps stop; the log shows
fallback_would_have_fired=True lines at exactly the moments dumps used to
occur, with the labeled reasoning printed beneath.
M2 true (GLM put reasoning inside content): dumps persist; the log shows
those cycles with large content_len and fallback_would_have_fired=False,
redirecting the investigation with evidence in hand.
Either way the mechanism question closes on live evidence.

Behavior guarantees
-------------------
- Non-empty content cycles: byte-identical return value to today; the only
  addition is the one diagnostic print line.
- Empty-content cycles: reasoning visibility is PRESERVED (printed to the
  container log, labeled) per the standing requirement; the command channel
  receives "", which takes the existing safe path in the loop (first_char
  gate no-ops a non-paren response with a format reminder).
- Soul-absent note (First Principles S7 Q1): this CLOSES a soul-absent
  surface (LLM deliberation reaching the person as sends no determination
  authored) and opens none.

Net change
----------
- lib_llm_ext.py: Edit D +2 lines, Edit F +15 lines, total +17 lines
- Verification: py_compile of the simulated file (Python target; the metta
  paren count does not apply and is replaced by py_compile, run in
  simulation and again against disk after write)

Deployment
----------
lib_llm_ext.py is BAKED into the image (mount map read 2026-07-04: only
memory, chroma_db, shared_files, soul are mounted). Rebuild required:
  docker compose build --no-cache clarityclaw && docker compose up -d

Usage
-----
Dry-run (default):
    python3 staging/apply_glm_empty_content_no_reasoning_return.py

Apply:
    python3 staging/apply_glm_empty_content_no_reasoning_return.py --apply

Reverse (after apply):
    python3 staging/apply_glm_empty_content_no_reasoning_return.py --reverse --apply

Pre-conditions
--------------
- Run from repo root
- lib_llm_ext.py at repo root matches the live-image bytes at both anchors
  (verified 2026-07-04 via in-container grep; the state checks below
  re-enforce this at apply time)

Backup file (forward apply only):
- lib_llm_ext.py.bak.glm_empty_content
"""
from __future__ import annotations

import argparse
import py_compile
import sys
import tempfile
import os
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

TARGET_PATH = Path("lib_llm_ext.py")
TARGET_BAK = Path("lib_llm_ext.py.bak.glm_empty_content")

# ============================================================================
# EDIT D: class docstring accuracy
# ============================================================================

D_OLD = '''      - In thinking mode, response may have empty message.content
        with reasoning text in message.reasoning_content -- fall back
        to reasoning_content when content is empty.'''

D_NEW = '''      - In thinking mode, response may have empty message.content
        with reasoning text in message.reasoning_content. That reasoning
        is PRINTED to the log for visibility but NOT returned as the
        response (returning it fed her deliberation to the command
        parser: draft send lines executed as real sends, 2026-07-04).'''

# ============================================================================
# EDIT F: chat() fallback block
# ============================================================================

F_OLD = '''            msg = response.choices[0].message
            text = (getattr(msg, "content", None) or "").strip()
            if not text:
                # GLM thinking-mode fallback: substance may live in reasoning_content
                text = (getattr(msg, "reasoning_content", None) or "").strip()
            return self._clean_text(text)'''

F_NEW = '''            msg = response.choices[0].message
            text = (getattr(msg, "content", None) or "").strip()
            reasoning = (getattr(msg, "reasoning_content", None) or "").strip()
            # Boundary diagnostic (2026-07-04): one line per call, makes the
            # empty-content mechanism observable and this fix falsifiable.
            print("[GlmProvider.chat] content_len=%d reasoning_len=%d fallback_would_have_fired=%s"
                  % (len(text), len(reasoning), (not text) and bool(reasoning)))
            if not text:
                # Empty-content cycle. The old fallback returned
                # reasoning_content as the response; the canon line splitter
                # then executed every draft (send ...) line inside her
                # deliberation (proven 2026-07-04: the 13:28 batch, one
                # entry, three sends, reasoning-as-content header) and
                # reasoning walls reached Mattermost. Visibility is
                # preserved by printing the reasoning here, labeled; the
                # command channel gets an empty response, which takes the
                # existing safe path in the loop (first_char gate no-ops
                # with a format reminder).
                if reasoning:
                    print("[GlmProvider.chat] content EMPTY; reasoning_content follows (visibility only, NOT returned as commands):")
                    print(reasoning)
                return ""
            return self._clean_text(text)'''

EXPECTED_LINE_DELTA_FORWARD = (
    (D_NEW.count("\n") - D_OLD.count("\n"))
    + (F_NEW.count("\n") - F_OLD.count("\n"))
)

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


def py_compile_ok(content: str, label: str) -> bool:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8") as tf:
        tf.write(content)
        tmp = tf.name
    try:
        py_compile.compile(tmp, doraise=True)
        print(f"  {label} py_compile: PASS")
        return True
    except py_compile.PyCompileError as exc:
        print(f"  {label} py_compile: FAIL")
        print(f"  {exc}")
        return False
    finally:
        os.unlink(tmp)


# ============================================================================
# SIMULATION
# ============================================================================

def simulate_forward(content: str) -> str:
    if find_target_substring_count(content, D_OLD) != 1:
        raise RuntimeError("edit D forward: docstring anchor not found exactly once.")
    content = content.replace(D_OLD, D_NEW, 1)
    if find_target_substring_count(content, F_OLD) != 1:
        raise RuntimeError("edit F forward: fallback block not found exactly once.")
    content = content.replace(F_OLD, F_NEW, 1)
    return content


def simulate_reverse(content: str) -> str:
    if find_target_substring_count(content, F_NEW) != 1:
        raise RuntimeError("edit F reverse: new block not found exactly once.")
    content = content.replace(F_NEW, F_OLD, 1)
    if find_target_substring_count(content, D_NEW) != 1:
        raise RuntimeError("edit D reverse: new docstring not found exactly once.")
    content = content.replace(D_NEW, D_OLD, 1)
    return content


# ============================================================================
# STATE CHECK PREDICATES
# ============================================================================

def forward_state_ok(content: str) -> tuple[bool, str]:
    d = find_target_substring_count(content, D_OLD) == 1
    f = find_target_substring_count(content, F_OLD) == 1
    new_absent = "fallback_would_have_fired" not in content
    ok = d and f and new_absent
    msg = f"anchors=(D:{d},F:{f}) new_absent={new_absent} -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def reverse_state_ok(content: str) -> tuple[bool, str]:
    d = find_target_substring_count(content, D_NEW) == 1
    f = find_target_substring_count(content, F_NEW) == 1
    ok = d and f
    msg = f"new_states=(D:{d},F:{f}) -> {'OK' if ok else 'FAIL'}"
    return ok, msg


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
        description="GLM empty-content fix: stop returning reasoning_content as the response (+diagnostic)"
    )
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== GLM EMPTY-CONTENT FIX: {direction} ==========")

    if not TARGET_PATH.exists():
        print(f"ERROR: {TARGET_PATH} not found. Run from repo root.")
        return 1

    content = TARGET_PATH.read_text()
    pre_lines = len(content.splitlines())
    print(f"\n>>> {TARGET_PATH} <<<")
    print(f"  Pre-edit line count: {pre_lines}")

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

    if not py_compile_ok(simulated, "simulated lib_llm_ext.py"):
        return 1

    print("\n========== DIFF PREVIEW ==========")
    print(diff_preview_first_change(content, simulated, "lib_llm_ext.py", context=2))

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
    if args.reverse:
        ok, msg = forward_state_ok(disk)
    else:
        ok, msg = reverse_state_ok(disk)
    print(f"  disk state: {msg}")
    if not py_compile_ok(disk, "on-disk lib_llm_ext.py"):
        ok = False
    if not ok:
        print("\nDISK VERIFICATION FAILED. File may be in inconsistent state.")
        if not args.reverse:
            print(f"Restore:  cp {TARGET_BAK} {TARGET_PATH}")
        return 1

    print("\n========== GLM EMPTY-CONTENT FIX COMPLETE ==========")
    print("Both edits applied. All checks pass.")
    if not args.reverse:
        print("\nNext: rebuild and watch the boundary log.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d")
        print("  docker logs clarity_omega 2>&1 | grep GlmProvider.chat | tail -20")
    return 0


if __name__ == "__main__":
    sys.exit(main())
