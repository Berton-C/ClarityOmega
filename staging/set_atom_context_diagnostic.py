#!/usr/bin/env python3
"""
set_atom_context_diagnostic.py

Runs the set-atom! execution-context probe (five frames) inside the
clarity_omega container and prints which invocation context(s) actually
perform the mutation. Same model as the other diagnostics: condensed verdict
to stdout, full output to a timestamped container log.

WHAT IT SETTLES:
  How to write the caller's mutation so set-atom! actually executes. Tests five
  framings, each with its own cap atom, each ending in a read-back:
    A: bare top-level writer call         (control; expect the known failure)
    B: writer called inside let* binding  (the loop hook context)
    C: set-atom! wrapped in explicit eval  (forcing, loop lines 134/155)
    D: set-atom! inlined directly in let*  (loop lines 95/100 pattern)
    E: progn with set-atom! in body position (Clarity's finding; do-set-phase! precedent)

DECISIVE OBSERVABLE per frame: the AFTER read.
    (counts invocations: 5 successes: 4) = mutation TOOK in that context
    (counts invocations: 4 successes: 3) = mutation did NOT take

USAGE (on the host where docker is available):
  python3 set_atom_context_diagnostic.py
  Optional:
    --container NAME   (default: clarity_omega)
    --probe PATH       (default: /PeTTa/repos/omegaclaw/soul/set_atom_context_probe.metta)
    --keep-temp
"""

import argparse
import datetime
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_PROBE = "/PeTTa/repos/omegaclaw/soul/set_atom_context_probe.metta"


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
    rc, probe_text, err = run(["docker", "exec", container, "cat", probe_path])
    if rc != 0:
        return None, None, f"could not read probe: {err}"

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = f"/tmp/set_atom_probe_combined_{ts}.metta"
    combined = "!(import! &self (library lib_import))\n" + probe_text + "\n"

    p = subprocess.run(
        ["docker", "exec", "-i", container, "sh", "-c", f"cat > {temp_path}"],
        input=combined, text=True, capture_output=True
    )
    if p.returncode != 0:
        return None, temp_path, f"failed to write temp file: {p.stderr}"

    rc, out, err = run(["docker", "exec", container, "sh", "-c",
                        f"cd /PeTTa && ./run.sh {temp_path} 2>&1"])

    log_path = f"/tmp/set_atom_context_diagnostic_{ts}.log"
    full_log = f"returncode: {rc}\n\n===== OUTPUT =====\n{out}\n"
    subprocess.run(
        ["docker", "exec", "-i", container, "sh", "-c", f"cat > {log_path}"],
        input=full_log, text=True, capture_output=True
    )

    if not keep_temp:
        run(["docker", "exec", container, "rm", "-f", temp_path])

    return out, log_path, None


def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


def extract_results(output):
    """
    Extract the trailing block of reduction results. This evaluator echoes all
    source and prolog goals first, then prints all results at the end as a
    contiguous block of bare values in evaluation order.
    """
    output = strip_ansi(output)
    lines = [ln.rstrip() for ln in output.splitlines()]

    def is_noise(line):
        s = line.strip()
        if not s:
            return True
        for p in ("--> metta runnable", "-->  prolog goal", "--> metta sexpr",
                  "--> metta function", "--> prolog clause", ":-", "^^^^^^",
                  "!(", "findall(", "match(", "reduce(", "A),", "_).", "B),",
                  "C),", "( B=C", "(import!", "library(", "import_prolog",
                  "(=", "+(", "/(", "*(", "-(", "==(", "(   ", "->", ";"):
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


def after_value_took(text):
    """A counts atom: 5/4 means took, 4/3 means did not. Return True/False/None."""
    if text is None:
        return None
    if "invocations: 5 successes: 4" in text:
        return True
    if "invocations: 4 successes: 3" in text:
        return False
    return None


def classify(results):
    """
    Walk the trailing result block in evaluation order and assign per-frame.

    Evaluation order of substantive results (markers print as quoted strings;
    'true' acks and unreduced terms interleave):
      FRAME A: marker, before(4/3), <do-revise A: term or true>, after(A)
      FRAME B: marker, (frame-B-result before: (counts) after: (counts))
      FRAME C: marker, before(4/3), <do-revise C>, after(C)
      FRAME D: marker, (frame-D-result before: (counts) after: (counts))
      FRAME E: marker, before(4/3), <do-revise E>, after(E)

    We split the result stream by frame markers, then within each frame pull the
    decisive AFTER value. For A/C/E the after value is the LAST counts atom in
    that frame's slice. For B/D it is the counts atom following 'after:' in the
    frame-result wrapper.
    """
    findings = {}

    # Split into frame slices by marker strings.
    frames = {}
    current = None
    for r in results:
        m = re.search(r'FRAME ([A-E]):', r)
        if m and (r.strip().startswith('"') or r.strip().startswith('===')):
            current = m.group(1)
            frames[current] = []
        elif current is not None:
            frames[current].append(r)

    def after_from_slice(slice_lines, frame):
        # B and D return a single frame-result wrapper with 'after:'.
        for ln in slice_lines:
            if "frame-" in ln and "after:" in ln:
                # pull the counts after 'after:'
                idx = ln.find("after:")
                tail = ln[idx:]
                if "invocations: 5 successes: 4" in tail:
                    return "(counts invocations: 5 successes: 4)"
                if "invocations: 4 successes: 3" in tail:
                    return "(counts invocations: 4 successes: 3)"
        # A, C, E: the after value is the last bare counts atom in the slice.
        counts = [ln for ln in slice_lines if ln.strip().startswith("(counts invocations:")]
        if counts:
            return counts[-1]
        return None

    for f in ("A", "B", "C", "D", "E"):
        slice_lines = frames.get(f, [])
        after = after_from_slice(slice_lines, f)
        findings[f] = {"after": after, "took": after_value_took(after),
                       "raw": slice_lines}

    return findings


