#!/usr/bin/env python3
"""
probe_dispatch_retention.py

Proves the retention design before it touches the registry:

  A0    sweep-dispatch-atoms! on a CLEAN state (every remove-atom matches zero)
        completes WITHOUT error. This is the map's open A0 cell (remove-atom on
        zero match) and it is load-bearing: cycle 1 sweeps before anything is
        written, so if remove-on-zero errors, getContext dies on cycle 1.
  SWEEP after one dispatch writes the transient records, the sweep removes ALL
        of them (count back to zero) -- confirms remove-by-variable clears the
        actual dispatch-* shapes (incl. dispatch-result with a nested-compound
        result), per the map's A1 proven pattern.
  BOUND dispatch, then (sweep + dispatch) again: only ONE cycle's worth of
        dispatch-result remains, not two. Proves the swap bounds accumulation.

Mechanism under test (the exact MeTTa proposed for the registry):
  sweep at the TOP of dispatch, before it writes the new cycle's records.
  Every remove-atom uses a VARIABLE value pattern (clears all ids, any count),
  per map Section 5. Every let bind is a single application on values, per the
  nested-in-bind rule.

USAGE (from repo root, after reverse has restored a clean tree):
  python3 staging/probe_dispatch_retention.py
"""

import datetime
import re
import subprocess

CONTAINER = "clarity_omega"
REPO = "/PeTTa/repos/omegaclaw"
DRAFT = REPO + "/soul/capability_registry_path_c_draft.metta"
SKILLS = REPO + "/src/skills.metta"
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG = "/tmp/probe_dispatch_retention_%s.log" % STAMP

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

# The proposed sweep + the skill_discovery surface. The sweep is what would be
# added to the registry and called at the top of dispatch.
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

;; ---- PROPOSED retention sweep (variable patterns clear all ids/counts) ----
(= (sweep-dispatch-atoms!)
   (let $_a (remove-atom &self (dispatch-invocation invocation-id: $i1 input-atom: $a1))
   (let $_b (remove-atom &self (capability-invoked invocation-id: $i2 handler: $h2 input-atom: $a2))
   (let $_c (remove-atom &self (dispatch-result invocation-id: $i3 result: $r3 handler: $h3))
   (let $_d (remove-atom &self (dispatch-chain-exhausted invocation-id: $i4))
   (let $_e (remove-atom &self (dispatch-chain-anchored invocation-id: $i5 anchor-handler: $h5))
   (let $_f (remove-atom &self (dispatch-fallback-activated invocation-id: $i6 input-atom: $a6 reason: $r6))
        swept))))))) 

;; dispatch-with-sweep = sweep THEN dispatch, the proposed cycle behavior.
(= (dispatch-with-sweep $k)
   (let $_ (sweep-dispatch-atoms!)
        (dispatch (skill-request cycle: $k) $k)))

;; counts (single calls on bound values; collapse/match nest fine in a bind)
(= (count-dispatch-results)
   (let $h (collapse (match &self
            (dispatch-result invocation-id: $i result: (skill-set skills: $s) handler: $hd) present))
        (size-atom $h)))
(= (count-all-dispatch-atoms)
   (let $a (collapse (match &self (dispatch-invocation invocation-id: $i input-atom: $x) di))
   (let $b (collapse (match &self (capability-invoked invocation-id: $i2 handler: $h input-atom: $x2) ci))
   (let $c (collapse (match &self (dispatch-result invocation-id: $i3 result: $r handler: $h3) dr))
   (let $d (collapse (match &self (dispatch-chain-exhausted invocation-id: $i4) ce))
   (let $na (size-atom $a)
   (let $nb (size-atom $b)
   (let $nc (size-atom $c)
   (let $nd (size-atom $d)
        (ALL di: $na ci: $nb dr: $nc ce: $nd))))))))))

;; --- A0: sweep on a CLEAN state (all removes match zero). Must not error. ---
(= (probe-A0)
   (let $_ (sweep-dispatch-atoms!)
        (let $n (count-dispatch-results)
             (A0 swept-clean-ok: yes results-remaining: $n))))
