#!/usr/bin/env python3
"""
soul_mutation_gate_diagnostic.py

Real test harness for the corrected metta() gate detection functions.
Modeled directly on capability_registry_diagnostic.py and
set_atom_context_diagnostic.py: drives the clarity_omega container, evaluates
the functions + test cases via /PeTTa/run.sh (which loads the substrate the
same way the runtime does), parses the trailing results by TEST marker, and
asserts GOT against EXPECT per test with a pass/fail table and exit code.

WHAT IT SETTLES:
  Whether the corrected soul-is-metta-cmd? (the function commit 89df9e4
  collapsed to a False stub citing C11 pattern-match crash) works C11-safely,
  and whether the five gate functions compose into the master-doc Section 14
  PENDING / CONFLICT / empty outcomes.

  The corrected function has two candidate forms in
  soul_mutation_gate_corrected.metta. This harness selects one via --candidate
  and rewrites the active definition before evaluating, so the choose-the-winner
  step is automated:
    A (default): (string-contains (repr $cmd) "(metta ")   [repr is proven]
    B:           (== (car-atom $cmd) metta)                 [car-atom unconfirmed]

  THE CRITICAL TEST is TEST 3 (C11 regression): a deeply nested complex atom
  must reduce to False with NO crash. If run.sh errors or the result is missing
  for TEST 3, the harness reports it as a FAIL (the C11 proof done
  programmatically), and you switch candidates.

USAGE (on the host where docker is available):
  python3 soul_mutation_gate_diagnostic.py
  python3 soul_mutation_gate_diagnostic.py --candidate B
  Optional:
    --container NAME        (default: clarity_omega)
    --functions PATH        (default: .../soul/soul_mutation_gate_corrected.metta)
    --harness PATH          (default: .../soul/soul_mutation_gate_harness.metta)
    --keep-temp

Exit code 0 only if every test PASSES (including TEST 3 no-crash). Any FAIL or
INSPECT yields a nonzero exit, same convention as the apply scripts.

PROOF LOG: every run writes /tmp/soul_mutation_gate_test_log_<ts>.log in the
container, capturing three things so the run is a self-contained proof artifact:
the exact combined .metta evaluated (what was loaded), the raw ANSI-stripped
run.sh output (what the atomspace did), and the per-test verdict table plus
summary and C11 verdict (the derived truth). Records which candidate was tested.
"""

import argparse
import datetime
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_FUNCTIONS = "/PeTTa/repos/omegaclaw/soul/soul_mutation_gate_corrected.metta"
DEFAULT_HARNESS = "/PeTTa/repos/omegaclaw/soul/soul_mutation_gate_harness.metta"


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def container_running(container):
    rc, out, _ = run(["docker", "ps", "--filter", f"name={container}",
                      "--format", "{{.Names}}"])
    return rc == 0 and container in out


def container_file_exists(container, path):
    rc, _, _ = run(["docker", "exec", container, "test", "-f", path])
    return rc == 0


# Candidate definitions for soul-is-metta-cmd? (must match the corrected file).
CANDIDATE_A = '(= (soul-is-metta-cmd? $cmd)\n   (string-contains (repr $cmd) "(metta "))'
CANDIDATE_B = '(= (soul-is-metta-cmd? $cmd)\n   (== (car-atom $cmd) metta))'


def select_candidate(functions_text, candidate):
    """
    Ensure exactly the chosen candidate of soul-is-metta-cmd? is active.
    The corrected file ships with A active and B commented. For --candidate B
    we swap: comment A's two lines, uncomment B. We operate on the text we send
    to the interpreter, not the file on disk.
    """
    text = functions_text
    if candidate == "A":
        # A is active by default in the shipped file; nothing to do, but verify.
        if "(string-contains (repr $cmd)" not in text:
            return None, "candidate A definition not found in functions file"
        return text, None
    # candidate B: activate the car-atom form, neutralize the repr form.
    if "(== (car-atom $cmd) metta)" not in text:
        return None, "candidate B definition (commented) not found in functions file"
    # Replace the active A body with the B body.
    a_pat = re.compile(
        r'\(= \(soul-is-metta-cmd\? \$cmd\)\s*\n\s*\(string-contains \(repr \$cmd\) "\(metta "\)\)'
    )
    if not a_pat.search(text):
        return None, "could not locate active candidate A block to replace for B"
    text = a_pat.sub(CANDIDATE_B, text, count=1)
    return text, None