def verdict(findings):
    rows = []
    for f in ("A", "B", "C", "D", "E"):
        info = findings.get(f, {})
        took = info.get("took")
        after = info.get("after")
        if took is True:
            status = "TOOK"
        elif took is False:
            status = "no-op"
        else:
            status = "INSPECT"
        rows.append((f, status, after))

    # Decision: prefer E (precedented), then B, then C, then D.
    winner = None
    for f in ("E", "B", "C", "D"):
        if findings.get(f, {}).get("took") is True:
            winner = f
            break

    notes = {
        "E": ("CALLER USES progn-BODY PATTERN",
              "progn with set-atom! in body position executes the mutation standalone. "
              "This matches do-set-phase! precedent, is self-contained (no dependency on "
              "loop re-evaluation), and returns a usable value. Write the caller's writers "
              "as (progn (set-atom! ...) $new). Fork comes down on MeTTa."),
        "B": ("CALLER CALLS WRITERS IN let* CONTEXT",
              "Writers execute when called inside a let* binding (the loop hook context). "
              "The caller's hooks invoke writers in let* binding position, so this works. "
              "Less robust than E (depends on call context) but sufficient. Fork: MeTTa."),
        "C": ("CALLER WRAPS WRITES IN eval",
              "set-atom! executes when wrapped in explicit eval. Use (eval (set-atom! ...)) "
              "in the writer. Robust but less idiomatic than progn. Fork: MeTTa."),
        "D": ("CALLER INLINES set-atom! IN HOOK let*",
              "set-atom! executes when inlined directly in a let* binding (no wrapping "
              "function), matching loop lines 95/100. Caller inlines writes in the hook. "
              "Fork: MeTTa."),
    }

    if winner:
        decision = notes[winner]
    else:
        a_control = findings.get("A", {}).get("took")
        if a_control is False:
            decision = ("NO CONTEXT EXECUTED set-atom! STANDALONE",
                        "Control A correctly shows no-op, but B/C/D/E also failed to mutate "
                        "standalone. This means set-atom! requires the live-loop evaluation "
                        "context specifically. Next step: test the writer inside the actual "
                        "loop, not standalone run.sh. Document the loop-context dependency.")
        else:
            decision = ("INSPECT: control did not behave as expected",
                        "Frame A (control) did not show the expected no-op. Read the raw block; "
                        "the probe or evaluator behaved unexpectedly before trusting B/C/D/E.")

    return rows, decision


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--probe", default=DEFAULT_PROBE)
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    print("=" * 70)
    print("set-atom! Execution-Context Probe: Five-Frame Diagnostic")
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
    out, log_path, err = evaluate(args.container, args.probe, args.keep_temp)
    if err:
        print(f"  [FAIL] {err}")
        sys.exit(1)
    print(f"  full log: {log_path} (container; maps to host shared_files/)")

    results = extract_results(out)
    if not results:
        print("\n  [WARN] no result block extracted. Raw (ANSI-stripped) below:")
        print("-" * 70)
        print(strip_ansi(out)[:3000])
        sys.exit(3)

    print("\n" + "=" * 70)
    print("RAW RESULT BLOCK (trailing reduction output, in order)")
    print("=" * 70)
    for r in results:
        print(f"  {r}")

    findings = classify(results)

    print("\n" + "=" * 70)
    print("PER-FRAME: did the mutation take? (after-read 5/4 = TOOK, 4/3 = no-op)")
    print("=" * 70)
    labels = {
        "A": "bare top-level call (control)",
        "B": "writer inside let* binding",
        "C": "set-atom! in explicit eval",
        "D": "set-atom! inlined in let*",
        "E": "progn body-position (Clarity)",
    }
    rows, decision = verdict(findings)
    for f, status, after in rows:
        print(f"  FRAME {f}  {labels[f]:32s} {status:8s} after={after}")

    print("\n" + "=" * 70)
    print("DECISION")
    print("=" * 70)
    print(f"  >>> {decision[0]}")
    print(f"  {decision[1]}")

    print(f"\n  Full output preserved at {log_path} inside the container.")
    print(f"  (host: shared_files/{log_path.split('/')[-1]})")


if __name__ == "__main__":
    main()
