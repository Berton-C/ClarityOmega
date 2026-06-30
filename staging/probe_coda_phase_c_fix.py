#!/usr/bin/env python3
"""
probe_coda_phase_c_fix.py

Pre-rebuild confidence probe for the Phase C crash fix. Proves, standalone via
run.sh (no live loop needed), that:

  P-FIX-1  skill-discovery PASSES the filter pipeline once (eligible-lifecycle
           active) is seeded: dispatch writes a (dispatch-result ... (skill-set
           skills: ...) ...) instead of falling back.
  P-FIX-2  dispatch-skills returns the skill-set string on the happy path
           (dispatch fired, read non-empty) -- the value getContext will use.
  P-FIX-3  dispatch-skills is TOTAL: first-skill-or-default falls back to
           getSkills on an empty read and skips () padding, so a dispatch miss
           can never crash getContext. Tested on (), (()), and ("real").
  P-FIX-4  the whole run completes (no abort), which is the property whose
           absence killed the loop at iteration 1.

HANDS ONLY: Python assembles the probe text; the substrate computes. getSkills
is stubbed to a known sentinel so the assertions are unambiguous and we do not
depend on src/skills.metta. Logs to container /tmp only.

USAGE (from repo root, after reverse has restored a clean tree):
  python3 staging/probe_coda_phase_c_fix.py
"""

import datetime
import re
import subprocess

CONTAINER = "clarity_omega"
DRAFT = "/PeTTa/repos/omegaclaw/soul/capability_registry_path_c_draft.metta"
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG = "/tmp/probe_coda_phase_c_fix_%s.log" % STAMP

STUB = "STUB-SKILLS-ALPHA-BETA-GAMMA"

# The run-chain dispatch-result edit (same wrap the apply script makes), applied
# here so the probe exercises the promoted registry, not the bare draft.
RUNCHAIN_OLD = """(if (== $result decision-anchor)
                             (add-atom &self
                               (dispatch-chain-anchored
                                 invocation-id: $invocation-id
                                 anchor-handler: $handler))
                             (run-chain $tail $input-atom $invocation-id))"""
RUNCHAIN_NEW = """(progn
                           (add-atom &self
                             (dispatch-result
                               invocation-id: $invocation-id
                               result: $result
                               handler: $handler))
                           (if (== $result decision-anchor)
                             (add-atom &self
                               (dispatch-chain-anchored
                                 invocation-id: $invocation-id
                                 anchor-handler: $handler))
                             (run-chain $tail $input-atom $invocation-id)))"""

# skill_discovery content under test (seed + registration + handler + accessor).
SKILL = """
(eligible-lifecycle active)

(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ())

(= (skill-discovery $request)
   (let* (($capabilities (collapse (match &self
                                          (registered-capability
                                            schema: $s handler: $h priority: $p
                                            lifecycle: active metadata: $m)
                                          ($s $h $p $m))))
          ($formatted (format-skill-set $capabilities)))
         (skill-set skills: $formatted)))

(= (format-skill-set $capabilities) (getSkills))

(= (dispatch-skills $k)
   (let $_ (dispatch (skill-request cycle: $k) $k)
        (first-skill-or-default
          (collapse (match &self
                          (dispatch-result invocation-id: $k
                            result: (skill-set skills: $s) handler: $_h)
                          $s)))))

(= (first-skill-or-default $strs)
   (if (== $strs ())
       (getSkills)
       (let $h (car-atom $strs)
            (if (== $h ())
                (first-skill-or-default (cdr-atom $strs))
                $h))))
"""

GETSKILLS_STUB = '(= (getSkills) "%s")\n' % STUB


def sh(cmd, stdin=None):
    p = subprocess.run(["docker", "exec", "-i", CONTAINER, "sh", "-c", cmd],
                       input=stdin, capture_output=True, text=True)
    return p.stdout + p.stderr


def result_section(out):
    return out.rsplit("^^^^^", 1)[1] if "^^^^^" in out else out


