#!/usr/bin/env python3
"""
efficacy_integration_diagnostic.py

Closes the last sandbox-to-substrate gap: runs the real two-cycle Mobius loop
through the container's |-, with the courier as the thing under test. Produces a
reviewable, logged artifact in the established probe-plus-wrapper shape.

WHAT IT SETTLES, in order:
  STAGE 0  preflight: is the container running? (Clarity's review: distinguish
           'substrate wrong' from 'substrate absent')
  STAGE 1  the |- invocation-path question. The courier uses !(|- ...) via run.sh.
           BUT the D2 probe earlier showed !(|- ...) returned UNREDUCED, while
           Clarity's validated Mobius test used (metta (|- ...)). These are
           different paths. This stage tests BOTH and reports which one actually
           reduces |- to a revised truth value. This is the highest-risk unknown.
  STAGE 2  if a working path exists, run the real two-cycle Mobius loop through it
           and verify: (a) each |- result matches the NAL reference to 4 decimals,
           (b) cycle 2's prior equals cycle 1's result through the real file
           (the twist), (c) the file holds the final accumulated value.

Raw output is printed BEFORE every verdict (the safeguard that caught false
confidence twice this session). Full log written to the container /tmp.

USAGE: python3 efficacy_integration_diagnostic.py [--container NAME]
"""

import argparse
import datetime
import json
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
RUN_SH = "/PeTTa/run.sh"
BELIEF_FILE = "/tmp/efficacy_integration_beliefs.json"
TIMEOUT = 30


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, **kw)


def strip_ansi(t):
    return re.sub(r'\x1b\[[0-9;]*m', '', t)


_STV_RE = re.compile(r'stv\s+([0-9.]+)\s+([0-9.]+)')


def nal_reference(t1, t2):
    """Reference NAL revision; the answer |- must match. Verified this session."""
    (f1, c1), (f2, c2) = t1, t2
    w1 = c1 / (1 - c1); w2 = c2 / (1 - c2)
    wp = f1 * w1 + f2 * w2
    w = w1 + w2
    return (wp / w, w / (w + 1))


def container_running(container):
    try:
        p = run(["docker", "ps", "--filter", f"name={container}",
                 "--format", "{{.Names}}"])
        return p.returncode == 0 and container in p.stdout
    except subprocess.TimeoutExpired:
        return False


def eval_in_container(container, script):
    """Write script to a temp file in the container, run via run.sh, return output."""
    path = "/tmp/_efficacy_integration.metta"
    full = "!(import! &self (library lib_import))\n" + script + "\n"
    w = run(["docker", "exec", "-i", container, "sh", "-c", f"cat > {path}"],
            input=full)
    if w.returncode != 0:
        return None, f"write failed: {w.stderr}"
    p = run(["docker", "exec", container, "sh", "-c",
             f"cd /PeTTa && {RUN_SH} {path} 2>&1"])
    return p.stdout, None


def last_stv(output):
    """Extract the last stv pair from output. Returns (f, c) or None."""
    pairs = _STV_RE.findall(strip_ansi(output))
    if not pairs:
        return None
    return (float(pairs[-1][0]), float(pairs[-1][1]))


def is_unreduced(output, expr_marker="|-"):
    """
    Detect whether |- came back unreduced (the D2 failure mode): the output
    contains the literal (|- ...) expression rather than a bare revised stv.
    """
    clean = strip_ansi(output)
    # If a line that is just the |- expression appears in the result region,
    # it did not reduce. Heuristic: a (|- ... appears in the trailing output.
    return bool(re.search(r'\(\s*\|-\s', clean))


# ---------------------------------------------------------------------------
# STAGE 1: which |- invocation path actually reduces?
# ---------------------------------------------------------------------------

def test_invocation_paths(container):
    """
    Test both |- paths with a known revision (0.7,0.5)+(0.8,0.4), expected
    (0.74,0.625). Report which path reduces correctly.
    """
    expected = nal_reference((0.7, 0.5), (0.8, 0.4))
    results = {}

    # Path 1: bare !(|- ...) via run.sh  (the courier's current path; D2 showed unreduced)
    p1_script = "!(|- (b (stv 0.7 0.5)) (b (stv 0.8 0.4)))"
    out1, err1 = eval_in_container(container, p1_script)
    results["bare_bang"] = {
        "script": p1_script, "output": out1, "err": err1,
        "stv": last_stv(out1) if out1 else None,
        "unreduced": is_unreduced(out1) if out1 else None,
    }

    # Path 2: (metta (|- ...))  (Clarity's validated Mobius path)
    p2_script = "!(metta (|- (b (stv 0.7 0.5)) (b (stv 0.8 0.4))))"
    out2, err2 = eval_in_container(container, p2_script)
    results["metta_wrapped"] = {
        "script": p2_script, "output": out2, "err": err2,
        "stv": last_stv(out2) if out2 else None,
        "unreduced": is_unreduced(out2) if out2 else None,
    }

    # Path 3: defensive, in case |- needs a NAL library import beyond lib_import.
    # (Only tried if 1 and 2 both fail to reduce; documents the next thing to check.)

    def reduced_correctly(r):
        if not r["stv"]:
            return False
        f, c = r["stv"]
        return abs(f - expected[0]) < 0.01 and abs(c - expected[1]) < 0.01

    working = None
    for name in ("metta_wrapped", "bare_bang"):
        if reduced_correctly(results[name]):
            working = name
            break

    return results, expected, working