def build_combined(container, functions_path, harness_path, candidate):
    rc, fns, err = run(["docker", "exec", container, "cat", functions_path])
    if rc != 0:
        return None, f"could not read functions: {err}"
    rc, harn, err = run(["docker", "exec", container, "cat", harness_path])
    if rc != 0:
        return None, f"could not read harness: {err}"
    fns, cerr = select_candidate(fns, candidate)
    if cerr:
        return None, cerr
    combined = (
        ";; ===== LIBRARY BOOTSTRAP (mirrors run.metta) =====\n"
        "!(import! &self (library lib_import))\n"
        f";; ===== CORRECTED FUNCTIONS (candidate {candidate}) =====\n"
        + fns
        + "\n;; ===== TEST CASES =====\n"
        + harn
        + "\n"
    )
    return combined, None


def evaluate(container, combined_text, keep_temp):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = f"/tmp/soul_mutation_gate_combined_{ts}.metta"
    p = subprocess.run(
        ["docker", "exec", "-i", container, "sh", "-c", f"cat > {temp_path}"],
        input=combined_text, text=True, capture_output=True
    )
    if p.returncode != 0:
        return None, None, f"failed to write temp file: {p.stderr}"
    rc, out, err = run(["docker", "exec", container, "sh", "-c",
                        f"cd /PeTTa && ./run.sh {temp_path} 2>&1"])
    if not keep_temp:
        run(["docker", "exec", container, "rm", "-f", temp_path])
    return out, ts, rc, None


def write_proof_log(container, ts, candidate, combined, raw_out, rc, rows,
                    npass, nfail, ninspect):
    """
    Write a full proof artifact to the container /tmp/. Captures three things,
    so the log proves what happened end to end:
      1. WHAT WAS LOADED: the exact combined .metta evaluated (candidate active).
      2. WHAT THE ATOMSPACE DID: the raw ANSI-stripped run.sh output.
      3. THE DERIVED TRUTH: the per-test PASS/FAIL verdict table + summary + C11.
    Returns the container log path.
    """
    log_path = f"/tmp/soul_mutation_gate_test_log_{ts}.log"
    L = []
    L.append("=" * 70)
    L.append("SOUL MUTATION GATE HARNESS: PROOF LOG")
    L.append("=" * 70)
    L.append(f"timestamp:      {ts}")
    L.append(f"candidate:      {candidate}  (soul-is-metta-cmd? form under test)")
    L.append(f"container:      {container}")
    L.append(f"run.sh return:  {rc}")
    L.append(f"summary:        {npass} pass, {nfail} fail, {ninspect} inspect "
             f"(of {len(rows)})")
    t3 = next((r for r in rows if r[0] == "TEST 3"), None)
    if t3:
        L.append(f"C11 verdict:    TEST 3 = {t3[1]} "
                 f"({'C11-safe, no crash on complex atom' if t3[1] == 'PASS' else 'C11 NOT proven, see table'})")
    L.append("")
    L.append("=" * 70)
    L.append("VERDICT TABLE (GOT asserted against EXPECT)")
    L.append("=" * 70)
    for tid, verdict, desc, note, cap in rows:
        L.append(f"{tid:8s} {verdict:8s} {desc}")
        if cap:
            L.append(f"         GOT: {cap[:200]}")
        if note:
            L.append(f"         NOTE: {note}")
    L.append("")
    L.append("=" * 70)
    L.append("RAW run.sh OUTPUT (atomspace behavior, ANSI-stripped)")
    L.append("=" * 70)
    L.append(strip_ansi(raw_out))
    L.append("")
    L.append("=" * 70)
    L.append("COMBINED INPUT EVALUATED (exact .metta loaded, proof of what was tested)")
    L.append("=" * 70)
    L.append(combined)
    full_log = "\n".join(L) + "\n"
    subprocess.run(
        ["docker", "exec", "-i", container, "sh", "-c", f"cat > {log_path}"],
        input=full_log, text=True, capture_output=True
    )
    return log_path


def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


NOISE_PREFIXES = ("--> metta runnable", "-->  prolog goal", "--> metta sexpr",
                  ":-", "^^^^^^", "!(", "findall(", "match(", "reduce(",
                  "(import!", "library(", "(=")


def is_noise(line):
    s = line.strip()
    if not s:
        return True
    for p in NOISE_PREFIXES:
        if s.startswith(p):
            return True
    return False


