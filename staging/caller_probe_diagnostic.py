#!/usr/bin/env python3
"""
caller_probe_diagnostic.py

Runs the caller-operations probe inside the clarity_omega container and prints
the caller-language fork verdict. Same model as capability_registry_diagnostic.py:
condensed verdict to stdout, full output to a timestamped container log.

WHAT IT SETTLES:
  The caller-language fork (MeTTa vs Python) by measuring whether the MeTTa
  runtime handles the caller's hardest operations cleanly. Probes:
    D1: count-update revision arithmetic (the caller's learning step)
    D2: native |- stv revision (availability check; error is valid data)
    E:  read-modify-write the efficacy atom in one invocation (the critical one)
    F:  full resolve-cycle chained end to end (the caller's inner loop)

FORK LOGIC (printed in the verdict):
  all clean (D1 computes, E composes, F chains)  -> build caller in MeTTa
  E fails (read-modify-write does not compose)   -> Python-first, port later
  D2 errors but D1/E/F clean                     -> MeTTa with counts form

USAGE (on the host where docker is available):
  python3 caller_probe_diagnostic.py
  Optional:
    --container NAME   (default: clarity_omega)
    --probe PATH       (default: /PeTTa/repos/omegaclaw/soul/caller_operations_probe.metta)
    --keep-temp        keep the combined temp file in the container
"""

import argparse
import datetime
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_PROBE = "/PeTTa/repos/omegaclaw/soul/caller_operations_probe.metta"


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


def evaluate(container, probe_path, keep_temp):
    """
    The probe is self-contained (no registry dependency). We still copy it to a
    temp file and run via run.sh, mirroring the runtime invocation, so the probe
    file in soul/ is not mutated and the run environment matches production.
    """
    rc, probe_text, err = run(["docker", "exec", container, "cat", probe_path])
    if rc != 0:
        return None, None, None, f"could not read probe: {err}"

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = f"/tmp/caller_probe_combined_{ts}.metta"
    bootstrap = "!(import! &self (library lib_import))\n"
    combined = bootstrap + probe_text + "\n"

    p = subprocess.run(
        ["docker", "exec", "-i", container, "sh", "-c", f"cat > {temp_path}"],
        input=combined, text=True, capture_output=True
    )
    if p.returncode != 0:
        return None, None, temp_path, f"failed to write temp file: {p.stderr}"

    rc, out, err = run(["docker", "exec", container, "sh", "-c",
                        f"cd /PeTTa && ./run.sh {temp_path} 2>&1"])

    # Write a full log into the container /tmp (maps to host shared_files/).
    log_path = f"/tmp/caller_probe_diagnostic_{ts}.log"
    full_log = f"returncode: {rc}\n\n===== OUTPUT =====\n{out}\n"
    subprocess.run(
        ["docker", "exec", "-i", container, "sh", "-c", f"cat > {log_path}"],
        input=full_log, text=True, capture_output=True
    )

    if not keep_temp:
        run(["docker", "exec", container, "rm", "-f", temp_path])

    return rc, out, log_path, None


def strip_ansi(text):
    """Remove ANSI color escapes (the evaluator colorizes its output)."""
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


def extract_results(output):
    """
    Extract the trailing block of reduction results.

    This evaluator (confirmed in prior runs) echoes all source lines and prolog
    goals first, then prints all results at the very end as a contiguous block
    of bare values in evaluation order. We collect the trailing non-noise lines.
    """
    output = strip_ansi(output)
    lines = [ln.rstrip() for ln in output.splitlines()]

    def is_noise(line):
        s = line.strip()
        if not s:
            return True
        for p in ("--> metta runnable", "-->  prolog goal", "--> metta sexpr",
                  ":-", "^^^^^^", "!(", "findall(", "match(", "reduce(",
                  "A),", "_).", "B),", "C),", "( B=C", "(import!",
                  "library(", "import_prolog"):
            if s.startswith(p):
                return True
        return False

    results = []
    for ln in reversed(lines):
        s = ln.strip()
        if not s:
            continue
        if is_noise(ln):
            if results:
                break
            continue
        results.append(s)
    results.reverse()
    return results


