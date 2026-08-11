#!/usr/bin/env python3
"""
efficacy_courier.py

The capability-registry NACE caller's read-compute-writeback piece.

ARCHITECTURE (settled 2026-05-31, see ClarityOmega_NACE_Persistence_Architecture.md):
  State lives in a FILE. Cognition lives in MeTTa's |-. Python is the COURIER.
  This module is the courier: it reads the efficacy belief from the file, asks
  MeTTa's |- to revise it given new evidence, and writes the result back.
  Python does NOT compute the revision. The revision is MeTTa's |-.

The Mobius twist: the belief written by one cycle is read back as the prior for
the next. revise() does not hold state; the file does.

The single point that touches the substrate is `revise_via_metta`, which invokes
run.sh with a one-line |- expression. Everything else is pure Python (file I/O,
evidence mapping, lifecycle) and is testable in isolation.

Belief file format (JSON, one entry per capability):
  { "handler-name": {"f": 0.7, "c": 0.5}, ... }

Evidence convention (NAL):
  confirmed    -> (f=1.0, c=0.1)   positive evidence, low confidence per observation
  disconfirmed -> (f=0.0, c=0.1)   negative evidence
  ambiguous    -> no revision (returns belief unchanged)
"""

import json
import os
import re
import subprocess


# ---------------------------------------------------------------------------
# File storage (the notebook)
# ---------------------------------------------------------------------------

def load_beliefs(belief_file):
    """Read the whole belief store. Returns {} if the file does not exist."""
    if not os.path.exists(belief_file):
        return {}
    try:
        with open(belief_file) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        # Clarity's review: silently returning {} on a corrupt file is a
        # learning-lobotomy disguised as graceful degradation. The next write
        # would overwrite the corrupt file with defaults, erasing all learning.
        # Raise instead, so corruption is visible and not silently healed-over.
        raise ValueError(
            f"belief file {belief_file} is corrupt: {e}. "
            f"Refusing to proceed and overwrite learned beliefs with defaults. "
            f"Inspect or restore the file.") from e
    except OSError as e:
        raise OSError(f"could not read belief file {belief_file}: {e}") from e


def read_belief(cap, belief_file, default=(0.5, 0.0)):
    """Read one capability's belief as (f, c). Default is agnostic (0.5, 0.0)."""
    beliefs = load_beliefs(belief_file)
    entry = beliefs.get(cap)
    if not entry:
        return default
    return (entry["f"], entry["c"])


def _validate_fc(fc):
    """
    Validate a truth value before writing. Clarity's review: |- will faithfully
    incorporate garbage if the courier writes garbage. f and c must be in [0,1].
    Confidence of exactly 1.0 is also rejected: NAL confidence asymptotes to 1
    but never reaches it (c = w/(w+1) < 1 for finite evidence), so c == 1.0
    signals a computation error, not a valid belief.
    """
    f, c = fc
    if not (isinstance(f, (int, float)) and isinstance(c, (int, float))):
        raise ValueError(f"truth value must be numeric, got {fc!r}")
    if not (0.0 <= f <= 1.0):
        raise ValueError(f"frequency out of range [0,1]: {f}")
    if not (0.0 <= c < 1.0):
        raise ValueError(f"confidence out of range [0,1): {c} (c must be < 1)")


def write_belief(cap, fc, belief_file):
    """Write one capability's belief back to the file. fc is (f, c)."""
    _validate_fc(fc)
    beliefs = load_beliefs(belief_file)
    beliefs[cap] = {"f": round(fc[0], 6), "c": round(fc[1], 6)}
    # Write atomically: temp then rename, so a crash mid-write does not corrupt.
    tmp = belief_file + ".tmp"
    with open(tmp, "w") as f:
        json.dump(beliefs, f, indent=2)
    os.replace(tmp, belief_file)
    return beliefs[cap]


# ---------------------------------------------------------------------------
# Evidence mapping (mechanical, not reasoning)
# ---------------------------------------------------------------------------

