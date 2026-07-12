#!/usr/bin/env python3
"""
validate_corner_gate_v3_monolith.py

Standalone validation for the Corner-Gate v3 monolith. Separate from the
apply script so proof reruns without reapplying.

USAGE:
  python3 staging/validate_corner_gate_v3_monolith.py --repo-root . --container clarity_omega
  python3 staging/validate_corner_gate_v3_monolith.py --repo-root . --expect-reversed
Options: --skip-container   static plus local-python only (D0, D1, D4, D6-local)
         --expected-engine-sha <sha>   override the pin (mock/self-test only)

WHAT ACTUALLY EXECUTES (claims equal proofs):
D0 static: installed MeTTa payload hashes vs frozen; installed marked helper
   body hash vs frozen (B2); engine pinned identity; retired file absent.
D1 imports: engine < pure < writers < corner_gate; corner_window_writers
   import gone; lib_quantale absent; no engine q- heads in payloads.
D4 seam R1 static: novelty raw, lastresults from results_final, line append
   only in the gate shim, recorder hook after state-delta.
D6-local (python, installed module): formatter totality, render discipline,
   divergence formatting, pin-only and empty signatures, target-extraction
   bases H1E/H4E/shell-unknown.
Container harness: D2 pure reductions (H1-H4, totality, dominant surface,
   RB1 numeric gates, NC2 verbatim engine reduction, MeTTa divergence
   decision, schema guard); D3 writer mechanics (bootstrap, idempotent
   contact events, window reset); D5 recorder-core scenarios with injected
   inputs, reading the STORED records (PC1 pathological with hidden-failure
   incrementing and the cycle-3 STORED next-move gate, PC2 healthy with
   support and accord gates, query+metta surface count, shell contact-credit
   and shell honesty, live MeTTa composer reduction); D6-metta negative
   controls (NC1 empty-cycle core, NC3 chain probe, NC4 nothing-fabricated
   on the stored empty-cycle record, NC5 via the healthy composer line).
D7 live-loop probes bounded to the CURRENT container boot via docker
   inspect StartedAt and docker logs --since (M2). D8 metrics from the same
   bounded window.
NOT covered here by design: S1A/S1B behavioral seam fixtures require live
   state-delta interplay and are observed during the 200-cycle window (the
   static R1 seam proof runs above).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

FROZEN_INSTALLED = {
    "soul/coupling_legibility.metta":
        "14705a549aec69198b9d03dd31ea162dd95ad8fd238c5fea3e99eb8712bf10f1",
    "soul/coupling_legibility_writers.metta":
        "c3df6c388b95784304465a3e2bddb25abda53c497344a0db89057029f6817537",
}
FROZEN_HELPER = "de3183e1f3504e2201d6ef80ec6e6650534b80d491e4df7efa38a099f1e87e54"
MANIFEST_REL = "lib_clarity_reasoning/lib_clarity_reasoning.metta"
LOOP_REL = "src/loop.metta"
HELPER_REL = "src/helper.py"
GATE_REL = "soul/corner_gap/corner_gate.metta"
CWW_IMPORT = "!(import! &self (library omegaclaw ./soul/corner_gap/corner_window_writers))"
ENGINE_SUB = "lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2"
ENGINE_REL = ("lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_"
              "dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta")
ENGINE_SHA_PIN = "693089e6b69d3b40c0772e3a068e337bb325048f39f9e0a4f8bd9e6f66012851"
PY_MARK_B = "# V3-MONOLITH BEGIN coupling_legibility helper payload"
PY_MARK_E = "# V3-MONOLITH END coupling_legibility helper payload"

PASSES, FAILS = [], []


def check(tier, label, ok, detail=""):
    line = "%s  %s  %s%s" % (tier, "PASS" if ok else "FAIL", label,
                             ("   " + detail) if detail else "")
    (PASSES if ok else FAILS).append(line)
    print(line)
    return ok


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def rd(p):
    with open(p) as f:
        return f.read()


def installed_helper_body_hash(helper_text):
    try:
        body = helper_text.split(PY_MARK_B, 1)[1].split(PY_MARK_E, 1)[0]
        return hashlib.sha256((body.strip("\n") + "\n").encode("utf-8")).hexdigest()
    except Exception:
        return "extract-failed"


def drun(argv):
    """Gated subprocess (M4): argument arrays, no shell; callers check rc."""
    return subprocess.run(argv, capture_output=True, text=True)


HARNESS_HEADER = "!(import! &self (library lib_import))\n"

FIXTURES = r"""
;; ================= D2 pure reductions =================
!(println! (V3FIX H1 (derive-honesty-state True True "file:aa11" "file:aa11")))
!(println! (V3FIX H2 (derive-honesty-state True True "file:aa11" "unknown")))
!(println! (V3FIX H3 (derive-honesty-state True True "unknown" "file:aa11")))
!(println! (V3FIX H4 (derive-honesty-state True True "file:aa11" "file:bb22")))
!(println! (V3FIX B4S (surface-for-head-total some-unknown-head)))
!(println! (V3FIX B4C (command-class-of-total some-unknown-head)))
!(println! (V3FIX DOM (dominant-surface-of (user-words runtime-output failed-query))))
!(println! (V3FIX RB1 (derive-support aligned misaligned aligned)))
!(println! (V3FIX RB1H (derive-support aligned aligned aligned)))
!(println! (V3FIX SCHEMA (coupling-legibility-schema-version)))
!(println! (V3FIX NC2 (q-llm-narration-alone-self-seeing? llm-says-i-learned no-trace no-orientation-shift)))
!(println! (V3FIX DIVY (coupling-contact-audit-render integrating-alignment blocked-no-contact)))
!(println! (V3FIX DIVN (coupling-contact-audit-render integrating-alignment integrating-alignment)))
;; ================= D3 writer mechanics =================
!(println! (V3FIX BOOT (do-bootstrap-coupling!)))
!(println! (V3FIX BAND1 (current-coupling-band)))
!(println! (V3FIX CE1 (do-record-contact-event! 301 runtime-output)))
!(println! (V3FIX CE2 (do-record-contact-event! 301 runtime-output)))
!(println! (V3FIX CEC (size-atom (coupling-contact-surfaces 301))))
;; ================= D5 recorder-core: PC1 pathological =================
!(println! (V3FIX PC1A (do-record-coupling-cycle-core! 501 False False "shell:deadbeef" "unknown" "unknown" (shell) none engaged 11)))
!(println! (V3FIX PC1B (do-record-coupling-cycle-core! 502 False False "shell:deadbeef" "unknown" "unknown" (shell) none engaged 12)))
!(println! (V3FIX PC1C (do-record-coupling-cycle-core! 503 False False "shell:deadbeef" "unknown" "unknown" (shell) none engaged 13)))
!(println! (V3FIX PC1FAIL (current-signature-fail-count)))
!(println! (V3FIX PC1CHAIN (latest-coupling-chain-state)))
!(println! (V3FIX PC1PV (latest-coupling-polarity-verdict)))
!(println! (V3FIX PC1NM (latest-coupling-next-move)))
!(println! (V3FIX PC1HON (latest-coupling-honesty)))
!(println! (V3FIX PC1CC (latest-coupling-contact-count)))
;; ================= reset between scenarios =================
!(remove-atom &self (coupling-cycle-record $o $a $b $c $d $e $f $f2 $g $h $i $j $k $l $m $n $p $q))
!(println! (V3FIX RESET (coupling-window-count)))
!(println! (V3FIX SIGR (do-set-command-signature! "none" False 0)))
;; ================= D5 recorder-core: PC2 healthy =================
!(println! (V3FIX PC2A (do-record-coupling-cycle-core! 601 True False "read-file:aaaa1111" "unknown" "file:aa11" (read-file) forward attending 21)))
!(println! (V3FIX PC2B (do-record-coupling-cycle-core! 602 False False "query:bbbb2222" "unknown" "atom-query:bb22" (query) forward engaged 22)))
!(println! (V3FIX PC2G (do-record-coupling-cycle-core! 603 False False "technical-analysis:cccc3333" "unknown" "unknown" (technical-analysis) forward engaged 23)))
!(println! (V3FIX PC2CHAIN (latest-coupling-chain-state)))
!(println! (V3FIX PC2NM (latest-coupling-next-move)))
!(println! (V3FIX PC2HON (latest-coupling-honesty)))
!(println! (V3FIX PC2SUP (latest-coupling-support)))
!(println! (V3FIX PC2TA (latest-coupling-task-accord)))
;; NC5 plus ruling item 8: live MeTTa composer reduction on the healthy window.
!(println! (V3FIX LINE (coupling-legibility-line)))
;; ================= D6 recorder-core negative controls =================
!(remove-atom &self (coupling-cycle-record $o2 $a2 $b2 $c2 $d2 $e2 $f3 $f4 $g2 $h2 $i2 $j2 $k2 $l2 $m2 $n2 $p2 $q2))
!(println! (V3FIX SIGR2 (do-set-command-signature! "none" False 0)))
!(println! (V3FIX NC1R (do-record-coupling-cycle-core! 701 False False "none" "unknown" "unknown" () none attending 31)))
!(println! (V3FIX NC1CC (latest-coupling-contact-count)))
!(println! (V3FIX NC1CH (latest-coupling-chain-state)))
!(println! (V3FIX NC4HON (latest-coupling-honesty)))
!(println! (V3FIX NC4SIG (current-signature-fail-count)))
!(println! (V3FIX NC3 (derive-chain-state repeated-failing-command hidden-error-surface error-feedback-hidden repeated-command trace-present 0)))
;; B2 surface fixture (ruling item 7): query plus metta in one batch.
!(remove-atom &self (coupling-cycle-record $o3 $a3 $b3 $c3 $d3 $e3 $f5 $f6 $g3 $h3 $i3 $j3 $k3 $l3 $m3 $n3 $p3 $q3))
!(println! (V3FIX QMR (do-record-coupling-cycle-core! 801 False False "query:dddd4444" "unknown" "atom-query:dd44" (query metta) forward engaged 41)))
!(println! (V3FIX QMCC (latest-coupling-contact-count)))
!(println! (V3FIX QMDS (latest-coupling-dominant-surface)))
!(println! (V3FIXDONE done))
"""

EXPECT = {
    "H1": "claim-completion", "H2": "name-action-not-verification",
    "H3": "not-computed", "H4": "name-action-not-verification",
    "B4S": "no-contact", "B4C": "neutral", "DOM": "failed-query",
    "SCHEMA": "v3-18-field",
    "NC2": "blocked-narration-only",
    "DIVY": "blocked-no-contact", "DIVN": "hidden",
    "BOOT": "bootstrap-coupling-done",
    "BAND1": "window-filling",
    "CE1": "runtime-output", "CE2": "runtime-output", "CEC": "1",
    "PC1A": "record-coupling-cycle-done", "PC1B": "record-coupling-cycle-done",
    "PC1C": "record-coupling-cycle-done",
    "PC1FAIL": "3", "PC1CHAIN": "loop-capture-seen",
    "PC1PV": "defensive-fixation-risk",
    "PC1NM": "block-reinforcement-and-seek-contact",
    "PC1HON": "not-computed", "PC1CC": "1",
    "RESET": "0", "SIGR": "0", "SIGR2": "0",
    "PC2A": "record-coupling-cycle-done", "PC2B": "record-coupling-cycle-done",
    "PC2G": "record-coupling-cycle-done",
    "PC2CHAIN": "self-seeing-contact", "PC2HON": "not-computed",
    "NC1R": "record-coupling-cycle-done",
    "NC1CC": "0", "NC1CH": "blocked-no-contact",
    "NC4HON": "not-computed", "NC4SIG": "0",
    "NC3": "loop-capture-seen",
    "QMR": "record-coupling-cycle-done",
    "QMCC": "1", "QMDS": "runtime-output",
}
EXPECT_SET = {
    "PC2NM": ("continue-inquiry", "preserve-learning-trace"),
    "PC2TA": ("integrating-alignment",),
}
NUMERIC = {"RB1": lambda v: float(v) <= 0.05,
           "RB1H": lambda v: float(v) >= 0.7,
           "PC2SUP": lambda v: float(v) >= 0.7}
D3IDS = ("BOOT", "BAND1", "CE1", "CE2", "CEC", "RESET", "SIGR", "SIGR2")
D5IDS = ("PC1A", "PC1B", "PC1C", "PC1FAIL", "PC1CHAIN", "PC1PV", "PC1NM",
         "PC1HON", "PC1CC", "PC2A", "PC2B", "PC2G", "PC2CHAIN", "PC2HON",
         "QMR", "QMCC", "QMDS")
D6IDS = ("NC1R", "NC1CC", "NC1CH", "NC4HON", "NC4SIG", "NC3", "NC2",
         "DIVY", "DIVN")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--container", default="clarity_omega")
    ap.add_argument("--expect-reversed", action="store_true")
    ap.add_argument("--skip-container", action="store_true")
    ap.add_argument("--expected-engine-sha", default=None)
    args = ap.parse_args()
    os.chdir(os.path.abspath(args.repo_root))
    pin = args.expected_engine_sha or ENGINE_SHA_PIN

    if args.expect_reversed:
        man, loop = rd(MANIFEST_REL), rd(LOOP_REL)
        check("R", "coupling imports absent", "./soul/coupling_legibility)" not in man)
        check("R", "corner_window_writers import restored", CWW_IMPORT in man)
        check("R", "hook restored", "(populate-corner-window! $metta_cmds $k)" in loop)
        check("R", "recorder hook absent", "do-record-coupling-cycle!" not in loop)
        check("R", "soul files absent",
              not os.path.exists("soul/coupling_legibility.metta")
              and not os.path.exists("soul/coupling_legibility_writers.metta"))
        check("R", "helper payload absent", PY_MARK_B not in rd(HELPER_REL))
        check("R", "v2 gate body restored", "held-by-corner-gate" in rd(GATE_REL))
        check("R", "engine pinned identity", sha(ENGINE_REL) == pin)
        done("EXPECT-REVERSED")
        return

    # ---------------- D0 ----------------
    for rel, want in FROZEN_INSTALLED.items():
        check("D0", "installed payload matches frozen hash " + rel,
              os.path.exists(rel) and sha(rel) == want)
    check("D0", "engine pinned identity (substrate)", sha(ENGINE_REL) == pin)
    check("D0", "installed marked helper body equals frozen payload (B2)",
          installed_helper_body_hash(rd(HELPER_REL)) == FROZEN_HELPER)
    check("D0", "corner_window_writers retired",
          not os.path.exists("soul/corner_gap/corner_window_writers.metta"))

    # ---------------- D1 ----------------
    man = rd(MANIFEST_REL)
    lines = man.splitlines()

    def line_of(sub):
        for i, l in enumerate(lines, 1):
            if sub in l and l.startswith("!(import!"):
                return i
        return -1
    e = line_of(ENGINE_SUB)
    p1 = line_of("./soul/coupling_legibility)")
    p2 = line_of("./soul/coupling_legibility_writers)")
    g = line_of("./soul/corner_gap/corner_gate")
    check("D1", "engine < pure < writers < corner_gate", 0 < e < p1 < p2 < g,
          "e=%d p=%d w=%d g=%d" % (e, p1, p2, g))
    check("D1", "corner_window_writers import gone", CWW_IMPORT not in man)
    check("D1", "lib_quantale absent", "./lib_clarity_reasoning/lib_quantale)" not in man)
    for rel in FROZEN_INSTALLED:
        check("D1", "no engine q- heads in " + rel, "\n(= (q-" not in rd(rel))

    # ---------------- D4 seam R1 ----------------
    loop = rd(LOOP_REL)
    gate = rd(GATE_REL)
    check("D4", "R1 novelty compares raw results",
          "(helper.safe_results_str (repr $results))" in loop)
    check("D4", "R1 lastresults from results_final", "(repr $results_final)" in loop)
    check("D4", "R1 line append only in gate shim",
          "coupling-legibility-line" in gate and "coupling-legibility-line" not in loop)
    check("D4", "R1 recorder hook after state-delta",
          loop.find("populate-state-delta") < loop.find("do-record-coupling-cycle!"))

    # ---------------- D6-local: installed helper module ----------------
    spec = importlib.util.spec_from_file_location("h", HELPER_REL)
    h = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(h)
        f = h.coupling_line_format
        outs = [
            f(2, "runtime-output", "self-seeing-contact", "integrating-alignment",
              "stable-high", 0.81, "no-additional-evidence-needed",
              "metabolization-candidate", "integrate-outcome", "claim-completion", "hidden"),
            f(0, "none", "loop-capture-seen", "disintegrating-cascade", "stable-low",
              0.04, "additional-evidence-needed",
              "blocked-repetition-without-metabolization",
              "block-reinforcement-and-seek-contact",
              "name-action-not-verification", "hidden"),
            f(None, None, None, None, None, None, None, None, None, None),
            f(2, "runtime-output", "x", "integrating-alignment", "stable-high", 0.8,
              "y", "z", "m", "not-computed", "blocked-no-contact"),
            f(1, "x" * 100, "$leak", "ok", "ok", "abc", "ok", "ok", "ok",
              "claim-completion", "hidden"),
        ]
        check("D6", "formatter returns strings, no $ leakage",
              all(isinstance(o, str) and "$" not in o for o in outs))
        check("D6", "render discipline: claim-completion hidden, non-healthy honesty shown",
              "claim-completion" not in outs[0]
              and "honesty name-action-not-verification" in outs[1])
        check("D6", "divergence formatting: contact-audit only when passed a real symbol",
              "contact-audit blocked-no-contact" in outs[3]
              and "contact-audit" not in outs[0])
        check("D6", "pin-only and empty signatures are none",
              h.coupling_command_signature('((pin "x"))') == "none"
              and h.coupling_command_signature("()") == "none")
        wcmd = '((write-file "/PeTTa/soul/f.md" "body") (send "done"))'
        at = h.coupling_action_target(wcmd)
        check("D6", "H1E same-target extraction equality",
              at != "unknown"
              and at == h.coupling_verify_target('((read-file "/PeTTa/soul/f.md"))'))
        check("D6", "H4E different-target extraction inequality",
              at != h.coupling_verify_target('((read-file "/PeTTa/soul/OTHER.md"))'))
        check("D6", "shell action target unknown (no false accusations)",
              h.coupling_action_target('((shell "rm x") (send "done"))') == "unknown")
    except Exception as ex:
        check("D6", "installed helper module loads", False, str(ex))

    # ---------------- container ladder ----------------
    if not args.skip_container:
        harness = HARNESS_HEADER
        for rel in (ENGINE_REL, "soul/coupling_legibility.metta",
                    "soul/coupling_legibility_writers.metta"):
            harness += "\n;; ==== inline: " + rel + " ====\n" + rd(rel) + "\n"
        harness += FIXTURES
        with open("/tmp/v3_harness.metta", "w") as f:
            f.write(harness)
        r1 = drun(["docker", "cp", "/tmp/v3_harness.metta",
                   args.container + ":/tmp/v3_harness.metta"])
        check("D2", "docker cp harness rc==0", r1.returncode == 0,
              (r1.stderr or "").strip()[:200])
        r2 = drun(["docker", "exec", args.container, "sh", "-c",
                   "cd /PeTTa && ./run.sh /tmp/v3_harness.metta 2>&1"])
        check("D2", "docker exec harness rc==0", r2.returncode == 0,
              (r2.stderr or "")[:200])
        out = (r2.stdout or "") + (r2.stderr or "")
        got = dict(re.findall(r"\(V3FIX (\S+) (.+?)\)\s*$", out, re.M))
        check("D2", "harness executed to completion", "V3FIXDONE" in out,
              "" if "V3FIXDONE" in out else out[-400:])
        for k, want in EXPECT.items():
            v = got.get(k, "<missing>").strip()
            tier = ("D3" if k in D3IDS else
                    "D5" if k in D5IDS else
                    "D6" if k in D6IDS else "D2")
            check(tier, "fixture " + k, v == want, "got %s want %s" % (v, want))
        for k, allowed in EXPECT_SET.items():
            v = got.get(k, "<missing>").strip()
            check("D5", "fixture " + k + " in " + "/".join(allowed), v in allowed,
                  "got " + v)
        for k, gatefn in NUMERIC.items():
            v = got.get(k, "")
            try:
                ok = gatefn(v)
            except Exception:
                ok = False
            check("D5", "fixture " + k + " numeric gate", ok, "got " + str(v))
        line = got.get("LINE", "<missing>")
        check("D5", "composer live MeTTa reduction renders COUPLING-STATE (NC5)",
              "COUPLING-STATE" in line and "$" not in line
              and "honesty" not in line and "contact-audit" not in line,
              "got " + line[:140])

        # ---------------- D7 bounded live-loop probes (M2) ----------------
        ri = drun(["docker", "inspect", "--format", "{{.State.StartedAt}}",
                   args.container])
        check("D7", "docker inspect rc==0", ri.returncode == 0,
              (ri.stderr or "").strip()[:120])
        since = (ri.stdout or "").strip()
        rl = drun(["docker", "logs", "--since", since, args.container])
        check("D7", "docker logs --since rc==0", rl.returncode == 0,
              (rl.stderr or "")[:120])
        logs = (rl.stdout or "") + (rl.stderr or "")
        cl = [l for l in logs.splitlines() if "COUPLING-STATE" in l]
        check("D7", "COUPLING-STATE lines in CURRENT-boot logs", len(cl) > 0,
              "%d lines since %s" % (len(cl), since))
        check("D7", "zero held-by-corner-gate in CURRENT-boot logs",
              "held-by-corner-gate" not in logs)
        if cl:
            ground = all("$" not in l.split("COUPLING-STATE", 1)[1]
                         and "(Error" not in l and "unreduced" not in l for l in cl)
            check("D7", "ground-symbol render check on live lines", ground)
        else:
            check("D7", "ground-symbol render check on live lines", False,
                  "no lines to check")

        # ---------------- D8 metrics (same bounded window) ----------------
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
        metrics = {"boundary_started_at": since, "lines": len(cl),
                   "support_min": min(supports) if supports else None,
                   "support_max": max(supports) if supports else None,
                   "band_transitions": transitions, "next_move_counts": moves}
        os.makedirs("staging", exist_ok=True)
        with open("staging/v3_observation_metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)
        check("D8", "observation metrics written (bounded window)", True,
              json.dumps(metrics))

    done("VALIDATE")


def done(tag):
    print("=" * 72)
    print("%s RESULT: %d PASS, %d FAIL" % (tag, len(PASSES), len(FAILS)))
    for l in FAILS:
        print("  " + l)
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
