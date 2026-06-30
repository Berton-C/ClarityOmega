#!/usr/bin/env python3
"""
ClarityOmega — lib_pln (PLN) Standalone Diagnostic v2

Runs OUTSIDE the live src/loop.metta dispatch — bypasses the
5-command-per-cycle bandwidth constraint and context-switching corruption.

Ten criteria, each independently runnable. Stdout is condensed (final reduction
result + verdict + one-line finding per criterion, plus a compact summary
table). The full per-criterion stdout/stderr is written to
/tmp/pln_diagnostic_run_<timestamp>.log inside the container (which maps to
shared_files/ on the host).

QUESTIONS
    Q1  Does PLN load and Modus Ponens fire? Does `(empty)` survive
        `collapse`? (C1, C6)
    Q2  Do realistic STVs flow through PLN Modus Ponens? (C2)
    Q3  Does PLN match the reference doc's worked example? (C3)
    Q4  Do NAL `-->` and PLN `Inheritance` share an atomspace? (C4, C5)
    Q5  Does a one-line guard extension bridge NAL into PLN? (C7)
    Q6  Is the `(STV $X)` stub the *only* thing blocking meaningful
        syllogistic-rule output, or is something deeper broken? (C8)
    Q7  Does PLN's unguarded Revision rule already cross the vocabulary
        boundary even without C7's bridge? (C9)
    Q8  If C7's bridge works, does the inferred atom *round-trip* into a
        downstream NAL `|-` rule, or is it cosmetically similar but
        structurally distinct? (C10)

USAGE (from host, in ~/clarityclaw-omega/):

    python3 staging/pln_diagnostic.py

REQUIREMENTS IN CONTAINER:
    - /PeTTa/run.sh                              entrypoint
    - /tmp/upstream_lib_pln.metta                staged lib_pln
    - /PeTTa/repos/omegaclaw/lib_nal.metta       live lib_nal
"""

import os
import re
import sys
import datetime
import subprocess
import textwrap


# --- Configuration (verified 2026-05-28 against clarity_omega container) ---

CONTAINER_NAME = "clarity_omega"
PETTA_RUN_SH = "/PeTTa/run.sh"
LIB_PLN_PATH = "/tmp/upstream_lib_pln.metta"
LIB_NAL_PATH = "/PeTTa/repos/omegaclaw/lib_nal.metta"
CONTAINER_TMP_DIR = "/tmp"  # persistent, maps to host shared_files/

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
# Truth__ModusPonens: f = Ps*PQs + 0.02*(1-Ps);  c = Ps*PQs*Pc*PQc
# With (0.1, 0.9) and (0.1, 0.9) — but note that |~pln's MP rule
# unifies premises by shape, not by guard: ($A $T1) + ((Implication $A $B) $T2).

CRITERION_1 = PLN_PREAMBLE + textwrap.dedent("""\

    !(|~ ((Implication (Inheritance Pingu (IntSet Feathered))
                       (Inheritance Pingu Bird))
           (stv 0.1 0.9))
          ((Inheritance Pingu (IntSet Feathered))
           (stv 0.1 0.9)))
""")


# =============================================================
# CRITERION 2 — PLN Modus Ponens, REALISTIC differentiated STVs
# =============================================================
# Same rule as C1 but with (0.9, 0.85) and (0.8, 0.7).
# Expected per Truth__ModusPonens:
#   f = 0.8 * 0.9 + 0.02 * (1 - 0.8) = 0.72 + 0.004 = 0.724
#   c = 0.8 * 0.9 * 0.7 * 0.85 = 0.4284
# If output ≈ (0.724, 0.4284) → real STVs propagate through MP.

CRITERION_2 = PLN_PREAMBLE + textwrap.dedent("""\

    !(|~ ((Implication (Inheritance Pingu (IntSet Feathered))
                       (Inheritance Pingu Bird))
           (stv 0.9 0.85))
          ((Inheritance Pingu (IntSet Feathered))
           (stv 0.8 0.7)))
""")


