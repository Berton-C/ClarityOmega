#!/usr/bin/env python3
"""
Apply script: Output-governance kernel seeds + producer-layer padding fixes.
Per output_governance_design_v1.md v1.3 (locked) build sequence step 2.
Authored in-house (Berton + Claude) against the real soul sources 2026-06-10.

The edits
---------
FILE 1: soul/soul_kernel.metta (chmod 444 interim guard; script handles perms)

  K1 (INSERT, ordering-critical): five soul-cmd-skill clauses inserted BEFORE
  the catch-all `(= (soul-cmd-skill $cmd)                unknown)`. PeTTa
  equations transpile to ordered Prolog clauses; appended clauses land after
  the catch-all and are unreachable. Without this, query/remember/pin/
  episodes/metta classify as unknown and the unknown=3 seed FLAG-floods
  every memory cycle.

  K2 (REPLACE, in-place): soul-rationality-gaps body wrapped in
  filter-empty-entries. An appended second equation would coexist
  nondeterministically with the old one, so this is a replacement.
  Fixes the SOUL-AUDIT nine-empty-parens false positive at the producer.

  K3 (APPEND): SECTION 6 OUTPUT GOVERNANCE SEEDS:
    - filter-empty-entries shared helper (used by K2 and B1)
    - operation-risk seeds (15 skills, Clarity's recalibrations honored;
      NO observation atom seeded: add-atom stores arguments unreduced, a
      seeded variable atom would unify with every lookup)
    - resolve-operation-risk in the registry resolve-lifecycle form
      (collapse, empty-test, car-atom; observation overrides seed;
      unseeded skills floor at 3 = FLAG, nothing PROCEEDs silently)
    - soul-file-class declarations, DEFAULT-DENY posture: constitutional
      x5, journal x1 (arc_log.md, the only real append target; soul_note.md
      does not exist in soul/ and is deliberately not seeded); any
      undeclared soul/ path resolves runtime-soul (protected) via
      soul-file-class-of
    - use-llm-eval False + accessor (D1 dormant fallback switch)

FILE 2: soul/get_soul_brief.metta

  B1 (REPLACE, in-place): brief-active-goals body wrapped in
  filter-empty-entries. Fixes the ActiveGoals fifteen-empty-parens in the
  assembled prompt at the producer.

Net change
----------
- soul_kernel.metta: K1 +5, K2 +1, K3 +block (computed at runtime)
- get_soul_brief.metta: B1 +1
- Paren delta 0 per file (code-aware count)

Harness (pre-apply, container, inlined per the transpile-visibility lesson)
---------------------------------------------------------------------------
--with-harness (works in dry-run and apply): writes the SIMULATED
post-edit kernel + test directives as ONE file to shared_files/ (the
container /tmp mount), runs it via run.sh in the live container (a fresh
process; does not touch the running loop), and greps expectations:
  resolve seed=3 / default=3 / override=4; cmd-skill query->query,
  frobnicate->unknown; file-class constitutional + runtime-soul default;
  filter-empty-entries (() a () b ()) -> (a b); use-llm-eval False.
Inlined because file-imported definitions are invisible to later
directives' transpilation (proven 2026-06-10); same-file definitions
reduce (the 12/12 gate harness precedent).

Usage (from repo root)
----------------------
Dry-run:            python3 staging/apply_governance_seeds.py
Dry-run + harness:  python3 staging/apply_governance_seeds.py --with-harness
Apply:              python3 staging/apply_governance_seeds.py --apply --with-harness
Reverse:            python3 staging/apply_governance_seeds.py --reverse --apply

Logs tee to shared_files/governance_seeds_<mode>_<UTCstamp>.log.
Backups: <file>.bak.govseeds (forward apply only).
Post-apply: container RESTART only (soul/ is bind-mounted; no rebuild needed
for these files): docker compose restart clarityclaw, then verify
SOUL-AUDIT reads "structurally sound" and the prompt's ActiveGoals is ().
soul_kernel.metta returns to chmod 444 after the write, forward and reverse.
"""
from __future__ import annotations

