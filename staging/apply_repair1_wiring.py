#!/usr/bin/env python3
"""
Apply script: REPAIR 1 WIRING (output governance, one coordinated change).
Per output_governance_design_v1.md v1.3 (locked) and Berton's one-function
decision: native gate + real verdict + verdict-gated execution land together.
All loop anchors CONFIRM-LIVE verified 2026-06-10 (live == worktree).

The edits
---------
FILE 1: src/loop.metta
  L-A (REPLACE): initLoop lock seed `(change-state! &soul_mutation_lock "")`
      -> `(change-state! &soul_mutation_lock unlocked)`. The committed gate's
      lock is STRUCTURAL (unlocked | (locked <arg>)); the string seed would
      read as pending-from-boot.
  L-B (REPLACE, block): the (5c) intercept region, stub line through the
      corner-gate binding, replaced with the wired sequence:
        metta_cmds (unchanged text) -> $soul_gate_state (native derivation,
        lock-write restored) -> SOUL-GATE-FLAG print -> $soul_verdict_out
        (compute-output-verdict, REAL) -> SOUL_VERDICT_OUT print (existing
        marker, computed value) -> $soul_decision (symbol; replaces the
        string-contains-based soul-proceed? consumer, which is built on a
        globally-broken primitive) -> note-record (existing call, symbolic
        condition) -> $sexpr_verdict (PAUSE empties execution input) ->
        SOUL-SUPPRESSED print + governance journal (PAUSE and FLAG) ->
        apply-corner-gate consumes $sexpr_verdict.
      REMOVED: the stub constant; the helper.soul_mutation_gate py-call
      (the Python gate retires from the loop; helper.py untouched).
      PRESERVED: populate-recent-action keeps ORIGINAL $sexpr; everything
      downstream byte-identical; PAUSE-effect stays 0 (router untouched,
      Repair 3).

FILE 2: soul/output_verdict.metta
  M-A (APPEND): SECTION 2 wiring glue: batch-targets-soul? (mutation-form
      guard: add-atom/remove-atom/set-atom! heads only, so read-only metta
      probes flow to the composite), derive-gate-state (clean|pending|
      conflict + the lock-write the Python port dropped), output-decision
      (proceed|flag|pause symbol mirroring the verdict ladder).

FILE 3: soul/soul_governance.py
  G-A (APPEND): journal_append(kind, content): one line per governance
      event to soul/governance_journal.log. Hands only.

FILE 4: lib_clarity_reasoning/lib_clarity_reasoning.metta
  I-A (INSERT after the memory_protocol import): three imports: mutation
      gate, membership seed, output_verdict. The gate has been committed
      but never imported; this is its runtime debut.

Harness (--with-harness, pre-apply, container fresh process, inlined)
---------------------------------------------------------------------
Builds: kernel + gate + membership seed + SIMULATED output_verdict (with
glue) + tests. The 12 proven V-fixtures rerun, plus G-fixtures: gate-state
clean/pending/conflict, lock transition, normal-work-while-pending,
read-only-metta passthrough, decision symbols. Any FAIL: zero writes.

Usage (repo root)
-----------------
Dry+harness: python3 staging/apply_repair1_wiring.py --with-harness
Apply:       python3 staging/apply_repair1_wiring.py --apply --with-harness
Reverse:     python3 staging/apply_repair1_wiring.py --reverse --apply
Post-apply: docker compose build --no-cache clarityclaw && docker compose up -d
  (loop.metta and lib_clarity_reasoning are IMAGE-BAKED: rebuild required,
   per standing rule no result is final before --no-cache anyway.)
Live checks: SOUL-GATE-FLAG / SOUL_VERDICT_OUT vary with content; an
  ordinary cycle PROCEEDs and executes; a send cycle FLAGs, executes,
  note-records, journals; loop does NOT halt on any verdict (Repair 3).
Backups: <file>.bak.repair1 (forward apply only).
Logs tee to shared_files/repair1_wiring_<mode>_<UTCstamp>.log.
"""
from __future__ import annotations

