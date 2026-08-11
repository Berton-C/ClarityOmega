#!/usr/bin/env python3
"""
Phase A.1 core bisect probe for Corner-Gate v3 (ClarityOmega). v2.

PURPOSE
  Localize and now verify the corridor fix set offline. Applies SIX
  in-memory patches to a COPY of the pure file (five collapse guards
  for partial engine tables, D-1, plus the derive-support arithmetic
  replacement for the Atom-typed guard hole, D-2), inserts 17 ordered
  sentinels into an in-memory copy of the CORE recorder, runs four
  injected calls, and reports how far each call gets with every bound
  value. Production files are NEVER modified. Fresh throwaway space.

ENVIRONMENT
  Container clarity_omega must be Up. Run from repo root. python3.

USAGE
  python3 staging/phase_a1_core_bisect_probe.py

PREDICTIONS (v2, stated before run)
  6 of 6 patches applied, paren balance preserved. All four calls
  RETURN. C1: S9 = 0.18, S11 = cannot-estimate-gap, S14 = evict-done.

OUTPUT
  Per-call reach report + ordered sentinel value trace.
  Full raw run: /tmp/phase_a1_core_bisect_raw.log
"""
import re
import subprocess
import sys

CONTAINER = "clarity_omega"
ENGINE = ("lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics"
          "_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta")
PURE = "soul/corner_gap/coupling_legibility.metta"
WRITERS = "soul/corner_gap/coupling_legibility_writers.metta"
TMP = "/tmp/phase_a1_probe.metta"
RAWLOG = "/tmp/phase_a1_core_bisect_raw.log"

# Six in-memory patches to the pure file.
# 1-4: collapse guards on the partial q-self-seeing tables (D-1).
# 5:   collapse guard on the partial residual table (D-1).
# 6:   derive-support arithmetic replacement (D-2): engine-identical
#      numerics, support = (min is as) * (min as os), per engine
#      q-meet min-strength and coherence-chain strength product.
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

SENTINELS = [
    ("S0", "($prevmove (latest-coupling-next-move))", "$prevmove"),
    ("S1", "($windowcount (coupling-window-count))", "$windowcount"),
    ("S2", "($_rc (record-contacts-for-heads! $ord $heads))", "rc-done"),
    ("S3", "($domsurf (dominant-surface-of $surfaces))", "$domsurf"),
    ("S4", "($failcount (do-set-command-signature! $sig $failed $ord))", "$failcount"),
    ("S5", "($honesty (derive-honesty-state $hasaction $hasclaim $atarget $vtarget))", "$honesty"),
    ("S5b", "($trace (derive-trace-symbol $windowcount))", "$trace"),
    ("S6", "($chainstate (derive-chain-state $repeat $errsurf $errfb $probe $trace $ccount))", "$chainstate"),
    ("S7", "($polverdict (derive-polarity-verdict $protection $contactability $suspicion $polarity $winpos))", "$polverdict"),
    ("S8", "($caccord (derive-contact-accord $ccount $windowcount $probe $prevfail))", "$caccord"),
    ("S9", "($support (derive-support $ileg $aleg $oleg))", "$support"),
    ("S10", "($band (derive-band $support $priorband))", "$band"),
    ("S11", "($residual (derive-residual-gap $support $windowcount))", "$residual"),
    ("S12", "($traceverdict (coupling-trace-verdict-with-current $polverdict))", "$traceverdict"),
    ("S13", "($nextmove (derive-next-move $chainstate $traceverdict $honesty))", "$nextmove"),
    ("S14", "($_evict (do-evict-oldest-record!))", "evict-done"),
]
NEXT_SEGMENT = {
    "ENTRY": "prelude reads (prevsig/prevfail/prevrec-ord/prevccount/prevmove)",
    "S0": "windowcount read",
    "S1": "contact events (clear, user-words/failed-query, record-contacts-for-heads!)",
    "S2": "surfaces collapse + ccount + dominant-surface-of",
    "S3": "hiddenfail/failed decision + do-set-command-signature!",
    "S4": "Gate H hasaction/hasclaim + derive-honesty-state",
    "S5": "D7 derivations (repeat/errsurf/errfb/probe/trace)",
    "S5b": "derive-chain-state (guarded)",
    "S6": "protection/contactability/suspicion/polarity/winpos + derive-polarity-verdict",
    "S7": "firsthead/firstclass/legs + derive-accord-summary + derive-contact-accord",
    "S8": "derive-support (arithmetic form, patch 6)",
    "S9": "priorband read + derive-band + do-set-coupling-band!",
    "S10": "derive-residual-gap (guarded)",
    "S11": "coupling-trace-verdict-with-current",
    "S12": "derive-next-move",
    "S13": "ctx bindings + do-evict-oldest-record!",
    "S14": "the record add-atom itself",
}