;; --- SWEEP: dispatch once, then sweep, expect zero remaining. ---
(= (probe-sweep)
   (let $_1 (dispatch (skill-request cycle: 1) 1)
        (let $before (count-dispatch-results)
             (let $_2 (sweep-dispatch-atoms!)
                  (let $after (count-dispatch-results)
                       (SWEEP before: $before after: $after))))))
;; --- BOUND: two cycles via dispatch-with-sweep, expect one result, not two. ---
(= (probe-bound)
   (let $_1 (dispatch-with-sweep 1)
        (let $_2 (dispatch-with-sweep 2)
             (let $n (count-dispatch-results)
                  (let $all (count-all-dispatch-atoms)
                       (BOUND results: $n all: $all))))))
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

    say("dispatch-retention probe %s" % STAMP)
    skills_src = sh("cat %s" % SKILLS)
    if "getSkills" not in skills_src:
        say("ERROR: could not read getSkills from %s" % SKILLS)
        return
    registry = sh("cat %s" % DRAFT)
    promoted = re.sub(r"\s+".join(re.escape(t) for t in RUNCHAIN_OLD.split()),
                      lambda m: RUNCHAIN_NEW, registry, count=1)

    # Each probe runs in its OWN fresh run.sh so state does not bleed between phases.
    def run_one(call):
        probe = skills_src + "\n" + promoted + "\n" + SKILL + '\n!("===R===")\n!(%s)\n' % call
        path = "/tmp/_ret_%s_%s.metta" % (call.replace("-", "_"), STAMP)
        sh("cat > %s" % path, stdin=probe)
        out = sh("cd /PeTTa && ./run.sh %s 2>&1" % path)
        return out

    out_a0 = run_one("probe-A0")
    out_sweep = run_one("probe-sweep")
    out_bound = run_one("probe-bound")
    buf.append("===== RAW A0 =====\n" + out_a0)
    buf.append("===== RAW SWEEP =====\n" + out_sweep)
    buf.append("===== RAW BOUND =====\n" + out_bound)

    def errd(o):
        return ("error" in o.lower()) or ("character_code" in o.lower())

    a0_ok = ("swept-clean-ok: yes" in out_a0.rsplit("===R===", 1)[-1]) and not errd(out_a0)
    m_sweep = re.search(r"SWEEP before:\s*(\d+)\s*after:\s*(\d+)", out_sweep)
    sweep_ok = bool(m_sweep) and int(m_sweep.group(1)) >= 1 and int(m_sweep.group(2)) == 0 and not errd(out_sweep)
    m_bound = re.search(r"BOUND results:\s*(\d+)\s*all:\s*\(ALL di:\s*(\d+)\s*ci:\s*(\d+)\s*dr:\s*(\d+)\s*ce:\s*(\d+)\)", out_bound)
    bound_ok = bool(m_bound) and int(m_bound.group(1)) == 1 and not errd(out_bound)

    say("")
    say("A0    sweep on clean state, no error      : %s  (%s)" % (
        "PASS" if a0_ok else "FAIL",
        out_a0.rsplit("===R===", 1)[-1].strip().splitlines()[-1] if "===R===" in out_a0 else "no result"))
    say("SWEEP one dispatch then sweep -> 0 left   : %s  (%s)" % (
        "PASS" if sweep_ok else "FAIL", m_sweep.group(0) if m_sweep else "no SWEEP line"))
    say("BOUND two swept cycles -> exactly 1 result: %s  (%s)" % (
        "PASS" if bound_ok else "FAIL", m_bound.group(0) if m_bound else "no BOUND line"))
    say("")
    if a0_ok and sweep_ok and bound_ok:
        say("VERDICT: ALL PASS. A0 is safe (remove-on-zero no-ops), the sweep clears")
        say("the actual dispatch-* shapes, and the per-cycle swap holds the atomspace")
        say("at one cycle's worth. Safe to fold sweep-dispatch-atoms! into dispatch.")
    else:
        say("VERDICT: NOT ALL PASS. Read the RAW sections; do NOT add the sweep yet.")
        if not a0_ok:
            say("  A0 FAIL is the blocker: remove-on-zero may error. If so, the sweep")
            say("  needs a guard (e.g. presence-check before remove) before it is safe.")
    sh("cat > %s" % LOG, stdin="\n".join(buf))
    print("\nRaw trace in-container at %s" % LOG)


if __name__ == "__main__":
    main()
