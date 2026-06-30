#!/usr/bin/env python3
"""
ClarityOmega — lib_pln (PLN) Standalone Diagnostic

Runs OUTSIDE the live src/loop.metta dispatch (per ask 4 — bypasses the
5-command-per-cycle bandwidth constraint and context-switching corruption).

The diagnostic exists to answer four empirical questions about lib_pln:

    Q1  Does PLN Modus Ponens fire at all with placeholder STVs, and do
        (empty) results from guard failures survive `collapse` without
        crashing the substrate? (C1, C6)

    Q2  Do realistic, differentiated STV inputs produce differentiated
        outputs — i.e. is the STV forward-declaration stub
        `(= (STV $X) (stv 0.1 0.9))` actually overriding our premises,
        or do real strengths flow through? (C2)

    Q3  Does PLN agree with its own reference documentation on the
        Abduction example bird/robin/flyer ⊢ (stv 0.767 0.422)? (C3)

    Q4  Do NAL and PLN share an atomspace via `-->` / `Inheritance`, or
        are they isolated vocabularies that cannot cross-pollinate? (C4, C5)

Each criterion is fully independent. The runner pattern is lifted from
sprint_0 phase_d_verification.py: write self-contained .metta file →
subprocess to /PeTTa/run.sh → parse reduction results after the LAST
`^^^^^` separator → per-criterion verify function with explicit pass/fail.

USAGE (from host, in ~/clarityclaw-omega/):

    python3 staging/pln_diagnostic.py

The script invokes `docker exec clarity_omega ...` itself; no manual
docker cp needed. lib_pln must already be staged at
/tmp/upstream_lib_pln.metta inside the container (you have done this).

REQUIREMENTS IN CONTAINER:
    - /PeTTa/run.sh present
    - /tmp/upstream_lib_pln.metta present
    - /PeTTa/repos/omegaclaw/lib_nal.metta present (for C4/C5 NAL+PLN tests)
"""

import os
import re
import sys
import subprocess
import textwrap


# --- Configuration (verified against `docker exec clarity_omega ...` on 2026-05-28) ---

CONTAINER_NAME = "clarity_omega"
PETTA_RUN_SH = "/PeTTa/run.sh"
LIB_PLN_PATH = "/tmp/upstream_lib_pln.metta"
LIB_NAL_PATH = "/PeTTa/repos/omegaclaw/lib_nal.metta"

# Where to drop test .metta files inside the container.
CONTAINER_TMP_DIR = "/tmp"

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*[mK]')


def strip_ansi(text):
    return ANSI_ESCAPE.sub('', text)


# =============================================================
# Preambles
# =============================================================

PLN_PREAMBLE = f'!(import! &self "{LIB_PLN_PATH}")\n'
NAL_PREAMBLE = f'!(import! &self "{LIB_NAL_PATH}")\n'
NAL_PLUS_PLN_PREAMBLE = NAL_PREAMBLE + PLN_PREAMBLE


# =============================================================
# CRITERION 1 — PLN Modus Ponens, placeholder STVs, in isolation
# =============================================================
# Exercise: (Implication (Inheritance $1 (IntSet Feathered))
#                        (Inheritance $1 Bird))   (stv 0.1 0.9)
#          + (Inheritance Pingu (IntSet Feathered)) (stv 0.1 0.9)
#       |~ (Inheritance Pingu Bird) (stv ? ?)
#
# Per reference doc, MP truth function: f = f1*f2, c = f1*f2*c1*c2.
# With (0.1,0.9) and (0.1,0.9): expected stv (0.01, 0.0081).
#
# Pass if: any reduction result emitted, none containing "ERROR"/"Exception",
# and ideally containing the literal "Inheritance Pingu Bird" or "stv".

CRITERION_1 = PLN_PREAMBLE + textwrap.dedent("""\

    ;; PLN Modus Ponens with placeholder STV (0.1 0.9) on both premises.
    !(|~ ((Implication (Inheritance $1 (IntSet Feathered))
                       (Inheritance $1 Bird))
           (stv 0.1 0.9))
          ((Inheritance Pingu (IntSet Feathered))
           (stv 0.1 0.9)))
""")


# =============================================================
# CRITERION 2 — PLN Modus Ponens, REALISTIC differentiated STVs
# =============================================================
# Same shape as C1, but with (0.9, 0.85) and (0.8, 0.7).
# Expected: stv (0.72, ~0.4284). If we get (0.01, 0.0081) — same as C1 —
# the STV stub is overriding real inputs and confirms the doc's warning.

