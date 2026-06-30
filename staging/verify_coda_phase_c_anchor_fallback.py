#!/usr/bin/env python3
"""
verify_coda_phase_c_anchor_fallback.py

Closes the residual the live_path harness left open: the dispatch-chain-anchored
and dispatch-fallback-activated paths were proven-by-construction (sweep patterns
field-matched to writers) but never proven-by-exercise, because skill-discovery
is non-anchor and always eligible, so neither branch fires in normal operation.

This is the rewrite of the obsolete verify_coda_phase_c_dispatch_result.py, which
failed for two reasons unrelated to the substrate: bare top-level !(dispatch ...)
compiles as DATA not a call (so its writes never fired), and its result parser
split on ^^^^^ which collides with run.sh's form separators. This harness uses
the live_path shape instead: every driver is a DEFINED function invoked by
!(probe-...), and the result separator is ===R===.

Against the DEPLOYED capability_registry.metta, with synthetic fixtures:

  ANCHOR        a handler returning decision-anchor drives run-chain's anchor
                branch. Expect: dispatch-result written (handler test-anchor),
                dispatch-chain-anchored written, dispatch-chain-exhausted NOT
                written (the anchor short-circuits). This also proves the
                dispatch-result write fires BEFORE the anchor branch (the wrap).

  ANCHOR-SWEEP  two anchor dispatches (each sweeps at the top of dispatch) leave
                exactly ONE dispatch-chain-anchored, not two. Exercises sweep
                pattern (e) against a REAL anchored atom.

  FALLBACK      a request matching no registered capability drives the fallback
                branch. Expect: dispatch-fallback-activated written, NO
                dispatch-result.

  FALLBACK-SWEEP  two fallback dispatches leave exactly ONE
                dispatch-fallback-activated, not two. Exercises sweep pattern
                (f) against a REAL fallback atom.

WHAT THIS DOES AND DOES NOT PROVE (honest boundary):
  It exercises the DEPLOYED registry's dispatch / run-chain / sweep with
  synthetic capabilities, in a FRESH AtomSpace per invocation. It proves the
  anchor and fallback WRITE paths and that the sweep clears those two atom
  shapes. It uses fixtures, not a production decision-anchor capability (none
  exists yet); when one lands, its real handler/schema should get its own
  exercise. The anchor/fallback MECHANICS, however, are registry-generic and
  fully exercised here.

USAGE (run from repo root):
  python3 staging/verify_coda_phase_c_anchor_fallback.py
"""

import datetime
import re
import subprocess

CONTAINER = "clarity_omega"
REPO = "/PeTTa/repos/omegaclaw"
REGISTRY = REPO + "/soul/capability_registry.metta"   # promoted (sweep + dispatch-result wrap)
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG = "/tmp/verify_coda_phase_c_anchor_fallback_%s.log" % STAMP

# Fixtures + defined-function drivers. The (eligible-lifecycle active) seed lives
# in skill_discovery.metta in production; we seed it here so test-anchor passes
# lifecycle-filter-step. nomatch-req intentionally matches no registration.
DRIVER = r"""
;; ---- fixtures ----
(eligible-lifecycle active)
(registered-capability schema: (anchor-req cycle: $k) handler: test-anchor priority: 100 lifecycle: active metadata: ())
(= (test-anchor $req) decision-anchor)

;; ---- counts (collapse/match nest in a bind; size-atom returns a bare scalar) ----
(= (count-result-testanchor)
   (let $h (collapse (match &self (dispatch-result invocation-id: $i result: $r handler: test-anchor) present)) (size-atom $h)))
(= (count-result-any)
   (let $h (collapse (match &self (dispatch-result invocation-id: $i result: $r handler: $hd) present)) (size-atom $h)))
(= (count-anchored)
   (let $h (collapse (match &self (dispatch-chain-anchored invocation-id: $i anchor-handler: $ah) present)) (size-atom $h)))
(= (count-anchored-testanchor)
   (let $h (collapse (match &self (dispatch-chain-anchored invocation-id: $i anchor-handler: test-anchor) present)) (size-atom $h)))
(= (count-exhausted)
   (let $h (collapse (match &self (dispatch-chain-exhausted invocation-id: $i) present)) (size-atom $h)))
(= (count-fallback)
   (let $h (collapse (match &self (dispatch-fallback-activated invocation-id: $i input-atom: $a reason: $r) present)) (size-atom $h)))

;; ---- ANCHOR: one decision-anchor dispatch ----
(= (probe-anchor)
   (let $_ (dispatch (anchor-req cycle: 1) 1)
   (let $res (count-result-testanchor)
   (let $anc (count-anchored-testanchor)
   (let $exh (count-exhausted)
        (ANCHOR result-testanchor: $res anchored: $anc exhausted: $exh))))))

;; ---- ANCHOR-SWEEP: two anchor dispatches -> exactly one anchored left ----
(= (probe-anchor-sweep)
   (let $_1 (dispatch (anchor-req cycle: 1) 1)
   (let $_2 (dispatch (anchor-req cycle: 2) 2)
   (let $n (count-anchored)
        (ANCHOR-SWEEP anchored-remaining: $n)))))

;; ---- FALLBACK: one no-match dispatch ----
(= (probe-fallback)
   (let $_ (dispatch (nomatch-req cycle: 1) 1)
   (let $fb (count-fallback)
   (let $res (count-result-any)
        (FALLBACK fallback: $fb result: $res)))))

;; ---- FALLBACK-SWEEP: two no-match dispatches -> exactly one fallback left ----
(= (probe-fallback-sweep)
   (let $_1 (dispatch (nomatch-req cycle: 1) 1)
   (let $_2 (dispatch (nomatch-req cycle: 2) 2)
   (let $n (count-fallback)
        (FALLBACK-SWEEP fallback-remaining: $n)))))
"""


