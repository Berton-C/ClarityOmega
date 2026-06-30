#!/usr/bin/env python3
"""
verify_nace.py -- verifies the NACE substrate + courier in the live container.

Tests in order of dependency, each showing RAW output before its verdict:
  STAGE 1  the eager-evaluation risk Clarity flagged: does (current-efficacy cap)
           reduce to a concrete (stv f c) before |-nal matches? If not, |-nal
           won't fire and the whole chain fails. This is the make-or-break.
  STAGE 2  the full revise chain: updated-belief-atom returns the revised atom.
  STAGE 3  the courier two-cycle Mobius through the real beliefs file: cycle 1
           revises, writes; cycle 2 reads cycle 1's written value as prior.

HANDS ONLY. The reference formula CHECKS the substrate, never computes production.

USAGE: python3 verify_nace.py [--container clarity_omega]
"""
import argparse
import re
import subprocess
import sys

CONTAINER = "clarity_omega"
SOUL = "/PeTTa/repos/omegaclaw/soul"
DEFS_FILE = f"{SOUL}/nace_substrate.metta"
BELIEFS_FILE = f"{SOUL}/nace_beliefs.metta"
LIB_NAL = "!(import! &self (library omegaclaw lib_nal))"
TIMEOUT = 30


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, **kw)


def strip(o):
    return re.sub(r'\x1b\[[0-9;]*m', '', o or "")


def cat(container, path):
    return run(["docker", "exec", container, "cat", path]).stdout


def write(container, path, text):
    run(["docker", "exec", "-i", container, "sh", "-c", f"cat > {path}"], input=text)


def evaluate(container, body):
    """Load lib_nal + both NACE files, then run body. Return stdout."""
    defs = cat(container, DEFS_FILE)
    beliefs = cat(container, BELIEFS_FILE)
    script = LIB_NAL + "\n" + defs + "\n" + beliefs + "\n" + body + "\n"
    write(container, "/tmp/_verify_nace.metta", script)
    return run(["docker", "exec", container, "sh", "-c",
                "cd /PeTTa && ./run.sh /tmp/_verify_nace.metta 2>&1"]).stdout


_STV = re.compile(r'stv\s+([0-9.]+)\s+([0-9.]+)')


def last_stv(o):
    pairs = _STV.findall(strip(o))
    return (float(pairs[-1][0]), float(pairs[-1][1])) if pairs else None


def ref_revision(f1, c1, f2, c2):
    c2w = lambda c: c / (1 - c) if c < 1 else float('inf')
    w2c = lambda w: w / (w + 1)
    if c1 == 0:
        return (f2, c2)  # zero-weight prior: evidence determines result
    w1, w2 = c2w(c1), c2w(c2)
    w = w1 + w2
    f = (w1 * f1 + w2 * f2) / w
    return min(1.0, f), min(0.99, max(max(w2c(w), c1), c2))


def close(a, b, tol=0.01):
    return a and b and abs(a[0]-b[0]) < tol and abs(a[1]-b[1]) < tol


def show(o, n=6):
    for ln in strip(o).splitlines()[-n:]:
        print(f"    {ln}")


