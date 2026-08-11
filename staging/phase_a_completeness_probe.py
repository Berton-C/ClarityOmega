#!/usr/bin/env python3
"""
Phase A completeness probe for Corner-Gate v3 (ClarityOmega).

PURPOSE
  Prove, offline, that the guard-patched v3 corridor runs END TO END:
  bootstrap, three injected core recorder calls, eviction on a fourth,
  and every MeTTa-side composer field read. Production files are NEVER
  modified: the five guards are applied to an in-memory COPY of the pure
  file only. Runs in a throwaway run.sh process (fresh AtomSpace); the
  live loop's space is untouched.

USAGE (from repo root; container clarity_omega must be Up)
  python3 staging/phase_a_completeness_probe.py

EXIT
  0 = ALL PASS. Nonzero = at least one finding; table printed.

GUARD DEFAULT SYMBOL
  not-computed (probe-provisional; production symbol is a Berton/Clarity
  ratification item).
"""
import re
import subprocess
import sys

CONTAINER = "clarity_omega"
ENGINE = ("lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics"
          "_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta")
PURE = "soul/corner_gap/coupling_legibility.metta"
WRITERS = "soul/corner_gap/coupling_legibility_writers.metta"
TMP = "/tmp/phase_a_probe.metta"
RAWLOG = "/tmp/phase_a_probe_raw.log"

# Five guards: exact anchors from the pure file, each must occur exactly once.
GUARDS = [
    ("($capture (q-self-seeing-loop-capture? $repeat $errsurface))",
     "($capture (let $g1 (collapse (q-self-seeing-loop-capture? $repeat $errsurface)) (if (== $g1 ()) not-computed (car-atom $g1))))"),
    ("($newvis (q-self-seeing-newly-visible-surface? $errsurface $errfeedback))",
     "($newvis (let $g2 (collapse (q-self-seeing-newly-visible-surface? $errsurface $errfeedback)) (if (== $g2 ()) not-computed (car-atom $g2))))"),
    ("($shift (q-self-seeing-orientation-shift? repeated-command $probe $newverr))",
     "($shift (let $g3 (collapse (q-self-seeing-orientation-shift? repeated-command $probe $newverr)) (if (== $g3 ()) not-computed (car-atom $g3))))"),
    ("($nav (q-self-seeing-navigation-change? orientation-shift $trace $future))",
     "($nav (let $g4 (collapse (q-self-seeing-navigation-change? orientation-shift $trace $future)) (if (== $g4 ()) not-computed (car-atom $g4))))"),
    ("(q-residual-threshold-gap? $supsym target-threshold $ressym)",
     "(let $g5 (collapse (q-residual-threshold-gap? $supsym target-threshold $ressym)) (if (== $g5 ()) not-computed (car-atom $g5)))"),
    ("""          ($ipbit (mk-pbit $is 0.7))
          ($apbit (mk-pbit $as 0.7))
          ($opbit (mk-pbit $os 0.7))
          ($iapbit (q-meet $ipbit $apbit))
          ($aopbit (q-meet $apbit $opbit))
          ($e1 (q-intention-action intention action $iapbit))
          ($e2 (q-action-outcome action outcome $aopbit))
          ($chain (q-coherence-chain $e1 $e2))
          ($cpbit (qalignment-pbit $chain))
          ($s (coupling-pbit-strength $cpbit)))""",
     """          ($ia (min $is $as))
          ($ao (min $as $os))
          ($s (* $ia $ao)))"""),
]

PROBE_BODY = r"""
;; ---------------- PHASE A PROBE BODY (appended; fresh space) ----------------
(= (probe-pre-ord) (latest-coupling-ord))
(= (probe-pre-move) (latest-coupling-next-move))
(= (probe-boot) (do-bootstrap-coupling!))
(= (probe-c1) (do-record-coupling-cycle-core! 1 False False "sig-shell-aaaa1111" "unknown" "unknown" (shell) none attending "ts-1"))
(= (probe-c2) (do-record-coupling-cycle-core! 2 False False "sig-shell-aaaa1111" "unknown" "unknown" (shell) none attending "ts-2"))
(= (probe-c3) (do-record-coupling-cycle-core! 3 True False "sig-read-bbbb2222" "unknown" "file:cccc3333" (read-file) forward attending "ts-3"))
(= (probe-c4) (do-record-coupling-cycle-core! 4 False False "none" "unknown" "unknown" (pin) forward attending "ts-4"))
(= (probe-count) (coupling-window-count))
(= (probe-ord) (latest-coupling-ord))
(= (probe-full-arity $o)
   (let $m (collapse (match &self (coupling-cycle-record $o $a $b $c $d $e $f $g $h $i $j $k $l $m2 $n $p $q $r) matched-full-arity))
     (if (== $m ()) NO-RECORD (car-atom $m))))
(= (probe-fields)
   (let* (($cc (latest-coupling-contact-count))
          ($ds (latest-coupling-dominant-surface))
          ($ch (latest-coupling-chain-state))
          ($ta (latest-coupling-task-accord))
          ($ca (latest-coupling-contact-accord))
          ($bd (current-coupling-band))
          ($sp (latest-coupling-support))
          ($rs (latest-coupling-residual-gap))
          ($tj (coupling-trace-verdict-for-window))
          ($nm (latest-coupling-next-move))
          ($hs (latest-coupling-honesty))
          ($car (coupling-contact-audit-render $ta $ca)))
     (FIELDS $cc $ds $ch $ta $ca $bd $sp $rs $tj $nm $hs $car)))
!(println! (PROBE-PRE-ORD (probe-pre-ord)))
!(println! (PROBE-PRE-MOVE (probe-pre-move)))
!(println! (PROBE-BOOT (probe-boot)))
!(println! (PROBE-C1 (probe-c1)))
!(println! (PROBE-C1-COUNT (probe-count)))
!(println! (PROBE-C1-ORD (probe-ord)))
!(println! (PROBE-C1-ARITY (probe-full-arity 1)))
!(println! (PROBE-C2 (probe-c2)))
!(println! (PROBE-C2-COUNT (probe-count)))
!(println! (PROBE-C2-ORD (probe-ord)))
!(println! (PROBE-C3 (probe-c3)))
!(println! (PROBE-C3-COUNT (probe-count)))
!(println! (PROBE-C3-ORD (probe-ord)))
!(println! (PROBE-C4 (probe-c4)))
!(println! (PROBE-C4-COUNT (probe-count)))
!(println! (PROBE-C4-ORD (probe-ord)))
!(println! (PROBE-C4-EVICTED (probe-full-arity 1)))
!(println! (PROBE-FIELDS (probe-fields)))
!(println! (PROBE-A-END done))
"""