CRITERION_2 = PLN_PREAMBLE + textwrap.dedent("""\

    ;; PLN Modus Ponens with realistic differentiated STVs.
    !(|~ ((Implication (Inheritance $1 (IntSet Feathered))
                       (Inheritance $1 Bird))
           (stv 0.9 0.85))
          ((Inheritance Pingu (IntSet Feathered))
           (stv 0.8 0.7)))
""")


# =============================================================
# CRITERION 3 — PLN Abduction (reference doc's worked example)
# =============================================================
# Per reference doc:
#   (Inheritance bird flyer) + (Inheritance robin flyer)
#       ⊢ (Inheritance robin bird) (stv 0.767 0.422)
#
# This anchors whether the engine matches its own documentation.
# Confidence ~0.422 should NOT exceed ~0.45 (NAL abduction ceiling).

CRITERION_3 = PLN_PREAMBLE + textwrap.dedent("""\

    ;; PLN Abduction per reference doc — expected (stv 0.767 0.422).
    !(|~ ((Inheritance bird flyer)  (stv 1.0 0.9))
          ((Inheritance robin flyer) (stv 1.0 0.9)))
""")


# =============================================================
# CRITERION 4 — NAL premise (-->) fed into PLN (|~)
# =============================================================
# NAL writes inheritance as (--> A B). PLN's rules pattern-match on
# (Inheritance A B). If they share the same atomspace via --> / Inheritance,
# the PLN rule should fire. If they are isolated vocabularies, PLN sees
# nothing and returns empty.

CRITERION_4 = NAL_PLUS_PLN_PREAMBLE + textwrap.dedent("""\

    ;; Premise written in NAL's --> form, consumed by PLN's |~.
    !(|~ ((--> bird flyer)  (stv 1.0 0.9))
          ((--> robin flyer) (stv 1.0 0.9)))
""")


# =============================================================
# CRITERION 5 — PLN premise (Inheritance) fed into NAL (|-)
# =============================================================
# Inverse of C4. NAL's |- is defined over the --> operator. Does it
# see (Inheritance A B) at all?

CRITERION_5 = NAL_PLUS_PLN_PREAMBLE + textwrap.dedent("""\

    ;; Premise in PLN's Inheritance form, consumed by NAL's |-.
    !(|- ((Inheritance bird animal)   (stv 1.0 0.9))
          ((Inheritance robin bird)    (stv 1.0 0.9)))
""")


# =============================================================
# CRITERION 6 — Empty-result substrate-safety probe
# =============================================================
# Feed deliberately badly-shaped premise to |~. PLN's guarded rules
# should refuse to fire and return (empty) via /safe or guard-failure
# paths. If `collapse` over (empty) crashes the substrate, the script
# either errors out or hangs. If it returns cleanly with no result,
# the substrate is safe.

CRITERION_6 = PLN_PREAMBLE + textwrap.dedent("""\

    ;; Premises that NO PLN rule should match. Guards should return
    ;; (empty); collapse should survive it.
    !(|~ ((SomeNonsenseLink foo bar) (stv 0.5 0.5))
          ((AnotherNonsense baz qux) (stv 0.5 0.5)))
""")


# =============================================================
# Runner infrastructure
# =============================================================


def write_metta_file_in_container(source, test_name):
    """Write source to a temp .metta file inside the container.

    Returns the in-container path.
    """
    container_path = f"{CONTAINER_TMP_DIR}/pln_diag_{test_name}.metta"
    # heredoc avoids shell-escaping landmines; tag is unique enough to avoid collisions
    cmd = [
        "docker", "exec", "-i", CONTAINER_NAME,
        "bash", "-c", f"cat > {container_path} << 'METTA_EOF_PLNDIAG'\n{source}\nMETTA_EOF_PLNDIAG"
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(f"Failed to write {container_path}: {r.stderr}")
    return container_path


def run_metta_in_container(metta_path):
    """Execute /PeTTa/run.sh against the .metta file inside the container."""
    cmd = [
        "docker", "exec", CONTAINER_NAME,
        "bash", PETTA_RUN_SH, metta_path,
    ]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120)


def cleanup_container_file(container_path):
    subprocess.run(
        ["docker", "exec", CONTAINER_NAME, "rm", "-f", container_path],
        capture_output=True, text=True, timeout=15,
    )


def extract_all_results(stdout_clean):
    """Capture every reduction result after the LAST `^^^^^` separator.

    Pattern lifted from sprint_0 phase_d_verification.py. PeTTa emits
    all !() reduction results stacked after the final separator.
    """
    lines = stdout_clean.split('\n')
    last_separator_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('^^^^^^^^^^^^^^^^^^^^^^'):
            last_separator_idx = i

    results_lines = lines if last_separator_idx == -1 else lines[last_separator_idx + 1:]

    results = []
    for line in results_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('-->'):
            continue
        if stripped.startswith('^^^^^^^^^^^^^^^^^^^^^^'):
            continue
        if stripped.startswith('---'):
            break
        results.append(stripped)
    return results