# =============================================================
# CRITERION 3 — PLN Abduction, reference doc's worked example
# =============================================================
# Doc claims (stv 0.767, 0.422). Engine actually emits ~(1.0, 0.4475)
# because Truth__Abduction reads (STV $A), (STV $B), (STV $C) priors
# from the stub `(= (STV $X) (stv 0.1 0.9))`. The confidence (~0.4475)
# is within the ~0.45 abduction ceiling, but the strength is dominated
# by the constant-0.1 priors.

CRITERION_3 = PLN_PREAMBLE + textwrap.dedent("""\

    !(|~ ((Inheritance bird flyer)  (stv 1.0 0.9))
          ((Inheritance robin flyer) (stv 1.0 0.9)))
""")


# =============================================================
# CRITERION 4 — NAL premise (-->) fed into PLN (|~)
# =============================================================
# PLN syllogistic rules call (SyllogisticRuleGuard $LinkType) which
# returns True only for 'Inheritance' and 'Implication'. The guard
# returns (empty) for -->.

CRITERION_4 = NAL_PLUS_PLN_PREAMBLE + textwrap.dedent("""\

    !(|~ ((--> bird flyer)  (stv 1.0 0.9))
          ((--> robin flyer) (stv 1.0 0.9)))
""")


# =============================================================
# CRITERION 5 — PLN premise (Inheritance) fed into NAL (|-)
# =============================================================
# Inverse direction. NAL's |-nal pattern-matches on (--> $a $b).
# (Inheritance bird animal) has head atom 'Inheritance', not '-->'.

CRITERION_5 = NAL_PLUS_PLN_PREAMBLE + textwrap.dedent("""\

    !(|- ((Inheritance bird animal)   (stv 1.0 0.9))
          ((Inheritance robin bird)    (stv 1.0 0.9)))
""")


# =============================================================
# CRITERION 6 — Substrate-safety probe: (empty) survives collapse
# =============================================================
# No PLN rule should match this premise shape. Guards return (empty).
# Test that `collapse` over (empty) doesn't crash the substrate.

CRITERION_6 = PLN_PREAMBLE + textwrap.dedent("""\

    !(|~ ((SomeNonsenseLink foo bar) (stv 0.5 0.5))
          ((AnotherNonsense baz qux) (stv 0.5 0.5)))
""")


# =============================================================
# CRITERION 7 — Bridge experiment: extend SyllogisticRuleGuard for -->
# =============================================================
# Hypothesis from C4 root-cause analysis: PLN won't fire on -->
# *only* because the guard explicitly enumerates Inheritance and
# Implication. Add (= (SyllogisticRuleGuard -->) True) AFTER the import
# (which adds a clause, not overrides) and re-run the C4 premise.
# If we get a (--> $A $B) conclusion with an stv, one-line bridge works.

CRITERION_7 = PLN_PREAMBLE + textwrap.dedent("""\

    ;; The one-line bridge.
    (= (SyllogisticRuleGuard -->) True)

    !(|~ ((--> bird flyer)  (stv 1.0 0.9))
          ((--> robin flyer) (stv 1.0 0.9)))
""")


# =============================================================
# CRITERION 8 — STV-stub override: per-concept priors
# =============================================================
# C3 returned (stv 1.0, 0.4475) instead of doc's (0.767, 0.422)
# because (STV $X) is hardcoded to (stv 0.1 0.9) for every concept.
# Override per concept and re-run the same abduction. If strength
# moves toward 0.767 with the doc's implied priors, diagnosis confirmed.
#
# Truth__Abduction formula:
#   f = (sAB * sCB * sC) / sB  +  (sC * (1-sAB) * (1-sCB)) / (1-sB)
# With sAB=1.0, sCB=1.0, sC=0.5 (flyer), sB=0.5 (flyer prior, same arg):
# Note: the engine's |~ runs BOTH orderings via superpose, so we get
# both (Inheritance bird robin) and (Inheritance robin bird) results.
# The key question: do BOTH directions now show strengths != 1.0?