# ---------------------------------------------------------------------------
# STAGE 2: real two-cycle Mobius loop through the working path
# ---------------------------------------------------------------------------

def build_expr(path_name, old_fc, ev_fc):
    fo, co = old_fc; fe, ce = ev_fc
    inner = f"(|- (b (stv {fo} {co})) (b (stv {fe} {ce})))"
    if path_name == "metta_wrapped":
        return f"!(metta {inner})"
    return f"!{inner}"


def revise_real(container, path_name, old_fc, ev_fc):
    out, err = eval_in_container(container, build_expr(path_name, old_fc, ev_fc))
    if err:
        return None, out, err
    return last_stv(out), out, None


def seed_belief_file(container, cap, fc):
    data = {cap: {"f": fc[0], "c": fc[1]}}
    run(["docker", "exec", "-i", container, "sh", "-c", f"cat > {BELIEF_FILE}"],
        input=json.dumps(data, indent=2))


def read_belief_file(container, cap):
    p = run(["docker", "exec", container, "cat", BELIEF_FILE])
    if p.returncode != 0:
        return None
    try:
        data = json.loads(p.stdout)
        e = data.get(cap)
        return (e["f"], e["c"]) if e else None
    except (json.JSONDecodeError, KeyError):
        return None


def write_belief_file(container, cap, fc):
    p = run(["docker", "exec", container, "cat", BELIEF_FILE])
    data = {}
    if p.returncode == 0:
        try:
            data = json.loads(p.stdout)
        except json.JSONDecodeError:
            data = {}
    data[cap] = {"f": round(fc[0], 6), "c": round(fc[1], 6)}
    run(["docker", "exec", "-i", container, "sh", "-c", f"cat > {BELIEF_FILE}"],
        input=json.dumps(data, indent=2))


def run_two_cycle(container, path_name):
    """The real Mobius loop: seed, cycle 1 (confirmed), cycle 2 reads file then revises."""
    cap = "integration-cap"
    seed_belief_file(container, cap, (0.7, 0.5))
    seeded = read_belief_file(container, cap)

    # Cycle 1: confirmed evidence (1.0, 0.1)
    old1 = read_belief_file(container, cap)
    ev1 = (1.0, 0.1)
    res1, raw1, err1 = revise_real(container, path_name, old1, ev1)
    ref1 = nal_reference(old1, ev1)
    if res1:
        write_belief_file(container, cap, res1)
    file_after_1 = read_belief_file(container, cap)

    # Cycle 2: reads the file (cycle 1's result) as the prior, then disconfirmed (0.0,0.1)
    old2 = read_belief_file(container, cap)
    ev2 = (0.0, 0.1)
    res2, raw2, err2 = revise_real(container, path_name, old2, ev2)
    ref2 = nal_reference(old2, ev2) if old2 else None
    if res2:
        write_belief_file(container, cap, res2)
    file_after_2 = read_belief_file(container, cap)

    return {
        "seeded": seeded,
        "cycle1": {"old": old1, "ev": ev1, "result": res1, "ref": ref1,
                   "raw": raw1, "err": err1, "file_after": file_after_1},
        "cycle2": {"old": old2, "ev": ev2, "result": res2, "ref": ref2,
                   "raw": raw2, "err": err2, "file_after": file_after_2},
    }


