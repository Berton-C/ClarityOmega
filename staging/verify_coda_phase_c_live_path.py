#!/usr/bin/env python3
"""
verify_coda_phase_c_live_path.py

Closes the two questions phase_d_coda_inloop_verification.py cannot, because that
harness reads only the log marker, and the companion harness
verify_coda_phase_c_dispatch_result.py only exercises registry mechanics on
synthetic fixtures (not the real skill-discovery capability, not dispatch-skills,
not the sweep).

  LIVE   The DEPLOYED dispatch path actually reaches skill-discovery and writes
         (dispatch-result ... handler: skill-discovery), and writes NO
         (dispatch-fallback-activated ...). This is the live-vs-fallback
         discriminator. The log cannot see it: skills-len 21 is produced
         IDENTICALLY whether dispatch fires (skill-discovery -> getSkills) or
         falls back (first-skill-or-default -> getSkills). Only the companion
         atoms distinguish the two worlds.

  SKILLS The real getContext accessor, (dispatch-skills $k), run end to end,
         returns a non-empty skill-set whose element count should match the live
         loop's skills-len (21 under Option a). Ties this harness to the live
         signal.

  BOUND  Three REAL dispatches (each sweeps at the top of dispatch, as deployed)
         leave exactly ONE cycle's worth of each dispatch-* family, not three.
         Proves the sweep bounds accumulation in the deployed code, which the
         log cannot show (transients are cleared and rewritten each cycle).

WHAT THIS DOES AND DOES NOT PROVE (the honest boundary):
  It exercises the EXACT on-disk files the live container loaded
  (capability_registry.metta, capabilities/skill_discovery.metta, skills.metta)
  in a FRESH AtomSpace per invocation. It does NOT read the live running loop's
  atomspace, which is not externally queryable. The inference from "this code
  path is live-not-fallback" to "the live loop is live-not-fallback" holds
  because the live loop loads these same files and the filtering decision
  depends only on the (eligible-lifecycle active) seed plus runtime observation
  atoms (capability-lifecycle/priority/efficacy-observation), and nothing
  currently writes those observations. If a learning surface that writes them
  lands later, re-run this against the live filtering state.

USAGE (run from repo root):
  python3 staging/verify_coda_phase_c_live_path.py
"""

import datetime
import re
import subprocess

CONTAINER = "clarity_omega"
REPO = "/PeTTa/repos/omegaclaw"
REGISTRY = REPO + "/soul/capability_registry.metta"            # promoted (sweep + dispatch-result wrap)
SKILLDISC = REPO + "/soul/capabilities/skill_discovery.metta"  # real accessor + handler
SKILLS = REPO + "/src/skills.metta"                            # getSkills
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG = "/tmp/verify_coda_phase_c_live_path_%s.log" % STAMP