import argparse
import datetime
import os
import stat
import subprocess
import sys
from pathlib import Path

_STAMP = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
LOG_DIR = Path("shared_files")
LOG_PATH = None  # set in main


class _Tee:
    def __init__(self, stream, logfile):
        self.stream = stream
        self.logfile = logfile

    def write(self, data):
        self.stream.write(data)
        self.logfile.write(data)

    def flush(self):
        self.stream.flush()
        self.logfile.flush()


KERNEL_PATH = Path("soul/soul_kernel.metta")
KERNEL_BAK = Path("soul/soul_kernel.metta.bak.govseeds")
BRIEF_PATH = Path("soul/get_soul_brief.metta")
BRIEF_BAK = Path("soul/get_soul_brief.metta.bak.govseeds")
CONTAINER = "clarity_omega"
HARNESS_HOST = LOG_DIR / "gov_harness.metta"
HARNESS_CONT = "/tmp/gov_harness.metta"

# ============================================================================
# K1: soul-cmd-skill extension (INSERT before the catch-all)
# ============================================================================

K1_ANCHOR = "(= (soul-cmd-skill $cmd)                unknown)"
K1_INSERT = (
    "(= (soul-cmd-skill (query $arg))        query)\n"
    "(= (soul-cmd-skill (remember $arg))     remember)\n"
    "(= (soul-cmd-skill (pin $arg))          pin)\n"
    "(= (soul-cmd-skill (episodes $arg))     episodes)\n"
    "(= (soul-cmd-skill (metta $arg))        metta)\n"
)

# ============================================================================
# K2: soul-rationality-gaps producer fix (REPLACE)
# ============================================================================

K2_OLD = (
    "(= (soul-rationality-gaps)\n"
    "   (collapse (let $v (match &self (soul-pattern $v $_) $v)\n"
    "     (if (soul-rationality-check $v) () $v))))"
)
K2_NEW = (
    "(= (soul-rationality-gaps)\n"
    "   (filter-empty-entries\n"
    "     (collapse (let $v (match &self (soul-pattern $v $_) $v)\n"
    "       (if (soul-rationality-check $v) () $v)))))"
)

# ============================================================================
# K3: SECTION 6 append block
# ============================================================================

