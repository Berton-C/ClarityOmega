#!/usr/bin/env python3
"""
apply_repair3_surfaceC.py -- Surface C (soul-mutation lock) all-at-once landing.

Lands the complete six-transition soul-mutation lock state machine in one
reversible pass. Built from the apply_task_state_step2_wiring.py template
(per-edit anchor constants, forward/reverse simulation with exact-occurrence
guards, code-aware paren counting, line-delta enforcement, --apply/--reverse/
--dry-run). Surgical edits only; no `git add .`; reversible.

================================ WHAT THIS LANDS ==============================

soul/ (already in place; NOT edited by this script, listed for the record):
  soul/soul_mutation_lock.metta -- the lock file, six transitions, pending-set
    included. Already at runtime location (verified identical to the built file).

soul_governance.py (already appended in-container during the probe arc; this
  script does NOT re-append, it VERIFIES presence and aborts if missing):
  mutation_fingerprint, gate_decision_record (6-arg), approval_scan.

EDIT 1 -- output_verdict.metta: remove the line-220 lock-write so derive-gate-
  state is a PURE CLASSIFIER. THE COLLISION FIX. derive-gate-state currently
  writes (locked soul-mutation-proposed) (arity-1) on pending; Surface C's
  pending-set writes (locked op head fp) (arity-4, SEAM-2 contract). Two writers,
  incompatible shapes. Resolution (Clarity-confirmed, both caveats verified
  against runtime): derive-gate-state classifies only; pending-set is the sole
  PENDING writer. soul-mutation-pending? (runtime, smgc.metta) is symbol-based
  (lock == unlocked), shape-agnostic -- removing the write does NOT break the
  conflict path.

EDIT 2 -- lib_clarity_reasoning.metta: register soul_mutation_lock import.

EDIT 3 -- loop.metta hook: gate-transition! (input region, $msgnew-guarded).
EDIT 4 -- loop.metta hook: pending-set! (5c, after derive-gate-state pending).
EDIT 5 -- loop.metta hook: stale-check! (5c, before commit, after gate-state).
EDIT 6 -- loop.metta hook: commit-clear! (5c, after $results_final).
EDIT 7 -- loop.metta hook: pause-voice-label (OUTPUT-PAUSE branch, H11).

All loop hooks are single named calls (artifact_0 Discipline 1).

USAGE:
    python3 staging/apply_repair3_surfaceC.py            # dry-run (default)
    python3 staging/apply_repair3_surfaceC.py --apply
    python3 staging/apply_repair3_surfaceC.py --reverse --apply
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import datetime


class _Tee:
    """Mirror stdout to a timestamped log artifact. The run IS the proof; the
    proof must persist. Every invocation writes shared_files/apply_surfaceC_
    <MODE>_<HHMMSS>.log so no run goes uncaptured (standing convention)."""

    def __init__(self, logpath):
        self._term = sys.stdout
        self._log = open(logpath, "w")

    def write(self, data):
        self._term.write(data)
        self._log.write(data)

    def flush(self):
        self._term.flush()
        self._log.flush()

    def close(self):
        self._log.close()

# ============================================================================
# FILE PATHS (relative to repo root)
# ============================================================================

OV_PATH = Path("soul/output_verdict.metta")
LIB_CR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LOOP_PATH = Path("src/loop.metta")
GOV_PATH = Path("soul/soul_governance.py")
LOCK_PATH = Path("soul/soul_mutation_lock.metta")

OV_BAK = Path("soul/output_verdict.metta.surfaceC.bak")
LIB_CR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.surfaceC.bak")
LOOP_BAK = Path("src/loop.metta.surfaceC.bak")

# ============================================================================
# EDIT 1: output_verdict.metta -- derive-gate-state becomes pure classifier
# ============================================================================
# Anchor: the current pending branch that writes the arity-1 lock.
# Replacement: return `pending` WITHOUT the change-state! (pure classification).

OV_ANCHOR = (
    "(= (derive-gate-state $cmds)\n"
    "   (if (batch-targets-soul? $cmds)\n"
    "       (if (soul-mutation-pending?)\n"
    "           conflict\n"
    "           (let $_ (change-state! &soul_mutation_lock (locked soul-mutation-proposed))\n"
    "                pending))\n"
    "       clean))"
)
OV_NEW = (
    "(= (derive-gate-state $cmds)\n"
    "   ;; Surface C: PURE CLASSIFIER. The lock-write (was: (locked soul-mutation-\n"
    "   ;; proposed)) is removed -- clarity-soul-mutation-pending-set! is the sole\n"
    "   ;; PENDING writer, writing the arity-4 SEAM-2 shape (locked op head fp).\n"
    "   ;; soul-mutation-pending? is symbol-based (lock == unlocked), shape-agnostic.\n"
    "   (if (batch-targets-soul? $cmds)\n"
    "       (if (soul-mutation-pending?)\n"
    "           conflict\n"
    "           pending)\n"
    "       clean))"
)

# ============================================================================
# EDIT 2: lib_clarity_reasoning.metta -- register soul_mutation_lock
# ============================================================================
# Anchor: the task_state_writers import (last soul import block per the file).

LIB_CR_ANCHOR = "!(import! &self (library omegaclaw ./soul/task_state_writers))"
LIB_CR_OLD_BLOCK = LIB_CR_ANCHOR + "\n"
LIB_CR_NEW_BLOCK = (
    LIB_CR_ANCHOR + "\n"
    "\n"
    ";; Surface C: soul-mutation lock state machine (the metta() self-mutation gate)\n"
    "!(import! &self (library omegaclaw ./soul/soul_mutation_lock))\n"
)

# ============================================================================
# EDIT 3: loop.metta -- gate-transition! hook (input region, $msgnew-guarded)
# ============================================================================
# Anchor: the post-msgnew last-activity hook (where new-message side-effects live).

LOOP_ANCHOR_GATE_TRANS = "                                       ($_ (if $msgnew (do-set-last-activity! (get_time)) _))"
LOOP_NEW_GATE_TRANS = (
    LOOP_ANCHOR_GATE_TRANS + "\n"
    "                                       ;; Surface C: approval/denial transition while a soul-mutation lock is held\n"
    "                                       ($_ (if $msgnew (clarity-soul-mutation-gate-transition! $msg $k) _))"
)

# ============================================================================
# EDIT 4 + 5: loop.metta -- pending-set! and stale-check! (5c, after gate-state)
# ============================================================================
# Anchor: the SOUL-GATE-FLAG println, immediately after derive-gate-state.
# pending-set fires when gate-state is pending (fresh detection); stale-check
# runs here so it precedes commit-clear (STALE precedence). Both land in one
# block after the anchor to keep a single, ordered insertion point.

LOOP_ANCHOR_GATE_FLAG = "                                       ($_ (println! (SOUL-GATE-FLAG $soul_gate_state (get-state &soul_mutation_lock))))"
LOOP_NEW_GATE_FLAG = (
    LOOP_ANCHOR_GATE_FLAG + "\n"
    "                                       ;; Surface C: PENDING entry -- sole arity-4 lock writer, on fresh detection\n"
    "                                       ($_ (if (== $soul_gate_state pending) (clarity-soul-mutation-pending-set! $metta_cmds $k) _))\n"
    "                                       ;; Surface C: STALE check -- runs BEFORE commit-clear (STALE precedence)\n"
    "                                       ($_ (clarity-soul-mutation-stale-check! $k))"
)

# ============================================================================
# EDIT 6: loop.metta -- commit-clear! hook (5c, after $results_final)
# ============================================================================
# Anchor: the RESULTS-EXECUTED println, immediately after $results_final binds.
# errored boolean: True when the &error channel is non-empty after execution.

LOOP_ANCHOR_RESULTS_EXEC = "                                       ($_ (println! (RESULTS-EXECUTED)))"
LOOP_NEW_RESULTS_EXEC = (
    LOOP_ANCHOR_RESULTS_EXEC + "\n"
    "                                       ;; Surface C: COMMIT/ERROR clearance -- approved lock cleared post-execution\n"
    "                                       ($_ (clarity-soul-mutation-commit-clear! $soul_gate_state $soul_decision (not (== (get-state &error) ()))))"
)

# ============================================================================
# EDIT 8: loop.metta -- seed the two state vars the gate hooks READ but that are
# only written conditionally (pending-set / approval). Without these, a get-state
# on an unseeded var throws nb_getval and crashes the container: &last_gate_
# fingerprint is read in the OUTPUT-PAUSE branch (any composite-PAUSE), and
# &authorized_approvers is read in gate-transition! (first approval). Seed both at
# initLoop, after the existing lock-state seeds (loop.metta line 31), to their
# already-designed values. The fingerprint hash auth (mutation_fingerprint /
# approval_scan match) is untouched; this only makes boot-state exist.
# Anchor is the UNIQUE two-line initLoop seed block (lines 30-31). The single
# line (change-state! &last_pause_note "") is NON-UNIQUE -- it also appears at
# line 151 inside the PAUSE branch (47-space indent). The two-line block
# (pending_soul_mutation then last_pause_note, both 10-space) occurs exactly
# once, so it is a safe anchor. The replacement KEEPS the block and appends the
# two new seeds after it.
LOOP_ANCHOR_SEED = (
    '          (change-state! &pending_soul_mutation "")\n'
    '          (change-state! &last_pause_note "")'
)
LOOP_NEW_SEED = (
    LOOP_ANCHOR_SEED + "\n"
    "          ;; Surface C: seed the gate-read vars so unseeded get-state cannot crash the\n"
    "          ;; container (last_gate_fingerprint read in OUTPUT-PAUSE; authorized_approvers\n"
    "          ;; read in gate-transition!). Already-designed values; hash auth untouched.\n"
    '          (change-state! &last_gate_fingerprint "")\n'
    '          (change-state! &authorized_approvers "berton_c")'
)

# EDIT 7: loop.metta -- pause-voice-label hook (OUTPUT-PAUSE branch, H11)
# ============================================================================
# Anchor: the OUTPUT-PAUSE soul_voice_out binding. Wrap the voice with the
# [SOUL-PAUSE <fp>] label so the announcement carries the fingerprint.

LOOP_ANCHOR_PAUSE_VOICE = "                                          (let* (($soul_voice_out (soul-llm-call\n                                                    (py-call (helper.soul_voice_prompt $person_state $soul_verdict_out))\n                                                    (provider)))"
LOOP_NEW_PAUSE_VOICE = (
    "                                          (let* (($soul_voice_raw (soul-llm-call\n"
    "                                                    (py-call (helper.soul_voice_prompt $person_state $soul_verdict_out))\n"
    "                                                    (provider)))\n"
    "                                                 ;; Surface C H11: prefix the pause voice with [SOUL-PAUSE <fp>]\n"
    "                                                 ($soul_voice_out (pause-voice-label (get-state &last_gate_fingerprint) $soul_voice_raw))"
)

# ============================================================================
# HELPERS (mirrored from template)
# ============================================================================

def code_aware_paren_count(text: str) -> tuple[int, int]:
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
# SIMULATION -- output_verdict.metta
# ============================================================================

def simulate_ov_forward(content: str) -> str:
    if find_target_substring_count(content, OV_ANCHOR) != 1:
        raise RuntimeError("ov forward: derive-gate-state anchor not found exactly once.")
    return content.replace(OV_ANCHOR, OV_NEW, 1)


def simulate_ov_reverse(content: str) -> str:
    if find_target_substring_count(content, OV_NEW) != 1:
        raise RuntimeError("ov reverse: pure-classifier block not found exactly once.")
    return content.replace(OV_NEW, OV_ANCHOR, 1)


# ============================================================================
# SIMULATION -- lib_clarity_reasoning.metta
# ============================================================================

def simulate_lib_cr_forward(content: str) -> str:
    if find_target_substring_count(content, LIB_CR_OLD_BLOCK) != 1:
        raise RuntimeError("lib_cr forward: task_state_writers import not found exactly once.")
    return content.replace(LIB_CR_OLD_BLOCK, LIB_CR_NEW_BLOCK, 1)


def simulate_lib_cr_reverse(content: str) -> str:
    if find_target_substring_count(content, LIB_CR_NEW_BLOCK) != 1:
        raise RuntimeError("lib_cr reverse: new import block not found exactly once.")
    return content.replace(LIB_CR_NEW_BLOCK, LIB_CR_OLD_BLOCK, 1)


# ============================================================================
# SIMULATION -- loop.metta (5 hook insertions)
# ============================================================================

def simulate_loop_forward(content: str) -> str:
    for anchor, label in [
        (LOOP_ANCHOR_GATE_TRANS, "gate-transition"),
        (LOOP_ANCHOR_GATE_FLAG, "pending-set+stale"),
        (LOOP_ANCHOR_RESULTS_EXEC, "commit-clear"),
        (LOOP_ANCHOR_PAUSE_VOICE, "pause-voice"),
        (LOOP_ANCHOR_SEED, "initloop-seed"),
    ]:
        if find_target_substring_count(content, anchor) != 1:
            raise RuntimeError(f"loop forward: anchor {label} not found exactly once.")
    content = content.replace(LOOP_ANCHOR_GATE_TRANS, LOOP_NEW_GATE_TRANS, 1)
    content = content.replace(LOOP_ANCHOR_GATE_FLAG, LOOP_NEW_GATE_FLAG, 1)
    content = content.replace(LOOP_ANCHOR_RESULTS_EXEC, LOOP_NEW_RESULTS_EXEC, 1)
    content = content.replace(LOOP_ANCHOR_PAUSE_VOICE, LOOP_NEW_PAUSE_VOICE, 1)
    content = content.replace(LOOP_ANCHOR_SEED, LOOP_NEW_SEED, 1)
    return content


def simulate_loop_reverse(content: str) -> str:
    for new, label in [
        (LOOP_NEW_SEED, "initloop-seed"),
        (LOOP_NEW_PAUSE_VOICE, "pause-voice"),
        (LOOP_NEW_RESULTS_EXEC, "commit-clear"),
        (LOOP_NEW_GATE_FLAG, "pending-set+stale"),
        (LOOP_NEW_GATE_TRANS, "gate-transition"),
    ]:
        if find_target_substring_count(content, new) != 1:
            raise RuntimeError(f"loop reverse: new state {label} not found exactly once.")
    content = content.replace(LOOP_NEW_SEED, LOOP_ANCHOR_SEED, 1)
    content = content.replace(LOOP_NEW_PAUSE_VOICE, LOOP_ANCHOR_PAUSE_VOICE, 1)
    content = content.replace(LOOP_NEW_RESULTS_EXEC, LOOP_ANCHOR_RESULTS_EXEC, 1)
    content = content.replace(LOOP_NEW_GATE_FLAG, LOOP_ANCHOR_GATE_FLAG, 1)
    content = content.replace(LOOP_NEW_GATE_TRANS, LOOP_ANCHOR_GATE_TRANS, 1)
    return content


# ============================================================================
# STATE CHECKS
# ============================================================================

def ov_forward_state_ok(content: str):
    has_anchor = find_target_substring_count(content, OV_ANCHOR) == 1
    no_new = "PURE CLASSIFIER" not in content
    ok = has_anchor and no_new
    return ok, f"line-220 lock-write present={has_anchor}, not-yet-pure={no_new} -> {'OK' if ok else 'FAIL'}"


def ov_reverse_state_ok(content: str):
    has_new = find_target_substring_count(content, OV_NEW) == 1
    return has_new, f"pure-classifier present={has_new} -> {'OK' if has_new else 'FAIL'}"


def lib_cr_forward_state_ok(content: str):
    has_anchor = find_target_substring_count(content, LIB_CR_ANCHOR + "\n") == 1
    no_new = "soul_mutation_lock" not in content
    ok = has_anchor and no_new
    return ok, f"anchor present={has_anchor}, lock-import absent={no_new} -> {'OK' if ok else 'FAIL'}"


def lib_cr_reverse_state_ok(content: str):
    has_new = find_target_substring_count(content, LIB_CR_NEW_BLOCK) == 1
    return has_new, f"lock-import block present={has_new} -> {'OK' if has_new else 'FAIL'}"


def loop_forward_state_ok(content: str):
    anchors = all(find_target_substring_count(content, a) == 1 for a in
                  [LOOP_ANCHOR_GATE_TRANS, LOOP_ANCHOR_GATE_FLAG, LOOP_ANCHOR_RESULTS_EXEC, LOOP_ANCHOR_PAUSE_VOICE, LOOP_ANCHOR_SEED])
    no_hooks = all(h not in content for h in
                   ["clarity-soul-mutation-gate-transition!", "clarity-soul-mutation-pending-set!",
                    "clarity-soul-mutation-stale-check!", "clarity-soul-mutation-commit-clear!",
                    "pause-voice-label", "change-state! &last_gate_fingerprint"])
    ok = anchors and no_hooks
    return ok, f"all 5 anchors present={anchors}, no hooks yet={no_hooks} -> {'OK' if ok else 'FAIL'}"


def loop_reverse_state_ok(content: str):
    hooks = all(find_target_substring_count(content, n) == 1 for n in
                [LOOP_NEW_GATE_TRANS, LOOP_NEW_GATE_FLAG, LOOP_NEW_RESULTS_EXEC, LOOP_NEW_PAUSE_VOICE, LOOP_NEW_SEED])
    return hooks, f"all 4 hook blocks present={hooks} -> {'OK' if hooks else 'FAIL'}"


# ============================================================================
# DEPENDENCY VERIFICATION (soul_governance fns + lock file present)
# ============================================================================

def verify_dependencies() -> bool:
    ok = True
    if not GOV_PATH.exists():
        print(f"  DEP FAIL: {GOV_PATH} not found.")
        return False
    gov = GOV_PATH.read_text()
    for fn in ["def mutation_fingerprint", "def gate_decision_record", "def approval_scan"]:
        present = fn in gov
        print(f"  soul_governance {fn.split()[1]}: {'present' if present else 'MISSING'}")
        ok = ok and present
    if not LOCK_PATH.exists():
        print(f"  DEP FAIL: {LOCK_PATH} not found.")
        return False
    lock = LOCK_PATH.read_text()
    for fn in ["clarity-soul-mutation-pending-set!", "clarity-soul-mutation-gate-transition!",
               "clarity-soul-mutation-stale-check!", "clarity-soul-mutation-commit-clear!", "pause-voice-label"]:
        present = fn in lock
        print(f"  lock file {fn}: {'present' if present else 'MISSING'}")
        ok = ok and present
    return ok


# ============================================================================
# PROCESS
# ============================================================================

def process_file(path, bak_path, sim_fwd, sim_rev, expected_delta, args, label,
                 check_parens, fwd_state, rev_state):
    print(f"\n>>> {label} <<<")
    if not path.exists():
        print(f"  ERROR: {path} not found. Run from repo root.")
        return False, "", ""
    content = path.read_text()
    pre_lines = len(content.splitlines())
    print(f"  Path: {path}")
    print(f"  Pre-edit line count: {pre_lines}")
    if check_parens:
        po, pc = code_aware_paren_count(content)
        pd = po - pc
        cp = "OK" if pd == 0 else "FAIL"
        print(f"  Pre-edit paren: opens={po} closes={pc} delta={pd} ({cp})")
        if cp != "OK":
            print(f"  PAREN FAIL for {label}. Aborting.")
            return False, content, ""
    state_ok, msg = (rev_state(content) if args.reverse else fwd_state(content))
    print(f"  State check: {msg}")
    if not state_ok:
        print(f"  STATE CHECK FAILED for {label}. Aborting.")
        return False, content, ""
    try:
        simulated = sim_rev(content) if args.reverse else sim_fwd(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return False, content, ""
    post_lines = len(simulated.splitlines())
    delta = post_lines - pre_lines
    if check_parens:
        so, sc = code_aware_paren_count(simulated)
        sd = so - sc
        cp = "OK" if sd == 0 else "FAIL"
        print(f"  Post-edit paren: opens={so} closes={sc} delta={sd} ({cp})")
        if cp != "OK":
            print(f"  POST-EDIT PAREN FAIL for {label}. Aborting.")
            return False, content, simulated
    exp = expected_delta if not args.reverse else -expected_delta
    cl = "OK" if delta == exp else "FAIL"
    print(f"  Line delta: {delta} (expected {exp}) ({cl})")
    if cl != "OK":
        print(f"  LINE DELTA FAIL for {label}. Aborting.")
        return False, content, simulated
    return True, content, simulated


def backup_if_needed(path, bak, dry):
    if dry or bak.exists():
        return
    bak.write_bytes(path.read_bytes())


def main():
    ap = argparse.ArgumentParser(description="Surface C all-at-once landing.")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    ap.add_argument("--reverse", action="store_true", help="reverse the edits")
    args = ap.parse_args()
    dry = not args.apply

    # Self-logging: capture this run as a persistent artifact (the run is proof).
    _mode = ("reverse" if args.reverse else "forward") + ("_dryrun" if dry else "_apply")
    _ts = datetime.datetime.now().strftime("%H%M%S")
    _logdir = Path("shared_files")
    _logdir.mkdir(exist_ok=True)
    _logpath = _logdir / f"apply_surfaceC_{_mode}_{_ts}.log"
    _tee = _Tee(_logpath)
    sys.stdout = _tee

    print("=" * 76)
    print("SURFACE C LANDING -- soul-mutation lock state machine (all-at-once)")
    print(f"MODE: {'REVERSE' if args.reverse else 'FORWARD'} / {'DRY-RUN' if dry else 'APPLY'}")
    print("=" * 76)

    print("\n>>> DEPENDENCY VERIFICATION <<<")
    if not args.reverse and not verify_dependencies():
        print("\nDEPENDENCIES MISSING. Append soul_governance fns / place lock file first. Aborting.")
        print(f"LOG WRITTEN: {_logpath}")
        sys.stdout = _tee._term; _tee.close()
        return 1

    # EXPECTED LINE DELTAS (forward)
    OV_DELTA = 3        # 7-line anchor -> 10-line block (+3: removes change-state!, adds 4 comment lines net +3)
    LIB_CR_DELTA = 3    # blank + comment + import
    LOOP_DELTA = 15     # gate-trans(+2) + pending/stale(+4) + commit(+2) + pause(+2) + seed(+5: 3 comment + 2 seed)

    results = []
    ov = process_file(OV_PATH, OV_BAK, simulate_ov_forward, simulate_ov_reverse,
                      OV_DELTA, args, "EDIT 1: output_verdict.metta (collision fix)",
                      True, ov_forward_state_ok, ov_reverse_state_ok)
    results.append(("output_verdict.metta", OV_PATH, OV_BAK, ov))

    lib = process_file(LIB_CR_PATH, LIB_CR_BAK, simulate_lib_cr_forward, simulate_lib_cr_reverse,
                       LIB_CR_DELTA, args, "EDIT 2: lib_clarity_reasoning.metta (registration)",
                       False, lib_cr_forward_state_ok, lib_cr_reverse_state_ok)
    results.append(("lib_clarity_reasoning.metta", LIB_CR_PATH, LIB_CR_BAK, lib))

    loop = process_file(LOOP_PATH, LOOP_BAK, simulate_loop_forward, simulate_loop_reverse,
                        LOOP_DELTA, args, "EDITS 3-7: loop.metta (5 hooks)",
                        True, loop_forward_state_ok, loop_reverse_state_ok)
    results.append(("loop.metta", LOOP_PATH, LOOP_BAK, loop))

    all_ok = all(r[3][0] for r in results)
    print("\n" + "=" * 76)
    print("ACTION SUMMARY")
    print("=" * 76)
    for name, _, _, (ok, _, _) in results:
        print(f"  {name:34} {'PASS' if ok else 'FAIL'}")
    if not all_ok:
        print("\nONE OR MORE EDITS FAILED. No files written. Resolve and re-run.")
        print(f"LOG WRITTEN: {_logpath}")
        sys.stdout = _tee._term; _tee.close()
        return 1

    if dry:
        print("\nDRY-RUN OK. All edits simulate clean. Re-run with --apply to write.")
        print(f"LOG WRITTEN: {_logpath}")
        sys.stdout = _tee._term; _tee.close()
        return 0

    for name, path, bak, (ok, original, simulated) in results:
        backup_if_needed(path, bak, dry)
        path.write_text(simulated)
        print(f"  WROTE {path} (backup: {bak})")
    print("\nAPPLIED. Next: docker compose build --no-cache clarityclaw && docker compose up -d")
    print("Then verify boot, then live end-to-end (trigger soul mutation, PENDING->APPROVED->COMMIT).")
    print(f"LOG WRITTEN: {_logpath}")
    sys.stdout = _tee._term; _tee.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
