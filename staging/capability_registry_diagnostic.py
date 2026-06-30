#!/usr/bin/env python3
"""
capability_registry_diagnostic.py

Runs the capability-registry caller-interface harness inside the clarity_omega
container and gathers validation output for review. Same model as the PLN
diagnostic: condensed verdict to stdout, full per-test output to a timestamped
log under the container /tmp (which maps to host shared_files/).

WHAT IT VERIFIES (the two interfaces the NACE caller depends on, plus two more):
  TEST 1/1a: dispatch writes (capability-invoked ...) atoms       [INTERFACE 1]
  TEST 2:    efficacy-filter-step gates on the 0.3 threshold      [INTERFACE 2]
  TEST 3:    efficacy observation override changes the outcome    [override path]
  TEST 4/4a: fallback fires on unmatched input                    [robustness]

HOW IT WORKS:
  The harness at soul/capability_registry_harness.metta depends on functions
  defined in soul/capability_registry_path_c_draft.metta (dispatch,
  resolve-and-filter-entries). Both must be evaluated in the same MeTTa context.
  This script builds a single combined MeTTa input (registry draft, then harness)
  and feeds it to the container's MeTTa evaluator, capturing all reduction output.

USAGE (run on the host, where docker is available):
  python3 capability_registry_diagnostic.py

  Optional flags:
    --container NAME    container name (default: clarity_omega)
    --registry PATH     registry draft path inside container
                        (default: /PeTTa/repos/omegaclaw/soul/capability_registry_path_c_draft.metta)
    --harness PATH      harness path inside container
                        (default: /PeTTa/repos/omegaclaw/soul/capability_registry_harness.metta)
    --keep-temp         do not delete the combined temp file after running
"""

import argparse
import datetime
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_REGISTRY = "/PeTTa/repos/omegaclaw/soul/capability_registry_path_c_draft.metta"
DEFAULT_HARNESS = "/PeTTa/repos/omegaclaw/soul/capability_registry_harness.metta"


def run(cmd):
    """Run a command, return (returncode, stdout, stderr)."""
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def container_running(container):
    rc, out, _ = run(["docker", "ps", "--filter", f"name={container}",
                      "--format", "{{.Names}}"])
    return rc == 0 and container in out


def container_file_exists(container, path):
    rc, _, _ = run(["docker", "exec", container, "test", "-f", path])
    return rc == 0


def find_metta_evaluator(container):
    """
    Locate how to evaluate a full-syntax MeTTa file inside the container.

    CONFIRMED via probe (2026-05-31): /PeTTa/run.sh takes a .metta file as a
    positional argument and evaluates its ! lines. run.sh wraps:
        swipl --stack_limit=8g -q -s /PeTTa/src/main.pl -- <file>
    with an optional LD_PRELOAD of libmork_ffi.so. We invoke run.sh directly
    so we inherit the exact evaluation environment the runtime uses.

    Returns (kind, invocation_prefix). kind 'run-sh' means run.sh <file>.
    """
    # Confirmed path: run.sh evaluates a file argument.
    rc, _, _ = run(["docker", "exec", container, "test", "-f", "/PeTTa/run.sh"])
    if rc == 0:
        return ("run-sh", ["/PeTTa/run.sh"])

    # Fallbacks retained in case run.sh is absent in some variant.
    rc, out, _ = run(["docker", "exec", container, "sh", "-c", "command -v metta"])
    if rc == 0 and out.strip():
        return ("metta-binary", [out.strip()])

    return (None, None)


def build_combined_input(container, registry_path, harness_path):
    """Concatenate library import + registry draft + harness into one MeTTa input.

    The leading import line mirrors run.metta's own bootstrap. Probe confirmed
    it evaluates cleanly and is harmless. We include it defensively so any
    registry function that depends on lib_import builtins resolves the same way
    it would inside the runtime.
    """
    rc, reg, err = run(["docker", "exec", container, "cat", registry_path])
    if rc != 0:
        return None, f"could not read registry: {err}"
    rc, harn, err = run(["docker", "exec", container, "cat", harness_path])
    if rc != 0:
        return None, f"could not read harness: {err}"
    combined = (
        ";; ===== LIBRARY BOOTSTRAP (mirrors run.metta) =====\n"
        "!(import! &self (library lib_import))\n"
        ";; ===== REGISTRY DRAFT (loaded first) =====\n"
        + reg
        + "\n;; ===== HARNESS (loaded second) =====\n"
        + harn
        + "\n"
    )
    return combined, None