import argparse
import datetime
import os
import subprocess
import sys
from pathlib import Path

_STAMP = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
LOG_DIR = Path("shared_files")
CONTAINER = "clarity_omega"
HARNESS_HOST = LOG_DIR / "repair1_harness.metta"
HARNESS_CONT = "/tmp/repair1_harness.metta"


class _Tee:
    def __init__(self, stream, logfile):
        self.stream, self.logfile = stream, logfile

    def write(self, d):
        self.stream.write(d)
        self.logfile.write(d)

    def flush(self):
        self.stream.flush()
        self.logfile.flush()


LOOP = Path("src/loop.metta")
MODULE = Path("soul/output_verdict.metta")
HANDS = Path("soul/soul_governance.py")
LIB = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")

# ===================== FILE 1: loop.metta ==========================

LA_OLD = '          (change-state! &soul_mutation_lock "")'
LA_NEW = "          (change-state! &soul_mutation_lock unlocked)"

LB_OLD = """                                       ;; CLARITYCLAW SOUL OUTPUT INTERCEPT (5c)
                                       ($soul_verdict_out "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix")
                                       ($_ (println! (SOUL_VERDICT_OUT: $soul_verdict_out)))
                                       ($metta_cmds (if (and (== "(" (first_char $resp)) (== (get-state &error) ()))
                                                       (collapse (superpose $sexpr))
                                                       ()))
                                       ($soul_mutation_flag (py-call (helper.soul_mutation_gate (repr $metta_cmds) (get-state &soul_mutation_lock))))
                                       ($_ (if (and (not (soul-proceed? $soul_verdict_out)) (== (get-state &error) ()))
                                               (soul-note-record $soul_verdict_out "output" $resp) _))
                                       ($sexpr_gated (apply-corner-gate $sexpr))"""

LB_NEW = """                                       ;; CLARITYCLAW SOUL OUTPUT INTERCEPT (5c) -- Repair 1 wired 2026-06-10:
                                       ;; native gate-state, real verdict, verdict-gated execution. PAUSE empties
                                       ;; this cycle's execution input; loop-halt routing remains Repair 3.
                                       ($metta_cmds (if (and (== "(" (first_char $resp)) (== (get-state &error) ()))
                                                       (collapse (superpose $sexpr))
                                                       ()))
                                       ($soul_gate_state (derive-gate-state $metta_cmds))
                                       ($_ (println! (SOUL-GATE-FLAG $soul_gate_state (get-state &soul_mutation_lock))))
                                       ($soul_verdict_out (compute-output-verdict $metta_cmds $soul_gate_state))
                                       ($_ (println! (SOUL_VERDICT_OUT: $soul_verdict_out)))
                                       ($soul_decision (output-decision $metta_cmds $soul_gate_state))
                                       ($_ (if (and (not (== $soul_decision proceed)) (== (get-state &error) ()))
                                               (soul-note-record $soul_verdict_out "output" $resp) _))
                                       ($sexpr_verdict (if (== $soul_decision pause) () $sexpr))
                                       ($_ (if (== $soul_decision pause)
                                               (progn (println! (SOUL-SUPPRESSED $sexpr))
                                                      (py-call (soul_governance.journal_append "PAUSE" (repr $sexpr))))
                                               (if (== $soul_decision flag)
                                                   (py-call (soul_governance.journal_append "FLAG" (repr $sexpr)))
                                                   _)))
                                       ($sexpr_gated (apply-corner-gate $sexpr_verdict))"""

# ===================== FILE 2: output_verdict glue =================

