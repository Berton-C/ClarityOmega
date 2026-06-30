#!/usr/bin/env python3
"""
probe_nesting_contradiction.py

Isolates one contradiction from the last verify run:
  Stage 1b: (Truth_Revision (current-efficacy web-search) (evidence-stv confirmed))
            REDUCED to (1.0, 0.1).   [two-arg, function-call args]
  Stage 2b: (Truth_Expectation (current-efficacy web-search))
            did NOT reduce.          [one-arg, function-call arg]

Same nesting shape (function-call passed as arg to a truth function), opposite
results. This probe pins down WHICH difference matters, with raw output before
every verdict. No fixes applied. Diagnosis only.

Tests, each loading lib_nal + both NACE files:
  A  Truth_Expectation on a LITERAL stv         -> does the fn work at all?
  B  Truth_Expectation on a function-call arg   -> reproduces Stage 2b failure?
  C  Truth_Revision on function-call args       -> reproduces Stage 1b success?
  D  Truth_Expectation on a let-bound result    -> does binding force it?
  E  Truth_Revision on a LITERAL + literal      -> control for A's counterpart

USAGE: python3 staging/probe_nesting_contradiction.py
"""
import re
import subprocess
import sys

CONTAINER = "clarity_omega"
SOUL = "/PeTTa/repos/omegaclaw/soul"
DEFS = f"{SOUL}/nace_substrate.metta"
BELIEFS = f"{SOUL}/nace_beliefs.metta"
LIB_NAL = "!(import! &self (library omegaclaw lib_nal))"
TIMEOUT = 30


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, **kw)


def strip(o):
    return re.sub(r'\x1b\[[0-9;]*m', '', o or "")


def cat(path):
    return run(["docker", "exec", CONTAINER, "cat", path]).stdout


def evaluate(body):
    defs = cat(DEFS)
    beliefs = cat(BELIEFS)
    script = LIB_NAL + "\n" + defs + "\n" + beliefs + "\n" + body + "\n"
    run(["docker", "exec", "-i", CONTAINER, "sh", "-c",
         "cat > /tmp/_probe_nest.metta"], input=script)
    return run(["docker", "exec", CONTAINER, "sh", "-c",
                "cd /PeTTa && ./run.sh /tmp/_probe_nest.metta 2>&1"]).stdout


def tail(o, n=4):
    for ln in strip(o).splitlines()[-n:]:
        print(f"    {ln}")


def reduced(o):
    """True if output shows a bare (stv f c) or a number, not an unreduced fn call."""
    clean = strip(o)
    # unreduced if the truth-function name still appears in the result region
    return not ("Truth_Expectation" in clean.splitlines()[-1] if clean.splitlines() else True) \
        or bool(re.search(r'\(stv\s+[0-9.]+\s+[0-9.]+\)\s*$', clean.strip())) \
        or bool(re.search(r'(?<![A-Za-z_])[01]\.\d+\s*$', clean.strip()))


def show(label, body):
    print("\n" + "=" * 64)
    print(label)
    print("=" * 64)
    print(f"  EXPR: {body}")
    out = evaluate(body)
    print("  RAW:")
    tail(out)
    return out


def main():
    if CONTAINER not in run(["docker", "ps", "--format", "{{.Names}}"]).stdout:
        print(f"container '{CONTAINER}' not running"); sys.exit(1)

    # A: Truth_Expectation on a literal stv. Baseline: does the fn reduce at all?
    a = show("A  Truth_Expectation on LITERAL stv (does the fn work?)",
             "!(Truth_Expectation (stv 0.5 0.0))")
    # expected 0.5

    # B: Truth_Expectation on a function-call arg (reproduces Stage 2b)
    b = show("B  Truth_Expectation on (current-efficacy web-search)  [Stage 2b]",
             "!(Truth_Expectation (current-efficacy web-search))")

    # C: Truth_Revision on function-call args (reproduces Stage 1b)
    cc = show("C  Truth_Revision on (current-efficacy ..) (evidence-stv ..)  [Stage 1b]",
              "!(Truth_Revision (current-efficacy web-search) (evidence-stv confirmed))")

    # D: Truth_Expectation on a let-bound result (does binding force it?)
    d = show("D  Truth_Expectation on a let-bound current-efficacy",
             "!(let $b (current-efficacy web-search) (Truth_Expectation $b))")

    # E: Truth_Revision on two literal stv (control)
    e = show("E  Truth_Revision on two LITERAL stv (control)",
             "!(Truth_Revision (stv 0.5 0.0) (stv 1.0 0.1))")

    print("\n" + "=" * 64)
    print("DIAGNOSIS GUIDE (read the RAW blocks above)")
    print("=" * 64)
    print("""
  A reduces, B does not  -> Truth_Expectation works on literals but not on a
      function-call arg. The single-arg fn does NOT reduce its argument first.
  C reduces, B does not  -> the difference is the FUNCTION, not the nesting.
      Truth_Revision reduces its call-args; Truth_Expectation does not.
      (Likely: Truth_Revision's head matches (stv ..)(stv ..) two-arg and the
       evaluator reduces args to match; Truth_Expectation's path differs.)
  D reduces, B does not  -> binding forces it. The fix is let-bind the inner
      call, THEN pass the variable. (Different from the let we tried, because
      here the inner call is the whole arg, not buried in revise-efficacy.)
  D also fails           -> binding does NOT force it; the issue is deeper and
      the fix is to make current-efficacy's result reach the fn already as a
      literal stv (e.g. compute expectation a different way, or restructure).
  E reduces              -> confirms Truth_Revision/Truth_Expectation work on
      literals; isolates the problem to function-call arguments specifically.

  The combination of which pass/fail tells us the exact fix with no guessing.
""")


if __name__ == "__main__":
    main()