def run_criterion(num, name, source, verify_fn, test_tag):
    print(f"\n{'='*78}")
    print(f"CRITERION {num}: {name}")
    print('='*78)

    try:
        container_path = write_metta_file_in_container(source, test_tag)
    except Exception as e:
        print(f"  SETUP FAILED: {e}")
        return False, "setup failure"

    try:
        try:
            result = run_metta_in_container(container_path)
        except subprocess.TimeoutExpired:
            print("  RESULT: TIMEOUT (>120s) — substrate may have hung on this input")
            return False, "timeout"

        stdout_clean = strip_ansi(result.stdout)
        stderr_clean = strip_ansi(result.stderr)
        results = extract_all_results(stdout_clean)

        print(f"Exit code: {result.returncode}")
        print(f"\n--- stdout (ANSI-stripped) ---\n{stdout_clean}")
        if stderr_clean.strip():
            print(f"\n--- stderr ---\n{stderr_clean}")
        print(f"\n--- Extracted reduction results ---")
        for i, r in enumerate(results):
            print(f"  [{i}] {r!r}")

        passed, explanation = verify_fn(stdout_clean, results, stderr_clean, result.returncode)
        print(f"\nVERDICT: {'PASS' if passed else 'FAIL'}")
        print(f"  {explanation}")
        return passed, explanation
    finally:
        cleanup_container_file(container_path)


# =============================================================
# Verification functions
# =============================================================


def _looks_crashed(stderr_clean, rc, results):
    """Heuristic for substrate crash vs. clean empty result."""
    if rc != 0:
        return True, f"nonzero exit ({rc})"
    crash_markers = ('ERROR', 'Exception', 'error(', 'Aborted', 'Segmentation')
    for marker in crash_markers:
        if marker in stderr_clean:
            return True, f"stderr contains {marker!r}"
        for r in results:
            if marker in r:
                return True, f"result contains {marker!r}"
    return False, ""


def verify_criterion_1(stdout, results, stderr, rc):
    crashed, why = _looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"Substrate crash: {why}. Reduction did not complete cleanly."

    if not results:
        return False, ("No reduction results emitted. Either |~ produced (empty), "
                       "or the import failed silently. Inspect stdout above.")

    # Look for the expected conclusion shape.
    joined = ' '.join(results)
    has_target = 'Inheritance' in joined and 'Pingu' in joined and 'Bird' in joined
    has_stv = 'stv' in joined
    has_empty = any(r.strip() in ('()', '[]') for r in results)

    if has_target and has_stv:
        return True, ("PLN Modus Ponens FIRED with placeholder STVs. "
                      "Conclusion (Inheritance Pingu Bird) with stv emitted. "
                      "Substrate handled rule cleanly.")
    if has_empty:
        return False, ("PLN returned empty list — rule did not match. "
                       "Could indicate: import failed, or |~ requires different premise shape.")
    return False, (f"Unexpected result shape. Got: {results}. "
                   f"Expected (Inheritance Pingu Bird ...) with stv.")


def verify_criterion_2(stdout, results, stderr, rc):
    crashed, why = _looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"Substrate crash: {why}"
    if not results:
        return False, "No reduction results emitted with realistic STVs."

    joined = ' '.join(results)
    if 'stv' not in joined:
        return False, f"No stv in output. Results: {results}"

    # Extract any stv tuple to compare against C1.
    # Expected MP math: f = 0.9*0.8 = 0.72, c = 0.72*0.85*0.7 = 0.4284
    stv_match = re.search(r'stv\s+([0-9.]+)\s+([0-9.]+)', joined)
    if not stv_match:
        return False, f"Could not parse stv tuple from: {joined}"

    f_out = float(stv_match.group(1))
    c_out = float(stv_match.group(2))

    # C1 placeholder math: f=0.01, c=0.0081. C2 expected: f=0.72, c=0.4284.
    # If f_out is close to 0.72 → real STVs flowing through.
    # If f_out is close to 0.01 → STV stub overriding inputs (doc warning confirmed).
    near_realistic = abs(f_out - 0.72) < 0.05
    near_placeholder = abs(f_out - 0.01) < 0.005

    if near_realistic:
        return True, (f"Real STVs FLOW THROUGH. Got stv ({f_out}, {c_out}); "
                      f"expected ~(0.72, 0.4284). Inputs propagate correctly — "
                      f"doc warning about STV stub override is NOT triggered here.")
    if near_placeholder:
        return False, (f"DOC WARNING CONFIRMED: output ({f_out}, {c_out}) matches "
                       f"placeholder math (~0.01, 0.0081) despite realistic inputs "
                       f"(0.9, 0.85) and (0.8, 0.7). STV stub is overriding premises. "
                       f"Every PLN deduction would use the hardcoded prior — "
                       f"confidence numbers are uninformative in this configuration.")
    return False, (f"Unexpected stv ({f_out}, {c_out}). Neither matches realistic "
                   f"expectation (~0.72, 0.4284) nor placeholder (~0.01, 0.0081). "
                   f"Investigate before drawing conclusions.")