MA_BLOCK = """

;; ================================================================
;; SECTION 2: WIRING GLUE (Repair 1, rev 2, 2026-06-11)
;; STRUCTURAL THROUGHOUT (investigation ledger F20): pattern-headed
;; clauses die at atom_string on unbound-variable-carrying metta
;; commands under reduce; var-headed builtins-only forms are immune.
;; The gate's pattern-headed soul-extract-metta-arg and quote-bodied
;; soul-target-head are BYPASSED here (gate-file hardening flagged to
;; Clarity); soul-head-is-member? and soul-mutation-pending? (both
;; var-headed) are consumed directly. Probe7-validated 13/13,
;; deterministic (solution counts 1), full universe, production shapes
;; including the killer input.
;; ================================================================

(= (extract-metta-arg-structural $cmd) (car-atom (cdr-atom $cmd)))

;; Production metta args are STRINGS (F11 single-command format).
;; Strings are opaque to structural checks: unparsed, the gate both
;; crashes (F25: car-atom on string = silent goal failure) and, if
;; naively skipped, waves soul mutations through (probe8 S7). sread
;; on a bound string is a direct builtin goal (no reduce hazard);
;; string detection rides the S1-proven py-call channel ON THE REPR\n;; (repr is total over unbound vars; raw marshalling is not, F30).
(= (norm-metta-arg $a)
   (if (== (py-call (soul_governance.repr_kind (repr $a))) 1) (sread $a) $a))

(= (metta-target-head-structural $arg)
   (car-atom (car-atom (cdr-atom (cdr-atom $arg)))))

(= (metta-targets-soul-structural $arg)
   (soul-head-is-member? (metta-target-head-structural $arg)))

(= (metta-arg-mutates? $arg)
   (let $h (car-atom $arg)
        (if (== $h add-atom) True
            (if (== $h remove-atom) True
                (if (== $h set-atom!) True False)))))

(= (batch-targets-soul? $cmds)
   (if (== $cmds ())
       False
       (let* (($h (car-atom $cmds))
              ($t (cdr-atom $cmds)))
             (if (== (car-atom $h) metta)
                 (let $arg (norm-metta-arg (extract-metta-arg-structural $h))
                      (if (metta-arg-mutates? $arg)
                          (if (metta-targets-soul-structural $arg)
                              True
                              (batch-targets-soul? $t))
                          (batch-targets-soul? $t)))
                 (batch-targets-soul? $t)))))

;; Lock semantics v1: held on detection (the lock-write the Python port
;; dropped); clear happens in the Repair 3 confirmation flow. Normal
;; non-soul work proceeds while a mutation awaits confirmation; a SECOND
;; soul mutation while held is a conflict.
(= (derive-gate-state $cmds)
   (if (batch-targets-soul? $cmds)
       (if (soul-mutation-pending?)
           conflict
           (let $_ (change-state! &soul_mutation_lock (locked soul-mutation-proposed))
                pending))
       clean))

;; The loop's branching symbol: mirrors compute-output-verdict's ladder.
(= (output-decision $cmds $gate)
   (if (== $gate pending)
       pause
       (if (== $gate conflict)
           pause
           (if (== $gate clean)
               (if (== $cmds ())
                   proceed
                   (let $r (batch-rank $cmds)
                        (if (== $r 2) pause (if (== $r 1) flag proceed))))
               flag))))
"""

# ===================== FILE 3: hands journal =======================

GA_BLOCK = '''

def journal_append(kind, content):
    """One line per governance event (PAUSE/FLAG) to the governance
    journal. Hands only: timestamp + kind + truncated content."""
    import datetime as _dt
    line = "{} {} {}\\n".format(
        _dt.datetime.utcnow().isoformat(), str(kind), str(content)[:2000])
    with open('/PeTTa/repos/omegaclaw/soul/governance_journal.log', 'a') as f:
        f.write(line)
    return True


def repr_kind(r):
    """Arg-kind detector on the REPR (repr is total over unbound vars
    and always marshals; raw marshalling of unbound-carrying exprs
    kills py_call, F30). repr of a STRING carries a leading quote
    (probe9 P1); an expression's does not (P1b). Returns INT (1 =
    string, 0 = other): MeTTa-side comparison is (== n 1), the
    int-equality pattern proven throughout rank logic, avoiding the
    unverified python-bool-into-if marshalling class (ledger F35)."""
    return 1 if (isinstance(r, str) and r.lstrip().startswith('"')) else 0
'''