def evidence_for(outcome):
    """
    Map a classified outcome to NAL evidence (f, c), or None for no-revision.
      confirmed    -> (1.0, 0.1)
      disconfirmed -> (0.0, 0.1)
      ambiguous    -> None (no evidence, no revision)
    """
    if outcome == "confirmed":
        return (1.0, 0.1)
    if outcome == "disconfirmed":
        return (0.0, 0.1)
    if outcome == "ambiguous":
        return None
    raise ValueError(f"unknown outcome: {outcome!r}")


# ---------------------------------------------------------------------------
# The revision (MeTTa's |-, the one substrate touch)
# ---------------------------------------------------------------------------

def build_revision_expr(old_fc, evidence_fc):
    """
    Build the single-invocation |- expression. The belief is carried as a
    minimal atom shape; only the stv values matter for the revision.
      (|- (b (stv f_old c_old)) (b (stv f_ev c_ev)))
    """
    fo, co = old_fc
    fe, ce = evidence_fc
    return f"!(|- (b (stv {fo} {co})) (b (stv {fe} {ce})))"


_STV_RE = re.compile(r'stv\s+([0-9.]+)\s+([0-9.]+)')


def parse_revision_result(output):
    """
    Parse the revised (f, c) out of run.sh output. The result block contains the
    revised expression; we extract the LAST stv pair (the revision result).
    Returns (f, c) or None if not found.
    """
    # Strip ANSI, take all stv pairs, the revised result is the last one printed.
    clean = re.sub(r'\x1b\[[0-9;]*m', '', output)
    pairs = _STV_RE.findall(clean)
    if not pairs:
        return None
    f, c = pairs[-1]
    return (float(f), float(c))


def revise_via_metta(old_fc, evidence_fc, container="clarity_omega",
                     run_sh="/PeTTa/run.sh", _runner=None, timeout=30):
    """
    Invoke MeTTa's |- to revise old_fc with evidence_fc. Returns (f, c).

    The actual substrate call goes through run.sh in the container. The _runner
    parameter allows injecting a test double in the sandbox (where there is no
    container); in production _runner is None and the real docker exec runs.

    THIS IS THE ONLY FUNCTION THAT TOUCHES THE SUBSTRATE. The revision arithmetic
    is MeTTa's, not Python's. Python builds the expression, MeTTa computes, Python
    parses the result.

    timeout (Clarity's review): docker exec has a timeout so a hung container
    cannot hang the courier indefinitely. On timeout, raises subprocess.TimeoutExpired.
    """
    expr = build_revision_expr(old_fc, evidence_fc)

    if _runner is not None:
        # Test path: the injected runner returns the raw output string.
        output = _runner(expr)
    else:
        # Production path: write the expr to a temp file, run via run.sh.
        # (A single bare |- line; the library bootstrap is prepended.)
        script = f"!(import! &self (library lib_import))\n{expr}\n"
        write = subprocess.run(
            ["docker", "exec", "-i", container, "sh", "-c",
             "cat > /tmp/_efficacy_revise.metta"],
            input=script, text=True, capture_output=True, timeout=timeout)
        if write.returncode != 0:
            raise RuntimeError(f"failed to write revision script: {write.stderr}")
        proc = subprocess.run(
            ["docker", "exec", container, "sh", "-c",
             f"cd /PeTTa && {run_sh} /tmp/_efficacy_revise.metta 2>&1"],
            capture_output=True, text=True, timeout=timeout)
        output = proc.stdout

    result = parse_revision_result(output)
    if result is None:
        raise RuntimeError(f"could not parse revision result from:\n{output[:500]}")
    return result


# ---------------------------------------------------------------------------
# The read-compute-writeback cycle (the Mobius loop, one step)
# ---------------------------------------------------------------------------

