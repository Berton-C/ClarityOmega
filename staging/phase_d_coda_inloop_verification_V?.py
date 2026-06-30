#!/usr/bin/env python3
"""
phase_d_coda_inloop_verification.py

The POST-WIRING half of Sprint 0-Coda Phase D. The substrate half
(phase_d_coda_verification.py) proved the Path C dispatcher reduces correctly
on fixture atoms in a fresh space. That harness CANNOT reach the live loop:
a one-shot run.sh file compiles inline (= ...) clauses but does not reduce soul
functions as the (omegaclaw) loop does per cycle, and external scripts cannot
query the live atomspace. So the in-loop criteria are a different SPECIES of
test: observe the RUNNING, WIRED container's log stream, not run a file.

ARTIFACT DISCIPLINE (the correction that produced this version):
  The log is the durable record. It preserves, PER SAMPLED CYCLE, the COMPLETE
  raw cycle block the loop emitted (every println from (---------iteration k)
  through (DIAG-CYCLE-END k)). The console stays readable (a compact harvested
  summary plus verdicts); the LOG carries the full evidence so a reader can
  re-derive every verdict and catch a false green. A verdict without its raw
  block beneath it is the failure mode this version exists to fix.

WHAT IT HARVESTS PER CYCLE (already present in the live log):
  PERSON_STATE, SOUL_VERDICT_IN, IDLE_DIRECTIVE_RAW, ALIVENESS_VERDICT,
  CHARS_SENT (or SILENT_CYCLE), SOUL-GATE-FLAG, SOUL_VERDICT_OUT,
  DIAG-RECENT-ACTION-COUNT, DIAG-IDLE-PATTERN-COUNT, RESPONSE head,
  and (post-wiring) DIAG-CYCLE-DISPATCH invocation-id + skills-len.

CRITERIA (post-wiring):
  P-2  dispatch fires in getContext each cycle  (DIAG-CYCLE-DISPATCH marker)
  P-3  handler output reaches the prompt         (skills-len > 0 each cycle)
  P-4  prompt parity                             (skills-len STABLE and > 0;
       CHARS_SENT is trend-only, NOT a band: it drifts upward with HISTORY)
  P-5  LLM behavior surface                       (RESPONSE / skill tail; manual)
  P-6  Criterion 5 watch                          (silent chain termination signs)

TEST-FIRST CONTRACT (the point of building this BEFORE Phase C wires):
  P-2/P-3/P-4 are observable ONLY if the cycle emits a marker of this shape:
      (DIAG-CYCLE-DISPATCH invocation-id: <id> skills-len: <n>)
  <id> from the (iii) counter atom (the gensym primitive probe came back
  unreduced); <n> is (string_length) of the resolved $skills-str. Recommended
  placement: the loop DIAG block, matching the (dispatch-invocation ...) and
  (dispatch-result ... (skill-set skills: $s) ...) atoms getContext wrote.
  Run this pre-wiring and it reports the marker ABSENT; the absence IS the
  contract Phase C must satisfy.

WHY ABSOLUTE CHARS_SENT IS NOT A PARITY BAND (finding from the first baseline):
  CHARS_SENT rose monotonically (42197 -> 43509, ~48 chars/cycle) because
  HISTORY accumulates each cycle. A post-wiring cycle sits higher for reasons
  unrelated to SKILLS. So parity is skills-len held constant under Option (a),
  not an absolute CHARS_SENT range. CHARS_SENT is logged as trend context only.

DISCIPLINE (carried from the established probe shape):
  - HANDS ONLY. Python reads logs, parses, compares to a recorded baseline.
  - RAW BLOCK BEFORE EVERY VERDICT, in the log artifact.
  - PREFLIGHT. Distinguish container-down / no-cycles / marker-absent.
  - The live log is println output, not run.sh trace; cycles are delimited by
    the loop's own iteration markers.

USAGE (run on the host, from repo root):
  Capture the pre-wiring baseline (BEFORE Phase C wires):
      python3 staging/phase_d_coda_inloop_verification.py --mode baseline --cycles 8
  Verify after Phase C wiring + rebuild + a few live cycles:
      python3 staging/phase_d_coda_inloop_verification.py --mode verify --cycles 8

  Flags:
    --container NAME     default clarity_omega
    --cycles N           most-recent complete cycles to read (default 8)
    --baseline-file PATH host path for the baseline artifact
                         (default ./phase_d_coda_chars_sent_baseline.json)
    --log-dir DIR        where to write the timestamped run log (default ".")
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
TIMEOUT = 60

# Real markers emitted by the running loop (src/loop.metta, verified):
RE_ITER = re.compile(r"\(-+iteration\s+(\d+)\)")
RE_CYCLE_END = re.compile(r"\(DIAG-CYCLE-END\s+(\d+)\)")
RE_CHARS_SENT = re.compile(r"\(CHARS_SENT:\s+(\d+)")
RE_SILENT = re.compile(r"\(SILENT_CYCLE\)")
RE_DISPATCH = re.compile(
    r"\(DIAG-CYCLE-DISPATCH\s+invocation-id:\s+(\S+)\s+skills-len:\s+(\d+)\)")
RE_ERROR = re.compile(r"\bError\b")

# Named single-line fields harvested from each cycle block. Each maps to a
# compiled regex capturing the payload after the marker.
FIELD_PATTERNS = {
    "PERSON_STATE": re.compile(r"\(PERSON_STATE:\s*(.*?)\)\s*$"),
    "SOUL_VERDICT_IN": re.compile(r"\(SOUL_VERDICT_IN:\s*(.*?)\)\s*$"),
    "ALIVENESS": re.compile(r"\(ALIVENESS_VERDICT:\s*(.*?)\)\s*$"),
    "SOUL_GATE_FLAG": re.compile(r"\(SOUL-GATE-FLAG\s+(.*?)\)\s*$"),
    "SOUL_VERDICT_OUT": re.compile(r"\(SOUL_VERDICT_OUT:\s*(.*?)\)\s*$"),
    "RECENT_ACTION_COUNT": re.compile(r"\(DIAG-RECENT-ACTION-COUNT\s+(.*?)\)\s*$"),
    "IDLE_PATTERN_COUNT": re.compile(r"\(DIAG-IDLE-PATTERN-COUNT\s+(.*?)\)\s*$"),
    "RESPONSE": re.compile(r"\(RESPONSE:\s*(.*)$"),
}

# Spec Section 8 recorded fence (iterations 1-2). Kept only as a loose sanity
# fence; the captured baseline supersedes it. NOT a tight parity band.
SPEC_FENCE_LO = 38653


class Recorder:
    def __init__(self):
        self.lines = []

    def pr(self, s=""):
        print(s)
        self.lines.append(s)

    def log_only(self, s=""):
        self.lines.append(s)

    def text(self):
        return "\n".join(self.lines) + "\n"


REC = Recorder()


def pr(s=""):
    REC.pr(s)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, **kw)


def strip_ansi(t):
    return re.sub(r"\x1b\[[0-9;]*m", "", t or "")


def stage(name):
    pr("\n" + "=" * 70)
    pr(name)
    pr("=" * 70)


def verdict_line(label, ok):
    pr("  " + label.ljust(56) + " " + ("PASS" if ok else "FAIL"))
    return ok


def container_running(container):
    try:
        p = run(["docker", "ps", "--filter", "name=" + container,
                 "--format", "{{.Names}}"])
        return p.returncode == 0 and container in p.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def write_container_file(container, path, text):
    """Write text to a file inside the container (no host write). Per Berton's
    directive: artifacts live in container /tmp (maps to host shared_files/),
    never in the repo root."""
    p = run(["docker", "exec", "-i", container, "sh", "-c", "cat > " + path],
            input=text)
    return p.returncode == 0


def read_container_file(container, path):
    p = run(["docker", "exec", container, "sh", "-c", "cat " + path + " 2>/dev/null"])
    return p.stdout if (p.returncode == 0 and p.stdout) else None


def read_logs(container, tail=6000):
    """Return the container log tail, ansi-stripped, or None."""
    p = run(["docker", "logs", "--tail", str(tail), container])
    text = (p.stdout or "") + (p.stderr or "")
    return strip_ansi(text) if text else None


def split_cycles(log_text, n):
    """Split the log into complete cycles, return the most recent n.

    A complete cycle runs from an iteration-start line to its DIAG-CYCLE-END.
    Returns a list of dicts: {k, text}. Incomplete trailing cycles are dropped.
    """
    lines = log_text.splitlines()
    starts = [(i, int(m.group(1))) for i, ln in enumerate(lines)
              for m in [RE_ITER.search(ln)] if m]
    cycles = []
    for idx, (line_i, k) in enumerate(starts):
        end_limit = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
        block = lines[line_i:end_limit]
        if any(RE_CYCLE_END.search(b) for b in block):
            cycles.append({"k": k, "text": "\n".join(block)})
    return cycles[-n:]


def cycle_chars_sent(block):
    m = RE_CHARS_SENT.search(block)
    if m:
        return int(m.group(1))
    if RE_SILENT.search(block):
        return "SILENT"
    return None


def cycle_dispatch(block):
    m = RE_DISPATCH.search(block)
    if m:
        return {"id": m.group(1), "skills_len": int(m.group(2))}
    return None


def harvest_fields(block):
    """Pull the named single-line fields out of a cycle block."""
    out = {}
    for line in block.splitlines():
        s = line.strip()
        for name, pat in FIELD_PATTERNS.items():
            if name in out:
                continue
            m = pat.search(s)
            if m:
                val = m.group(1).strip()
                out[name] = (val[:120] + " ...") if len(val) > 120 else val
    return out


def log_raw_cycle(cyc):
    """Write the COMPLETE raw cycle block to the log artifact (not console)."""
    REC.log_only("")
    REC.log_only("-" * 70)
    REC.log_only("RAW CYCLE " + str(cyc["k"]) + " (full loop output)")
    REC.log_only("-" * 70)
    REC.log_only(cyc["text"])


def harvested_summary_line(cyc):
    f = harvest_fields(cyc["text"])
    cs = cycle_chars_sent(cyc["text"])
    parts = [
        "cycle " + str(cyc["k"]).rjust(6),
        "alive=" + str(f.get("ALIVENESS", "?")),
        "gate=" + str(f.get("SOUL_GATE_FLAG", "?")),
        "ra=" + str(f.get("RECENT_ACTION_COUNT", "?")),
        "idle=" + str(f.get("IDLE_PATTERN_COUNT", "?")),
        "CHARS_SENT=" + str(cs),
    ]
    return "  " + "  ".join(parts), f, cs


def chars_drift(samples):
    """samples: list of (k, chars). Return (monotonic_up, per_adjacent_growth)."""
    seq = [(k, c) for k, c in samples if isinstance(c, int)]
    if len(seq) < 2:
        return None, None
    seq.sort()
    diffs = [seq[i + 1][1] - seq[i][1] for i in range(len(seq) - 1)]
    monotonic_up = all(d >= 0 for d in diffs)
    adj = [seq[i + 1][1] - seq[i][1] for i in range(len(seq) - 1)
           if seq[i + 1][0] - seq[i][0] == 1]
    per_cycle = round(sum(adj) / len(adj), 1) if adj else None
    return monotonic_up, per_cycle


# ---------------------------------------------------------------------------
# MODES
# ---------------------------------------------------------------------------

def mode_baseline(container, log_text, n, baseline_file):
    stage("MODE: BASELINE (pre-wiring; full raw evidence preserved in log)")
    pr("  Captured BEFORE Phase C wires. The console shows a harvested summary;")
    pr("  the LOG below preserves the complete raw block of every sampled cycle.")
    cycles = split_cycles(log_text, n)
    if not cycles:
        pr("  [FAIL] no complete cycles in the log tail. Is the loop iterating?")
        return False

    samples = []
    fields_seen = []
    for cyc in cycles:
        log_raw_cycle(cyc)                       # full evidence -> log artifact
        line, f, cs = harvested_summary_line(cyc)  # compact -> console + log
        pr(line)
        samples.append((cyc["k"], cs))
        fields_seen.append((cyc["k"], f))

    chars = [c for _, c in samples if isinstance(c, int)]
    if not chars:
        pr("\n  [WARN] all sampled cycles were SILENT; no CHARS_SENT to baseline.")
        return False

    xs = sorted(chars)
    summ = {"min": xs[0], "max": xs[-1], "median": xs[len(xs) // 2], "n": len(xs)}
    mono, per_cycle = chars_drift(samples)

    stage("BASELINE FINDINGS")
    pr("  CHARS_SENT: min=" + str(summ["min"]) + " max=" + str(summ["max"])
       + " median=" + str(summ["median"]) + " (n=" + str(summ["n"]) + ")")
    pr("  monotonic upward: " + str(mono)
       + "   per-adjacent-cycle growth: " + str(per_cycle) + " chars")
    if mono:
        pr("  >>> Absolute CHARS_SENT is NOT a parity band: it drifts upward with")
        pr("  HISTORY each cycle. Parity must be skills-len (the DIAG marker) held")
        pr("  constant under Option (a). CHARS_SENT is recorded as trend context.")

    payload = {
        "captured": datetime.datetime.now().isoformat(),
        "container": container,
        "cycles_read": n,
        "cycle_numbers": [k for k, _ in samples],
        "chars_sent": summ,
        "chars_monotonic_up": mono,
        "chars_per_adjacent_cycle_growth": per_cycle,
        "parity_metric": "skills-len (stable, >0); CHARS_SENT trend-only",
        "note": "pre-wiring getSkills path; absolute CHARS_SENT drifts with history",
    }
    tmp_path = "/tmp/" + os.path.basename(baseline_file)
    if write_container_file(container, tmp_path, json.dumps(payload, indent=2)):
        pr("  baseline written: " + tmp_path + "  (container; maps to host shared_files/)")
    else:
        pr("  [WARN] could not write baseline file to " + tmp_path)
    return True


def mode_verify(container, log_text, n, baseline_file):
    stage("MODE: VERIFY (post-wiring; full raw evidence preserved in log)")
    cycles = split_cycles(log_text, n)
    if not cycles:
        pr("  [FAIL] no complete cycles in the log tail. Is the loop iterating?")
        return {"_preflight": False}

    baseline = None
    tmp_path = "/tmp/" + os.path.basename(baseline_file)
    raw = read_container_file(container, tmp_path)
    if raw:
        try:
            baseline = json.loads(raw)
            pr("  baseline loaded: " + tmp_path)
        except ValueError as e:
            pr("  [WARN] baseline unreadable (" + str(e) + ")")
    else:
        pr("  [WARN] no baseline at " + tmp_path
           + "; run --mode baseline pre-wiring first.")

    # Full raw evidence to log + compact harvested table to console, per cycle.
    dispatch_ids, skills_lens, samples = [], [], []
    errors_near_absent = 0
    for cyc in cycles:
        log_raw_cycle(cyc)
        line, f, cs = harvested_summary_line(cyc)
        disp = cycle_dispatch(cyc["text"])
        pr(line + "  dispatch=" + (str(disp) if disp else "ABSENT"))
        samples.append((cyc["k"], cs))
        if disp:
            dispatch_ids.append(disp["id"])
            skills_lens.append(disp["skills_len"])
        elif cs != "SILENT" and RE_ERROR.search(cyc["text"]):
            errors_near_absent += 1

    nonsilent = [c for c in cycles if cycle_chars_sent(c["text"]) != "SILENT"]
    results = {}

    # P-2
    stage("P-2  DISPATCH FIRES IN getContext (per-cycle, distinct invocation-id)")
    if not dispatch_ids:
        pr("  >>> DIAG-CYCLE-DISPATCH ABSENT across all sampled cycles. Either")
        pr("  Phase C has not wired the dispatch into getContext, or the wiring")
        pr("  did not add the marker println this harness requires. THIS IS THE")
        pr("  TEST-FIRST CONTRACT: add")
        pr("    (DIAG-CYCLE-DISPATCH invocation-id: <id> skills-len: <n>)")
        pr("  so P-2/P-3/P-4 become observable. P-2..P-4 = PRE-CONDITION-NOT-MET")
        pr("  (not FAIL: the substrate may be correct but is unobservable here).")
        results["P-2 dispatch fires (marker present)"] = False
        results["P-3 handler output reaches prompt"] = None
        results["P-4 parity (skills-len stable + >0)"] = None
        return results
    fires_each = len(dispatch_ids) >= len(nonsilent) and len(nonsilent) > 0
    distinct = len(set(dispatch_ids)) == len(dispatch_ids)
    pr("  ids: " + str(dispatch_ids))
    verdict_line("dispatch marker present every non-silent cycle", fires_each)
    verdict_line("invocation-ids distinct (per-invocation isolation)", distinct)
    results["P-2 dispatch fires (marker present)"] = fires_each and distinct

    # P-3
    stage("P-3  HANDLER OUTPUT REACHES PROMPT (skills-len > 0)")
    pr("  skills-len per cycle: " + str(skills_lens))
    all_positive = bool(skills_lens) and all(x > 0 for x in skills_lens)
    results["P-3 handler output reaches prompt"] = verdict_line(
        "skills-len > 0 on every dispatching cycle", all_positive)

    # P-4 (skills-len-centric; CHARS_SENT trend-only per the baseline finding)
    stage("P-4  PROMPT PARITY (skills-len STABLE and > 0; CHARS_SENT trend-only)")
    skills_stable = len(set(skills_lens)) == 1 if skills_lens else False
    pr("  distinct skills-len values: " + str(sorted(set(skills_lens))))
    mono, per_cycle = chars_drift(samples)
    pr("  CHARS_SENT trend: monotonic_up=" + str(mono)
       + " per-adjacent-cycle=" + str(per_cycle)
       + " (context only; not a band, per baseline finding)")
    verdict_line("skills-len stable across cycles (Option a: one hardcoded list)",
                 skills_stable)
    results["P-4 parity (skills-len stable + >0)"] = skills_stable and all_positive

    # P-5
    stage("P-5  LLM BEHAVIOR SURFACE (manual; Standard metric per spec)")
    pr("  RESPONSE head per cycle (compare to pre-Coda at the Standard metric:")
    pr("  same skill name AND argument structure under equivalent input):")
    for cyc in cycles:
        f = harvest_fields(cyc["text"])
        if "RESPONSE" in f:
            pr("    cycle " + str(cyc["k"]) + ": " + f["RESPONSE"])
    pr("  P-5 is observational; this harness does not auto-pass it.")

    # P-6
    stage("P-6  CRITERION 5 WATCH (silent chain termination)")
    pr("  cycles with an Error near an absent dispatch marker: "
       + str(errors_near_absent))
    if errors_near_absent:
        pr("  >>> POSSIBLE Criterion 5 firing. Inspect those cycles in the raw")
        pr("  blocks above: a handler crash under reduce/2 ends the chain silently.")

    return results


def write_log(args, ts, container):
    fname = "phase_d_coda_inloop_" + ts + ".log"
    text = REC.text()
    cont_path = "/tmp/" + fname
    if write_container_file(container, cont_path, text):
        cont_msg = cont_path + "  (container; maps to host shared_files/)"
    else:
        cont_msg = "(container write failed)"
    print("\nLog artifact written:")
    print("  " + cont_msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--mode", choices=["baseline", "verify"], default="verify")
    ap.add_argument("--cycles", type=int, default=8)
    ap.add_argument("--baseline-file",
                    default="phase_d_coda_chars_sent_baseline.json",
                    help="basename; written/read in container /tmp")
    args = ap.parse_args()
    c = args.container

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pr("=" * 70)
    pr("Phase D Coda IN-LOOP verification (running container, " + args.mode + ")")
    pr("timestamp: " + ts + "   container: " + c)
    pr("=" * 70)

    stage("STAGE 0  PREFLIGHT")
    if not container_running(c):
        pr("  [FAIL] container '" + c + "' not running. Start it and re-run.")
        write_log(args, ts, c)
        sys.exit(1)
    pr("  [OK] container '" + c + "' running")
    log_text = read_logs(c)
    if not log_text:
        pr("  [FAIL] no log output from container.")
        write_log(args, ts, c)
        sys.exit(1)
    pr("  [OK] read " + str(len(log_text.splitlines())) + " log lines")

    if args.mode == "baseline":
        ok = mode_baseline(c, log_text, args.cycles, args.baseline_file)
        results = {"baseline captured": ok}
    else:
        results = mode_verify(c, log_text, args.cycles, args.baseline_file)

    stage("SUMMARY")
    for k, v in results.items():
        mark = "PASS" if v is True else ("FAIL" if v is False else "PRE-COND-NOT-MET")
        pr("  " + k.ljust(48) + " " + mark)

    stage("THE GAP (read regardless of pass/fail)")
    pr("  This harness observes the LIVE loop; it cannot see the dispatch")
    pr("  companion atoms directly (the live atomspace is not externally")
    pr("  queryable), so P-2/P-3/P-4 depend on the (DIAG-CYCLE-DISPATCH ...)")
    pr("  marker the wiring must emit. Parity is skills-len held constant under")
    pr("  Option (a); absolute CHARS_SENT drifts with HISTORY and is trend-only.")
    pr("  A byte-exact SKILLS-block diff would need the wiring to log the block")
    pr("  itself. P-5 (behavior) and P-6 (Criterion 5) stay observational.")
    pr("  Full raw cycle blocks are preserved above this summary in the log.")

    write_log(args, ts, c)
    if any(v is False for v in results.values()):
        sys.exit(3)


if __name__ == "__main__":
    main()