K3_BLOCK = """

;; ================================================================
;; SECTION 6: OUTPUT GOVERNANCE SEEDS
;; Source: output_governance_design_v1.md v1.3 (locked 2026-06-10).
;; Authored by Berton + Claude against this file's real Section 2/3
;; vocabulary; Clarity's recalibrations honored as seed values.
;; ================================================================

;; Shared recursive filter: drops () markers from a collapsed list.
;; Used by soul-rationality-gaps (this file) and brief-active-goals
;; (get_soul_brief.metta). The collapse-with-()-branches padding fix,
;; applied at the producers.
(= (filter-empty-entries $list)
   (if (== $list ())
       ()
       (let* (($h (car-atom $list))
              ($t (cdr-atom $list))
              ($rest (filter-empty-entries $t)))
             (if (== $h ()) $rest (cons-atom $h $rest)))))

;; --- D4: operation-risk (values-as-revisable-policy) ---
;; operation-risk = execution risk of invoking the skill THIS cycle.
;; DISTINCT from irreversible-weight (Section 3) = undo cost of the result.
;; Scale: 1 minimal, 2 medium, 3 high, 4 critical.
;; Seeds are constitutional and never edited at runtime; revision happens
;; ONLY via (operation-risk-observation $skill $score) override atoms,
;; written by external governance or future learning (NACE, Sprint 12+).
;; NOTE: no observation atom is seeded here, deliberately. add-atom stores
;; arguments unreduced; a seeded variable atom would unify with every
;; lookup and poison the resolver.

!(add-atom &self (operation-risk send 3))
!(add-atom &self (operation-risk shell 3))
!(add-atom &self (operation-risk write-file 2))
!(add-atom &self (operation-risk append-file 2))
!(add-atom &self (operation-risk search 1))
!(add-atom &self (operation-risk read-file 1))
!(add-atom &self (operation-risk query 1))
!(add-atom &self (operation-risk remember 1))
!(add-atom &self (operation-risk pin 1))
!(add-atom &self (operation-risk episodes 1))
!(add-atom &self (operation-risk metta 2))
!(add-atom &self (operation-risk package-install 3))
!(add-atom &self (operation-risk credential-storage 4))
!(add-atom &self (operation-risk crontab-modification 4))
!(add-atom &self (operation-risk unknown 3))

;; Resolver: observation overrides seed; registry resolve-lifecycle form.
;; Unseeded skills floor at 3 (FLAG): nothing PROCEEDs silently.
(= (resolve-operation-risk $skill)
   (let $obs (collapse (match &self (operation-risk-observation $skill $r) $r))
        (if (== $obs ())
            (let $seed (collapse (match &self (operation-risk $skill $s) $s))
                 (if (== $seed ()) 3 (car-atom $seed)))
            (car-atom $obs))))

;; --- D3: protected-target declaration (target-first, default-deny) ---
;; The gate rule, not a judgment call: a path's class decides its mutation
;; policy on EVERY route (metta-route, file-route, future routes).
;; DEFAULT-DENY: any soul/ path NOT declared here resolves to runtime-soul
;; (protected) via soul-file-class-of. Only journals are allow-listed; a
;; new soul file is protected the moment it exists. Scope note: the gate
;; evaluates Clarity's COMMAND-ROUTE writes; machine-written state files
;; (idle_state.json etc.) are loop machinery, not gated commands.
;; Classes: constitutional (strictest; Sprint 11 partition target),
;; runtime-soul (protected, gate parity), journal (append-route
;; PROCEED-under-VALUE-GROUNDING).

!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_kernel.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_utils.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_memory.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_mutation_gate_corrected.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_namespace_membership_seed.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/arc_log.md" journal))

;; Accessor with the default-deny fallback built in.
(= (soul-file-class-of $path)
   (let $c (collapse (match &self (soul-file-class $path $cl) $cl))
        (if (== $c ()) runtime-soul (car-atom $c))))

;; --- D1: LLM-eval fallback switch (dormant, restorable) ---
!(add-atom &self (use-llm-eval False))
(= (soul-use-llm-eval?) (match &self (use-llm-eval $b) $b))
"""

# ============================================================================
# B1: brief-active-goals producer fix (REPLACE)
# ============================================================================

B1_OLD = (
    "(= (brief-active-goals)\n"
    "   (collapse (match &self (= (active-goal $n) $g)\n"
    "     (brief-active-goal-entry $n))))"
)
B1_NEW = (
    "(= (brief-active-goals)\n"
    "   (filter-empty-entries\n"
    "     (collapse (match &self (= (active-goal $n) $g)\n"
    "       (brief-active-goal-entry $n)))))"
)

# ============================================================================
# Harness content (tests appended to the SIMULATED kernel)
# ============================================================================

HARNESS_TESTS = """
;; ===== GOVERNANCE SEEDS HARNESS (inlined tests) =====
!(println! (T1-resolve-seed (resolve-operation-risk send)))
!(println! (T2-resolve-default (resolve-operation-risk frobnicate-skill)))
!(add-atom &self (operation-risk-observation send 4))
!(println! (T3-resolve-override (resolve-operation-risk send)))
!(println! (T4-cmdskill-query (soul-cmd-skill (query "x"))))
!(println! (T5-cmdskill-unknown (soul-cmd-skill (frobnicate "x"))))
!(println! (T6-class-constitutional (soul-file-class-of "/PeTTa/repos/omegaclaw/soul/soul_kernel.metta")))
!(println! (T7-class-default (soul-file-class-of "/PeTTa/repos/omegaclaw/soul/some_new_file.metta")))
!(println! (T8-filter (filter-empty-entries (() a () b ()))))
!(println! (T9-llm-eval (soul-use-llm-eval?)))
"""

