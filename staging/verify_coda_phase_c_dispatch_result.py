#!/usr/bin/env python3
"""
verify_coda_phase_c_dispatch_result.py

Targeted substrate re-verify for Sprint 0-Coda Phase C Change 0's run-chain edit
(the dispatch-result write), plus Clarity's review items 2 and 3. Deterministic,
runs via run.sh against a fresh AtomSpace; does NOT need the live loop. This is
the re-verify owed because the run-chain edit changed the file the 2026-06-14
14:34 substrate log had certified.

What it proves:
  P-DR-1  a non-anchor handler result is captured: run-chain writes
          (dispatch-result invocation-id: ... result: (skill-set skills: ...) ...)
  ITEM-2  car-atom over the collapsed dispatch-result match returns the WHOLE
          multi-word skills string (no space truncation)
  P-DR-2  the chain still terminates correctly: a non-anchor result reaches
          dispatch-chain-exhausted (unchanged path), AND a decision-anchor
          result reaches dispatch-chain-anchored (unchanged path) WITH its
          dispatch-result also written (write fires before the branch)
  ITEM-3  the (== $result decision-anchor) comparison is symbol-vs-symbol:
          a (skill-set ...) compound is never == decision-anchor (recurses),
          a bare decision-anchor symbol is == decision-anchor (anchors)

Method: HANDS ONLY. Python builds the MeTTa probe text and ships it to the
container; the substrate computes. Raw compilation output is recorded before
every verdict. Logs are written to the container /tmp only.

USAGE (run from repo root):
  python3 verify_coda_phase_c_dispatch_result.py
"""

import datetime
import subprocess

CONTAINER = "clarity_omega"
REGISTRY_IN_CONTAINER = "/PeTTa/repos/omegaclaw/soul/capability_registry.metta"
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_IN_CONTAINER = "/tmp/verify_coda_phase_c_dispatch_result_%s.log" % STAMP


class Recorder:
    """Tees condensed verdicts to console and the full raw trace to a container /tmp log."""

    def __init__(self):
        self.buf = []

    def raw(self, text):
        self.buf.append(text)

    def say(self, text):
        print(text)
        self.buf.append(text)

    def flush_to_container(self):
        payload = "\n".join(self.buf)
        run_in_container("cat > %s" % LOG_IN_CONTAINER, stdin=payload)
        print("\nFull raw trace written in-container to %s" % LOG_IN_CONTAINER)


def run_in_container(cmd, stdin=None):
    full = ["docker", "exec", "-i", CONTAINER, "sh", "-c", cmd]
    p = subprocess.run(full, input=stdin, capture_output=True, text=True)
    return p.stdout + p.stderr


def run_metta(probe_body, rec):
    """Inline the patched registry, then evaluate the probe body, in one fresh process."""
    registry_body = run_in_container("cat %s" % REGISTRY_IN_CONTAINER)
    probe = "/tmp/_coda_probe_%s.metta" % STAMP
    full = registry_body + "\n\n" + probe_body + "\n"
    run_in_container("cat > %s" % probe, stdin=full)
    out = run_in_container("cd /PeTTa && ./run.sh %s 2>&1" % probe)
    rec.raw("===== PROBE =====\n" + probe_body)
    rec.raw("===== RAW OUTPUT (after last separator is the result section) =====\n" + out)
    return out


def result_section(out):
    """Read only what follows the final ^^^^^ separator (the printed results)."""
    if "^^^^^" in out:
        return out.rsplit("^^^^^", 1)[1]
    return out


def is_unreduced(section, token):
    """An echoed function call (not a value) signals a failure to reduce."""
    return ("(string_length" in section) or ("(car-atom" in section and token == "skills")


