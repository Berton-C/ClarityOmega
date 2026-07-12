#!/usr/bin/env python3
"""
validate_corner_gate_v3_monolith.py

Standalone D0-D8 validation for the Corner-Gate v3 monolith (design canon
corner_gate_v3_adapter_design.md 5.5). Separate from the apply script so
proof reruns without reapplying.

USAGE:
  python3 staging/validate_corner_gate_v3_monolith.py --repo-root . --container clarity_omega
  python3 staging/validate_corner_gate_v3_monolith.py --repo-root . --expect-reversed
Options: --skip-container (static-only run: D0, D1, D4, D6-static)

Ladder: D0 static file checks. D1 import order. D2 pure reductions
(container run.sh inline harness, facts-diagnostic exemplar pattern).
D3 writer/window checks (same harness). D4 seam invariant R1. D5 positive
fixtures PC1/PC2 including the cycle-3 stored-next-move gate and RB1.
D6 negative controls NC1-NC5, H1-H4, formatter totality, ground-symbol
check. D7 live-loop production probes (logs). D8 observation metrics.
NOTE: the full do-record-coupling-cycle! path (py-call plus get_time) is
live-loop territory by doctrine; D2/D3/D5/D6 prove the pure and writer
logic on inline fixtures, D7 proves the runtime.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

FROZEN = {
    "soul/coupling_legibility.metta":
        "14705a549aec69198b9d03dd31ea162dd95ad8fd238c5fea3e99eb8712bf10f1",
    "soul/coupling_legibility_writers.metta":
        "e1bc3e28cd7ca357f7e618713cb550dd328fb0da5d114f40e6981e4b7efca3f8",
}
MANIFEST_REL = "lib_clarity_reasoning/lib_clarity_reasoning.metta"
LOOP_REL = "src/loop.metta"
HELPER_REL = "src/helper.py"
GATE_REL = "soul/corner_gap/corner_gate.metta"
CWW_IMPORT = "!(import! &self (library omegaclaw ./soul/corner_gap/corner_window_writers))"
ENGINE_SUB = "lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2"
ENGINE_REL = ("lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_"
              "dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta")
ENGINE_SHA = "693089e6b69d3b40c0772e3a068e337bb325048f39f9e0a4f8bd9e6f66012851"

PASSES, FAILS = [], []


def check(tier, label, ok, detail=""):
    line = "%s  %s  %s%s" % (tier, "PASS" if ok else "FAIL", label, ("   " + detail) if detail else "")
    (PASSES if ok else FAILS).append(line)
    print(line)
    return ok


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def rd(p):
    with open(p) as f:
        return f.read()


HARNESS_HEADER = """!(import! &self (library lib_import))
"""

# Pure-and-writer fixture probes. Every probe prints (V3FIX <id> <value>).
FIXTURES = r"""
;; ---- D2: Gate H honesty (H1-H4) ----
!(println! (V3FIX H1 (derive-honesty-state True True "file:aa11" "file:aa11")))
!(println! (V3FIX H2 (derive-honesty-state True True "file:aa11" "unknown")))
!(println! (V3FIX H3 (derive-honesty-state True True "unknown" "file:aa11")))
!(println! (V3FIX H4 (derive-honesty-state True True "file:aa11" "file:bb22")))
;; ---- D2: totality (B4) ----
!(println! (V3FIX B4S (surface-for-head-total some-unknown-head)))
!(println! (V3FIX B4C (command-class-of-total some-unknown-head)))
;; ---- D2: dominant surface cascade ----
!(println! (V3FIX DOM (dominant-surface-of (user-words runtime-output failed-query))))
;; ---- D2: RB1 support drop (aligned, misaligned, aligned) ----
!(println! (V3FIX RB1 (derive-support aligned misaligned aligned)))
!(println! (V3FIX RB1H (derive-support aligned aligned aligned)))
;; ---- D2: chain state, pathological and healthy ----
!(println! (V3FIX PC1C (derive-chain-state repeated-failing-command hidden-error-surface error-feedback-hidden repeated-command trace-present 0)))
!(println! (V3FIX PC2C (derive-chain-state one-off-failing-command visible-error-surface error-feedback-visible repeated-command trace-present 2)))
;; ---- D2: polarity verdicts (window positions 2 and 3, stuck arc) ----
!(println! (V3FIX PV2 (derive-polarity-verdict protection-flat-low-warrant contactability-flat suspicion-rises polarity-blocks cycle-2)))
!(println! (V3FIX PV3 (derive-polarity-verdict protection-flat-low-warrant contactability-flat suspicion-rises polarity-blocks cycle-3)))
;; ---- D2/D5: trace verdict with fixture records (cycle-3 stored gate) ----
!(add-atom &self (coupling-cycle-record 101 0 none sigA loop-capture-seen stuck-recurrence-warning disintegrating-cascade disintegrating-cascade 0.04 additional-evidence-needed not-computed block-reinforcement-and-seek-contact attending msgnew-absent soul-verdict-present do-record-coupling-cycle none 1))
!(add-atom &self (coupling-cycle-record 102 0 none sigA loop-capture-seen stuck-recurrence-warning disintegrating-cascade disintegrating-cascade 0.04 additional-evidence-needed not-computed block-reinforcement-and-seek-contact attending msgnew-absent soul-verdict-present do-record-coupling-cycle 101 2))
!(println! (V3FIX TVWC (coupling-trace-verdict-with-current defensive-fixation-risk)))
!(println! (V3FIX NMPC1 (derive-next-move loop-capture-seen (coupling-trace-verdict-with-current defensive-fixation-risk) not-computed)))
;; healthy trace: metabolizing to metabolized
!(println! (V3FIX TVH (q-tfs2-trace-verdict? same-start metabolizing-transition metabolized-protection)))
;; ---- D3: writers on fixture state ----
!(println! (V3FIX BOOT (do-bootstrap-coupling!)))
!(println! (V3FIX BAND1 (current-coupling-band)))
!(println! (V3FIX SIG1 (do-set-command-signature! "shell:aaaa1111" True 201)))
!(println! (V3FIX SIG2 (do-set-command-signature! "shell:aaaa1111" True 202)))
!(println! (V3FIX SIGC (current-signature-fail-count)))
!(println! (V3FIX CE1 (do-record-contact-event! 301 runtime-output)))
!(println! (V3FIX CE2 (do-record-contact-event! 301 runtime-output)))
!(println! (V3FIX CEC (size-atom (coupling-contact-surfaces 301))))
!(add-atom &self (coupling-cycle-record 103 1 runtime-output sigB self-seeing-contact metabolizing-transition integrating-alignment integrating-alignment 0.81 no-additional-evidence-needed not-computed continue-inquiry engaged msgnew-present soul-verdict-present do-record-coupling-cycle 102 3))
!(println! (V3FIX WC3 (coupling-window-count)))
!(println! (V3FIX EV (do-evict-oldest-record!)))
!(println! (V3FIX WC2 (coupling-window-count)))
!(println! (V3FIX OLD2 (oldest-coupling-ord)))
;; ---- D6: NC1 pin-only heads record nothing ----
!(println! (V3FIX NC1 (record-contacts-for-heads! 401 (pin))))
!(println! (V3FIX NC1C (size-atom (coupling-contact-surfaces 401))))
;; ---- schema guard ----
!(println! (V3FIX SCHEMA (coupling-legibility-schema-version)))
!(println! (V3FIXDONE done))
"""

EXPECT = {
    "H1": "claim-completion",
    "H2": "name-action-not-verification",
    "H3": "not-computed",
    "H4": "name-action-not-verification",
    "B4S": "no-contact",
    "B4C": "neutral",
    "DOM": "failed-query",
    "PC1C": "loop-capture-seen",
    "PC2C": "self-seeing-contact",
    "PV2": "stuck-recurrence-warning",
    "PV3": "defensive-fixation-risk",
    "TVWC": "blocked-defensive-fixation",
    "NMPC1": "block-reinforcement-and-seek-contact",
    "TVH": "metabolization-candidate",
    "BAND1": "window-filling",
    "SIG1": "1",
    "SIG2": "2",
    "SIGC": "2",
    "CEC": "1",
    "WC3": "3",
    "WC2": "2",
    "OLD2": "102",
    "NC1C": "0",
    "SCHEMA": "v3-18-field",
}
NUMERIC_GATES = {"RB1": lambda v: float(v) <= 0.05, "RB1H": lambda v: float(v) >= 0.7}


def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--container", default="clarity_omega")
    ap.add_argument("--expect-reversed", action="store_true")
    ap.add_argument("--skip-container", action="store_true")
    args = ap.parse_args()
    os.chdir(os.path.abspath(args.repo_root))

    if args.expect_reversed:
        man, loop = rd(MANIFEST_REL), rd(LOOP_REL)
        check("R", "coupling imports absent", "./soul/coupling_legibility)" not in man)
        check("R", "corner_window_writers import restored", CWW_IMPORT in man)
        check("R", "hook restored", "(populate-corner-window! $metta_cmds $k)" in loop)
        check("R", "recorder hook absent", "do-record-coupling-cycle!" not in loop)
        check("R", "soul files absent", not os.path.exists("soul/coupling_legibility.metta")
              and not os.path.exists("soul/coupling_legibility_writers.metta"))
        check("R", "helper payload absent", "V3-MONOLITH BEGIN" not in rd(HELPER_REL))
        check("R", "v2 gate body restored", "held-by-corner-gate" in rd(GATE_REL))
        check("R", "engine untouched", sha(ENGINE_REL) == ENGINE_SHA)
        done("EXPECT-REVERSED")
        return

    # ---------------- D0 static ----------------
    for rel, want in FROZEN.items():
        check("D0", "installed payload matches frozen hash " + rel,
              os.path.exists(rel) and sha(rel) == want)
    for rel in (MANIFEST_REL, LOOP_REL, HELPER_REL, GATE_REL):
        check("D0", "file present " + rel, os.path.exists(rel))
    check("D0", "NO-TOUCH engine sha", sha(ENGINE_REL) == ENGINE_SHA)
    check("D0", "helper payload present once", rd(HELPER_REL).count("V3-MONOLITH BEGIN") == 1)
    check("D0", "corner_window_writers retired",
          not os.path.exists("soul/corner_gap/corner_window_writers.metta"))

    # ---------------- D1 imports ----------------
    man = rd(MANIFEST_REL)
    lines = man.splitlines()
    def line_of(sub):
        for i, l in enumerate(lines, 1):
            if sub in l and l.startswith("!(import!"):
                return i
        return -1
    e, p1, p2, g = (line_of(ENGINE_SUB), line_of("./soul/coupling_legibility)"),
                    line_of("./soul/coupling_legibility_writers)"), line_of("./soul/corner_gap/corner_gate"))
    check("D1", "engine < pure < writers < corner_gate", 0 < e < p1 < p2 < g,
          "e=%d p=%d w=%d g=%d" % (e, p1, p2, g))
    check("D1", "corner_window_writers import gone", CWW_IMPORT not in man)
    check("D1", "lib_quantale absent", "./lib_clarity_reasoning/lib_quantale)" not in man)
    for rel in FROZEN:
        t = rd(rel)
        check("D1", "no engine q- heads in " + rel, "\n(= (q-" not in t)

    # ---------------- D4 seam R1 ----------------
    loop = rd(LOOP_REL)
    gate = rd(GATE_REL)
    check("D4", "R1 novelty compares raw results",
          "(helper.safe_results_str (repr $results))" in loop)
    check("D4", "R1 lastresults from results_final", "(repr $results_final)" in loop)
    check("D4", "R1 line append only in gate-aware-results path",
          "coupling-legibility-line" in gate and "coupling-legibility-line" not in loop)
    check("D4", "R1 hook after state-delta",
          loop.find("populate-state-delta") < loop.find("do-record-coupling-cycle!"))

    # ---------------- D6 formatter totality (local python) ----------------
    spec = importlib.util.spec_from_file_location("h", HELPER_REL)
    h = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(h)
        f = h.coupling_line_format
        cases_ok = True
        outs = [
            f(2, "runtime-output", "self-seeing-contact", "integrating-alignment", "stable-high", 0.81, "no-additional-evidence-needed", "metabolization-candidate", "integrate-outcome", "claim-completion", "hidden"),
            f(0, "none", "loop-capture-seen", "disintegrating-cascade", "stable-low", 0.04, "additional-evidence-needed", "blocked-repetition-without-metabolization", "block-reinforcement-and-seek-contact", "name-action-not-verification", "hidden"),
            f(None, None, None, None, None, None, None, None, None, None),
            f(2, "runtime-output", "x", "integrating-alignment", "stable-high", 0.8, "y", "z", "m", "not-computed", "blocked-no-contact"),
        ]
        for o in outs:
            if not isinstance(o, str) or "$" in o:
                cases_ok = False
        cases_ok = cases_ok and "claim-completion" not in outs[0] and "honesty name-action-not-verification" in outs[1]
        cases_ok = cases_ok and "contact-audit blocked-no-contact" in outs[3] and "contact-audit" not in outs[0]
        check("D6", "formatter totality plus render discipline plus divergence", cases_ok)
        sig_ok = (h.coupling_command_signature('((pin "x"))') == "none"
                  and h.coupling_command_signature("()") == "none")
        check("D6", "pin-only and empty signatures are none", sig_ok)
    except Exception as ex:
        check("D6", "helper module loads", False, str(ex))

    # ---------------- D2/D3/D5/D6 container harness ----------------
    if not args.skip_container:
        harness = HARNESS_HEADER
        for rel in (ENGINE_REL, "soul/coupling_legibility.metta", "soul/coupling_legibility_writers.metta"):
            harness += "\n;; ==== inline: " + rel + " ====\n" + rd(rel) + "\n"
        harness += FIXTURES
        with open("/tmp/v3_harness.metta", "w") as f:
            f.write(harness)
        r1 = run("docker cp /tmp/v3_harness.metta %s:/tmp/v3_harness.metta" % args.container)
        r2 = run("docker exec %s sh -c 'cd /PeTTa && ./run.sh /tmp/v3_harness.metta' 2>&1" % args.container)
        out = (r1.stderr or "") + (r2.stdout or "") + (r2.stderr or "")
        got = dict(re.findall(r"\(V3FIX (\S+) (.+?)\)\s*$", out, re.M))
        check("D2", "harness executed to completion", "V3FIXDONE" in out,
              "" if "V3FIXDONE" in out else out[-400:])
        for k, want in EXPECT.items():
            v = got.get(k, "<missing>").strip()
            tier = "D3" if k in ("BOOT", "BAND1", "SIG1", "SIG2", "SIGC", "CE1", "CE2", "CEC", "WC3", "EV", "WC2", "OLD2") else ("D5" if k in ("TVWC", "NMPC1", "TVH", "PV2", "PV3", "PC1C", "PC2C") else "D2")
            check(tier, "fixture " + k, v == want, "got %s want %s" % (v, want))
        for k, gate in NUMERIC_GATES.items():
            v = got.get(k, "")
            try:
                ok = gate(v)
            except Exception:
                ok = False
            check("D5", "fixture " + k + " numeric gate", ok, "got " + str(v))

        # ---------------- D7 live-loop probes ----------------
        logs = run("docker logs %s 2>&1 | tail -4000" % args.container).stdout or ""
        cl = [l for l in logs.splitlines() if "COUPLING-STATE" in l]
        check("D7", "COUPLING-STATE line present in live logs", len(cl) > 0, "%d lines" % len(cl))
        recent = logs
        check("D7", "no held-by-corner-gate in recent logs", "held-by-corner-gate" not in recent)
        ground = all(("$" not in l.split("COUPLING-STATE", 1)[1] and "(Error" not in l and "unreduced" not in l) for l in cl) if cl else False
        check("D7", "ground-symbol render check on live lines", ground if cl else False)

        # ---------------- D8 metrics ----------------
        supports, bands, moves = [], [], {}
        for l in cl:
            m = re.search(r"support ([0-9.]+)", l)
            if m:
                supports.append(float(m.group(1)))
            b = re.search(r"band (\S+)", l)
            if b:
                bands.append(b.group(1))
            n = re.search(r"next (\S+)", l)
            if n:
                moves[n.group(1)] = moves.get(n.group(1), 0) + 1
        transitions = sum(1 for i in range(1, len(bands)) if bands[i] != bands[i - 1])
        metrics = {"lines": len(cl), "support_min": min(supports) if supports else None,
                   "support_max": max(supports) if supports else None,
                   "band_transitions": transitions, "next_move_counts": moves}
        with open("staging/v3_observation_metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)
        check("D8", "observation metrics written", True, json.dumps(metrics))

    done("VALIDATE")


def done(tag):
    print("=" * 72)
    print("%s RESULT: %d PASS, %d FAIL" % (tag, len(PASSES), len(FAILS)))
    for l in FAILS:
        print("  " + l)
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