HARNESS_EXPECT = [
    ("T1-resolve-seed 3", "resolver returns seed (send=3)"),
    ("T2-resolve-default 3", "resolver default floor (unseeded=3)"),
    ("T3-resolve-override 4", "observation overrides seed (send->4)"),
    ("T4-cmdskill-query query", "cmd-skill extension reachable (query)"),
    ("T5-cmdskill-unknown unknown", "catch-all intact (frobnicate->unknown)"),
    ("T6-class-constitutional constitutional", "declared class resolves"),
    ("T7-class-default runtime-soul", "default-deny fallback"),
    ("T8-filter (a b)", "filter drops () markers"),
    ("T9-llm-eval false", "llm-eval switch reads False (lowercase: booleans render as Prolog atoms)"),
]

# ============================================================================
# Helpers (template-conformant)
# ============================================================================

def code_aware_paren_count(text: str) -> tuple[int, int]:
    opens = closes = 0
    in_string = False
    escape = False
    i, n = 0, len(text)
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
    count = start = 0
    while True:
        idx = text.find(target, start)
        if idx == -1:
            return count
        count += 1
        start = idx + 1


def require_once(content: str, target: str, label: str) -> None:
    c = count_sub(content, target)
    if c != 1:
        raise RuntimeError(f"{label}: expected anchor exactly once, found {c}.")


# ============================================================================
# Simulations
# ============================================================================

def simulate_kernel_forward(content: str) -> str:
    require_once(content, K1_ANCHOR, "K1 catch-all anchor")
    if "(soul-cmd-skill (query $arg))" in content:
        raise RuntimeError("K1: query clause already present.")
    content = content.replace(K1_ANCHOR, K1_INSERT + K1_ANCHOR, 1)
    require_once(content, K2_OLD, "K2 gaps producer")
    if "filter-empty-entries" in content:
        raise RuntimeError("K2/K3: filter helper already present.")
    content = content.replace(K2_OLD, K2_NEW, 1)
    if "SECTION 6: OUTPUT GOVERNANCE SEEDS" in content:
        raise RuntimeError("K3: Section 6 already present.")
    return content + K3_BLOCK


def simulate_kernel_reverse(content: str) -> str:
    if "SECTION 6: OUTPUT GOVERNANCE SEEDS" not in content:
        raise RuntimeError("kernel reverse: Section 6 absent.")
    idx = content.index("\n\n;; ================================================================\n;; SECTION 6")
    content = content[:idx]
    require_once(content, K2_NEW, "kernel reverse: K2 wrapped form")
    content = content.replace(K2_NEW, K2_OLD, 1)
    require_once(content, K1_INSERT + K1_ANCHOR, "kernel reverse: K1 insertion")
    content = content.replace(K1_INSERT + K1_ANCHOR, K1_ANCHOR, 1)
    return content


def simulate_brief_forward(content: str) -> str:
    require_once(content, B1_OLD, "B1 brief-active-goals")
    if B1_NEW in content:
        raise RuntimeError("B1: wrapped form already present.")
    return content.replace(B1_OLD, B1_NEW, 1)


def simulate_brief_reverse(content: str) -> str:
    require_once(content, B1_NEW, "brief reverse: wrapped form")
    return content.replace(B1_NEW, B1_OLD, 1)


# ============================================================================
# State checks
# ============================================================================

def kernel_fwd_ok(c: str):
    a = count_sub(c, K1_ANCHOR) == 1
    b = "(soul-cmd-skill (query $arg))" not in c
    d = count_sub(c, K2_OLD) == 1
    e = "SECTION 6: OUTPUT GOVERNANCE SEEDS" not in c
    ok = a and b and d and e
    return ok, f"catchall={a}, ext-absent={b}, gaps-old={d}, sec6-absent={e} -> {'OK' if ok else 'FAIL'}"


def kernel_rev_ok(c: str):
    a = "SECTION 6: OUTPUT GOVERNANCE SEEDS" in c
    b = count_sub(c, K2_NEW) == 1
    d = count_sub(c, K1_INSERT + K1_ANCHOR) == 1
    ok = a and b and d
    return ok, f"sec6={a}, gaps-new={b}, ext-present={d} -> {'OK' if ok else 'FAIL'}"