# Driver: count helpers (collapse/match nest fine in a bind; size-atom returns a
# bare scalar that renders clean per the Atom Operations Map read-instrument
# rule) plus three probes driving the REAL dispatch / dispatch-skills.
DRIVER = r"""
;; ---- discriminating counts (handler pinned to the symbol skill-discovery) ----
(= (count-result-skilldisc)
   (let $h (collapse (match &self
            (dispatch-result invocation-id: $i result: $r handler: skill-discovery) present))
        (size-atom $h)))
(= (count-capinvoked-skilldisc)
   (let $h (collapse (match &self
            (capability-invoked invocation-id: $i handler: skill-discovery input-atom: $a) present))
        (size-atom $h)))
(= (count-fallback)
   (let $h (collapse (match &self
            (dispatch-fallback-activated invocation-id: $i input-atom: $a reason: $rsn) present))
        (size-atom $h)))

;; ---- per-family counts (variable patterns; count all ids) ----
(= (count-fam-di) (let $a (collapse (match &self (dispatch-invocation invocation-id: $i input-atom: $x) di)) (size-atom $a)))
(= (count-fam-ci) (let $a (collapse (match &self (capability-invoked invocation-id: $i handler: $h input-atom: $x) ci)) (size-atom $a)))
(= (count-fam-dr) (let $a (collapse (match &self (dispatch-result invocation-id: $i result: $r handler: $h) dr)) (size-atom $a)))
(= (count-fam-ce) (let $a (collapse (match &self (dispatch-chain-exhausted invocation-id: $i) ce)) (size-atom $a)))
(= (count-fam-an) (let $a (collapse (match &self (dispatch-chain-anchored invocation-id: $i anchor-handler: $h) an)) (size-atom $a)))
(= (count-fam-fb) (let $a (collapse (match &self (dispatch-fallback-activated invocation-id: $i input-atom: $x reason: $r) fb)) (size-atom $a)))

;; ---- LIVE: one real dispatch, then read the discriminating atoms ----
(= (probe-live)
   (let $_ (dispatch (skill-request cycle: 1) 1)
   (let $res (count-result-skilldisc)
   (let $inv (count-capinvoked-skilldisc)
   (let $fb (count-fallback)
        (LIVE result-skilldisc: $res capinvoked-skilldisc: $inv fallback: $fb))))))

;; ---- SKILLS: the real getContext accessor, end to end ----
(= (probe-skills)
   (let $s (dispatch-skills 7)
        (SKILLS len: (size-atom $s))))

;; ---- BOUND: three real dispatches (each sweeps at top), then count families ----
(= (probe-bound)
   (let $_1 (dispatch (skill-request cycle: 1) 1)
   (let $_2 (dispatch (skill-request cycle: 2) 2)
   (let $_3 (dispatch (skill-request cycle: 3) 3)
   (let $di (count-fam-di)
   (let $ci (count-fam-ci)
   (let $dr (count-fam-dr)
   (let $ce (count-fam-ce)
   (let $an (count-fam-an)
   (let $fb (count-fam-fb)
        (BOUND di: $di ci: $ci dr: $dr ce: $ce an: $an fb: $fb)))))))))))
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

    say("verify_coda_phase_c_live_path %s" % STAMP)

    # Read the DEPLOYED files (exactly what the live container loaded).
    skills_src = sh("cat %s" % SKILLS)
    registry_src = sh("cat %s" % REGISTRY)
    skilldisc_src = sh("cat %s" % SKILLDISC)

    # Preflight: confirm we read the deployed artifacts, not stubs.
    pf = []
    if "getSkills" not in skills_src:
        pf.append("getSkills missing from %s" % SKILLS)
    if "sweep-dispatch-atoms!" not in registry_src:
        pf.append("sweep-dispatch-atoms! missing from deployed registry (not promoted?)")
    if "dispatch-result" not in registry_src:
        pf.append("dispatch-result write missing from deployed registry (run-chain not wrapped?)")
    if "dispatch-skills" not in skilldisc_src:
        pf.append("dispatch-skills missing from %s" % SKILLDISC)
    if "(eligible-lifecycle active)" not in skilldisc_src:
        pf.append("eligible-lifecycle seed missing from %s" % SKILLDISC)
    if pf:
        for m in pf:
            say("PREFLIGHT FAIL: " + m)
        say("Aborting: not exercising the deployed surface. Nothing run.")
        sh("cat > %s" % LOG, stdin="\n".join(buf))
        return
    say("preflight OK: deployed registry has sweep + dispatch-result wrap; "
        "skill_discovery has dispatch-skills + eligible-lifecycle seed")

    base = skills_src + "\n" + registry_src + "\n" + skilldisc_src + "\n" + DRIVER + "\n"

    def run_one(call):
        probe = base + '!("===R===")\n!(%s)\n' % call
        path = "/tmp/_vlp_%s_%s.metta" % (call.replace("-", "_"), STAMP)
        sh("cat > %s" % path, stdin=probe)
        return sh("cd /PeTTa && ./run.sh %s 2>&1" % path)

    out_live = run_one("probe-live")
    out_skills = run_one("probe-skills")
    out_bound = run_one("probe-bound")
    buf.append("===== RAW LIVE =====\n" + out_live)
    buf.append("===== RAW SKILLS =====\n" + out_skills)
    buf.append("===== RAW BOUND =====\n" + out_bound)

    # LIVE
    m_live = re.search(
        r"LIVE result-skilldisc:\s*(\d+)\s*capinvoked-skilldisc:\s*(\d+)\s*fallback:\s*(\d+)",
        tail_after_sep(out_live))
    live_ok = (bool(m_live)
               and int(m_live.group(1)) >= 1     # skill-discovery wrote a result
               and int(m_live.group(2)) >= 1     # skill-discovery was actually invoked
               and int(m_live.group(3)) == 0     # no fallback fired
               and not errd(out_live))

    # SKILLS
    m_sk = re.search(r"SKILLS len:\s*(\d+)", tail_after_sep(out_skills))
    sk_len = int(m_sk.group(1)) if m_sk else None
    sk_ok = bool(m_sk) and sk_len > 0 and not errd(out_skills)

    # BOUND
    m_b = re.search(
        r"BOUND di:\s*(\d+)\s*ci:\s*(\d+)\s*dr:\s*(\d+)\s*ce:\s*(\d+)\s*an:\s*(\d+)\s*fb:\s*(\d+)",
        tail_after_sep(out_bound))
    if m_b:
        di, ci, dr, ce, an, fb = (int(m_b.group(i)) for i in range(1, 7))
        bound_ok = (di == 1 and ci == 1 and dr == 1 and ce == 1 and an == 0 and fb == 0
                    and not errd(out_bound))
    else:
        bound_ok = False

    say("")
    say("LIVE   dispatch reaches skill-discovery, no fallback : %s  (%s)" % (
        "PASS" if live_ok else "FAIL", m_live.group(0) if m_live else "no LIVE line"))
    say("SKILLS dispatch-skills returns non-empty skill-set   : %s  (len=%s%s)" % (
        "PASS" if sk_ok else "FAIL", sk_len,
        ", matches live 21" if sk_len == 21 else (", live logs 21" if sk_len is not None else "")))
    say("BOUND  3 dispatches -> 1 cycle's worth per family     : %s  (%s)" % (
        "PASS" if bound_ok else "FAIL", m_b.group(0) if m_b else "no BOUND line"))
    say("")

    if live_ok and sk_ok and bound_ok:
        say("VERDICT: ALL PASS. The DEPLOYED dispatch path is live (skill-discovery")
        say("is invoked and writes the result; no fallback), the real getContext")
        say("accessor returns a non-empty skill-set, and the sweep holds each")
        say("dispatch-* family at one cycle's worth across three dispatches.")
        if sk_len != 21:
            say("NOTE: SKILLS len is %s, not the 21 the live loop logs. Path is live," % sk_len)
            say("      but reconcile the count before treating parity as exact.")
        say("Combined with phase_d (marker every cycle, skills-len stable 21), this")
        say("is firm ground: live-not-fallback and retention-bounded in the deployed")
        say("build. See the honest-boundary note in the header re: runtime observations.")
    else:
        say("VERDICT: NOT ALL PASS. Read the RAW sections below; do NOT commit on this.")
        if not live_ok:
            say("  LIVE FAIL is the blocker: either fallback fired (fallback != 0) or")
            say("  skill-discovery was not invoked. The deployed path is NOT live.")
        if not bound_ok:
            say("  BOUND FAIL: the sweep is not holding families at one cycle's worth.")

    sh("cat > %s" % LOG, stdin="\n".join(buf))
    print("\nRaw trace in-container at %s  (maps to host shared_files/)" % LOG)


if __name__ == "__main__":
    main()