def classify(results):
    """
    Map the trailing results positionally to the probes.

    Expected substantive results in evaluation order (markers print as their
    own string; pure-arithmetic and match results are the substantive ones):

      PROBE D1:
        revise-confirmed     -> (counts invocations: 5 successes: 4)
        revise-disconfirmed  -> (counts invocations: 5 successes: 3)
        counts-te            -> 0.7  (a float)
      PROBE D2:
        |- result            -> a revised stv  OR  an error/unreduced expr
      PROBE E:
        current (before)     -> (counts invocations: 4 successes: 3)
        do-revise (ack)      -> true  (or a unit)
        current (after)      -> (counts invocations: 5 successes: 4)  IF compose
      PROBE F:
        resolve (ack)        -> true
        current (after)      -> revised counts
        resolved-invocation  -> ((100 confirmed))
        pending (after)      -> ()  (empty: removed)

    Because 'true' acks and marker strings interleave, we classify by content
    and by order of appearance among the substantive (non-'true') results.
    """
    findings = {}

    # Separate the substantive results (drop bare 'true' and marker echoes).
    subst = []
    for r in results:
        if r == "true":
            continue
        if r.startswith('"=== PROBE') or r.startswith('=== PROBE'):
            continue
        subst.append(r)

    findings["_substantive"] = subst

    # An UNREDUCED expression is one the evaluator returned unchanged because the
    # operator did not reduce. These are NOT results; their presence is the
    # finding. Detect by leading operator that should have reduced.
    def is_unreduced(r):
        s = r.strip()
        return (s.startswith("(|-") or s.startswith("(set-atom!")
                or s.startswith("(add-atom") or s.startswith("(remove-atom"))

    # POSITIONAL mapping over the substantive results, treating unreduced
    # expressions as markers-of-non-execution rather than as values.
    # Expected order of substantive (non-'true') results:
    #   0: D1 confirmed   (counts 5/4)
    #   1: D1 disconfirmed (counts 5/3)
    #   2: D1 te          (float)
    #   3: D2 |- result   (revised stv, OR unreduced (|- ...) = ABSENT)
    #   4: E before       (counts 4/3)
    #   5: E do-revise    (true/unit, OR unreduced (set-atom! ...) = did not execute)
    #   6: E after        (counts: 5/4 if composed, 4/3 if not)
    #   7: F resolve ack  (true/unit, OR unreduced)
    #   8: F efficacy     (counts: revised if composed, unchanged if not)
    #   9: F resolved     ((100 confirmed))
    #  10: F pending      (() empty)
    # We index the counts atoms and detect unreduced markers separately.
    counts_atoms = [r for r in subst if r.strip().startswith("(counts invocations:")]
    floats = [r.strip() for r in subst
              if re.fullmatch(r'-?\d+\.\d+', r.strip()) or re.fullmatch(r'0', r.strip())]

    def at(i):
        return counts_atoms[i] if len(counts_atoms) > i else None

    # D1: counts[0], counts[1], first float.
    findings["d1_confirmed"] = at(0)
    findings["d1_disconfirmed"] = at(1)
    findings["d1_te"] = floats[0] if floats else None

    # D2: a CLEAN stv result means |- reduced. An unreduced (|- ...) means ABSENT.
    d2 = None
    d2_unreduced = False
    for r in subst:
        if is_unreduced(r) and r.strip().startswith("(|-"):
            d2_unreduced = True
        elif "stv" in r and "cap-efficacy-stv" in r and not is_unreduced(r):
            d2 = r
    findings["d2"] = d2
    findings["d2_unreduced"] = d2_unreduced

    # E: detect whether do-revise executed. If an unreduced (set-atom! ...)
    # appears, the write did NOT execute. The decisive evidence is the
    # E-after read: counts index 3 (0,1 are D1; 2 is E-before; 3 is E-after).
    findings["e_setatom_unreduced"] = any(
        r.strip().startswith("(set-atom!") for r in subst)
    findings["e_before"] = at(2)
    findings["e_after"] = at(3)
    findings["e_before_ok"] = bool(at(2) and "invocations: 4 successes: 3" in at(2))
    # CRITICAL: after must be 5/4. If it is 4/3, the write did not take.
    findings["e_after_ok"] = bool(at(3) and "invocations: 5 successes: 4" in at(3))
    findings["e_after_unchanged"] = bool(at(3) and "invocations: 4 successes: 3" in at(3))

    # F: efficacy-after-resolve is counts index 4. Should be revised if composed.
    findings["f_efficacy"] = at(4)
    findings["f_efficacy_revised"] = bool(at(4) and "invocations: 4 successes: 3" not in at(4))
    findings["f_resolved_present"] = any("100" in r and "confirmed" in r for r in subst)
    findings["f_pending_empty"] = not any("pending-invocation" in r for r in subst)

    return findings