def evaluate(container, kind, prefix, combined_text):
    """
    Write combined_text to a container temp file and evaluate it via the
    confirmed run.sh path (or a fallback binary). run.sh takes the file as a
    positional argument. We cd into /PeTTa first because run.sh resolves its
    own SCRIPT_DIR but the mork_ffi LD_PRELOAD check is relative to it.
    Returns (returncode, stdout, stderr, temp_path).
    """
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = f"/tmp/cap_registry_combined_{ts}.metta"

    # Write the combined file into the container via stdin to avoid quoting issues.
    p = subprocess.run(
        ["docker", "exec", "-i", container, "sh", "-c", f"cat > {temp_path}"],
        input=combined_text, text=True, capture_output=True
    )
    if p.returncode != 0:
        return p.returncode, "", f"failed to write temp file: {p.stderr}", temp_path

    if kind == "run-sh":
        # Mirror the runtime invocation: cd /PeTTa && ./run.sh <file>
        cmd = ["docker", "exec", container, "sh", "-c",
               f"cd /PeTTa && ./run.sh {temp_path} 2>&1"]
    elif kind == "metta-binary":
        cmd = ["docker", "exec", container] + prefix + [temp_path]
    else:
        return 1, "", f"no runnable evaluator (kind={kind})", temp_path

    rc, out, err = run(cmd)
    return rc, out, err, temp_path


def parse_tests(output):
    """
    Split the output by the harness's TEST markers and capture what followed.

    The run.sh evaluator (confirmed via probe) wraps each ! line in structural
    noise: a '--> metta runnable -->' echo of the source line, then a
    '-->  prolog goal  -->' block, then the actual result. String-literal !
    lines (the harness's '=== TEST N: ... ===' markers) print their content.

    We detect a marker when the TEST string appears, then collect subsequent
    lines, filtering the evaluator's structural noise so the captured section
    is the actual reduction results. Because the marker string is itself echoed
    as a 'metta runnable' line AND printed as a result, we dedupe by only
    starting a new section on the first occurrence of each distinct marker.
    """
    noise_prefixes = (
        "--> metta runnable",
        "-->  prolog goal",
        ":-",
        "^^^^^^",
        "!(",            # echoed source ! lines
    )

    def is_noise(line):
        s = line.strip()
        if not s:
            return True
        for p in noise_prefixes:
            if s.startswith(p):
                return True
        return False

    sections = {}
    order = []
    current = None
    buf = []
    marker = re.compile(r'=== (TEST [0-9][0-9a-z]*):')
    for line in output.splitlines():
        m = marker.search(line)
        if m:
            tid = m.group(1)
            if tid in sections or tid == current:
                # Already capturing or captured this marker; the echo duplicate.
                continue
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = tid
            order.append(tid)
            buf = []
        elif current is not None:
            if not is_noise(line):
                buf.append(line)
    if current is not None and current not in sections:
        sections[current] = "\n".join(buf).strip()
    return sections