def resolve_one(cap, outcome, belief_file, container="clarity_omega", _runner=None):
    """
    One read-compute-writeback step for one capability's efficacy.

      1. read  the current belief from the file
      2. map   the outcome to evidence (or no-op for ambiguous)
      3. revise via MeTTa |-  (the cognition, in the substrate)
      4. write the revised belief back to the file

    Returns a dict describing what happened, for the caller's audit log.
    The revised belief becomes the prior for the next cycle (the Mobius twist),
    because it is now in the file that the next read_belief will load.
    """
    old = read_belief(cap, belief_file)
    ev = evidence_for(outcome)

    if ev is None:
        # ambiguous: no evidence, no revision. The belief is unchanged.
        return {"cap": cap, "outcome": outcome, "old": old, "new": old,
                "revised": False, "reason": "ambiguous-no-evidence"}

    new = revise_via_metta(old, ev, container=container, _runner=_runner)
    written = write_belief(cap, new, belief_file)
    return {"cap": cap, "outcome": outcome, "old": old, "new": new,
            "written": written, "revised": True}


# ---------------------------------------------------------------------------
# Truth expectation (for the filter step's threshold check; pure read-side)
# ---------------------------------------------------------------------------

def truth_expectation(fc):
    """
    Canonical NAL-standard truth expectation: te = f*c + 0.5*(1-c).
    Used by the efficacy-filter-step to gate dispatch (threshold 0.3).
    This is a READ-side computation (deciding eligibility), not the revision.
    """
    f, c = fc
    return f * c + 0.5 * (1 - c)


if __name__ == "__main__":
    # Self-test in the sandbox using an injected runner that mimics run.sh
    # output for the |- revision. The reference arithmetic is the NAL formula
    # validated this session (cycle convergence verified to four decimals).
    import tempfile

    def nal_revise_reference(f1, c1, f2, c2):
        """Reference NAL revision, the answer MeTTa's |- must match."""
        w1 = c1 / (1 - c1); w2 = c2 / (1 - c2)
        wp1 = f1 * w1; wp2 = f2 * w2
        w = w1 + w2; wp = wp1 + wp2
        return (wp / w, w / (w + 1))

    def fake_runner(expr):
        """Mimic run.sh: parse the two stv pairs from expr, return NAL revision."""
        pairs = _STV_RE.findall(expr)
        (f1, c1), (f2, c2) = [(float(a), float(b)) for a, b in pairs]
        rf, rc = nal_revise_reference(f1, c1, f2, c2)
        # Mimic run.sh printing the revised expression with the result stv last.
        return f"--> metta runnable -->\n(b (stv {rf:.6f} {rc:.6f}))\n"

    print("=== efficacy_courier self-test (sandbox, injected runner) ===\n")

    bf = tempfile.mktemp(suffix=".json")

    # Seed a belief, then run TWO resolve cycles (the Mobius twist test).
    write_belief("test-cap", (0.7, 0.5), bf)
    print(f"seeded: {read_belief('test-cap', bf)}")

    # Cycle 1: confirmed evidence (1.0, 0.1)
    r1 = resolve_one("test-cap", "confirmed", bf, _runner=fake_runner)
    print(f"cycle 1 (confirmed): {r1['old']} -> {r1['new']}")

    # Cycle 2: reads cycle 1's file output as the prior (the twist), disconfirmed
    r2 = resolve_one("test-cap", "disconfirmed", bf, _runner=fake_runner)
    print(f"cycle 2 (disconfirmed): {r2['old']} -> {r2['new']}")

    # The decisive check: cycle 2's OLD must equal cycle 1's NEW (read from file).
    twist_ok = (r2["old"] == r1["new"])
    print(f"\nMobius twist (cycle 2 prior == cycle 1 result, via file): {twist_ok}")

    # Ambiguous: no revision
    r3 = resolve_one("test-cap", "ambiguous", bf, _runner=fake_runner)
    print(f"cycle 3 (ambiguous): revised={r3['revised']} (expect False)")

    # Truth expectation read-side
    te = truth_expectation(read_belief("test-cap", bf))
    print(f"truth expectation of final belief: {te:.4f}")

    os.remove(bf)
    print("\nself-test complete:",
          "PASS" if (twist_ok and not r3["revised"]) else "CHECK OUTPUT")