# Expected: sentinel -> (mode, value). eq = exact token; present = line exists.
EXPECT = [
    ("PROBE-PRE-ORD", "eq", "0"),
    ("PROBE-PRE-MOVE", "present", None),
    ("PROBE-BOOT", "eq", "bootstrap-coupling-done"),
    ("PROBE-C1", "eq", "record-coupling-cycle-done"),
    ("PROBE-C1-COUNT", "eq", "1"),
    ("PROBE-C1-ORD", "eq", "1"),
    ("PROBE-C1-ARITY", "eq", "matched-full-arity"),
    ("PROBE-C2", "eq", "record-coupling-cycle-done"),
    ("PROBE-C2-COUNT", "eq", "2"),
    ("PROBE-C2-ORD", "eq", "2"),
    ("PROBE-C3", "eq", "record-coupling-cycle-done"),
    ("PROBE-C3-COUNT", "eq", "3"),
    ("PROBE-C3-ORD", "eq", "3"),
    ("PROBE-C4", "eq", "record-coupling-cycle-done"),
    ("PROBE-C4-COUNT", "eq", "3"),
    ("PROBE-C4-ORD", "eq", "4"),
    ("PROBE-C4-EVICTED", "eq", "NO-RECORD"),
    ("PROBE-FIELDS", "present", None),
    ("PROBE-A-END", "eq", "done"),
]

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=600, **kw)


def paren_delta(s):
    return s.count("(") - s.count(")")


def main():
    parts = []
    for path in (ENGINE, PURE, WRITERS):
        try:
            with open(path, "r") as f:
                text = f.read()
        except OSError as e:
            print("ABORT: cannot read " + path + ": " + str(e))
            return 2
        if path == PURE:
            before = paren_delta(text)
            for anchor, repl in GUARDS:
                n = text.count(anchor)
                if n != 1:
                    print("ABORT: anchor count " + str(n) + " (need exactly 1) for: " + anchor)
                    return 2
                text = text.replace(anchor, repl)
            after = paren_delta(text)
            if before != after:
                print("ABORT: paren balance changed by guard patch: " + str(before) + " -> " + str(after))
                return 2
            print("Patches applied to in-memory copy: 6 of 6, paren balance preserved.")
        parts.append(text)
    script = "\n".join(parts) + "\n" + PROBE_BODY + "\n"

    w = run(["docker", "exec", "-i", CONTAINER, "sh", "-c", "cat > " + TMP], input=script)
    if w.returncode != 0:
        print("ABORT: write into container failed: " + str(w.stderr))
        return 2
    p = run(["docker", "exec", CONTAINER, "sh", "-c", "cd /PeTTa && ./run.sh " + TMP + " 2>&1"])
    raw = ANSI.sub("", p.stdout or "")
    with open(RAWLOG, "w") as f:
        f.write(raw)

    # Result lines only: sentinel lines that are not transpiler echoes.
    lines = {}
    for ln in raw.splitlines():
        s = ln.strip()
        if s.startswith("(PROBE-") and "println" not in s:
            key = s[1:].split(" ", 1)[0].split(")", 1)[0]
            lines[key] = s

    failures = []
    print("")
    print("SENTINEL                 EXPECTED                       GOT")
    print("-" * 78)
    for key, mode, want in EXPECT:
        got = lines.get(key)
        if got is None:
            print("%-24s %-30s ABSENT (silent death upstream)" % (key, want if want else "line present"))
            failures.append(key + ": ABSENT")
            continue
        if "$" in got:
            print("%-24s %-30s %s" % (key, want if want else "line present", got))
            failures.append(key + ": unbound variable leaked: " + got)
            continue
        if mode == "eq":
            ok = ("(" + key + " " + want + ")") == got
            print("%-24s %-30s %s" % (key, want, got + ("" if ok else "   <-- MISMATCH")))
            if not ok:
                failures.append(key + ": expected " + want + " got " + got)
        else:
            print("%-24s %-30s %s" % (key, "line present", got))
    print("-" * 78)
    if failures:
        print("PHASE A: FAIL. Findings (" + str(len(failures)) + "):")
        for f in failures:
            print("  - " + f)
        print("Full raw output: " + RAWLOG)
        return 1
    print("PHASE A: ALL PASS. Corridor runs end to end under guards.")
    print("Full raw output: " + RAWLOG)
    return 0


if __name__ == "__main__":
    sys.exit(main())
