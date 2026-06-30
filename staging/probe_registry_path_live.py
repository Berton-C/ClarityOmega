#!/usr/bin/env python3
"""
probe_registry_path_live.py

Proves the question PR-DSIZE=21 could NOT answer: did the registry actually
DISPATCH skill-discovery (registry path live), or did first-skill-or-default
fall back to getSkills? Both yield a 21-element list, so the count cannot tell
them apart. This reads the atoms dispatch writes, which CAN.

It dispatches once, then in the SAME evaluation reads three presence facts:
  - dispatch-result carrying a skill-set        -> skillset count
  - dispatch-fallback-activated                 -> fallback count (+ reason)
  - capability-invoked                          -> handler that ran (+ count)

Each read returns a BARE SYMBOL (per the Atom Operations Map read-instrument
rule: never return a compound) and is counted by list length. Every let bind is
either a core-form nest (collapse/match, which reduce in a bind) or a single
ordinary call on an already-bound value (size-atom $v), per the nested-in-bind
rule -- no ordinary fn is given a call-valued argument in a bind.

Interpretation:
  REGISTRY PATH LIVE  : skillset >= 1, fallback == 0, capinvoked names skill-discovery
  FELL BACK           : skillset == 0, fallback >= 1 (reason printed); registry inert

USAGE (from repo root, after reverse has restored a clean tree):
  python3 staging/probe_registry_path_live.py
"""

import datetime
import re
import subprocess

CONTAINER = "clarity_omega"
REPO = "/PeTTa/repos/omegaclaw"
DRAFT = REPO + "/soul/capability_registry_path_c_draft.metta"
SKILLS = REPO + "/src/skills.metta"
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG = "/tmp/probe_registry_path_live_%s.log" % STAMP

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

SKILL = """
(eligible-lifecycle active)
(registered-capability schema: (skill-request cycle: $k) handler: skill-discovery
   priority: 100 lifecycle: active metadata: ())
(= (skill-discovery $request)
   (let* (($capabilities (collapse (match &self
        (registered-capability schema: $s handler: $h priority: $p lifecycle: active metadata: $m)
        ($s $h $p $m))))
          ($formatted (format-skill-set $capabilities)))
         (skill-set skills: $formatted)))
(= (format-skill-set $capabilities) (getSkills))
(= (dispatch-skills $k)
   (let $_ (dispatch (skill-request cycle: $k) $k)
        (first-skill-or-default
          (collapse (match &self
            (dispatch-result invocation-id: $k result: (skill-set skills: $s) handler: $_h) $s)))))
(= (first-skill-or-default $strs)
   (if (== $strs ())
       (getSkills)
       (let $h (car-atom $strs)
            (if (== $h ()) (first-skill-or-default (cdr-atom $strs)) $h))))

;; Dispatch once, then read the three presence facts in the SAME evaluation
;; (writes are visible to subsequent reads within one evaluation). Every bind
;; is a core-form nest or a single ordinary call on a value.
(= (prove-registry-path)
   (let $_ (dispatch (skill-request cycle: 1) 1)
   (let $ss (collapse (match &self
              (dispatch-result invocation-id: 1 result: (skill-set skills: $s) handler: $hd) skillset-present))
   (let $fb (collapse (match &self
              (dispatch-fallback-activated invocation-id: 1 input-atom: $i reason: $r) $r))
   (let $ci (collapse (match &self
              (capability-invoked invocation-id: 1 handler: $h2 input-atom: $i2) $h2))
   (let $nss (size-atom $ss)
   (let $nfb (size-atom $fb)
   (let $nci (size-atom $ci)
        (PROOF skillset: $nss fallback: $nfb capinvoked: $nci who: $ci reason: $fb)))))))))
"""


def sh(cmd, stdin=None):
    p = subprocess.run(["docker", "exec", "-i", CONTAINER, "sh", "-c", cmd],
                       input=stdin, capture_output=True, text=True)
    return p.stdout + p.stderr


def main():
    buf = []

    def say(s):
        print(s)
        buf.append(s)

    say("registry-path-live probe %s" % STAMP)
    skills_src = sh("cat %s" % SKILLS)
    if "getSkills" not in skills_src:
        say("ERROR: could not read getSkills from %s" % SKILLS)
        return
    registry = sh("cat %s" % DRAFT)
    promoted = re.sub(r"\s+".join(re.escape(t) for t in RUNCHAIN_OLD.split()),
                      lambda m: RUNCHAIN_NEW, registry, count=1)

    probe = skills_src + "\n" + promoted + "\n" + SKILL + '\n!("===PROOF===")\n!(prove-registry-path)\n'
    path = "/tmp/_rplprobe_%s.metta" % STAMP
    sh("cat > %s" % path, stdin=probe)
    out = sh("cd /PeTTa && ./run.sh %s 2>&1" % path)
    buf.append("===== RAW =====\n" + out)
    res = out.rsplit("===PROOF===", 1)[-1]

    def num(label):
        m = re.search(label + r":\s*(\d+)", res)
        return int(m.group(1)) if m else None

    skillset = num("skillset")
    fallback = num("fallback")
    capinvoked = num("capinvoked")
    who = re.search(r"who:\s*(\[[^\]]*\]|\([^)]*\))", res)
    reason = re.search(r"reason:\s*(\[[^\]]*\]|\([^)]*\))", res)
    who = who.group(1) if who else "?"
    reason = reason.group(1) if reason else "?"
    err = ("error" in out.lower()) or ("character_code" in out.lower())

    say("skillset-present dispatch-results : %s" % skillset)
    say("dispatch-fallback-activated       : %s   reason=%s" % (fallback, reason))
    say("capability-invoked                : %s   who=%s" % (capinvoked, who))
    say("any error in run                  : %s" % err)
    say("")

    live = (skillset is not None and skillset >= 1 and fallback == 0
            and capinvoked is not None and capinvoked >= 1 and not err)
    fell = (skillset == 0 and fallback is not None and fallback >= 1)
    if live:
        say("VERDICT: REGISTRY PATH LIVE.")
        say("  dispatch fired, skill-discovery handler ran (who=%s), and a skill-set" % who)
        say("  dispatch-result was written. Skills surface THROUGH the registry, not")
        say("  via the getSkills fallback. This is what the count alone could not show.")
    elif fell:
        say("VERDICT: FELL BACK (registry inert).")
        say("  No skill-set dispatch-result; dispatch-fallback-activated fired")
        say("  (reason=%s). Skills come from the getSkills fallback, so the loop" % reason)
        say("  survives but Phase C's registry path is NOT driving content. Investigate")
        say("  the filter pipeline before claiming the registry path live.")
    else:
        say("VERDICT: INCONCLUSIVE -- read RAW. skillset=%s fallback=%s capinvoked=%s"
            % (skillset, fallback, capinvoked))
    sh("cat > %s" % LOG, stdin="\n".join(buf))
    print("\nRaw trace in-container at %s" % LOG)


if __name__ == "__main__":
    main()