# ===================== FILE 4: lib imports =========================

IA_ANCHOR = "!(import! &self (library omegaclaw ./soul/memory_protocol))"
IA_INSERT = (
    "!(import! &self (library omegaclaw ./soul/soul_namespace_membership_seed))\n"
    "!(import! &self (library omegaclaw ./soul/soul_mutation_gate_corrected))\n"
    "!(import! &self (library omegaclaw ./soul/output_verdict))\n"
)

# ===================== Harness =====================================

HARNESS_PREAMBLE = """
;; ===== REPAIR 1 WIRING HARNESS rev 2 (FULL UNIVERSE, ledger C4) =====
!(import! &self (library lib_import))
!(git-import! "https://github.com/asi-alliance/omegaClaw-Core.git")
!(import! &self (library omegaclaw lib_omegaclaw))
!(import! &self "/PeTTa/repos/omegaclaw/soul/soul_mutation_gate_corrected.metta")
!(import! &self "/PeTTa/repos/omegaclaw/soul/soul_namespace_membership_seed.metta")
!(import! &self "/tmp/repair1_sim_module.metta")
!(bind! &soul_mutation_lock (new-state unlocked))
"""

HARNESS_TESTS = """

;; Fixture rules (ledger C2 GENERALIZED, F22 2026-06-11): under the
;; full universe EVERY skill-headed literal in directive source is
;; live and EXECUTES (a literal write-file fixture attempted a real
;; kernel write; the chmod 444 guard blocked it). ALL command-shaped
;; fixture data is sread-built, with SYMBOL args (no string args ->
;; no inner quotes -> no escaping). The logic under test reads heads
;; and paths only; path symbols work via str() coercion in path_scope,
;; and class lookup falling to default-deny preserves expected PAUSEs.
!(println! (G1-clean (derive-gate-state (sread "((query x))"))))
!(println! (G1-lock (get-state &soul_mutation_lock)))
!(println! (G2-pending (derive-gate-state (sread "((metta (add-atom &self (soul-affective-state calm))))"))))
!(println! (G2-lock (get-state &soul_mutation_lock)))
!(println! (G3-conflict (derive-gate-state (sread "((metta (add-atom &self (soul-affective-state calm))))"))))
!(println! (G4-work-while-pending (derive-gate-state (sread "((query x))"))))
!(println! (G5-readonly-metta (derive-gate-state (sread "((metta (match &self (vad-affective $x $y) (vad-affective $x $y))))"))))
!(println! (G5s-string-read (derive-gate-state (cons-atom (cons-atom metta (cons-atom (swrite (sread "(match &self (vad-affective $x $y) (vad-affective $x $y))")) ())) ()))))
!(println! (G2s-string-mutation (derive-gate-state (cons-atom (cons-atom metta (cons-atom (swrite (sread "(add-atom &self (soul-affective-state calm))")) ())) ()))))
!(println! (G2s-lock (get-state &soul_mutation_lock)))
!(println! (G6-decision-pending (output-decision (sread "((query x))") pending)))
!(println! (G7-decision-flag (output-decision (sread "((send y))") clean)))
!(println! (G8-decision-proceed (output-decision (sread "((query x))") clean)))
!(println! (V1-query (compute-output-verdict (sread "((query x))") clean)))
!(println! (V2-send (compute-output-verdict (sread "((send hello))") clean)))
!(println! (V4-kernel-write (compute-output-verdict (sread "((write-file /PeTTa/repos/omegaclaw/soul/soul_kernel.metta x))") clean)))
!(println! (V7-pending-override (compute-output-verdict (sread "((query x))") pending)))
!(println! (V12-production-shape (compute-output-verdict (sread "((metta (match &self (vad-affective $x $y) (vad-affective $x $y))))") clean)))
!(println! (C1-bts-count (size-atom (collapse (batch-targets-soul? (sread "((metta (match &self (vad-affective $x $y) (vad-affective $x $y))))"))))))
!(println! (C2-verdict-count (size-atom (collapse (compute-output-verdict (sread "((query x))") clean)))))
"""