def assess(sections):
    """
    Apply pass/fail criteria to the parsed sections. Returns a list of
    (test_id, verdict, note) tuples. Verdict is PASS, FAIL, or INSPECT.
    Criteria are intentionally conservative: where the output shape is
    hard to assert mechanically, we mark INSPECT and surface the raw text.
    """
    results = []

    # TEST 1a: capability-invoked for high + default, NOT low
    t1a = sections.get("TEST 1a", "")
    if t1a:
        has_high = "test-cap-high" in t1a
        has_default = "test-cap-default" in t1a
        has_low = "test-cap-low" in t1a
        if has_high and has_default and not has_low:
            results.append(("TEST 1a", "PASS",
                            "capability-invoked written for high+default, low correctly filtered (INTERFACE 1 + 2)"))
        elif has_low:
            results.append(("TEST 1a", "FAIL",
                            "test-cap-low appears but should have been filtered at efficacy 0.1 < 0.3"))
        else:
            results.append(("TEST 1a", "INSPECT",
                            f"expected high+default present, low absent; got: {t1a[:200]}"))
    else:
        results.append(("TEST 1a", "INSPECT", "no output captured for TEST 1a"))

    # TEST 2: eligible set = high + default only
    t2 = sections.get("TEST 2", "")
    if t2:
        has_high = "test-cap-high" in t2
        has_default = "test-cap-default" in t2
        has_low = "test-cap-low" in t2
        if has_high and has_default and not has_low:
            results.append(("TEST 2", "PASS",
                            "efficacy threshold gates dispatch correctly (INTERFACE 2)"))
        elif has_low:
            results.append(("TEST 2", "FAIL",
                            "test-cap-low in eligible set; efficacy filter not gating at 0.3"))
        else:
            results.append(("TEST 2", "INSPECT", f"got: {t2[:200]}"))
    else:
        results.append(("TEST 2", "INSPECT", "no output captured for TEST 2"))

    # TEST 3: after observation override, low passes too (all three present)
    t3 = sections.get("TEST 3", "")
    if t3:
        has_high = "test-cap-high" in t3
        has_default = "test-cap-default" in t3
        has_low = "test-cap-low" in t3
        if has_high and has_default and has_low:
            results.append(("TEST 3", "PASS",
                            "observation override (0.8) lifts test-cap-low past threshold; override path works"))
        elif not has_low:
            results.append(("TEST 3", "FAIL",
                            "test-cap-low still filtered after 0.8 override; override path not consulted"))
        else:
            results.append(("TEST 3", "INSPECT", f"got: {t3[:200]}"))
    else:
        results.append(("TEST 3", "INSPECT", "no output captured for TEST 3"))

    # TEST 4a: fallback atom written
    t4a = sections.get("TEST 4a", "")
    if t4a:
        if "no-matching-capability" in t4a:
            results.append(("TEST 4a", "PASS",
                            "fallback fires on unmatched input; caller treats fallback cycle as nothing-to-log"))
        else:
            results.append(("TEST 4a", "INSPECT", f"expected no-matching-capability; got: {t4a[:200]}"))
    else:
        results.append(("TEST 4a", "INSPECT", "no output captured for TEST 4a"))

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--registry", default=DEFAULT_REGISTRY)
    ap.add_argument("--harness", default=DEFAULT_HARNESS)
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    print("=" * 70)
    print("Capability Registry Caller-Interface Diagnostic")
    print("=" * 70)

    print("\nPREFLIGHT")
    if not container_running(args.container):
        print(f"  [FAIL] container '{args.container}' not running")
        sys.exit(1)
    print(f"  [OK] container '{args.container}' running")

    for label, path in (("registry", args.registry), ("harness", args.harness)):
        if not container_file_exists(args.container, path):
            print(f"  [FAIL] {label} not found at {path}")
            sys.exit(1)
        print(f"  [OK] {label}: {path}")

    kind, prefix = find_metta_evaluator(args.container)
    if kind is None:
        print("  [FAIL] no MeTTa evaluator found in container")
        print("         (no /PeTTa/run.sh, no `metta` binary)")
        print("         Locate the runtime's MeTTa evaluator and re-run with it.")
        sys.exit(1)
    print(f"  [OK] evaluator: {kind} ({' '.join(prefix)})")

    print("\nBUILDING COMBINED INPUT (registry + harness)")
    combined, err = build_combined_input(args.container, args.registry, args.harness)
    if combined is None:
        print(f"  [FAIL] {err}")
        sys.exit(1)
    print(f"  [OK] combined input: {len(combined)} chars")

    print("\nEVALUATING")
    rc, out, errout, temp_path = evaluate(args.container, kind, prefix, combined)
    print(f"  evaluator returncode: {rc}")
    print(f"  combined temp file: {temp_path} (container; maps to host shared_files/)")

    # Write the full log inside the container /tmp
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f"/tmp/cap_registry_diagnostic_{ts}.log"
    full_log = (
        f"returncode: {rc}\n\n===== STDOUT =====\n{out}\n\n===== STDERR =====\n{errout}\n"
    )
    subprocess.run(
        ["docker", "exec", "-i", args.container, "sh", "-c", f"cat > {log_path}"],
        input=full_log, text=True, capture_output=True
    )
    print(f"  full log: {log_path} (container; maps to host shared_files/)")

    if not args.keep_temp:
        run(["docker", "exec", args.container, "rm", "-f", temp_path])

    print("\nPARSING TESTS")
    sections = parse_tests(out)
    if not sections:
        print("  [WARN] no TEST markers found in output.")
        print("  This usually means the evaluator did not run the ! lines, or")
        print("  the registry/harness failed to load. Raw stdout below:")
        print("-" * 70)
        print(out[:3000])
        print("-" * 70)
        if errout.strip():
            print("STDERR:")
            print(errout[:2000])
        sys.exit(3)
    print(f"  parsed {len(sections)} test sections: {', '.join(sorted(sections))}")

    print("\n" + "=" * 70)
    print("PER-TEST OUTPUT")
    print("=" * 70)
    for tid in sorted(sections):
        print(f"\n--- {tid} ---")
        body = sections[tid]
        print(body if body else "(empty)")

    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    results = assess(sections)
    n_pass = sum(1 for _, v, _ in results if v == "PASS")
    for tid, verdict, note in results:
        print(f"  {tid:10s} {verdict:8s} {note}")
    print(f"\n  {n_pass} of {len(results)} criteria PASS")

    print("\n" + "=" * 70)
    print("THE GAP (read regardless of pass/fail)")
    print("=" * 70)
    print("  The efficacy-filter-step reads capability-efficacy-rate (baseline)")
    print("  and capability-efficacy-observation (override). It does NOT read a")
    print("  learned counts atom. The NACE caller writes learned efficacy as")
    print("  counts. For the filter to consume what the caller learns, extend")
    print("  efficacy-filter-step to read the learned atom in resolution order:")
    print("  observation > learned > declared-baseline > default. This is the")
    print("  one registry edit the caller build depends on. TEST 3 confirms the")
    print("  override path works today; the learned-atom path is the edit needed.")

    print(f"\n  Full output preserved at {log_path} inside the container.")
    print(f"  (host: shared_files/{log_path.split('/')[-1]})")


if __name__ == "__main__":
    main()