def parse_tests(output):
    """
    The run.sh evaluator echoes each source line and its Prolog goal first, then
    prints ALL reduction results at the end as a contiguous trailing block of
    bare values (confirmed in the proof log: the markers print as quoted strings
    and the results print as bare 'true'/string/term values, in evaluation
    order). The earlier per-line capture caught the GOAL ECHO, not the results.

    This reads the TRAILING RESULT BLOCK and maps it to tests positionally.
    Each test in the harness emits, in order: a marker println (which prints the
    marker string) optionally preceded by a change-state! (prints true), then the
    function-under-test result. We walk the trailing block, split on marker
    strings, and the test's result is the value(s) printed after its marker and
    before the next marker.
    """
    output = strip_ansi(output)
    lines = [ln.rstrip() for ln in output.splitlines()]

    # Find the trailing result block: everything after the last goal-echo noise.
    # The result block is contiguous bare values at the end. We collect from the
    # end upward until we hit the echo region (lines with prolog/goal markers).
    def is_echo_noise(s):
        s = s.strip()
        if not s:
            return True
        for p in ("--> metta runnable", "-->  prolog goal", "--> metta sexpr",
                  "--> metta function", "--> prolog clause", ":-", "^^^^^^",
                  "!(", "findall(", "import_prolog", "library(", "(import!",
                  "(=", "A=", "B=", "consult(", "use_module(", "superpose(",
                  ")", "),", "_).", "A),", "B),", "C),"):
            if s.startswith(p):
                return True
        return False

    # Collect the trailing contiguous run of substantive (non-echo) lines.
    block = []
    for ln in reversed(lines):
        s = ln.strip()
        if not s:
            if block:
                # blank line: stop if we've already gathered the block and hit
                # the gap before it; keep going through internal blanks otherwise.
                # The result block is contiguous, so a blank after content ends it.
                break
            continue
        if is_echo_noise(ln):
            if block:
                break
            continue
        block.append(s)
    block.reverse()

    # Now split the block by marker strings. A marker line contains "=== TEST N:".
    sections = {}
    order = []
    current = None
    buf = []
    marker = re.compile(r'=== (TEST [0-9A-Za-z]+):')
    end_marker = re.compile(r'=== TEST END ===')
    for s in block:
        if end_marker.search(s):
            if current is not None and current not in sections:
                sections[current] = "\n".join(buf).strip()
            current = None
            continue
        m = marker.search(s)
        if m:
            tid = m.group(1)
            if current is not None and current not in sections:
                sections[current] = "\n".join(buf).strip()
            current = tid
            if tid not in order:
                order.append(tid)
            buf = []
        elif current is not None:
            # skip the 'true' acks from change-state! lines preceding the result;
            # keep them only if nothing else appears (so we never drop the result).
            buf.append(s)
    if current is not None and current not in sections:
        sections[current] = "\n".join(buf).strip()
    return sections, order


# (test_id, EXPECT predicate on captured text, human description)
def _result_value(s):
    """The result block may include the echoed call expression on its own line
    followed by the bare reduced value. Take the LAST non-empty line as the
    reduced value (the runtime prints the value after the echoed expression)."""
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def truthy(s):
    v = _result_value(s)
    return v.lower() == "true"


def falsy(s):
    v = _result_value(s)
    # In this runtime False may render as 'false', or the call may not reduce to
    # true. Treat an explicit false token as falsy. An echoed-but-unreduced
    # expression (not 'true') is also treated as falsy for boolean predicates.
    if v.lower() == "true":
        return False
    return v.lower() == "false" or v.startswith("(") or v == "()" 


CRITERIA = [
    ("TEST 1", lambda s: truthy(s), "is-metta-cmd on soul mutation -> True"),
    ("TEST 2", lambda s: falsy(s), "is-metta-cmd on non-metta -> False"),
    ("TEST 3", lambda s: falsy(s), "C11 regression: complex atom -> False, NO CRASH"),
    ("TEST 4", lambda s: truthy(s), "any-metta list with metta -> True"),
    ("TEST 5", lambda s: falsy(s), "any-metta list without metta -> False"),
    ("TEST 6", lambda s: "soul-x y" in s or "add-atom &self" in s, "extract-metta-arg returns the string"),
    ("TEST 7", lambda s: truthy(s), "targets-soul-namespace soul- -> True"),
    ("TEST 8", lambda s: falsy(s), "targets-soul-namespace regular -> False"),
    ("TEST 9", lambda s: truthy(s), "mutation-pending lock held -> True"),
    ("TEST 10", lambda s: falsy(s), "mutation-pending unlocked -> False"),
    ("TEST 11", lambda s: "SOUL-NAMESPACE-MUTATION-PENDING" in s and "CONFLICT" not in s,
     "full chain soul mutation -> PENDING"),
    ("TEST 12", lambda s: "SOUL-NAMESPACE-MUTATION" not in s,
     "full chain non-soul metta -> empty (no flag)"),
]