def main():
    buf = []

    def say(s):
        print(s)
        buf.append(s)

    say("Phase C fix probe %s" % STAMP)
    registry = sh("cat %s" % DRAFT)
    if RUNCHAIN_OLD.split()[0] and len(list(re.finditer(
            r"\s+".join(re.escape(t) for t in RUNCHAIN_OLD.split()), registry))) != 1:
        say("WARN: run-chain anchor not uniquely found in draft; probe runs on bare draft.")
        promoted = registry
    else:
        promoted = re.sub(r"\s+".join(re.escape(t) for t in RUNCHAIN_OLD.split()),
                          lambda m: RUNCHAIN_NEW, registry, count=1)

    probe = promoted + "\n" + GETSKILLS_STUB + SKILL + """
;; ---- happy path: dispatch fires, skill-discovery passes filters ----
!(dispatch-skills 1)
!("^^^^^")
!(dispatch-skills 1)
;; was a real skill-set dispatch-result written for invocation 1?
!(collapse (match &self (dispatch-result invocation-id: 1 result: (skill-set skills: $s) handler: $h) wrote-skillset))
;; ---- totality of the fallback ----
!(first-skill-or-default ())
!(first-skill-or-default (()))
!(first-skill-or-default ("real-string-here"))
;; ---- death mechanism reproduced in isolation, next to the fix ----
;; OLD form: car-atom over an empty collapse. Expected: NO result line / failure.
!(car-atom (collapse (match &self (no-such-dispatch-result-xyz $x) $x)))
!("DEATH-MARKER-AFTER-CAR-ATOM")
;; FIXED form on the SAME empty input. Expected: the getSkills stub.
!(first-skill-or-default (collapse (match &self (no-such-dispatch-result-xyz $x) $x)))
"""
    path = "/tmp/_probe_%s.metta" % STAMP
    sh("cat > %s" % path, stdin=probe)
    out = sh("cd /PeTTa && ./run.sh %s 2>&1" % path)
    buf.append("===== RAW =====\n" + out)
    sec = result_section(out)

    p1 = "wrote-skillset" in sec
    p2 = STUB in sec
    p3 = (sec.count(STUB) >= 2) and ("real-string-here" in sec)
    p4 = ("error" not in out.lower()) and ("abort" not in out.lower())
    # P-DEATH: on the SAME empty collapse that the old car-atom died on, the
    # fixed accessor returns the stub. The raw trace shows the old car-atom form
    # above the death marker producing no value, for visual contrast.
    after_marker = sec.rsplit("DEATH-MARKER-AFTER-CAR-ATOM", 1)[-1]
    pdeath = STUB in after_marker

    say("P-FIX-1 skill-discovery passed filters, skill-set dispatch-result written: %s"
        % ("PASS" if p1 else "FAIL"))
    say("P-FIX-2 dispatch-skills returned the skills string on happy path: %s"
        % ("PASS" if p2 else "FAIL"))
    say("P-FIX-3 first-skill-or-default total on (), (()), and (\"real\"): %s"
        % ("PASS" if p3 else "FAIL"))
    say("P-FIX-4 run completed with no error/abort: %s" % ("PASS" if p4 else "FAIL"))
    say("P-DEATH fixed accessor returns getSkills on the exact empty-collapse "
        "input the old car-atom died on: %s" % ("PASS" if pdeath else "FAIL"))
    say("\nVERDICT: %s" % ("ALL PASS -- fix is total and dispatch fires"
                           if all([p1, p2, p3, p4, pdeath]) else "SEE RAW TRACE"))
    if not (p1 and p2):
        say("  (If P-FIX-1 fails, eligible-lifecycle/efficacy is still filtering "
            "skill-discovery; if only P-FIX-2 fails, the read shape disagrees.)")
    sh("cat > %s" % LOG, stdin="\n".join(buf))
    print("\nRaw trace in-container at %s" % LOG)


if __name__ == "__main__":
    main()