def container_up(container):
    p = run(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"])
    return p.returncode == 0 and container in p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=CONTAINER)
    a = ap.parse_args()
    c = a.container

    print("=" * 64)
    print("Verify NACE substrate + courier (live container)")
    print("=" * 64)
    if not container_up(c):
        print(f"  [FAIL] container '{c}' not running.")
        sys.exit(1)
    print(f"  [OK] container '{c}' running")

    results = {}

    # STAGE 1: the eager-evaluation risk Clarity named.
    print("\n" + "=" * 64)
    print("STAGE 1  does (current-efficacy web-search) reduce to a concrete stv?")
    print("=" * 64)
    out = evaluate(c, "!(current-efficacy web-search)")
    print("  RAW:"); show(out)
    got = last_stv(out)
    # web-search seeds at (0.5, 0.0); current-efficacy should return exactly that
    v1 = close(got, (0.5, 0.0))
    print(f"  reduced to: {got}   expected (0.5, 0.0)")
    print(f"  VERDICT: {'PASS' if v1 else 'FAIL -- if this echoes unreduced, |-nal cannot fire downstream'}")
    results["current-efficacy reduces"] = v1

    # STAGE 1b: does |-nal then fire on the reduced value?
    print("\n" + "=" * 64)
    print("STAGE 1b  does revise-efficacy fire |-nal on the reduced belief?")
    print("=" * 64)
    out = evaluate(c, "!(revise-efficacy web-search confirmed)")
    print("  RAW:"); show(out)
    got = last_stv(out)
    exp = ref_revision(0.5, 0.0, 1.0, 0.1)  # -> (1.0, 0.1)
    v1b = close(got, exp)
    print(f"  reduced to: {got}   reference ({exp[0]:.4f}, {exp[1]:.4f})")
    print(f"  VERDICT: {'PASS' if v1b else 'FAIL'}")
    results["revise-efficacy fires |-nal"] = v1b

    # STAGE 2: the write-back atom form.
    print("\n" + "=" * 64)
    print("STAGE 2  updated-belief-atom returns the persistable atom")
    print("=" * 64)
    out = evaluate(c, "!(updated-belief-atom web-search confirmed)")
    print("  RAW:"); show(out)
    clean = strip(out)
    has = "cap-efficacy" in clean and "web-search" in clean
    # reject if the inner expression did not reduce (must be a bare stv, not
    # an unevaluated Truth_Revision/|-nal sitting inside the atom)
    unreduced_inner = "Truth_Revision" in clean or "|-nal" in clean
    # the atom must contain exactly (cap-efficacy web-search (stv f c))
    clean_atom = re.search(
        r'\(cap-efficacy\s+web-search\s+\(stv\s+[0-9.]+\s+[0-9.]+\)\)', clean)
    v2 = has and not unreduced_inner and bool(clean_atom) and close(last_stv(out), exp)
    print(f"  contains (cap-efficacy web-search ...): {has}")
    print(f"  inner expression reduced (no Truth_Revision/|-nal left): {not unreduced_inner}")
    print(f"  atom is clean (cap-efficacy web-search (stv f c)): {bool(clean_atom)}")
    print(f"  VERDICT: {'PASS' if v2 else 'FAIL'}")
    results["updated-belief-atom"] = v2

    # STAGE 2b: the dispatch gate (efficacy-expectation + should-dispatch).
    # These nest function calls as ARGUMENTS (not inside a data atom), so they
    # should reduce the way revise-efficacy did in Stage 1b. This confirms it.
    print("\n" + "=" * 64)
    print("STAGE 2b  efficacy-expectation + should-dispatch (the gate)")
    print("=" * 64)
    out = evaluate(c, "!(efficacy-expectation web-search)")
    print("  RAW (expectation):"); show(out, 3)
    # agnostic (0.5, 0.0): Truth_Expectation = 0.0*(0.5-0.5)+0.5 = 0.5
    exp_num = None
    m = re.search(r'(?<![0-9.])(0\.\d+|[01])(?![0-9.])', strip(out).splitlines()[-1]) if strip(out).splitlines() else None
    out2 = evaluate(c, "!(should-dispatch web-search)")
    print("  RAW (should-dispatch):"); show(out2, 3)
    clean2 = strip(out2)
    gate_true = "True" in clean2
    gate_false = "False" in clean2
    # expectation 0.5 >= 0.3 so gate should be True; and it must actually reduce
    # (not echo the unreduced (should-dispatch web-search) expression)
    reduced = gate_true or gate_false
    v2b = gate_true and not gate_false
    print(f"  gate reduced to a boolean: {reduced}")
    print(f"  gate returned True (0.5 >= 0.3): {gate_true}")
    print(f"  VERDICT: {'PASS' if v2b else 'FAIL'}")
    results["should-dispatch gate"] = v2b

    # STAGE 3: courier two-cycle Mobius through the real beliefs file.
    print("\n" + "=" * 64)
    print("STAGE 3  courier two-cycle Mobius (writes the real beliefs file)")
    print("=" * 64)
    import importlib.util
    spec = importlib.util.spec_from_file_location("nc", "soul/nace_courier.py")
    try:
        nc = importlib.util.module_from_spec(spec); spec.loader.exec_module(nc)
        nc.CONTAINER = c
    except Exception as e:
        print(f"  [SKIP] could not import nace_courier.py: {e}")
        nc = None

    v3 = False
    if nc:
        # snapshot the beliefs file so we can restore it after the test
        original = cat(c, BELIEFS_FILE)
        try:
            a1 = nc.cycle("web-search", "confirmed")
            f1 = last_stv(a1)
            print(f"  cycle 1 (confirmed): wrote {a1}")
            a2 = nc.cycle("web-search", "confirmed")
            f2 = last_stv(a2)
            print(f"  cycle 2 (confirmed, reads cycle 1 as prior): wrote {a2}")
            # cycle 2 prior is cycle 1 result (f1); revise with confirmed again
            exp2 = ref_revision(f1[0], f1[1], 1.0, 0.1)
            twist = close(f2, exp2)
            file_now = last_stv(cat(c, BELIEFS_FILE))
            persisted = close(file_now, f2)
            print(f"  cycle 2 reference (prior {f1} + confirmed): ({exp2[0]:.4f}, {exp2[1]:.4f})")
            print(f"  beliefs file now holds: {file_now}")
            v3 = twist and persisted
            print(f"  Mobius twist (c2 used c1 as prior): {twist}")
            print(f"  file persisted c2 result: {persisted}")
        finally:
            write(c, BELIEFS_FILE, original)  # restore
            print("  (beliefs file restored to original)")
    print(f"  VERDICT: {'PASS' if v3 else 'FAIL'}")
    results["courier two-cycle Mobius"] = v3

    # SUMMARY
    print("\n" + "=" * 64)
    print("SUMMARY")
    print("=" * 64)
    for k, v in results.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    if all(results.values()):
        print("\n  >>> NACE VERIFIED IN SUBSTRATE. Cognition is |-nal; Python is hands.")
        print("  The courier closes the Mobius loop through the real beliefs file.")
    else:
        print("\n  >>> NOT VERIFIED. Read each RAW block against its verdict.")
        if not results.get("current-efficacy reduces"):
            print("  STAGE 1 is the root: current-efficacy did not reduce to a concrete")
            print("  stv, so |-nal cannot match. This is the eager-eval risk Clarity named.")


if __name__ == "__main__":
    main()
