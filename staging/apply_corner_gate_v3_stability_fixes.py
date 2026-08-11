#!/usr/bin/env python3
"""
Apply script: Corner-Gate v3 stability fixes (Phase B).

Purpose
-------
Phase A (phase_a_completeness_probe.py v2, ALL PASS 19/19) and Phase A.1
(phase_a1_core_bisect_probe.py v2, all four injected calls RETURNED) proved
a six-patch fix set for the v3 coupling corridor offline, plus the separately
proven populator amplifier fix. This script lands all three defect fixes as
one coordinated all-or-none change:

- D-1: five collapse guards for partial engine clause tables called bare
  (four q-self-seeing calls in derive-chain-state, one residual call in
  derive-residual-gap). Guard default symbol not-computed follows the
  in-file derive-polarity-verdict convention; probe-proven; subject to
  Clarity ratification at review.
- D-2: derive-support rewritten to engine-identical arithmetic
  (support = (min is as) * (min as os), per engine q-meet min-strength and
  coherence-chain strength product). Root cause: this runtime types bare
  symbols as %Undefined%, never Atom, so transpiler-emitted type guards for
  Atom-carrying constructor signatures (qalignment) are unsatisfiable at
  every call site. Fixtures verified: RB1 0.04; probe 0.18 and 0.81.
- D-3: populate-recent-action prune collapse-wrapped (certified 2026-06-04
  sibling shape from do-clear-state-delta!). Root cause: bare superpose in
  a let* binding leaks N Prolog choice points into loop.metta's cycle tail,
  amplifying the D-1/D-2 failure into per-atom replays.

The eight edits
---------------
Edits 1-4: soul/corner_gap/coupling_legibility.metta, derive-chain-state
  Anchor: each bare q-self-seeing-* binding line (byte-exact, validated
  6 of 6 by the Phase A/A.1 v2 probe runs against this file)
  Replacement: collapse guard with not-computed default. Line delta 0 each.

Edit 5: soul/corner_gap/coupling_legibility.metta, derive-residual-gap
  Anchor: the bare (q-residual-threshold-gap? ...) call
  Replacement: collapse guard with not-computed default. Line delta 0.

Edit 6: soul/corner_gap/coupling_legibility.metta, derive-support
  Anchor: the ten-line typed algebra chain (mk-pbit through
  coupling-pbit-strength), byte-exact
  Replacement: three-line arithmetic form. Line delta -7.

Edit 7: soul/recent_action_populator.metta, $_prune binding
  Anchor: the four-line bare-superpose prune block, byte-exact
  Replacement: five-line guard-empty + collapse-wrapped form. Line delta +1.

Edit 8: none. No loop.metta hook changes; no import changes; both files
  are existing soul/ substrate, already imported. artifact_1 documents
  loop.metta phases and is unaffected (no hook added or moved); the
  investigation record lands in the docs commit alongside this script.

Net change
----------
- coupling_legibility.metta: -7 lines; paren delta 0
- recent_action_populator.metta: +1 line; paren delta 0

Mechanism
---------
- Guards convert zero-solution engine reductions into not-computed instead
  of failing the recorder let* silently (the 176-to-178 death).
- The arithmetic derive-support removes the only corridor path through
  Atom-typed constructor guards, with numerics identical to the engine
  formulas (engine q-meet min-strength; coherence-chain strength product).
- The populator prune contains its nondeterminism (one solution) and
  handles the empty snapshot without halting, per the certified clearer
  shape, ending choice-point leakage into the cycle tail.

Usage
-----
Dry-run (default):
    python3 staging/apply_corner_gate_v3_stability_fixes.py

Apply:
    python3 staging/apply_corner_gate_v3_stability_fixes.py --apply

Reverse (after apply):
    python3 staging/apply_corner_gate_v3_stability_fixes.py --reverse --apply

Pre-conditions
--------------
- Phase A v2 ALL PASS and Phase A.1 v2 all-RETURNED on this repo state
- Clarity review of the dry-run output (her files; not-computed default
  ratification)
- Container restartable after apply

Backup files (forward apply only)
---------------------------------
- soul/corner_gap/coupling_legibility.metta.bak.cgv3_stability
- soul/recent_action_populator.metta.bak.cgv3_stability

Deploy note
-----------
soul/ is bind-mounted into the container (compose config verified
2026-07-21: ./soul -> /PeTTa/repos/omegaclaw/soul), so these edits reach
the runtime on container restart without a rebuild. The conservative
rebuild path also works and is printed on success.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

PURE_PATH = Path("soul/corner_gap/coupling_legibility.metta")
PURE_BAK = Path("soul/corner_gap/coupling_legibility.metta.bak.cgv3_stability")

POP_PATH = Path("soul/recent_action_populator.metta")
POP_BAK = Path("soul/recent_action_populator.metta.bak.cgv3_stability")

# ============================================================================
# EDITS 1-5: collapse guards (coupling_legibility.metta)
# ============================================================================

GUARD_EDITS = [
    ("edit 1 (capture guard)",
     "($capture (q-self-seeing-loop-capture? $repeat $errsurface))",
     "($capture (let $g1 (collapse (q-self-seeing-loop-capture? $repeat $errsurface)) (if (== $g1 ()) not-computed (car-atom $g1))))"),
    ("edit 2 (newvis guard)",
     "($newvis (q-self-seeing-newly-visible-surface? $errsurface $errfeedback))",
     "($newvis (let $g2 (collapse (q-self-seeing-newly-visible-surface? $errsurface $errfeedback)) (if (== $g2 ()) not-computed (car-atom $g2))))"),
    ("edit 3 (shift guard)",
     "($shift (q-self-seeing-orientation-shift? repeated-command $probe $newverr))",
     "($shift (let $g3 (collapse (q-self-seeing-orientation-shift? repeated-command $probe $newverr)) (if (== $g3 ()) not-computed (car-atom $g3))))"),
    ("edit 4 (nav guard)",
     "($nav (q-self-seeing-navigation-change? orientation-shift $trace $future))",
     "($nav (let $g4 (collapse (q-self-seeing-navigation-change? orientation-shift $trace $future)) (if (== $g4 ()) not-computed (car-atom $g4))))"),
    ("edit 5 (residual guard)",
     "(q-residual-threshold-gap? $supsym target-threshold $ressym)",
     "(let $g5 (collapse (q-residual-threshold-gap? $supsym target-threshold $ressym)) (if (== $g5 ()) not-computed (car-atom $g5)))"),
]

# ============================================================================
# EDIT 6: derive-support arithmetic (coupling_legibility.metta)
# ============================================================================

SUPPORT_OLD = (
    "          ($ipbit (mk-pbit $is 0.7))\n"
    "          ($apbit (mk-pbit $as 0.7))\n"
    "          ($opbit (mk-pbit $os 0.7))\n"
    "          ($iapbit (q-meet $ipbit $apbit))\n"
    "          ($aopbit (q-meet $apbit $opbit))\n"
    "          ($e1 (q-intention-action intention action $iapbit))\n"
    "          ($e2 (q-action-outcome action outcome $aopbit))\n"
    "          ($chain (q-coherence-chain $e1 $e2))\n"
    "          ($cpbit (qalignment-pbit $chain))\n"
    "          ($s (coupling-pbit-strength $cpbit)))"
)
SUPPORT_NEW = (
    "          ($ia (min $is $as))\n"
    "          ($ao (min $as $os))\n"
    "          ($s (* $ia $ao)))"
)

# ============================================================================
# EDIT 7: populator prune (recent_action_populator.metta)
# ============================================================================

# Byte-exact block extracted 2026-07-21 from the file (occurrence count 1;
# note the non-uniform internal spacing, preserved deliberately).
POP_OLD = (
    "($_prune       (let $old (superpose $to-remove)\n"
    "                                   (if (== $old ())\n"
    "                                       ()\n"
    "                                       (remove-atom &self $old))))"
)
POP_NEW = (
    "($_prune       (if (== $to-remove ())\n"
    "                                   ()\n"
    "                                   (let $_drained (collapse (let $old (superpose $to-remove)\n"
    "                                                                 (if (== $old ()) () (remove-atom &self $old))))\n"
    "                                      ())))"
)

# ============================================================================
# HELPERS (per apply_task_state_step2_wiring.py template)
# ============================================================================

def code_aware_paren_count(text: str) -> tuple[int, int]:
    """Count parens excluding those inside string literals and line comments."""
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


# ============================================================================
# SIMULATION
# ============================================================================

def simulate_pure_forward(content: str) -> str:
    """Apply edits 1-6 to coupling_legibility.metta."""
    for label, old, new in GUARD_EDITS:
        if find_target_substring_count(content, old) != 1:
            raise RuntimeError(f"pure forward {label}: anchor not found exactly once.")
        content = content.replace(old, new, 1)
    if find_target_substring_count(content, SUPPORT_OLD) != 1:
        raise RuntimeError("pure forward edit 6: derive-support block not found exactly once.")
    content = content.replace(SUPPORT_OLD, SUPPORT_NEW, 1)
    return content


def simulate_pure_reverse(content: str) -> str:
    """Remove edits 1-6 from coupling_legibility.metta (reverse order)."""
    if find_target_substring_count(content, SUPPORT_NEW) != 1:
        raise RuntimeError("pure reverse edit 6: arithmetic block not found exactly once.")
    content = content.replace(SUPPORT_NEW, SUPPORT_OLD, 1)
    for label, old, new in reversed(GUARD_EDITS):
        if find_target_substring_count(content, new) != 1:
            raise RuntimeError(f"pure reverse {label}: guarded form not found exactly once.")
        content = content.replace(new, old, 1)
    return content


def simulate_pop_forward(content: str) -> str:
    """Apply edit 7 to recent_action_populator.metta."""
    if find_target_substring_count(content, POP_OLD) != 1:
        raise RuntimeError(
            "pop forward edit 7: $_prune block not found exactly once (byte drift?). "
            "Paste the $_prune block from the file to re-anchor.")
    return content.replace(POP_OLD, POP_NEW, 1)


def simulate_pop_reverse(content: str) -> str:
    """Remove edit 7 from recent_action_populator.metta."""
    if find_target_substring_count(content, POP_NEW) != 1:
        raise RuntimeError("pop reverse edit 7: collapse-wrapped block not found exactly once.")
    return content.replace(POP_NEW, POP_OLD, 1)


# ============================================================================
# STATE CHECK PREDICATES
# ============================================================================

def pure_forward_state_ok(content: str) -> tuple[bool, str]:
    anchors = all(find_target_substring_count(content, o) == 1 for _, o, _ in GUARD_EDITS)
    a6 = find_target_substring_count(content, SUPPORT_OLD) == 1
    new_absent = ("(let $g1 (collapse" not in content) and (SUPPORT_NEW not in content)
    ok = anchors and a6 and new_absent
    msg = f"anchors 1-5 present={anchors}, support block present={a6}, new absent={new_absent} -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def pure_reverse_state_ok(content: str) -> tuple[bool, str]:
    news = all(find_target_substring_count(content, n) == 1 for _, _, n in GUARD_EDITS)
    n6 = find_target_substring_count(content, SUPPORT_NEW) == 1
    ok = news and n6
    msg = f"guarded forms present={news}, arithmetic block present={n6} -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def pop_forward_state_ok(content: str) -> tuple[bool, str]:
    a = find_target_substring_count(content, POP_OLD) == 1
    n = "collapse (let $old (superpose $to-remove)" not in content
    ok = a and n
    msg = f"prune block present={a}, collapse form absent={n} -> {'OK' if ok else 'FAIL'}"
    return ok, msg


def pop_reverse_state_ok(content: str) -> tuple[bool, str]:
    n = find_target_substring_count(content, POP_NEW) == 1
    msg = f"collapse-wrapped block present={n} -> {'OK' if n else 'FAIL'}"
    return n, msg


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

def check_file_exists(path: Path, label: str) -> bool:
    if not path.exists():
        print(f"ERROR: {label} not found at {path}. Run from repo root.")
        return False
    return True


def process_file(path, bak_path, simulate_fn, simulate_reverse_fn,
                 expected_line_delta_forward, args, label, check_parens,
                 forward_state_check_fn, reverse_state_check_fn):
    print(f"\n>>> {label} <<<")
    content = path.read_text()
    pre_lines = len(content.splitlines())
    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    print(f"  Path: {path}")
    print(f"  Pre-edit line count: {pre_lines}")
    if check_parens:
        c_paren = "OK" if pre_d == 0 else "FAIL"
        print(f"  Pre-edit paren count: opens={pre_o} closes={pre_c} delta={pre_d} ({c_paren})")
        if c_paren != "OK":
            print(f"  PAREN COUNT FAILED for {label}. Aborting.")
            return False, content, ""
    if args.reverse:
        state_ok, state_msg = reverse_state_check_fn(content)
    else:
        state_ok, state_msg = forward_state_check_fn(content)
    print(f"  State check: {state_msg}")
    if not state_ok:
        print(f"  STATE CHECK FAILED for {label}. Aborting.")
        return False, content, ""
    try:
        simulated = simulate_reverse_fn(content) if args.reverse else simulate_fn(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return False, content, ""
    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines
    if check_parens:
        post_o, post_c = code_aware_paren_count(simulated)
        post_d = post_o - post_c
        c_paren_post = "OK" if post_d == 0 else "FAIL"
        print(f"  Post-edit paren count: opens={post_o} closes={post_c} delta={post_d} ({c_paren_post})")
        if c_paren_post != "OK":
            print(f"  POST-EDIT PAREN COUNT FAILED for {label}. Aborting.")
            return False, content, simulated
    expected_delta = expected_line_delta_forward if not args.reverse else -expected_line_delta_forward
    c_lines = "OK" if line_delta == expected_delta else "FAIL"
    print(f"  Line delta: {line_delta} (expected {expected_delta}) ({c_lines})")
    if c_lines != "OK":
        print(f"  LINE DELTA FAILED for {label}. Aborting.")
        return False, content, simulated
    return True, content, simulated


def verify_disk(path, args, label, forward_check_fn, reverse_check_fn, check_parens):
    disk = path.read_text()
    if check_parens:
        o, c = code_aware_paren_count(disk)
        d = o - c
        ok_p = d == 0
        print(f"  {label} disk paren: opens={o} closes={c} delta={d} ({'OK' if ok_p else 'FAIL'})")
        if not ok_p:
            return False
    if args.reverse:
        ok, msg = forward_check_fn(disk)
    else:
        ok, msg = reverse_check_fn(disk)
    print(f"  {label} disk state: {msg}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Corner-Gate v3 stability fixes: D-1 guards + D-2 derive-support + D-3 populator prune"
    )
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== CGV3 STABILITY FIXES: {direction} ==========")

    if not all([
        check_file_exists(PURE_PATH, "coupling_legibility.metta"),
        check_file_exists(POP_PATH, "recent_action_populator.metta"),
    ]):
        return 1

    ok_pure, pure_orig, pure_sim = process_file(
        PURE_PATH, PURE_BAK,
        simulate_pure_forward, simulate_pure_reverse,
        expected_line_delta_forward=-7,
        args=args, label="coupling_legibility.metta",
        check_parens=True,
        forward_state_check_fn=pure_forward_state_ok,
        reverse_state_check_fn=pure_reverse_state_ok,
    )
    if not ok_pure:
        return 1

    ok_pop, pop_orig, pop_sim = process_file(
        POP_PATH, POP_BAK,
        simulate_pop_forward, simulate_pop_reverse,
        expected_line_delta_forward=1,
        args=args, label="recent_action_populator.metta",
        check_parens=True,
        forward_state_check_fn=pop_forward_state_ok,
        reverse_state_check_fn=pop_reverse_state_ok,
    )
    if not ok_pop:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview_first_change(pure_orig, pure_sim, "coupling_legibility.metta (first changed region)", context=2))
    print()
    print(diff_preview_first_change(pop_orig, pop_sim, "recent_action_populator.metta", context=2))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        for path, bak in [(PURE_PATH, PURE_BAK), (POP_PATH, POP_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    PURE_PATH.write_text(pure_sim)
    print(f"Wrote: {PURE_PATH}")
    POP_PATH.write_text(pop_sim)
    print(f"Wrote: {POP_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    v1 = verify_disk(PURE_PATH, args, "coupling_legibility.metta",
                     pure_forward_state_ok, pure_reverse_state_ok, check_parens=True)
    v2 = verify_disk(POP_PATH, args, "recent_action_populator.metta",
                     pop_forward_state_ok, pop_reverse_state_ok, check_parens=True)

    if not (v1 and v2):
        print("\nDISK VERIFICATION FAILED. File(s) may be in inconsistent state.")
        if not args.reverse:
            print("Restore:")
            print(f"  cp {PURE_BAK} {PURE_PATH}")
            print(f"  cp {POP_BAK} {POP_PATH}")
        return 1

    print("\n========== CGV3 STABILITY FIXES COMPLETE ==========")
    print("All edits applied. All checks pass.")
    if not args.reverse:
        print("\nDeploy (soul/ is bind-mounted; restart suffices):")
        print("  docker compose restart clarityclaw && sleep 20 && docker logs clarity_omega 2>&1 | grep -aE 'iteration|TRACE-17|COUPLING' | tail -40")
        print("Conservative alternative (full rebuild):")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    return 0


if __name__ == "__main__":
    sys.exit(main())