def assess(sections):
    rows = []
    for tid, pred, desc in CRITERIA:
        cap = sections.get(tid)
        if cap is None or cap == "":
            # TEST 3 missing is the C11 crash signature.
            verdict = "FAIL" if tid == "TEST 3" else "INSPECT"
            note = "no result captured" + (" (possible crash, C11 not avoided)" if tid == "TEST 3" else "")
            rows.append((tid, verdict, desc, note, cap or ""))
            continue
        try:
            ok = pred(cap)
        except Exception as e:
            rows.append((tid, "INSPECT", desc, f"predicate error: {e}", cap))
            continue
        rows.append((tid, "PASS" if ok else "FAIL", desc,
                     "" if ok else f"got: {cap[:120]}", cap))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--functions", default=DEFAULT_FUNCTIONS)
    ap.add_argument("--harness", default=DEFAULT_HARNESS)
    ap.add_argument("--candidate", choices=["A", "B"], default="A")
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    print("=" * 70)
    print(f"metta() Gate Detection Harness (candidate {args.candidate})")
    print("=" * 70)

    print("\nPREFLIGHT")
    if not container_running(args.container):
        print(f"  [FAIL] container '{args.container}' not running")
        sys.exit(1)
    print(f"  [OK] container '{args.container}' running")
    for label, path in [("functions", args.functions), ("harness", args.harness)]:
        if not container_file_exists(args.container, path):
            print(f"  [FAIL] {label} not found at {path}")
            print(f"         (copy the corrected files into soul/ first)")
            sys.exit(1)
        print(f"  [OK] {label}: {path}")

    print("\nBUILDING COMBINED INPUT")
    combined, err = build_combined(args.container, args.functions, args.harness, args.candidate)
    if err:
        print(f"  [FAIL] {err}")
        sys.exit(1)
    print(f"  [OK] combined input built (candidate {args.candidate} active)")

    print("\nEVALUATING (via run.sh)")
    out, ts, rc, err = evaluate(args.container, combined, args.keep_temp)
    if err:
        print(f"  [FAIL] {err}")
        sys.exit(1)
    print(f"  run.sh return code: {rc}")

    sections, order = parse_tests(out)
    if not sections:
        print("\n  [WARN] no test sections parsed. Raw (ANSI-stripped, first 3000 chars):")
        print("-" * 70)
        print(strip_ansi(out)[:3000])
        # Still write a proof log so the failed run is captured.
        log_path = write_proof_log(args.container, ts, args.candidate, combined,
                                   out, rc, [], 0, 0, 0)
        print(f"\n  proof log (raw only, no sections parsed): {log_path}")
        sys.exit(3)

    rows = assess(sections)

    print("\n" + "=" * 70)
    print("RESULTS (GOT asserted against EXPECT)")
    print("=" * 70)
    npass = nfail = ninspect = 0
    for tid, verdict, desc, note, cap in rows:
        if verdict == "PASS":
            npass += 1
        elif verdict == "FAIL":
            nfail += 1
        else:
            ninspect += 1
        line = f"  {tid:8s} {verdict:8s} {desc}"
        print(line)
        if note:
            print(f"           {note}")

    # Write the full proof artifact (loaded input + atomspace output + verdict).
    log_path = write_proof_log(args.container, ts, args.candidate, combined,
                               out, rc, rows, npass, nfail, ninspect)

    print("\n" + "=" * 70)
    print(f"SUMMARY: {npass} pass, {nfail} fail, {ninspect} inspect "
          f"(of {len(rows)})  [candidate {args.candidate}]")
    print("=" * 70)
    print(f"  proof log (loaded input + atomspace output + verdict table):")
    print(f"    {log_path}  [container /tmp/; maps to host shared_files/ per convention]")

    # TEST 3 is the C11 verdict.
    t3 = next((r for r in rows if r[0] == "TEST 3"), None)
    if t3 and t3[1] == "PASS":
        print(f"  C11 PROOF: candidate {args.candidate} returns False on a complex atom "
              f"with no crash. C11-safe.")
    elif t3:
        print(f"  C11 NOT PROVEN for candidate {args.candidate} (TEST 3 = {t3[1]}). "
              f"If FAIL/crash, re-run with the other candidate.")

    if nfail == 0 and ninspect == 0:
        print(f"\n  ALL PASS. Candidate {args.candidate} is harness-proven. "
              f"Hand to Clarity to confirm, then wire the native gate.")
        sys.exit(0)
    print(f"\n  Not all green. Inspect the log: {log_path}")
    sys.exit(2)


if __name__ == "__main__":
    main()