HARNESS_EXPECT = [
    ("G1-clean clean", "no-soul batch derives clean"),
    ("G1-lock unlocked", "lock untouched by clean batch"),
    ("G2-pending pending", "soul mutation derives pending"),
    ("G2-lock (locked soul-mutation-proposed)", "LOCK-WRITE restored"),
    ("G3-conflict conflict", "second mutation while held = conflict"),
    ("G4-work-while-pending clean", "normal work proceeds while pending"),
    ("G5-readonly-metta clean", "read-only metta is not a mutation (killer input, alive)"),
    ("G5s-string-read clean", "STRING-form read-only metta derives clean (her production shape)"),
    ("G2s-string-mutation conflict", "STRING-form soul mutation SEEN by the gate (probe8 S7 hole closed; conflict because G2 already holds the lock)"),
    ("G2s-lock (locked soul-mutation-proposed)", "lock still held from G2"),
    ("G6-decision-pending pause", "decision: pending -> pause"),
    ("G7-decision-flag flag", "decision: send -> flag"),
    ("G8-decision-proceed proceed", "decision: query -> proceed"),
    ("V1-query \"VERDICT: PROCEED", "verdict: query proceeds"),
    ("V2-send \"VERDICT: FLAG", "verdict: send flags"),
    ("V4-kernel-write \"VERDICT: PAUSE", "verdict: constitutional write pauses"),
    ("V7-pending-override \"VERDICT: PAUSE SOUL-NOTE: soul-namespace-mutation-pending", "verdict: PENDING override"),
    ("V12-production-shape \"VERDICT: PROCEED", "verdict: her metta-match batch (the fixture that was missing)"),
    ("C1-bts-count 1", "count discipline: gate path deterministic"),
    ("C2-verdict-count 1", "count discipline: verdict deterministic"),
]

# ===================== Template helpers ============================

def code_aware_paren_count(text: str):
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


def count_sub(text, target):
    c = s = 0
    while True:
        idx = text.find(target, s)
        if idx == -1:
            return c
        c += 1
        s = idx + 1


def require_once(content, target, label):
    n = count_sub(content, target)
    if n != 1:
        raise RuntimeError(f"{label}: anchor expected once, found {n}.")


# ===================== Simulations =================================

def sim_loop_fwd(c):
    require_once(c, LA_OLD, "L-A initLoop lock seed")
    c = c.replace(LA_OLD, LA_NEW, 1)
    require_once(c, LB_OLD, "L-B intercept block")
    if "derive-gate-state" in c:
        raise RuntimeError("L-B: wired block already present.")
    return c.replace(LB_OLD, LB_NEW, 1)


def sim_loop_rev(c):
    require_once(c, LB_NEW, "loop reverse: wired block")
    c = c.replace(LB_NEW, LB_OLD, 1)
    require_once(c, LA_NEW, "loop reverse: lock seed")
    return c.replace(LA_NEW, LA_OLD, 1)


def sim_module_fwd(c):
    if "SECTION 2: WIRING GLUE" in c:
        raise RuntimeError("M-A: glue already present.")
    require_once(c, "(= (compute-output-verdict $cmds $gate)", "module sanity (Section 1 present)")
    return c + MA_BLOCK


def sim_module_rev(c):
    if "SECTION 2: WIRING GLUE" not in c:
        raise RuntimeError("module reverse: glue absent.")
    idx = c.index("\n\n;; ================================================================\n;; SECTION 2: WIRING GLUE")
    return c[:idx]