PROBE_BODY = r"""
;; ------------- PHASE A.1 PROBE BODY (appended; fresh space) -------------
(= (probe-boot) (do-bootstrap-coupling!))
(= (probe-c1) (do-record-coupling-cycle-core! 1 False False "sig-shell-aaaa1111" "unknown" "unknown" (shell) none attending "ts-1"))
(= (probe-c2) (do-record-coupling-cycle-core! 2 False False "sig-shell-aaaa1111" "unknown" "unknown" (shell) none attending "ts-2"))
(= (probe-c3) (do-record-coupling-cycle-core! 3 True False "sig-read-bbbb2222" "unknown" "file:cccc3333" (read-file) forward attending "ts-3"))
(= (probe-c4) (do-record-coupling-cycle-core! 4 False False "none" "unknown" "unknown" (pin) forward attending "ts-4"))
!(println! (PROBE-BOOT (probe-boot)))
!(println! (MARK-C1-BEGIN x))
!(println! (PROBE-C1 (probe-c1)))
!(println! (MARK-C1-END x))
!(println! (MARK-C2-BEGIN x))
!(println! (PROBE-C2 (probe-c2)))
!(println! (MARK-C2-END x))
!(println! (MARK-C3-BEGIN x))
!(println! (PROBE-C3 (probe-c3)))
!(println! (MARK-C3-END x))
!(println! (MARK-C4-BEGIN x))
!(println! (PROBE-C4 (probe-c4)))
!(println! (MARK-C4-END x))
!(println! (PROBE-A1-END done))
"""

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
            applied = 0
            for anchor, repl in GUARDS:
                n = text.count(anchor)
                if n != 1:
                    print("ABORT: patch anchor count " + str(n) + " (need exactly 1) for anchor beginning: "
                          + anchor.splitlines()[0].strip())
                    print("If this is patch 6, whitespace may differ from the repo file; paste the")
                    print("derive-support body from soul/corner_gap/coupling_legibility.metta.")
                    return 2
                text = text.replace(anchor, repl)
                applied += 1
            if paren_delta(text) != before:
                print("ABORT: paren balance changed by patches: " + str(before) + " -> " + str(paren_delta(text)))
                return 2
            print("Patches applied to in-memory pure copy: " + str(applied) + " of " + str(len(GUARDS))
                  + ", paren balance preserved.")
        if path == WRITERS:
            before = paren_delta(text)
            for sid, anchor, val in SENTINELS:
                if text.count(anchor) != 1:
                    print("ABORT: sentinel anchor not unique (" + sid + "): " + anchor)
                    return 2
                ins = anchor + "\n          ($_" + sid.lower() + " (println! (CORE-" + sid + " " + val + ")))"
                text = text.replace(anchor, ins)
            if paren_delta(text) != before:
                print("ABORT: paren balance changed by sentinels")
                return 2
            print("Sentinels: " + str(len(SENTINELS)) + " inserted into in-memory core copy.")
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

    seq = []
    for ln in raw.splitlines():
        s = ln.strip()
        if "println" in s:
            continue
        if s.startswith("(CORE-") or s.startswith("(PROBE-") or s.startswith("(MARK-"):
            seq.append(s)

    print("")
    print("ORDERED TRACE (result lines only):")
    for s in seq:
        print("  " + s)

    print("")
    print("PER-CALL REACH REPORT:")
    all_returned = True
    for c in ["C1", "C2", "C3", "C4"]:
        inside = False
        reached = []
        returned = False
        for s in seq:
            if s.startswith("(MARK-" + c + "-BEGIN"):
                inside = True
                continue
            if s.startswith("(MARK-" + c + "-END"):
                break
            if inside and s.startswith("(CORE-"):
                sid = s[6:].split(" ", 1)[0].split(")", 1)[0]
                reached.append((sid, s))
            if inside and s.startswith("(PROBE-" + c + " "):
                returned = True
        if returned:
            print("  " + c + ": RETURNED (full corridor).")
        elif not reached:
            all_returned = False
            print("  " + c + ": died before S0; segment: " + NEXT_SEGMENT["ENTRY"])
        else:
            all_returned = False
            last = reached[-1][0]
            print("  " + c + ": died in segment after " + last + ": " + NEXT_SEGMENT.get(last, "?"))
        for sid, s in reached:
            print("      " + s)
    print("")
    if all_returned:
        print("PHASE A.1 v2: ALL FOUR CALLS RETURNED under the six-patch fix set.")
        print("Next: apply patch 6 to the Phase A completeness probe and require ALL PASS.")
    else:
        print("PHASE A.1 v2: at least one call still dies. Findings above join the fix set.")
    print("Full raw output: " + RAWLOG)
    return 0 if all_returned else 1


if __name__ == "__main__":
    sys.exit(main())
