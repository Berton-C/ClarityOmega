#!/usr/bin/env python3
"""
Apply script: Soul Restoration Repair 1 (Surface 1) -- Output Intercept.
Wires the real output soul verdict in loop.metta plus the artifact_1 phase
entry update, as one coordinated change.

Purpose
-------
The output intercept (loop.metta) is a hardcoded stub:
  ($soul_verdict_out "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix")
The master doc (ClarityClaw Soul Architecture Strategy, Section 14, lines 1403-1436)
specifies a real soul evaluation: native MeTTa mutation gate, then a verdict from
soul-eval-prompt over the parsed response and the mutation flag. This script restores
that, corrected for the two sanctioned divergences and one compliance fix found in the
master-doc compliance pass.

Corrections baked in (vs the earlier loop-only drafts)
------------------------------------------------------
1. Mutation flag uses the NATIVE MeTTa block (doc 1414-1428), replacing
   helper.soul_mutation_gate. The five functions (soul-any-metta?, soul-is-metta-cmd?,
   soul-extract-metta-arg, soul-metta-targets-soul-namespace?, soul-mutation-pending?)
   exist in soul_utils. This also fixes the dropped-lock bug: the native block writes
   &soul_mutation_lock in-gate, so the CONFLICT path works (the Python helper did not).
2. Verdict input is (repr $sexpr), per doc line 1434.
3. Verdict LLM call keeps soul-llm-call ... (provider) -- sanctioned progression
   (Berton), NOT useGPT as the doc literally shows.
4. Output context is (soul-brief-symbolic) -- Option B, doc line 1404.

PRESERVES (verified in the inverse audit):
- the corner_gap line ($sexpr_gated (apply-corner-gate $sexpr)) below this region
- the soul-note-record on non-proceed (now reads a real verdict)
- $metta_cmds computation (the native block consumes it)

Does NOT enforce PAUSE on the output verdict. Output-side halting is Repair 3
(PAUSE router re-enable), gated and downstream. After this repair the output verdict
is real, computed, logged, and the mutation flag is native; execution still proceeds.
Correct intermediate state.

The two edits (one coordinated change, all or none)
---------------------------------------------------
Edit 1: src/loop.metta -- replace the hardcoded verdict region (output intercept)
  Anchor: the hardcoded $soul_verdict_out line + its comment + println, and the
  Python mutation line.
  Result: native mutation block + real verdict (soul-brief-symbolic, repr $sexpr,
  soul-llm-call), $metta_cmds and corner_gap preserved.

Edit 2: docs/design/artifact_1_loop_metta_wiring_diagram.md -- Phase 4.5 update
  (Discipline 4 maintenance contract per artifact 0). Closes the output-intercept
  elevation flag and the mutation-gate elevation flag, records the restored state.

Usage
-----
Dry-run (default):  python3 apply_repair1_output_intercept_v3.py
Apply:              python3 apply_repair1_output_intercept_v3.py --apply
Reverse:            python3 apply_repair1_output_intercept_v3.py --reverse --apply

Pre-conditions
--------------
- soul_utils.metta has the five native mutation functions and soul-brief-symbolic
  (confirmed present)
- Container can be rebuilt after apply
- Anchors confirmed against live src/loop.metta lines 125-134 and artifact_1 Phase 4.5

Backup files (forward apply only):
- src/loop.metta.bak.repair1_output_intercept
- docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.repair1_output_intercept
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.repair1_output_intercept")

ARTIFACT1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ARTIFACT1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.repair1_output_intercept")

IND = " " * 39  # exact live loop indentation for this region

# ============================================================================
# EDIT 1: loop.metta output intercept
# ============================================================================

# Anchors (exact live text, confirmed via sed -n '125,134p' src/loop.metta)
LOOP_OLD_COMMENT = IND + ";; CLARITYCLAW SOUL OUTPUT INTERCEPT (5c)\n"
LOOP_OLD_VERDICT = IND + '($soul_verdict_out "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix")\n'
LOOP_OLD_VERDICT_PRINT = IND + '($_ (println! (SOUL_VERDICT_OUT: $soul_verdict_out)))\n'
LOOP_OLD_MUTATION_PY = IND + '($soul_mutation_flag (py-call (helper.soul_mutation_gate (repr $metta_cmds) (get-state &soul_mutation_lock))))\n'

LOOP_METTA_CMDS_ANCHOR = IND + '($metta_cmds (if (and (== "(" (first_char $resp)) (== (get-state &error) ()))\n'

# New native mutation block (replaces the Python mutation line)
LOOP_NEW_MUTATION_NATIVE = (
    IND + ";; metta() gate: native MeTTa soul-namespace mutation detection (master doc Section 14).\n"
    + IND + ";; Writes &soul_mutation_lock in-gate so the CONFLICT path works.\n"
    + IND + "($soul_mutation_flag\n"
    + IND + "  (if (soul-any-metta? $metta_cmds)\n"
    + IND + "      (let $args (collapse (let $c (superpose $metta_cmds)\n"
    + IND + "                   (if (soul-is-metta-cmd? $c) (soul-extract-metta-arg $c) ())))\n"
    + IND + "           (if (any (collapse (let $a (superpose $args)\n"
    + IND + "                      (soul-metta-targets-soul-namespace? $a))))\n"
    + IND + "               (if (soul-mutation-pending?)\n"
    + IND + '                   "SOUL-NAMESPACE-MUTATION-CONFLICT"\n'
    + IND + "                   (progn\n"
    + IND + "                     (change-state! &soul_mutation_lock\n"
    + IND + '                       (py-str ("LOCKED: " (car-atom $args))))\n'
    + IND + '                     "SOUL-NAMESPACE-MUTATION-PENDING"))\n'
    + IND + '               ""))\n'
    + IND + '      ""))\n'
)

# New real verdict block (inserted after the native mutation block)
LOOP_NEW_VERDICT_BLOCK = (
    IND + ";; OUTPUT EVALUATION: real verdict per master doc Section 14 (soul-llm-call preserved).\n"
    + IND + "($soul_context_out (soul-brief-symbolic))\n"
    + IND + '($soul_verdict_out (soul-llm-call (py-call (helper.soul_eval_prompt $soul_context_out (py-str ((repr $sexpr) " " $soul_mutation_flag)) $person_state)) (provider)))\n'
    + IND + "($_ (change-state! &soul_verdict_out $soul_verdict_out))\n"
    + IND + "($_ (println! (SOUL_VERDICT_OUT: $soul_verdict_out)))\n"
)

# ============================================================================
# EDIT 2: artifact_1 Phase 4.5 update (Discipline 4)
# ============================================================================

ARTIFACT1_OLD_FLAG = (
    '- 🔧 ELEVATION FLAG (architecturally significant): This is the explicit output-side soul evaluation stub. '
    'The note "output-intercept-pending-runtime-fix" acknowledges this is incomplete. Needs to: (a) parse $sexpr '
    'to find proposed actions, (b) assess each action against the irreversibility-action-assessment vocabulary '
    'already in the soul brief, (c) check against soul mutation gate output, (d) produce verdict. Effort: 2-3 hours. '
    'Value: HIGH - closes a known safety stub, gives Clarity output-side governance not just input-side.'
)

ARTIFACT1_NEW_FLAG = (
    '- ✅ RESTORED (Soul Restoration Repair 1, master doc Section 14): the hardcoded stub is replaced with a real '
    'output verdict. The native MeTTa mutation gate computes $soul_mutation_flag (soul-any-metta? through '
    'soul-mutation-pending?, writing &soul_mutation_lock in-gate so the CONFLICT path works), then $soul_verdict_out '
    'is computed from soul-eval-prompt over (repr $sexpr) and the mutation flag, against a fresh (soul-brief-symbolic) '
    'output context, dispatched via soul-llm-call (sanctioned progression, preserved over the doc useGPT). '
    'NOTE: this restores the verdict computation only; output-side PAUSE enforcement is Repair 3 (gated). The verdict '
    'is real, computed, and logged here, but does not yet halt execution. SN-FPN coupling channel is now live on the '
    'evaluation side; the halt side lands with Repair 3.'
)

ARTIFACT1_OLD_MUTGATE_FLAG = (
    '- 🔧 ELEVATION FLAG (READY TO SHIP): Lines 127-140 are the COMMENTED-OUT MeTTa version of this gate. '
    'The work is already drafted. Validation: compare commented MeTTa logic to Python helper logic, confirm equivalence, '
    'uncomment, test. Effort: 30 minutes. Value: HIGH per architectural-cleanliness, MEDIUM per operational impact '
    '(mutations are infrequent).'
)

ARTIFACT1_NEW_MUTGATE_FLAG = (
    '- ✅ RESTORED (Soul Restoration Repair 1): the native MeTTa mutation gate is now wired into the output intercept, '
    'replacing the Python helper.soul_mutation_gate. The native block (soul-any-metta?, soul-is-metta-cmd?, '
    'soul-extract-metta-arg, soul-metta-targets-soul-namespace?, soul-mutation-pending?) is the master-doc Section 14 form. '
    'This also fixes a behavioral regression in the Python helper: it computed the PENDING string but never wrote '
    '&soul_mutation_lock, so the CONFLICT path was dead; the native block writes the lock in-gate.'
)

# ============================================================================
# HELPERS (per reference convention: code-aware paren count, substring count)
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


def count_sub(text: str, target: str) -> int:
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

def simulate_loop_forward(content: str) -> str:
    for label, anchor in [
        ("comment", LOOP_OLD_COMMENT),
        ("hardcoded verdict", LOOP_OLD_VERDICT),
        ("verdict println", LOOP_OLD_VERDICT_PRINT),
        ("python mutation line", LOOP_OLD_MUTATION_PY),
    ]:
        if count_sub(content, anchor) != 1:
            raise RuntimeError(f"loop forward: anchor '{label}' not found exactly once.")
    t = content
    t = t.replace(LOOP_OLD_COMMENT, "", 1)
    t = t.replace(LOOP_OLD_VERDICT, "", 1)
    t = t.replace(LOOP_OLD_VERDICT_PRINT, "", 1)
    t = t.replace(LOOP_OLD_MUTATION_PY, LOOP_NEW_MUTATION_NATIVE, 1)
    t = t.replace(LOOP_NEW_MUTATION_NATIVE, LOOP_NEW_MUTATION_NATIVE + LOOP_NEW_VERDICT_BLOCK, 1)
    return t


def simulate_loop_reverse(content: str) -> str:
    if count_sub(content, LOOP_NEW_MUTATION_NATIVE) != 1 or count_sub(content, LOOP_NEW_VERDICT_BLOCK) != 1:
        raise RuntimeError("loop reverse: new blocks not found exactly once.")
    if count_sub(content, LOOP_METTA_CMDS_ANCHOR) != 1:
        raise RuntimeError("loop reverse: $metta_cmds anchor not found exactly once.")
    t = content
    t = t.replace(LOOP_NEW_MUTATION_NATIVE + LOOP_NEW_VERDICT_BLOCK, LOOP_NEW_MUTATION_NATIVE, 1)
    t = t.replace(LOOP_NEW_MUTATION_NATIVE, LOOP_OLD_MUTATION_PY, 1)
    t = t.replace(LOOP_METTA_CMDS_ANCHOR,
                  LOOP_OLD_COMMENT + LOOP_OLD_VERDICT + LOOP_OLD_VERDICT_PRINT + LOOP_METTA_CMDS_ANCHOR, 1)
    return t


def simulate_artifact1_forward(content: str) -> str:
    for label, anchor in [("output flag", ARTIFACT1_OLD_FLAG), ("mutgate flag", ARTIFACT1_OLD_MUTGATE_FLAG)]:
        if count_sub(content, anchor) != 1:
            raise RuntimeError(f"artifact1 forward: anchor '{label}' not found exactly once.")
    t = content
    t = t.replace(ARTIFACT1_OLD_FLAG, ARTIFACT1_NEW_FLAG, 1)
    t = t.replace(ARTIFACT1_OLD_MUTGATE_FLAG, ARTIFACT1_NEW_MUTGATE_FLAG, 1)
    return t


def simulate_artifact1_reverse(content: str) -> str:
    for label, anchor in [("new output flag", ARTIFACT1_NEW_FLAG), ("new mutgate flag", ARTIFACT1_NEW_MUTGATE_FLAG)]:
        if count_sub(content, anchor) != 1:
            raise RuntimeError(f"artifact1 reverse: anchor '{label}' not found exactly once.")
    t = content
    t = t.replace(ARTIFACT1_NEW_FLAG, ARTIFACT1_OLD_FLAG, 1)
    t = t.replace(ARTIFACT1_NEW_MUTGATE_FLAG, ARTIFACT1_OLD_MUTGATE_FLAG, 1)
    return t


# ============================================================================
# STATE CHECKS
# ============================================================================

def loop_forward_state_ok(content: str) -> tuple[bool, str]:
    a = all(count_sub(content, x) == 1 for x in
            [LOOP_OLD_COMMENT, LOOP_OLD_VERDICT, LOOP_OLD_VERDICT_PRINT, LOOP_OLD_MUTATION_PY])
    n = "soul-brief-symbolic" not in content
    ok = a and n
    return ok, f"old anchors present={a}, new absent={n} -> {'OK' if ok else 'FAIL'}"


def loop_reverse_state_ok(content: str) -> tuple[bool, str]:
    n = count_sub(content, LOOP_NEW_MUTATION_NATIVE) == 1 and count_sub(content, LOOP_NEW_VERDICT_BLOCK) == 1
    return n, f"new blocks present={n} -> {'OK' if n else 'FAIL'}"


def artifact1_forward_state_ok(content: str) -> tuple[bool, str]:
    a = count_sub(content, ARTIFACT1_OLD_FLAG) == 1 and count_sub(content, ARTIFACT1_OLD_MUTGATE_FLAG) == 1
    return a, f"old flags present={a} -> {'OK' if a else 'FAIL'}"


def artifact1_reverse_state_ok(content: str) -> tuple[bool, str]:
    n = count_sub(content, ARTIFACT1_NEW_FLAG) == 1 and count_sub(content, ARTIFACT1_NEW_MUTGATE_FLAG) == 1
    return n, f"new flags present={n} -> {'OK' if n else 'FAIL'}"


# ============================================================================
# PROCESS / VERIFY
# ============================================================================

def process_file(path, bak, sim_fwd, sim_rev, args, label, check_parens, fwd_ok, rev_ok):
    if not path.exists():
        print(f"ERROR: {label} not found at {path} (run from repo root).")
        return False, None, None
    orig = path.read_text()
    pre_ok, pre_msg = (rev_ok(orig) if args.reverse else fwd_ok(orig))
    print(f"  {label} pre-state: {pre_msg}")
    if not pre_ok:
        print(f"  {label}: PRE-STATE CHECK FAILED. Halting (no change).")
        return False, orig, None
    try:
        sim = sim_rev(orig) if args.reverse else sim_fwd(orig)
    except RuntimeError as e:
        print(f"  {label}: SIMULATION FAILED: {e}")
        return False, orig, None
    if check_parens:
        o0, c0 = code_aware_paren_count(orig)
        o1, c1 = code_aware_paren_count(sim)
        delta = (o1 - c1) - (o0 - c0)
        print(f"  {label} code-aware paren delta: {delta} (target 0)")
        if delta != 0:
            print(f"  {label}: PAREN DELTA NONZERO. Halting.")
            return False, orig, None
    return True, orig, sim


def diff_preview(orig: str, sim: str, label: str, context: int = 2) -> str:
    o = orig.splitlines()
    s = sim.splitlines()
    i = 0
    while i < min(len(o), len(s)) and o[i] == s[i]:
        i += 1
    start = max(0, i - context)
    out = [f"--- {label} (first change near line {i + 1}) ---"]
    for k in range(start, min(i + context + 8, max(len(o), len(s)))):
        ol = o[k] if k < len(o) else ""
        sl = s[k] if k < len(s) else ""
        if ol != sl:
            if ol:
                out.append(f"  - {ol}")
            if sl:
                out.append(f"  + {sl}")
        else:
            out.append(f"    {ol}")
    return "\n".join(out)


def verify_disk(path, args, label, fwd_ok, rev_ok, check_parens):
    disk = path.read_text()
    if check_parens:
        o, c = code_aware_paren_count(disk)
        if (o - c) != 0:
            print(f"  {label} disk paren delta nonzero ({o - c}). FAIL")
            return False
    ok, msg = (fwd_ok(disk) if args.reverse else rev_ok(disk))
    print(f"  {label} disk state: {msg}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="Soul Restoration Repair 1: output intercept + artifact_1 (one coordinated change)")
    ap.add_argument("--apply", action="store_true", help="write changes (default dry-run)")
    ap.add_argument("--reverse", action="store_true", help="reverse the edits")
    args = ap.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== SOUL RESTORATION REPAIR 1: {direction} ==========")

    ok_loop, loop_orig, loop_sim = process_file(
        LOOP_PATH, LOOP_BAK, simulate_loop_forward, simulate_loop_reverse,
        args, "loop.metta", True, loop_forward_state_ok, loop_reverse_state_ok)
    if not ok_loop:
        return 1

    ok_art, art_orig, art_sim = process_file(
        ARTIFACT1_PATH, ARTIFACT1_BAK, simulate_artifact1_forward, simulate_artifact1_reverse,
        args, "artifact_1.md", False, artifact1_forward_state_ok, artifact1_reverse_state_ok)
    if not ok_art:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview(loop_orig, loop_sim, "loop.metta"))
    print()
    print(diff_preview(art_orig, art_sim, "artifact_1.md", context=1))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write. Both files change together (all or none).")
        return 0

    if not args.reverse:
        for path, bak in [(LOOP_PATH, LOOP_BAK), (ARTIFACT1_PATH, ARTIFACT1_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    LOOP_PATH.write_text(loop_sim)
    print(f"Wrote: {LOOP_PATH}")
    ARTIFACT1_PATH.write_text(art_sim)
    print(f"Wrote: {ARTIFACT1_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    v1 = verify_disk(LOOP_PATH, args, "loop.metta", loop_forward_state_ok, loop_reverse_state_ok, True)
    v2 = verify_disk(ARTIFACT1_PATH, args, "artifact_1.md", artifact1_forward_state_ok, artifact1_reverse_state_ok, False)
    if not (v1 and v2):
        print("\nDISK VERIFICATION FAILED. Restore:")
        if not args.reverse:
            print(f"  cp {LOOP_BAK} {LOOP_PATH}")
            print(f"  cp {ARTIFACT1_BAK} {ARTIFACT1_PATH}")
        return 1

    print("\n========== REPAIR 1 COMPLETE ==========")
    print("Both edits applied. All checks pass.")
    if not args.reverse:
        print("\nNext: rebuild and observe the output verdict become real (not the static stub).")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d && sleep 15 && docker logs clarity_omega 2>&1 | grep SOUL_VERDICT_OUT | tail -20")
        print("Expect: SOUL_VERDICT_OUT varies with command content, no longer 'output-intercept-pending-runtime-fix'.")
        print("Expect: real-but-not-halting (PAUSE enforcement is Repair 3, gated, downstream).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