def brief_fwd_ok(c: str):
    a = count_sub(c, B1_OLD) == 1
    return a, f"goals-old present={a} -> {'OK' if a else 'FAIL'}"


def brief_rev_ok(c: str):
    a = count_sub(c, B1_NEW) == 1
    return a, f"goals-wrapped present={a} -> {'OK' if a else 'FAIL'}"


# ============================================================================
# Permissions
# ============================================================================

def make_writable(path: Path):
    os.chmod(path, 0o644)


def make_readonly(path: Path):
    os.chmod(path, 0o444)


def is_readonly(path: Path) -> bool:
    return not (os.stat(path).st_mode & stat.S_IWUSR)


# ============================================================================
# Harness
# ============================================================================

def run_harness(simulated_kernel: str) -> bool:
    print("\n========== PRE-APPLY HARNESS (container, fresh process) ==========")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    HARNESS_HOST.write_text(simulated_kernel + HARNESS_TESTS)
    print(f"  harness written: {HARNESS_HOST} (container: {HARNESS_CONT})")
    try:
        p = subprocess.run(
            ["docker", "exec", CONTAINER, "sh", "-c",
             f"cd /PeTTa && ./run.sh {HARNESS_CONT} 2>&1"],
            capture_output=True, text=True, timeout=120)
    except Exception as exc:
        print(f"  HARNESS EXECUTION FAILED: {exc}")
        return False
    out = p.stdout or ""
    raw_log = LOG_DIR / f"governance_seeds_harness_raw_{_STAMP}.log"
    raw_log.write_text(out)
    print(f"  FULL raw MeTTa output (transpile + reduction record): {raw_log}")
    tail = "\n".join(out.splitlines()[-12:])
    print("  --- output tail (full record in the raw log) ---")
    for ln in tail.splitlines():
        print(f"    {ln}")
    out_l = out.lower()
    all_ok = True
    print("  --- expectations (case-insensitive: booleans render lowercase) ---")
    for expect, label in HARNESS_EXPECT:
        hit = expect.lower() in out_l
        print(f"  [{'PASS' if hit else 'FAIL'}] {label}: '{expect}'")
        all_ok = all_ok and hit
    return all_ok


# ============================================================================
# Process + verify (template-conformant)
# ============================================================================

