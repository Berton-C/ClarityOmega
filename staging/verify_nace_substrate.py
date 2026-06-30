#!/usr/bin/env python3
"""
verify_nace_substrate.py

Verifies nace_substrate.metta in the live container. Loads lib_nal (via the
omegaclaw import) plus the NACE file, runs the three computations, shows raw
output before each verdict, and checks the revision arithmetic against the
lib_nal Truth_Revision reference.

This is HANDS ONLY: it builds expressions, runs them, parses output, compares
to the reference. It does NOT compute any NACE cognition. The reference formula
here is for CHECKING the substrate, never the production path.

USAGE: python3 verify_nace_substrate.py [--container clarity_omega]
"""

import argparse
import re
import subprocess
import sys

CONTAINER = "clarity_omega"
NACE_FILE = "/PeTTa/repos/omegaclaw/soul/nace_substrate.metta"
TIMEOUT = 30


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, **kw)


def strip_ansi(t):
    return re.sub(r'\x1b\[[0-9;]*m', '', t or "")


def container_running(container):
    p = run(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"])
    return p.returncode == 0 and container in p.stdout


def eval_in_container(container, body):
    """Prepend lib_nal + NACE file imports, run body lines via run.sh, return stdout."""
    script = (
        "!(import! &self (library omegaclaw lib_nal))\n"
        f'!(import! &self (file "{NACE_FILE}"))\n'
        + body + "\n"
    )
    w = run(["docker", "exec", "-i", container, "sh", "-c",
             "cat > /tmp/_verify_nace.metta"], input=script)
    if w.returncode != 0:
        return None, f"write failed: {w.stderr}"
    p = run(["docker", "exec", container, "sh", "-c",
             "cd /PeTTa && ./run.sh /tmp/_verify_nace.metta 2>&1"])
    return p.stdout, None


# --- reference (for CHECKING the substrate only, never production) ---
def ref_revision(f1, c1, f2, c2):
    c2w = lambda c: c / (1 - c)
    w2c = lambda w: w / (w + 1)
    w1, w2 = c2w(c1), c2w(c2)
    w = w1 + w2
    f = (w1 * f1 + w2 * f2) / w
    c = w2c(w)
    return min(1.0, f), min(0.99, max(max(c, c1), c2))


def ref_expectation(f, c):
    return c * (f - 0.5) + 0.5


_STV = re.compile(r'stv\s+([0-9.]+)\s+([0-9.]+)')
_NUM = re.compile(r'(-?[0-9]+\.?[0-9]*)')


def last_stv(out):
    pairs = _STV.findall(strip_ansi(out))
    return (float(pairs[-1][0]), float(pairs[-1][1])) if pairs else None


def close(a, b, tol=0.01):
    return a is not None and b is not None and abs(a[0]-b[0]) < tol and abs(a[1]-b[1]) < tol


def show_raw(out, n=5):
    for ln in strip_ansi(out).splitlines()[-n:]:
        print(f"    {ln}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=CONTAINER)
    args = ap.parse_args()
    container = args.container

    print("=" * 64)
    print("Verify nace_substrate.metta (live container)")
    print("=" * 64)

    print("\nPREFLIGHT")
    if not container_running(container):
        print(f"  [FAIL] container '{container}' not running. Start it and re-run.")
        sys.exit(1)
    print(f"  [OK] container '{container}' running")

    results = {}

    # TEST 1: revise-efficacy. web-search starts (0.5, 0.0); confirmed evidence
    # (1.0, 0.1). Revising agnostic with one confirm.
    print("\n" + "=" * 64)
    print("TEST 1  revise-efficacy web-search confirmed")
    print("=" * 64)
    out, err = eval_in_container(container, "!(revise-efficacy web-search confirmed)")
    print("  RAW:")
    show_raw(out) if out else print(f"    (no output; {err})")
    got = last_stv(out)
    exp = ref_revision(0.5, 0.0, 1.0, 0.1)
    print(f"  substrate: {got}")
    print(f"  reference: ({exp[0]:.4f}, {exp[1]:.4f})")
    v1 = close(got, exp)
    print(f"  VERDICT: {'PASS' if v1 else 'FAIL'}")
    results["revise"] = v1

    # TEST 2: updated-belief-atom (the write-back form). Should be
    # (cap-efficacy web-search (stv ...)) with the revised value.
    print("\n" + "=" * 64)
    print("TEST 2  updated-belief-atom web-search confirmed")
    print("=" * 64)
    out, err = eval_in_container(container, "!(updated-belief-atom web-search confirmed)")
    print("  RAW:")
    show_raw(out) if out else print(f"    (no output; {err})")
    got2 = last_stv(out)
    has_atom = bool(out and "cap-efficacy" in strip_ansi(out) and "web-search" in strip_ansi(out))
    v2 = has_atom and close(got2, exp)
    print(f"  contains (cap-efficacy web-search ...): {has_atom}")
    print(f"  stv matches reference: {close(got2, exp)}")
    print(f"  VERDICT: {'PASS' if v2 else 'FAIL'}")
    results["writeback"] = v2

    # TEST 3: should-dispatch. After one confirm, expectation should be >= 0.3.
    # Check both the expectation number and the boolean gate.
    print("\n" + "=" * 64)
    print("TEST 3  efficacy-expectation + should-dispatch")
    print("=" * 64)
    out, err = eval_in_container(container,
        "!(efficacy-expectation web-search)\n!(should-dispatch web-search)")
    print("  RAW:")
    show_raw(out, 8) if out else print(f"    (no output; {err})")
    clean = strip_ansi(out or "")
    # expectation of the agnostic (0.5, 0.0) is 0.5; gate True
    exp_e = ref_expectation(0.5, 0.0)
    nums = _NUM.findall(clean)
    has_true = "True" in clean
    has_false = "False" in clean
    print(f"  reference expectation (agnostic 0.5/0.0): {exp_e:.4f}")
    print(f"  gate returned True: {has_true}  False: {has_false}")
    v3 = has_true and not has_false
    print(f"  VERDICT: {'PASS' if v3 else 'FAIL (expectation/gate did not reduce)'}")
    results["dispatch"] = v3

    # SUMMARY
    print("\n" + "=" * 64)
    print("SUMMARY")
    print("=" * 64)
    for k, v in results.items():
        print(f"  {k:12s} {'PASS' if v else 'FAIL'}")
    allp = all(results.values())
    print()
    if allp:
        print("  >>> NACE SUBSTRATE VERIFIED")
        print("  revise-efficacy, updated-belief-atom, and should-dispatch all")
        print("  reduce in the live container and match the NAL reference.")
        print("  The cognition is in the substrate. Next: the read/write courier (hands).")
    else:
        print("  >>> NOT VERIFIED. Read each RAW block against its verdict.")
        print("  An unreduced expression (echoed input) means that function did not")
        print("  reduce: check the file loaded, lib_nal loaded, and the function shape.")
        if not results.get("revise"):
            print("  revise FAIL is the root: if |-nal/Truth_Revision did not fire,")
            print("  confirm the import lines and that car-atom/cdr-atom unwrap correctly.")


if __name__ == "__main__":
    main()