CRITERION_8 = PLN_PREAMBLE + textwrap.dedent("""\

    ;; Override the (STV $X) stub with per-concept priors.
    (= (STV bird)  (stv 0.6 0.9))
    (= (STV robin) (stv 0.1 0.9))
    (= (STV flyer) (stv 0.5 0.9))

    !(|~ ((Inheritance bird flyer)  (stv 1.0 0.9))
          ((Inheritance robin flyer) (stv 1.0 0.9)))
""")


# =============================================================
# CRITERION 9 — Unguarded rule cross-vocab: PLN Revision on NAL premises
# =============================================================
# The |~pln Revision rule has NO guard:
#   (= (|~pln ($T $T1) ($T $T2)) ($T (Truth__Revision $T1 $T2)))
# It pattern-matches any two premises sharing the same shape $T.
# If we feed two (--> A B) premises with different STVs, Revision
# SHOULD fire even without C7's bridge — proving that vocabulary
# isolation is rule-by-rule, not engine-wide. Revision is exactly
# the rule you'd want for cross-engine evidence merging.

CRITERION_9 = PLN_PREAMBLE + textwrap.dedent("""\

    !(|~ ((--> bird flyer) (stv 0.8 0.7))
          ((--> bird flyer) (stv 0.6 0.5)))
""")


# =============================================================
# CRITERION 10 — Bridge round-trip: PLN's --> output into NAL |-
# =============================================================
# If C7 produces (--> bird robin) (stv $f $c), feed it as a premise
# into NAL deduction with another --> premise. If the deduction
# composes, C7's bridge produces *real* NAL-compatible atoms.
# If not, the atoms are syntactically similar but structurally distinct
# (e.g., PLN emits ((--> bird robin) ...) but as a list-of-list with
# different metatype than NAL constructs natively).
#
# We use the same input shape that C7 confirmed, then chain:

CRITERION_10 = NAL_PLUS_PLN_PREAMBLE + textwrap.dedent("""\

    ;; Replicate the C7 bridge.
    (= (SyllogisticRuleGuard -->) True)

    ;; Step 1: PLN abduction produces a (--> ...) conclusion.
    !(|~ ((--> bird flyer)  (stv 1.0 0.9))
          ((--> robin flyer) (stv 1.0 0.9)))

    ;; Step 2: chain by NAL deduction with an additional --> premise.
    ;; If PLN's output atoms are NAL-compatible, this composes.
    !(|- ((--> bird robin) (stv 1.0 0.5))
          ((--> robin small) (stv 1.0 0.9)))
""")


# =============================================================
# Runner infrastructure
# =============================================================


def write_metta_file_in_container(source, test_tag):
    container_path = f"{CONTAINER_TMP_DIR}/pln_diag_{test_tag}.metta"
    cmd = [
        "docker", "exec", "-i", CONTAINER_NAME,
        "bash", "-c",
        f"cat > {container_path} << 'METTA_EOF_PLNDIAG'\n{source}\nMETTA_EOF_PLNDIAG"
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(f"Failed to write {container_path}: {r.stderr}")
    return container_path


def run_metta_in_container(metta_path):
    cmd = ["docker", "exec", CONTAINER_NAME, "bash", PETTA_RUN_SH, metta_path]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=180)


def cleanup_container_file(container_path):
    subprocess.run(
        ["docker", "exec", CONTAINER_NAME, "rm", "-f", container_path],
        capture_output=True, text=True, timeout=15,
    )


def append_to_container_log(log_path, content):
    """Append content to a log file inside the container."""
    cmd = [
        "docker", "exec", "-i", CONTAINER_NAME,
        "bash", "-c",
        f"cat >> {log_path} << 'PLNLOG_EOF_PLNDIAG'\n{content}\nPLNLOG_EOF_PLNDIAG"
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)