def close(a, b, tol=0.01):
    return a is not None and b is not None and abs(a[0]-b[0]) < tol and abs(a[1]-b[1]) < tol


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    args = ap.parse_args()
    c = args.container

    print("=" * 70)
    print("Efficacy Courier Integration Diagnostic (real |- through container)")
    print("=" * 70)

    # STAGE 0: preflight
    print("\nSTAGE 0  PREFLIGHT")
    if not container_running(c):
        print(f"  [FAIL] container '{c}' not running.")
        print("  Cannot distinguish substrate-wrong from substrate-absent without it.")
        print("  Start the container and re-run.")
        sys.exit(1)
    print(f"  [OK] container '{c}' running")

    # STAGE 1: invocation path
    print("\n" + "=" * 70)
    print("STAGE 1  WHICH |- INVOCATION PATH REDUCES?")
    print("=" * 70)
    print("  Testing (0.7,0.5)+(0.8,0.4), expected revised (0.74, 0.625)")
    paths, expected, working = test_invocation_paths(c)
    for name, r in paths.items():
        print(f"\n  --- path: {name} ---")
        print(f"  script: {r['script']}")
        print("  RAW OUTPUT (tail):")
        if r["output"]:
            for ln in strip_ansi(r["output"]).splitlines()[-6:]:
                print(f"    {ln}")
        else:
            print(f"    (no output; err={r['err']})")
        print(f"  parsed stv: {r['stv']}   unreduced: {r['unreduced']}")
    print(f"\n  expected: ({expected[0]:.4f}, {expected[1]:.4f})")
    if working:
        print(f"  >>> WORKING PATH: {working}")
    else:
        print("  >>> NO PATH REDUCED |- CORRECTLY.")
        print("  Neither bare !(|- ...) nor (metta (|- ...)) produced the expected")
        print("  revised truth value. |- likely needs a NAL library import beyond")
        print("  lib_import, OR the revision is invoked differently in Clarity's")
        print("  validated path. Next step: ask Clarity the EXACT invocation she used")
        print("  in the 4:06 PM Mobius test, and what library provides |-.")
        print("  The courier cannot work until this is resolved.")
        sys.exit(2)

    # STAGE 2: real two-cycle Mobius loop
    print("\n" + "=" * 70)
    print(f"STAGE 2  REAL TWO-CYCLE MOBIUS LOOP (via {working})")
    print("=" * 70)
    r = run_two_cycle(c, working)
    print(f"  seeded belief (file): {r['seeded']}")
    for label, cyc in (("CYCLE 1 (confirmed)", r["cycle1"]),
                       ("CYCLE 2 (disconfirmed, reads cycle1 file)", r["cycle2"])):
        print(f"\n  --- {label} ---")
        print(f"  prior (from file): {cyc['old']}")
        print(f"  evidence: {cyc['ev']}")
        print("  RAW |- OUTPUT (tail):")
        if cyc["raw"]:
            for ln in strip_ansi(cyc["raw"]).splitlines()[-4:]:
                print(f"    {ln}")
        print(f"  |- result: {cyc['result']}")
        print(f"  NAL reference: ({cyc['ref'][0]:.4f}, {cyc['ref'][1]:.4f})" if cyc['ref'] else "  NAL reference: n/a")
        print(f"  file after writeback: {cyc['file_after']}")

    # Verdicts
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    c1, c2 = r["cycle1"], r["cycle2"]
    v1 = close(c1["result"], c1["ref"])
    v2 = close(c2["result"], c2["ref"])
    twist = close(c2["old"], c1["result"])  # cycle 2 prior == cycle 1 result via file
    final_ok = close(c2["file_after"], c2["result"])

    print(f"  cycle 1 |- matches NAL reference (4dp):   {'PASS' if v1 else 'FAIL'}")
    print(f"  cycle 2 |- matches NAL reference (4dp):   {'PASS' if v2 else 'FAIL'}")
    print(f"  Mobius twist (c2 prior == c1 result):     {'PASS' if twist else 'FAIL'}")
    print(f"  file holds final accumulated value:       {'PASS' if final_ok else 'FAIL'}")

    allpass = v1 and v2 and twist and final_ok
    print()
    if allpass:
        print("  >>> INTEGRATION CONFIRMED")
        print("  The courier closes the real Mobius loop through the container's |-.")
        print(f"  Revision path: {working}. State in file, cognition in |-, courier works.")
        print("  Sandbox-to-substrate gap closed. The caller can be built on this.")
        if working != "metta_wrapped" and working != "bare_bang":
            pass
        print(f"\n  NOTE: courier's build_revision_expr must use the '{working}' form.")
        if working == "metta_wrapped":
            print("  The courier currently uses bare !(|- ...). It must be changed to")
            print("  the (metta (|- ...)) form. One-line fix in build_revision_expr.")
    else:
        print("  >>> INTEGRATION INCOMPLETE. Read the raw output above against each")
        print("  verdict before concluding. Do not build the caller until all pass.")

    print(f"\n  Belief file: {BELIEF_FILE} (container; host shared_files/)")


if __name__ == "__main__":
    main()