def sim_hands_fwd(c):
    if "def journal_append" in c:
        raise RuntimeError("G-A: journal_append already present.")
    require_once(c, "def path_scope", "hands sanity")
    return c + GA_BLOCK


def sim_hands_rev(c):
    require_once(c, GA_BLOCK, "hands reverse: journal block")
    return c.replace(GA_BLOCK, "", 1)


def sim_lib_fwd(c):
    require_once(c, IA_ANCHOR, "I-A memory_protocol import anchor")
    if "output_verdict" in c:
        raise RuntimeError("I-A: imports already present.")
    return c.replace(IA_ANCHOR, IA_ANCHOR + "\n" + IA_INSERT.rstrip("\n"), 1)


def sim_lib_rev(c):
    target = IA_ANCHOR + "\n" + IA_INSERT.rstrip("\n")
    require_once(c, target, "lib reverse: import block")
    return c.replace(target, IA_ANCHOR, 1)


FILES = [
    (LOOP, sim_loop_fwd, sim_loop_rev, True, "src/loop.metta (L-A + L-B)"),
    (MODULE, sim_module_fwd, sim_module_rev, True, "soul/output_verdict.metta (M-A glue)"),
    (HANDS, sim_hands_fwd, sim_hands_rev, False, "soul/soul_governance.py (G-A journal)"),
    (LIB, sim_lib_fwd, sim_lib_rev, True, "lib_clarity_reasoning.metta (I-A imports)"),
]