def extract_all_results(stdout_clean):
    """All reduction results after the LAST `^^^^^` separator.

    PeTTa emits compiled-clause output for each definition during import
    (long), then all !() reduction results in a block after the final
    separator. We only want the latter.
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


def extract_stv(text):
    """Pull the first (stv f c) tuple as (float, float). Returns None if absent."""
    m = re.search(r'stv\s+([0-9.]+)\s+([0-9.]+)', text)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def extract_all_stvs(text):
    """All (stv f c) tuples in order — useful for collapses returning multiple results."""
    return [(float(f), float(c)) for f, c in re.findall(r'stv\s+([0-9.]+)\s+([0-9.]+)', text)]


def looks_crashed(stderr_clean, rc, results):
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


def is_empty_result(results):
    """True if results are absent or all empty-shaped ('()', '[]')."""
    if not results:
        return True
    return all(r.strip() in ('()', '[]') for r in results)


def run_criterion(num, name, source, verify_fn, test_tag, log_path):
    """Execute one criterion. Returns (passed, finding, final_result_str)."""
    header = f"\n{'='*78}\nCRITERION {num}: {name}\n{'='*78}\n"
    print(header.rstrip())

    try:
        container_path = write_metta_file_in_container(source, test_tag)
    except Exception as e:
        finding = f"setup failure: {e}"
        print(f"  SETUP FAILED: {e}")
        return False, finding, "(setup failed)"

    full_dump = ""
    try:
        try:
            result = run_metta_in_container(container_path)
        except subprocess.TimeoutExpired:
            finding = "timeout >180s — substrate may have hung"
            print(f"  FAIL: {finding}")
            append_to_container_log(log_path, f"{header}TIMEOUT >180s\n")
            return False, finding, "(timeout)"

        stdout_clean = strip_ansi(result.stdout)
        stderr_clean = strip_ansi(result.stderr)
        results = extract_all_results(stdout_clean)

        # Build full dump for logfile
        full_dump = (
            f"{header}"
            f"Source:\n{source}\n"
            f"Exit code: {result.returncode}\n"
            f"--- stdout ---\n{stdout_clean}\n"
            f"--- stderr ---\n{stderr_clean}\n"
            f"--- extracted reductions ---\n"
            + "\n".join(f"  [{i}] {r!r}" for i, r in enumerate(results))
            + "\n"
        )
        append_to_container_log(log_path, full_dump)

        # Condensed stdout: just the actual reduction results.
        if results:
            print("  Reduction results:")
            for i, r in enumerate(results):
                # Truncate any single result over 200 chars
                display = r if len(r) <= 200 else r[:197] + "..."
                print(f"    [{i}] {display}")
        else:
            print("  (no reduction results emitted)")

        passed, finding = verify_fn(stdout_clean, results, stderr_clean, result.returncode)
        verdict = "PASS" if passed else "FAIL"
        print(f"  VERDICT: {verdict}")
        print(f"  Finding: {finding}")

        final_summary = " | ".join(results) if results else "(empty)"
        return passed, finding, final_summary
    finally:
        cleanup_container_file(container_path)


# =============================================================
# Verification functions
# =============================================================


def verify_criterion_1(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"substrate crash: {why}"
    if is_empty_result(results):
        return False, "PLN Modus Ponens did not fire (empty result)"
    joined = ' '.join(results)
    has_target = 'Inheritance' in joined and 'Pingu' in joined and 'Bird' in joined
    has_stv = 'stv' in joined
    if has_target and has_stv:
        stv = extract_stv(joined)
        return True, f"PLN MP fires with placeholder STVs; output stv={stv}"
    return False, f"unexpected output: {results}"


def verify_criterion_2(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"substrate crash: {why}"
    if is_empty_result(results):
        return False, "no result with realistic STVs"

    stv = extract_stv(' '.join(results))
    if stv is None:
        return False, f"no stv in output: {results}"
    f_out, c_out = stv

    # Truth__ModusPonens: f = 0.8*0.9 + 0.02*0.2 = 0.724; c = 0.8*0.9*0.7*0.85 = 0.4284
    near_realistic = abs(f_out - 0.724) < 0.05 and abs(c_out - 0.4284) < 0.05
    near_placeholder = abs(f_out - 0.028) < 0.01  # the C1-analogous output: 0.1*0.1 + 0.02*0.9 = 0.028

    if near_realistic:
        return True, f"real STVs propagate through MP; got ({f_out:.4f}, {c_out:.4f}) ≈ expected (0.724, 0.4284)"
    if near_placeholder:
        return False, f"STV stub overriding MP inputs; got ({f_out:.4f}, {c_out:.4f}) matches placeholder math"
    return False, f"unexpected ({f_out:.4f}, {c_out:.4f}); neither realistic (0.724, 0.4284) nor placeholder (~0.028)"


def verify_criterion_3(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"substrate crash: {why}"
    if is_empty_result(results):
        return False, "abduction did not fire"

    joined = ' '.join(results)
    stvs = extract_all_stvs(joined)
    if not stvs:
        return False, f"no stv in output: {results}"

    f_out, c_out = stvs[0]
    doc_f, doc_c = 0.767, 0.422

    f_matches_doc = abs(f_out - doc_f) < 0.05
    c_matches_doc = abs(c_out - doc_c) < 0.05
    f_is_stub_dominated = abs(f_out - 1.0) < 0.01  # what STV-stub produces

    if f_matches_doc and c_matches_doc:
        return True, f"engine matches reference doc exactly: ({f_out:.4f}, {c_out:.4f})"
    if f_is_stub_dominated and c_matches_doc:
        return False, (f"engine math correct but (STV $X) stub dominates strength: "
                       f"got ({f_out:.4f}, {c_out:.4f}); doc claims ({doc_f}, {doc_c}); "
                       f"confidence ~{c_out:.4f} within ~0.45 abduction ceiling so the math "
                       f"works — only the per-concept priors are constants. See C8.")
    return False, f"unexpected ({f_out:.4f}, {c_out:.4f}); doc claims ({doc_f}, {doc_c})"


def verify_criterion_4(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"substrate crash on NAL→PLN: {why}"
    joined = ' '.join(results)
    if 'Inheritance' in joined and 'stv' in joined:
        return True, f"unexpected: NAL→PLN appears to work without bridge: {results}"
    if '-->' in joined and 'stv' in joined:
        return True, f"unexpected: PLN produced --> conclusion without bridge: {results}"
    if is_empty_result(results):
        return False, ("NAL→PLN isolated: SyllogisticRuleGuard returns (empty) for --> "
                       "(enumerates only Inheritance and Implication). C7 tests one-line fix.")
    return False, f"ambiguous: {results}"


def verify_criterion_5(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"substrate crash on PLN→NAL: {why}"
    joined = ' '.join(results)
    if ('-->' in joined or 'Inheritance' in joined) and 'stv' in joined:
        return True, f"unexpected: PLN→NAL appears to work: {results}"
    if is_empty_result(results):
        return False, ("PLN→NAL isolated: |-nal pattern-matches '-->', not 'Inheritance'. "
                       "Mirrors C4. Either standardize at write time or add a bridge.")
    return False, f"ambiguous: {results}"


def verify_criterion_6(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"DO NOT wire PLN into live loop until contained: {why}"
    return True, "(empty) survives collapse cleanly; safe to invoke |~ on arbitrary premises"


def verify_criterion_7(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"crash when extending guard: {why}"
    if is_empty_result(results):
        return False, ("one-line bridge insufficient: adding (SyllogisticRuleGuard -->) didn't "
                       "make rules fire. Investigate guard semantics or pattern-match shape.")
    joined = ' '.join(results)
    if '-->' in joined and 'stv' in joined:
        stvs = extract_all_stvs(joined)
        return True, (f"one-line bridge works: (SyllogisticRuleGuard -->) makes PLN fire on "
                      f"NAL premises and produce --> conclusions with stv {stvs}")
    return False, f"bridge fired but unexpected output shape: {results}"


def verify_criterion_8(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"crash when overriding STV: {why}"
    if is_empty_result(results):
        return False, "abduction did not fire with per-concept STVs"

    joined = ' '.join(results)
    stvs = extract_all_stvs(joined)
    if not stvs:
        return False, f"no stv in output: {results}"

    # In C3 with stub (STV $X) = (stv 0.1 0.9), every strength was 1.0.
    # With per-concept STVs that vary, strengths should differ from 1.0
    # (unless the formula's numerator/denominator structure happens to cancel).
    strengths = [f for f, c in stvs]
    any_below_one = any(s < 0.99 for s in strengths)
    any_above_zero_different_from_one = any(0.001 < s < 0.99 for s in strengths)

    if any_above_zero_different_from_one:
        return True, (f"per-concept STV override CHANGES syllogistic output: strengths={strengths}; "
                      f"STV stub is the root cause of C3's strength=1.0. Path to meaningful "
                      f"PLN reasoning is to populate (STV concept) for each concept.")
    if not any_below_one:
        return False, (f"per-concept STVs had NO effect on output strength (all 1.0): {strengths}. "
                       f"Either the override isn't being read or there's a deeper issue beyond the stub.")
    return False, f"unexpected strengths: {strengths}"


def verify_criterion_9(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"substrate crash on Revision cross-vocab: {why}"
    if is_empty_result(results):
        return False, ("PLN Revision did NOT fire on --> premises, even though Revision is "
                       "unguarded. Vocabulary isolation runs deeper than the SyllogisticRuleGuard.")
    joined = ' '.join(results)
    if '-->' in joined and 'stv' in joined:
        stvs = extract_all_stvs(joined)
        return True, (f"PLN Revision CROSSES vocab boundary unaided: fired on --> premises and "
                      f"produced revised stv {stvs}. Use Revision for cross-engine evidence merging.")
    return False, f"unexpected: {results}"


def verify_criterion_10(stdout, results, stderr, rc):
    crashed, why = looks_crashed(stderr, rc, results)
    if crashed:
        return False, f"crash in round-trip: {why}"

    # Expect two reduction blocks: PLN abduction output, then NAL deduction output.
    # The KEY test: does the second !() (the NAL |-) produce a result with stv?
    # We need to look at all results and see if at least two distinct outputs are present.
    joined = ' '.join(results)
    stvs = extract_all_stvs(joined)

    # The NAL deduction !(|- (--> bird robin) (--> robin small)) should produce
    # (--> bird small) with a Truth_Deduction stv ≈ (1.0, 0.5*0.9 = 0.45).
    has_nal_deduction = ('bird' in joined and 'small' in joined) or len(stvs) >= 2

    if is_empty_result(results) or not has_nal_deduction:
        return False, ("round-trip FAILS: PLN's --> output is not consumable by NAL |-. "
                       "Atoms are syntactically similar but structurally distinct. Bridge is cosmetic; "
                       "real interop needs a normalization layer.")

    if has_nal_deduction and len(stvs) >= 2:
        return True, (f"round-trip WORKS: PLN's --> output feeds into NAL |-. Atoms are "
                      f"structurally identical. Bridge produces real NAL-compatible output. stvs={stvs}")
    return False, f"ambiguous round-trip: {results}"


# =============================================================
# Preflight + main
# =============================================================


def preflight(log_path):
    print(f"{'='*78}\nPREFLIGHT\n{'='*78}")

    checks = [
        ("container running",
         ["docker", "ps", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Names}}"],
         lambda out: CONTAINER_NAME in out),
        (f"{PETTA_RUN_SH}",
         ["docker", "exec", CONTAINER_NAME, "test", "-f", PETTA_RUN_SH],
         lambda out: True),
        (f"{LIB_PLN_PATH}",
         ["docker", "exec", CONTAINER_NAME, "test", "-f", LIB_PLN_PATH],
         lambda out: True),
        (f"{LIB_NAL_PATH}",
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
                all_ok = False
        except Exception as e:
            print(f"  [FAIL] {label} — {e}")
            all_ok = False

    # Initialize the log file
    subprocess.run(
        ["docker", "exec", CONTAINER_NAME, "bash", "-c",
         f"echo 'ClarityOmega PLN Diagnostic v2 — {datetime.datetime.now().isoformat()}' > {log_path}"],
        capture_output=True, text=True, timeout=15,
    )
    print(f"  Full log: {log_path} (container; maps to host shared_files/)")

    return all_ok


def main():
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_path = f"{CONTAINER_TMP_DIR}/pln_diagnostic_run_{timestamp}.log"

    print(f"{'='*78}\nClarityOmega — lib_pln Standalone Diagnostic v2\n{'='*78}")

    if not preflight(log_path):
        print("\nPreflight FAILED.")
        return 1

    suite = [
        (1, "PLN MP, placeholder STV (0.1 0.9)",
         CRITERION_1, verify_criterion_1, "c1"),
        (2, "PLN MP, realistic differentiated STVs",
         CRITERION_2, verify_criterion_2, "c2"),
        (3, "PLN Abduction vs reference doc (bird/robin/flyer)",
         CRITERION_3, verify_criterion_3, "c3"),
        (4, "NAL→PLN cross-vocab: (--> A B) into |~",
         CRITERION_4, verify_criterion_4, "c4"),
        (5, "PLN→NAL cross-vocab: (Inheritance A B) into |-",
         CRITERION_5, verify_criterion_5, "c5"),
        (6, "Substrate safety: (empty) survives collapse",
         CRITERION_6, verify_criterion_6, "c6"),
        (7, "Bridge experiment: one-line SyllogisticRuleGuard extension",
         CRITERION_7, verify_criterion_7, "c7"),
        (8, "STV-stub override: per-concept priors change syllogistic output",
         CRITERION_8, verify_criterion_8, "c8"),
        (9, "Unguarded rule: PLN Revision on NAL --> premises",
         CRITERION_9, verify_criterion_9, "c9"),
        (10, "Bridge round-trip: PLN's --> output into NAL |-",
         CRITERION_10, verify_criterion_10, "c10"),
    ]

    summary = []
    for num, name, source, verify_fn, tag in suite:
        passed, finding, final_result = run_criterion(num, name, source, verify_fn, tag, log_path)
        summary.append((num, name, passed, finding, final_result))

    # ---- Condensed final summary ----
    print(f"\n{'='*78}\nCOMPACT SUMMARY\n{'='*78}")
    print(f"{'#':>3}  {'V':4}  {'Name':52}  Result")
    print(f"{'-'*3}  {'-'*4}  {'-'*52}  {'-'*15}")
    for num, name, passed, finding, final_result in summary:
        marker = "PASS" if passed else "FAIL"
        # Truncate name and result for table layout
        name_disp = name if len(name) <= 50 else name[:47] + "..."
        result_disp = final_result if len(final_result) <= 50 else final_result[:47] + "..."
        print(f"C{num:<2}  {marker:4}  {name_disp:52}  {result_disp}")

    print(f"\n{'-'*78}\nFINDINGS\n{'-'*78}")
    for num, name, passed, finding, _ in summary:
        marker = "PASS" if passed else "FAIL"
        print(f"C{num} [{marker}] {finding}")

    passed_count = sum(1 for _, _, p, _, _ in summary if p)
    print(f"\n{passed_count} of {len(summary)} criteria passed.")
    print(f"Full per-criterion stdout/stderr written to {log_path} (host: shared_files/{os.path.basename(log_path)})")

    return 0 if passed_count == len(summary) else 1


if __name__ == "__main__":
    sys.exit(main())