def process_file(path, sim_fwd, sim_rev, fwd_ok, rev_ok, args, label):
    print(f"\n>>> {label} <<<")
    content = path.read_text()
    pre_lines = len(content.splitlines())
    o, c = code_aware_paren_count(content)
    print(f"  Path: {path}")
    print(f"  Pre-edit lines: {pre_lines}; parens opens={o} closes={c} delta={o-c} ({'OK' if o == c else 'FAIL'})")
    if o != c:
        return False, content, ""
    ok, msg = (rev_ok if args.reverse else fwd_ok)(content)
    print(f"  State check: {msg}")
    if not ok:
        return False, content, ""
    try:
        sim = (sim_rev if args.reverse else sim_fwd)(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return False, content, ""
    so, sc = code_aware_paren_count(sim)
    post_lines = len(sim.splitlines())
    print(f"  Post-edit lines: {post_lines} (delta {post_lines - pre_lines});"
          f" parens opens={so} closes={sc} delta={so-sc} ({'OK' if so == sc else 'FAIL'})")
    if so != sc:
        return False, content, sim
    return True, content, sim


def main() -> int:
    ap = argparse.ArgumentParser(description="Governance kernel seeds + padding fixes")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    ap.add_argument("--with-harness", action="store_true",
                    help="Run the inlined container harness against the simulated kernel")
    args = ap.parse_args()

    global LOG_PATH
    mode = ("reverse" if args.reverse else "forward") + ("_apply" if args.apply else "_dryrun")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH = LOG_DIR / f"governance_seeds_{mode}_{_STAMP}.log"
    logfile = open(LOG_PATH, "w")
    sys.stdout = _Tee(sys.__stdout__, logfile)

    print(f"\n========== GOVERNANCE SEEDS: {mode.upper()} ==========")
    print(f"Run log: {LOG_PATH}")

    for p, lbl in [(KERNEL_PATH, "soul_kernel"), (BRIEF_PATH, "get_soul_brief")]:
        if not p.exists():
            print(f"ERROR: {lbl} not found at {p}. Run from repo root.")
            return 1

    kernel_was_ro = is_readonly(KERNEL_PATH)
    print(f"  kernel read-only guard currently: {'ON' if kernel_was_ro else 'OFF'}")

    ok_k, k_orig, k_sim = process_file(
        KERNEL_PATH, simulate_kernel_forward, simulate_kernel_reverse,
        kernel_fwd_ok, kernel_rev_ok, args, "soul_kernel.metta (K1+K2+K3)")
    if not ok_k:
        return 1
    ok_b, b_orig, b_sim = process_file(
        BRIEF_PATH, simulate_brief_forward, simulate_brief_reverse,
        brief_fwd_ok, brief_rev_ok, args, "get_soul_brief.metta (B1)")
    if not ok_b:
        return 1

    if args.with_harness:
        target_kernel = k_sim if not args.reverse else k_orig
        if not args.reverse:
            if not run_harness(target_kernel):
                print("\nHARNESS FAILED. No writes have occurred. Read the output above.")
                return 1
        else:
            print("\n  (harness skipped on reverse: restoring proven pre-state)")

    if not args.apply:
        print("\n========== ACTION-SUMMARY (DRY-RUN) ==========")
        print("  Both files simulated clean; paren-delta 0; anchors exact."
              + (" Harness PASS." if args.with_harness and not args.reverse else ""))
        print("  No writes have occurred. Re-run with --apply to write.")
        print(f"  Full log: {LOG_PATH}")
        return 0

    if not args.reverse:
        for path, bak in [(KERNEL_PATH, KERNEL_BAK), (BRIEF_PATH, BRIEF_BAK)]:
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    try:
        if kernel_was_ro:
            make_writable(KERNEL_PATH)
            print("  kernel guard lifted (644) for the write")
        KERNEL_PATH.write_text(k_sim)
        print(f"Wrote: {KERNEL_PATH}")
    finally:
        make_readonly(KERNEL_PATH)
        print("  kernel guard restored (444)")
    BRIEF_PATH.write_text(b_sim)
    print(f"Wrote: {BRIEF_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    kd = KERNEL_PATH.read_text()
    bd = BRIEF_PATH.read_text()
    ko, kc = code_aware_paren_count(kd)
    bo, bc = code_aware_paren_count(bd)
    ok1, msg1 = (kernel_rev_ok if not args.reverse else kernel_fwd_ok)(kd)
    ok2, msg2 = (brief_rev_ok if not args.reverse else brief_fwd_ok)(bd)
    print(f"  kernel parens delta={ko-kc} ({'OK' if ko == kc else 'FAIL'}); state: {msg1}")
    print(f"  brief parens delta={bo-bc} ({'OK' if bo == bc else 'FAIL'}); state: {msg2}")
    print(f"  kernel guard: {'ON (444)' if is_readonly(KERNEL_PATH) else 'OFF: FAIL'}")
    if not (ok1 and ok2 and ko == kc and bo == bc and is_readonly(KERNEL_PATH)):
        print("\nDISK VERIFICATION FAILED. Restore from .bak.govseeds copies.")
        return 1

    print("\n========== ACTION-SUMMARY ==========")
    print(f"  Direction: {'REVERSE' if args.reverse else 'FORWARD'}. kernel K1+K2+K3,"
          f" brief B1 {'applied' if not args.reverse else 'reversed'}; guard restored.")
    print(f"  Full log: {LOG_PATH}")
    if not args.reverse:
        print("\nNext: container RESTART only (soul/ is bind-mounted; no rebuild):")
        print("  docker compose restart clarityclaw && sleep 20 && docker logs clarity_omega 2>&1 | grep -E 'SOUL-AUDIT|ActiveGoals' | tail -5")
        print("  Expect: SOUL-AUDIT structurally sound; ActiveGoals () not (() x15).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