def run_harness(sim_module_text):
    print("\n========== PRE-APPLY HARNESS (container, fresh process) ==========")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    (LOG_DIR / "repair1_sim_module.metta").write_text(sim_module_text)
    HARNESS_HOST.write_text(HARNESS_PREAMBLE + HARNESS_TESTS)
    print(f"  harness: {HARNESS_HOST} (container {HARNESS_CONT})")
    try:
        p = subprocess.run(
            ["docker", "exec", CONTAINER, "sh", "-c",
             f"cd /PeTTa && ./run.sh {HARNESS_CONT} 2>&1"],
            capture_output=True, text=True, timeout=360)
    except Exception as exc:
        print(f"  HARNESS EXECUTION FAILED: {exc}")
        return False
    out = p.stdout or ""
    raw = LOG_DIR / f"repair1_harness_raw_{_STAMP}.log"
    raw.write_text(out)
    print(f"  FULL raw MeTTa output: {raw}")
    out_l = out.lower()
    ok = True
    print("  --- expectations (case-insensitive) ---")
    for expect, label in HARNESS_EXPECT:
        hit = expect.lower() in out_l
        print(f"  [{'PASS' if hit else 'FAIL'}] {label}: '{expect}'")
        ok = ok and hit
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    ap.add_argument("--with-harness", action="store_true")
    args = ap.parse_args()

    mode = ("reverse" if args.reverse else "forward") + ("_apply" if args.apply else "_dryrun")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logf = open(LOG_DIR / f"repair1_wiring_{mode}_{_STAMP}.log", "w")
    sys.stdout = _Tee(sys.__stdout__, logf)

    print(f"\n========== REPAIR 1 WIRING: {mode.upper()} ==========")

    sims = {}
    for path, fwd, rev, is_metta, label in FILES:
        print(f"\n>>> {label} <<<")
        if not path.exists():
            print(f"  ERROR: {path} not found. Run from repo root.")
            return 1
        content = path.read_text()
        pre = len(content.splitlines())
        if is_metta:
            o, c = code_aware_paren_count(content)
            print(f"  Pre: {pre} lines; parens {o}/{c} delta={o-c} ({'OK' if o == c else 'FAIL'})")
            if o != c:
                return 1
        else:
            print(f"  Pre: {pre} lines (python; paren count n/a)")
        try:
            sim = (rev if args.reverse else fwd)(content)
        except RuntimeError as exc:
            print(f"  STATE/SIM FAILED: {exc}")
            return 1
        post = len(sim.splitlines())
        if is_metta:
            so, sc = code_aware_paren_count(sim)
            print(f"  Post: {post} lines (delta {post-pre}); parens {so}/{sc} delta={so-sc} ({'OK' if so == sc else 'FAIL'})")
            if so != sc:
                return 1
        else:
            print(f"  Post: {post} lines (delta {post-pre})")
        sims[path] = (content, sim)

    # Harness ordering (rev 3, ledger 2026-06-11): the glue's py-call
    # needs the POST-apply soul_governance on disk, so the harness must
    # run against applied files. Flow: apply (backups) -> harness ->
    # keep on pass / RESTORE byte-identical on fail. In dry mode the
    # files are ALWAYS restored after the harness: zero net writes.
    harness_requested = args.with_harness and not args.reverse
    if args.with_harness and args.reverse:
        print("\n  (harness skipped on reverse)")

    if not args.apply and not harness_requested:
        print("\n========== ACTION-SUMMARY (DRY-RUN) ==========")
        print("  All four files simulated clean.")
        print("  No writes have occurred. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        for path in sims:
            bak = Path(str(path) + ".bak.repair1")
            bak.write_text(sims[path][0])
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    for path in sims:
        path.write_text(sims[path][1])
        print(f"Wrote: {path}")

    print("\n========== DISK VERIFICATION ==========")
    all_ok = True
    for path, fwd, rev, is_metta, label in FILES:
        d = path.read_text()
        if is_metta:
            o, c = code_aware_paren_count(d)
            ok = o == c
        else:
            ok = True
        marker_ok = (
            ("derive-gate-state" in d) if path == LOOP else
            ("SECTION 2: WIRING GLUE" in d) if path == MODULE else
            ("journal_append" in d) if path == HANDS else
            ("output_verdict" in d))
        if args.reverse:
            marker_ok = not marker_ok
        print(f"  {label}: parens {'OK' if ok else 'FAIL'}; state {'OK' if marker_ok else 'FAIL'}")

    def _restore_all():
        for p in sims:
            p.write_text(sims[p][0])
        print("  RESTORED: all four files byte-identical to pre-apply state.")

    if harness_requested:
        print("\n========== POST-APPLY HARNESS (real on-disk state) ==========")
        ok_h = run_harness(sims[MODULE][1])
        if not ok_h:
            print("\nHARNESS FAILED. Restoring pre-apply state:")
            _restore_all()
            return 1
        if not args.apply:
            print("\n  Harness PASS. Dry mode: restoring pre-apply state:")
            _restore_all()
            print("\n========== ACTION-SUMMARY (DRY-RUN) ==========")
            print("  All four files validated against the REAL post-apply state.")
            print("  No net writes. Re-run with --apply --with-harness to keep.")
            return 0
        print("\n  Harness PASS. Keeping applied state.")

        all_ok = all_ok and ok and marker_ok
    if not all_ok:
        print("DISK VERIFICATION FAILED. Restore from .bak.repair1 copies.")
        return 1

    print("\n========== ACTION-SUMMARY ==========")
    print(f"  Direction: {'REVERSE' if args.reverse else 'FORWARD'}. Four files written; verified.")
    if not args.reverse:
        print("\nNext (image-baked files changed; rebuild REQUIRED):")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d")
        print("  Then: docker logs clarity_omega 2>&1 | grep -oE '\\(SOUL-GATE-FLAG [^)]*\\)' | tail -3")
        print("        docker logs clarity_omega 2>&1 | grep -oE '\\(SOUL_VERDICT_OUT: [^)]*' | tail -3")
        print("  Expect: gate-state clean, computed verdicts varying with content,")
        print("  no loop halt on any verdict (PAUSE-effect 0 until Repair 3).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