def verdict(findings):
    """Apply the fork logic and return (lines, fork_decision)."""
    out = []

    # D1
    d1_ok = (findings["d1_confirmed"] and "invocations: 5 successes: 4" in findings["d1_confirmed"]
             and findings["d1_disconfirmed"] and "invocations: 5 successes: 3" in findings["d1_disconfirmed"])
    out.append(("PROBE D1 (revision arithmetic)",
                "PASS" if d1_ok else "INSPECT",
                f"confirmed={findings['d1_confirmed']}, disconfirmed={findings['d1_disconfirmed']}, te={findings['d1_te']}"))

    # D2: unreduced (|- ...) means the operator did not reduce = ABSENT.
    if findings["d2"] and not findings["d2_unreduced"]:
        out.append(("PROBE D2 (native |- stv)", "AVAILABLE",
                    f"|- produced a revised stv: {findings['d2']}"))
        d2_available = True
    else:
        out.append(("PROBE D2 (native |- stv)", "ABSENT",
                    "|- returned unreduced (operator not defined here). Use counts form. Valid data, not failure."))
        d2_available = False

    # E (the critical one): the write must execute AND the after-read must show 5/4.
    e_ok = findings["e_before_ok"] and findings["e_after_ok"]
    if e_ok:
        e_note = "before(4/3) and after(5/4): set-atom! executed and composed in one invocation"
    elif findings["e_setatom_unreduced"] and findings["e_after_unchanged"]:
        e_note = "set-atom! returned UNREDUCED and after-read still 4/3: the write did NOT execute in this evaluation path"
    elif findings["e_after_unchanged"]:
        e_note = "after-read still 4/3: read-modify-write did not take"
    else:
        e_note = f"after-read not the expected 5/4: got {findings['e_after']}"
    out.append(("PROBE E (read-modify-write)",
                "PASS" if e_ok else "FAIL", e_note))

    # F: bookkeeping (add/remove) vs learning (revision). Separate them.
    f_bookkeeping = findings["f_resolved_present"] and findings["f_pending_empty"]
    f_learning = findings["f_efficacy_revised"]
    f_ok = f_bookkeeping and f_learning
    if f_ok:
        f_note = "resolved-invocation written, pending removed, AND efficacy revised: full cycle works"
    elif f_bookkeeping and not f_learning:
        f_note = f"bookkeeping works (audit written, pending removed) but efficacy NOT revised (still {findings['f_efficacy']}): same write blocker as E"
    else:
        f_note = f"resolved={findings['f_resolved_present']}, pending-empty={findings['f_pending_empty']}, efficacy-revised={f_learning}"
    out.append(("PROBE F (full resolve-cycle)",
                "PASS" if f_ok else "PARTIAL" if f_bookkeeping else "FAIL", f_note))

    # Fork decision
    if d1_ok and e_ok and f_ok:
        if d2_available:
            fork = ("BUILD CALLER IN METTA",
                    "All hardest operations run clean, including native |-. Caller is small, "
                    "port cost approaches zero. MeTTa wins on code-preservation.")
        else:
            fork = ("BUILD CALLER IN METTA (counts form)",
                    "Hardest operations run clean using the counts representation. Native |- "
                    "absent, so use counts (D1) not stv-merge. Caller still works in MeTTa.")
    elif not e_ok:
        fork = ("DO NOT BUILD YET: read-modify-write blocker found",
                "The caller's core resolve operation (read efficacy, set-atom! the revision) did "
                "NOT execute in standalone run.sh evaluation: set-atom! returned unreduced and the "
                "value did not change. D1 shows the arithmetic is fine; the blocker is the in-place "
                "mutation. RESOLVE THIS FIRST: determine whether set-atom! requires the live-loop "
                "evaluation context (vs standalone run.sh), a different mutation form, or a "
                "split read/write across evaluation boundaries. This bears on the caller's structure "
                "in EITHER language and must be understood before building.")
    else:
        fork = ("INSPECT BEFORE DECIDING",
                "Mixed results. Read the per-probe output and the raw block before choosing.")

    return out, fork


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--probe", default=DEFAULT_PROBE)
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    print("=" * 70)
    print("Caller Operations Probe: Fork Decision Diagnostic")
    print("=" * 70)

    print("\nPREFLIGHT")
    if not container_running(args.container):
        print(f"  [FAIL] container '{args.container}' not running")
        sys.exit(1)
    print(f"  [OK] container '{args.container}' running")
    if not container_file_exists(args.container, args.probe):
        print(f"  [FAIL] probe not found at {args.probe}")
        sys.exit(1)
    print(f"  [OK] probe: {args.probe}")

    print("\nEVALUATING (via run.sh)")
    rc, out, log_path, err = evaluate(args.container, args.probe, args.keep_temp)
    if err:
        print(f"  [FAIL] {err}")
        sys.exit(1)
    print(f"  evaluator returncode: {rc}")
    print(f"  full log: {log_path} (container; maps to host shared_files/)")

    results = extract_results(out)
    if not results:
        print("\n  [WARN] no result block extracted. Raw output (ANSI-stripped) below:")
        print("-" * 70)
        print(strip_ansi(out)[:3000])
        print("-" * 70)
        sys.exit(3)

    print("\n" + "=" * 70)
    print("RAW RESULT BLOCK (trailing reduction output, in order)")
    print("=" * 70)
    for r in results:
        print(f"  {r}")

    findings = classify(results)

    print("\n" + "=" * 70)
    print("PER-PROBE VERDICT")
    print("=" * 70)
    rows, fork = verdict(findings)
    for label, status, note in rows:
        print(f"  {label:32s} {status:10s} {note}")

    print("\n" + "=" * 70)
    print("FORK DECISION")
    print("=" * 70)
    print(f"  >>> {fork[0]}")
    print(f"  {fork[1]}")

    print(f"\n  Full output preserved at {log_path} inside the container.")
    print(f"  (host: shared_files/{log_path.split('/')[-1]})")


if __name__ == "__main__":
    main()