def verify_criterion_3(stdout, results, stderr, rc):
    crashed, why = _looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"Substrate crash: {why}"
    if not results:
        return False, "No reduction results — PLN Abduction did not fire."

    joined = ' '.join(results)
    has_target = 'Inheritance' in joined and 'robin' in joined and 'bird' in joined
    stv_match = re.search(r'stv\s+([0-9.]+)\s+([0-9.]+)', joined)

    if not has_target or not stv_match:
        return False, (f"Expected (Inheritance robin bird) with stv. Got: {results}")

    f_out = float(stv_match.group(1))
    c_out = float(stv_match.group(2))

    # Reference doc: stv (0.767 0.422). Allow modest tolerance.
    f_ok = abs(f_out - 0.767) < 0.05
    c_ok = abs(c_out - 0.422) < 0.05

    if f_ok and c_ok:
        return True, (f"PLN Abduction matches reference doc. "
                      f"Got stv ({f_out}, {c_out}); expected ~(0.767, 0.422). "
                      f"Confidence respects the ~0.45 abduction ceiling.")
    return False, (f"Engine output diverges from reference doc. "
                   f"Got stv ({f_out}, {c_out}); doc claims ~(0.767, 0.422). "
                   f"f_ok={f_ok} c_ok={c_ok}. Investigate: doc may be stale, "
                   f"or this PLN build differs from documented version.")


def verify_criterion_4(stdout, results, stderr, rc):
    crashed, why = _looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"Substrate crash on NAL→PLN cross-vocab: {why}"

    joined = ' '.join(results)
    has_inheritance_conclusion = 'Inheritance' in joined and 'stv' in joined
    has_arrow_conclusion = ('-->' in joined) and 'stv' in joined
    has_empty = any(r.strip() in ('()', '[]') for r in results) or not results

    if has_inheritance_conclusion or has_arrow_conclusion:
        return True, (f"NAL→PLN CROSS-VOCAB WORKS. PLN |~ consumed --> premise "
                      f"and produced an inheritance conclusion with stv. "
                      f"They share atomspace. Result: {results}")
    if has_empty:
        return False, ("NAL→PLN ISOLATED. PLN |~ did not match --> premises. "
                       "--> and Inheritance are distinct atoms; PLN cannot consume "
                       "NAL-style premises without translation. This is a juicy "
                       "finding: if you want cross-engine reasoning, you'll need "
                       "an explicit (--> $A $B) ↔ (Inheritance $A $B) bridge rule, "
                       "or to standardize on one vocabulary at write time.")
    return False, f"Ambiguous result. Inspect manually: {results}"


def verify_criterion_5(stdout, results, stderr, rc):
    crashed, why = _looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"Substrate crash on PLN→NAL cross-vocab: {why}"

    joined = ' '.join(results)
    has_arrow_conclusion = '-->' in joined and 'stv' in joined
    has_inheritance_conclusion = 'Inheritance' in joined and 'stv' in joined
    has_empty = any(r.strip() in ('()', '[]') for r in results) or not results

    if has_arrow_conclusion or has_inheritance_conclusion:
        return True, (f"PLN→NAL CROSS-VOCAB WORKS. NAL |- consumed Inheritance "
                      f"premise. Result: {results}")
    if has_empty:
        return False, ("PLN→NAL ISOLATED. NAL |- did not match Inheritance premises. "
                       "Inheritance and --> are distinct atoms; NAL cannot consume "
                       "PLN-style premises. Mirrors C4 finding from the other side.")
    return False, f"Ambiguous result. Inspect manually: {results}"