def sh(cmd, stdin=None):
    p = subprocess.run(["docker", "exec", "-i", CONTAINER, "sh", "-c", cmd],
                       input=stdin, capture_output=True, text=True)
    return p.stdout + p.stderr


def errd(o):
    return ("error" in o.lower()) or ("character_code" in o.lower())


def tail_after_sep(o):
    return o.rsplit("===R===", 1)[-1] if "===R===" in o else o


def main():
    buf = []

    def say(s):
        print(s)
        buf.append(s)

    say("verify_coda_phase_c_anchor_fallback %s" % STAMP)

    registry_src = sh("cat %s" % REGISTRY)
    pf = []
    if "sweep-dispatch-atoms!" not in registry_src:
        pf.append("sweep-dispatch-atoms! missing from deployed registry")
    if "dispatch-chain-anchored" not in registry_src:
        pf.append("dispatch-chain-anchored writer/sweep missing from deployed registry")
    if "dispatch-fallback-activated" not in registry_src:
        pf.append("dispatch-fallback-activated writer/sweep missing from deployed registry")
    if pf:
        for m in pf:
            say("PREFLIGHT FAIL: " + m)
        say("Aborting: deployed registry is not the swept Phase C surface.")
        sh("cat > %s" % LOG, stdin="\n".join(buf))
        return
    say("preflight OK: deployed registry has the sweep and both anchor/fallback writers")

    base = registry_src + "\n" + DRIVER + "\n"

    def run_one(call):
        probe = base + '!("===R===")\n!(%s)\n' % call
        path = "/tmp/_anc_%s_%s.metta" % (call.replace("-", "_"), STAMP)
        sh("cat > %s" % path, stdin=probe)
        return sh("cd /PeTTa && ./run.sh %s 2>&1" % path)

    out_anchor = run_one("probe-anchor")
    out_answeep = run_one("probe-anchor-sweep")
    out_fallback = run_one("probe-fallback")
    out_fbsweep = run_one("probe-fallback-sweep")
    buf.append("===== RAW ANCHOR =====\n" + out_anchor)
    buf.append("===== RAW ANCHOR-SWEEP =====\n" + out_answeep)
    buf.append("===== RAW FALLBACK =====\n" + out_fallback)
    buf.append("===== RAW FALLBACK-SWEEP =====\n" + out_fbsweep)

    m_an = re.search(r"ANCHOR result-testanchor:\s*(\d+)\s*anchored:\s*(\d+)\s*exhausted:\s*(\d+)",
                     tail_after_sep(out_anchor))
    anchor_ok = (bool(m_an)
                 and int(m_an.group(1)) >= 1     # dispatch-result written (handler test-anchor)
                 and int(m_an.group(2)) >= 1     # dispatch-chain-anchored written
                 and int(m_an.group(3)) == 0     # did NOT fall through to exhausted
                 and not errd(out_anchor))

    m_as = re.search(r"ANCHOR-SWEEP anchored-remaining:\s*(\d+)", tail_after_sep(out_answeep))
    answeep_ok = bool(m_as) and int(m_as.group(1)) == 1 and not errd(out_answeep)

    m_fb = re.search(r"FALLBACK fallback:\s*(\d+)\s*result:\s*(\d+)", tail_after_sep(out_fallback))
    fallback_ok = (bool(m_fb)
                   and int(m_fb.group(1)) >= 1   # dispatch-fallback-activated written
                   and int(m_fb.group(2)) == 0   # no dispatch-result on a no-match
                   and not errd(out_fallback))

    m_fs = re.search(r"FALLBACK-SWEEP fallback-remaining:\s*(\d+)", tail_after_sep(out_fbsweep))
    fbsweep_ok = bool(m_fs) and int(m_fs.group(1)) == 1 and not errd(out_fbsweep)

    say("")
    say("ANCHOR        result+anchored written, no exhausted : %s  (%s)" % (
        "PASS" if anchor_ok else "FAIL", m_an.group(0) if m_an else "no ANCHOR line"))
    say("ANCHOR-SWEEP  2 anchor dispatches -> 1 anchored left : %s  (%s)" % (
        "PASS" if answeep_ok else "FAIL", m_as.group(0) if m_as else "no ANCHOR-SWEEP line"))
    say("FALLBACK      fallback written, no dispatch-result   : %s  (%s)" % (
        "PASS" if fallback_ok else "FAIL", m_fb.group(0) if m_fb else "no FALLBACK line"))
    say("FALLBACK-SWEEP 2 fallback dispatches -> 1 fallback left: %s  (%s)" % (
        "PASS" if fbsweep_ok else "FAIL", m_fs.group(0) if m_fs else "no FALLBACK-SWEEP line"))
    say("")

    if anchor_ok and answeep_ok and fallback_ok and fbsweep_ok:
        say("VERDICT: ALL PASS. The anchor and fallback WRITE paths fire correctly,")
        say("and the sweep clears a real dispatch-chain-anchored atom and a real")
        say("dispatch-fallback-activated atom. Both sweep patterns that were")
        say("proven-by-construction are now proven-by-exercise. The full six-pattern")
        say("sweep set is exercised (4 via live_path, these 2 here).")
    else:
        say("VERDICT: NOT ALL PASS. Read the RAW sections; the affected branch or")
        say("sweep pattern is not behaving as the registry definition implies.")

    sh("cat > %s" % LOG, stdin="\n".join(buf))
    print("\nRaw trace in-container at %s  (maps to host shared_files/)" % LOG)


if __name__ == "__main__":
    main()