def main():
    rec = Recorder()
    rec.say("Sprint 0-Coda Phase C dispatch-result substrate re-verify  %s" % STAMP)
    rec.say("Registry under test: %s\n" % REGISTRY_IN_CONTAINER)

    # Test fixtures: one informational capability (returns a multi-word skill-set,
    # like skill-discovery), one anchoring capability (returns the bare symbol).
    # Both registered 5-field, lifecycle active, efficacy defaults to 1.0.
    fixtures = """
;; ---- test fixtures (multi-word skill-set + a bare decision-anchor) ----
(registered-capability schema: (probe-skill cycle: $k) handler: test-skill priority: 100 lifecycle: active metadata: ())
(registered-capability schema: (probe-anchor cycle: $k) handler: test-anchor priority: 100 lifecycle: active metadata: ())
(= (test-skill $req) (skill-set skills: "alpha beta gamma delta"))
(= (test-anchor $req) decision-anchor)
"""

    # --- ITEM-2 + P-DR-1: non-anchor result captured, whole multi-word string back ---
    probe_a = fixtures + """
!(dispatch (probe-skill cycle: 7) 7)
!("^^^^^")
;; the exact extraction getContext uses:
!(car-atom (collapse (match &self (dispatch-result invocation-id: $_id result: (skill-set skills: $s) handler: $_h) $s)))
"""
    out_a = run_metta(probe_a, rec)
    sec_a = result_section(out_a)
    item2_ok = ("alpha beta gamma delta" in sec_a) and not is_unreduced(sec_a, "skills")
    rec.say("P-DR-1 / ITEM-2  dispatch-result captured, whole multi-word string via car-atom:  %s"
            % ("PASS" if item2_ok else "FAIL"))
    if not item2_ok:
        rec.say("    expected 'alpha beta gamma delta' in result section; got:\n    %r"
                % sec_a.strip()[:300])

    # --- P-DR-2 (non-anchor path): chain reaches exhausted, dispatch-result present ---
    probe_b = fixtures + """
!(dispatch (probe-skill cycle: 8) 8)
!("^^^^^")
!(collapse (match &self (dispatch-chain-exhausted invocation-id: 8) reached-exhausted))
!(collapse (match &self (dispatch-result invocation-id: 8 result: $r handler: $h) has-result))
"""
    out_b = run_metta(probe_b, rec)
    sec_b = result_section(out_b)
    nonanchor_ok = ("reached-exhausted" in sec_b) and ("has-result" in sec_b)
    rec.say("P-DR-2 non-anchor: chain exhausted AND dispatch-result written:  %s"
            % ("PASS" if nonanchor_ok else "FAIL"))

    # --- P-DR-2 (anchor path) + ITEM-3: bare symbol anchors, dispatch-result still written ---
    probe_c = fixtures + """
!(dispatch (probe-anchor cycle: 9) 9)
!("^^^^^")
!(collapse (match &self (dispatch-chain-anchored invocation-id: 9 anchor-handler: $h) reached-anchored))
!(collapse (match &self (dispatch-result invocation-id: 9 result: $r handler: $h) has-result))
"""
    out_c = run_metta(probe_c, rec)
    sec_c = result_section(out_c)
    anchor_ok = ("reached-anchored" in sec_c) and ("has-result" in sec_c)
    rec.say("P-DR-2 anchor + ITEM-3: bare symbol anchors AND dispatch-result written:  %s"
            % ("PASS" if anchor_ok else "FAIL"))

    # --- ITEM-3 control: compound (skill-set ...) is never == decision-anchor ---
    probe_d = fixtures + """
!("^^^^^")
!(== (skill-set skills: "x") decision-anchor)
!(== decision-anchor decision-anchor)
"""
    out_d = run_metta(probe_d, rec)
    sec_d = result_section(out_d)
    # expect: first comparison False (compound != anchor), second True (symbol == symbol)
    item3_ok = ("False" in sec_d) and ("True" in sec_d)
    rec.say("ITEM-3 control: (skill-set ...) != decision-anchor, symbol == symbol:  %s"
            % ("PASS" if item3_ok else "FAIL"))

    all_ok = item2_ok and nonanchor_ok and anchor_ok and item3_ok
    rec.say("\n===== THE GAP =====")
    rec.say("This re-verifies ONLY the run-chain dispatch-result change and items 2/3 on")
    rec.say("fixtures. It does NOT exercise the real getSkills integration, the marker")
    rec.say("emission, or P-4 parity: those are the in-loop verify (phase_d_coda_inloop_")
    rec.say("verification.py --mode verify) after rebuild, because getSkills + the prompt")
    rec.say("assembly + CHARS basis only exist in the live loop.")
    rec.say("\nVERDICT: %s" % ("ALL PASS" if all_ok else "ONE OR MORE FAILED, see raw trace"))
    rec.flush_to_container()


if __name__ == "__main__":
    main()