def verify_criterion_6(stdout, results, stderr, rc):
    """Empty-result substrate-safety probe.

    Pass = process exits cleanly, no crash markers, regardless of whether
    results is empty or () or some unmatched-reducer noise.
    """
    crashed, why = _looks_crashed(stderr, rc, results)
    if crashed:
        return False, (f"SUBSTRATE NOT SAFE on guard-failure path: {why}. "
                       f"PLN guards returning (empty) DO crash through collapse. "
                       f"This contraindicates wiring PLN into the live loop until "
                       f"the failure mode is contained.")
    return True, ("Substrate handled non-matching premises cleanly. "
                  "(empty) survived collapse without crash. Safe to invoke |~ "
                  "speculatively without pre-validation of premise shapes.")


# =============================================================
# Preflight
# =============================================================


def preflight():
    """Verify container, run.sh, lib_pln, and lib_nal are all present."""
    print("="*78)
    print("PREFLIGHT")
    print("="*78)

    checks = [
        ("container running",
         ["docker", "ps", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Names}}"],
         lambda out: CONTAINER_NAME in out),
        (f"{PETTA_RUN_SH} exists",
         ["docker", "exec", CONTAINER_NAME, "test", "-f", PETTA_RUN_SH],
         lambda out: True),
        (f"{LIB_PLN_PATH} exists",
         ["docker", "exec", CONTAINER_NAME, "test", "-f", LIB_PLN_PATH],
         lambda out: True),
        (f"{LIB_NAL_PATH} exists",
         ["docker", "exec", CONTAINER_NAME, "test", "-f", LIB_NAL_PATH],
         lambda out: True),
    ]

    all_ok = True
    for label, cmd, validator in checks:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            ok = (r.returncode == 0) and validator(r.stdout)
            print(f"  [{'OK' if ok else 'FAIL'}] {label}")
            if not ok:
                if r.stdout.strip():
                    print(f"        stdout: {r.stdout.strip()!r}")
                if r.stderr.strip():
                    print(f"        stderr: {r.stderr.strip()!r}")
                all_ok = False
        except Exception as e:
            print(f"  [FAIL] {label} — exception: {e}")
            all_ok = False

    return all_ok


# =============================================================
# Main
# =============================================================


def main():
    print("="*78)
    print("ClarityOmega — lib_pln Standalone Diagnostic")
    print("="*78)

    if not preflight():
        print("\nPreflight FAILED. Resolve the above before running criteria.")
        return 1

    suite = [
        (1, "PLN Modus Ponens, placeholder STV (0.1 0.9)",
         CRITERION_1, verify_criterion_1, "c1"),
        (2, "PLN Modus Ponens, realistic differentiated STVs",
         CRITERION_2, verify_criterion_2, "c2"),
        (3, "PLN Abduction matches reference doc (bird/robin/flyer)",
         CRITERION_3, verify_criterion_3, "c3"),
        (4, "NAL→PLN cross-vocab: (--> A B) into |~",
         CRITERION_4, verify_criterion_4, "c4"),
        (5, "PLN→NAL cross-vocab: (Inheritance A B) into |-",
         CRITERION_5, verify_criterion_5, "c5"),
        (6, "Substrate-safety probe: (empty) survives collapse",
         CRITERION_6, verify_criterion_6, "c6"),
    ]

    summary = []
    for num, name, source, verify_fn, tag in suite:
        passed, explanation = run_criterion(num, name, source, verify_fn, tag)
        summary.append((num, name, passed, explanation))

    print("\n" + "="*78)
    print("SUMMARY")
    print("="*78)
    for num, name, passed, explanation in summary:
        marker = "PASS" if passed else "FAIL"
        print(f"  [{marker}] C{num}: {name}")

    passed_count = sum(1 for _, _, p, _ in summary if p)
    print(f"\n{passed_count} of {len(summary)} criteria passed.")

    # Interpretation guide — regardless of pass/fail, surface the juicy findings.
    print("\n" + "-"*78)
    print("INTERPRETATION GUIDE")
    print("-"*78)
    print("  C1 PASS → PLN engine is alive; lib_pln imports cleanly.")
    print("  C2 PASS → real STVs propagate. C2 FAIL with placeholder-shaped output")
    print("            → STV stub is overriding inputs; confidence is uninformative.")
    print("  C3 PASS → engine matches reference doc.")
    print("            C3 FAIL with different stv → doc and runtime have drifted.")
    print("  C4 PASS → NAL --> and PLN Inheritance unify. Cross-engine reasoning works.")
    print("  C4 FAIL → vocabularies are isolated. Bridge rule required for interop.")
    print("  C5 confirms C4 from the other direction.")
    print("  C6 PASS → safe to invoke |~ on arbitrary premises (guards return cleanly).")
    print("  C6 FAIL → DO NOT wire PLN into live loop until empty-path is contained.")

    return 0 if passed_count == len(summary) else 1


if __name__ == "__main__":
    sys.exit(main())
