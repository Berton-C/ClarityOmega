#!/usr/bin/env python3
"""
T55 — Live Post-Results Continuation Map

Hypothesis
----------
In the untouched ClarityOmega production loop, the entire continuation after
RESULTS-EXECUTED is re-entered multiple times before one recursive cycle
boundary. If true, the three writer traces AND the diagnostics placed after
all writers (DIAG-CYCLE-START/END) will have the same multiplicity within each
completed response segment.

What this learns
----------------
A. TRACE triplets multiply, and DIAG START/END multiply by the same factor:
   multiplicity is upstream of the writer corridor; the whole continuation is
   re-entered.
B. TRACE triplets multiply, but DIAG START/END occur once:
   multiplicity is internal to the writer corridor and reconverges afterward.
C. All occur once:
   failure did not reproduce in the observed segments.

Non-invasive
------------
- edits no file;
- invokes no MeTTa function;
- does not start, stop, restart, or rebuild the container;
- only follows the existing production container log;
- writes one primary evidence log.

Run from the ClarityOmega repo root:
    python3 staging/t55_live_post_results_continuation_map.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import re
import select
import subprocess
import sys
import time

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_OUT = Path("/tmp/cg-v3-investigation/second-failure/t55/t55-evidence.log")
DEFAULT_RESULTS = 3
DEFAULT_TIMEOUT = 300
DEFAULT_GRACE = 20

TS_RE = re.compile(r"^(\S+)\s+(.*)$")
RUNTIME_PATTERNS = {
    "RESULTS": re.compile(r"^\(RESULTS-EXECUTED\)\s*$"),
    "TRACE172": re.compile(r"^\(TRACE-172-EXIT\)\s*$"),
    "TRACE175": re.compile(r"^\(TRACE-175-ENTRY\)\s*$"),
    "TRACE176": re.compile(r"^\(TRACE-176-ENTRY\)\s*$"),
    "DIAG_START": re.compile(r"^\(DIAG-CYCLE-START\s+([^\s\)]+)\)\s*$"),
    "DIAG_END": re.compile(r"^\(DIAG-CYCLE-END\s+([^\s\)]+)\)\s*$"),
    "ITERATION": re.compile(r"^\(---------iteration\s+([^\s\)]+)\)\s*$"),
    "POPULATOR": re.compile(r"^\(POPULATOR-DIAG\s+cycle-id\s+([^\s\)]+).*"),
    "TASK_STATE": re.compile(r"^TASK-STATE:"),
    "IDLE": re.compile(r"^\(IDLE_DIRECTIVE_RAW:"),
    "ALIVE": re.compile(r"^\(ALIVENESS_VERDICT:"),
    "CHARS": re.compile(r"^\(CHARS_SENT:"),
    "SILENT": re.compile(r"^\(SILENT_CYCLE\)\s*$"),
}


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def container_running(name: str) -> bool:
    p = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", name],
        capture_output=True,
        text=True,
    )
    return p.returncode == 0 and p.stdout.strip() == "true"


def classify(payload: str):
    for kind, rx in RUNTIME_PATTERNS.items():
        m = rx.match(payload)
        if m:
            value = m.group(1) if m.lastindex else None
            return kind, value
    return None, None


def summarize_segment(index: int, events: list[dict]) -> dict:
    counts = {k: 0 for k in RUNTIME_PATTERNS}
    values = {"DIAG_START": [], "DIAG_END": [], "ITERATION": [], "POPULATOR": []}
    for e in events:
        counts[e["kind"]] += 1
        if e["kind"] in values and e["value"] is not None:
            values[e["kind"]].append(e["value"])

    trace_counts = [counts["TRACE172"], counts["TRACE175"], counts["TRACE176"]]
    traces_balanced = len(set(trace_counts)) == 1
    trace_n = trace_counts[0] if traces_balanced else None
    diag_balanced = counts["DIAG_START"] == counts["DIAG_END"]
    diag_n = counts["DIAG_START"] if diag_balanced else None

    if traces_balanced and trace_n and trace_n > 1 and diag_balanced and diag_n == trace_n:
        verdict = "WHOLE-CONTINUATION-REENTRY"
    elif traces_balanced and trace_n and trace_n > 1 and diag_balanced and diag_n == 1:
        verdict = "WRITER-CORRIDOR-INTERNAL-MULTIPLICITY"
    elif traces_balanced and trace_n == 1 and diag_balanced and diag_n == 1:
        verdict = "SINGLE-VALUED-THIS-SEGMENT"
    elif trace_n == 0 and diag_n == 0:
        verdict = "NO-POST-RESULTS-WITNESSES"
    else:
        verdict = "INCONCLUSIVE-MIXED-CARDINALITY"

    return {
        "index": index,
        "counts": counts,
        "values": values,
        "trace_counts": trace_counts,
        "traces_balanced": traces_balanced,
        "diag_balanced": diag_balanced,
        "verdict": verdict,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--results", type=int, default=DEFAULT_RESULTS,
                    help="number of RESULTS-EXECUTED boundaries to observe")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--grace", type=int, default=DEFAULT_GRACE,
                    help="seconds retained after final RESULTS boundary")
    ap.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    if not container_running(args.container):
        print(f"T55 ERROR: container {args.container!r} is not running.", file=sys.stderr)
        print("Start it by your normal production procedure, then rerun T55.", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    start = now_utc()

    proc = subprocess.Popen(
        ["docker", "logs", "--timestamps", "--since", start, "--follow", args.container],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdout is not None

    captured: list[dict] = []
    result_count = 0
    final_boundary_at: float | None = None
    deadline = time.monotonic() + args.timeout

    try:
        while time.monotonic() < deadline:
            if final_boundary_at is not None and time.monotonic() - final_boundary_at >= args.grace:
                break

            ready, _, _ = select.select([proc.stdout], [], [], 0.5)
            if not ready:
                if proc.poll() is not None:
                    break
                continue

            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None:
                    break
                continue

            line = line.rstrip("\n")
            m = TS_RE.match(line)
            if not m:
                continue
            timestamp, payload = m.groups()
            kind, value = classify(payload)
            if kind is None:
                continue

            # Ignore every startup/translation line until the first exact
            # runtime RESULTS-EXECUTED marker.
            if result_count == 0 and kind != "RESULTS":
                continue

            captured.append({
                "timestamp": timestamp,
                "payload": payload,
                "kind": kind,
                "value": value,
            })

            if kind == "RESULTS":
                result_count += 1
                if result_count >= args.results and final_boundary_at is None:
                    final_boundary_at = time.monotonic()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)

    # Segments begin at each RESULTS marker and end immediately before the next.
    result_positions = [i for i, e in enumerate(captured) if e["kind"] == "RESULTS"]
    segments: list[list[dict]] = []
    for n, pos in enumerate(result_positions):
        end = result_positions[n + 1] if n + 1 < len(result_positions) else len(captured)
        segments.append(captured[pos:end])

    summaries = [summarize_segment(i + 1, seg) for i, seg in enumerate(segments)]

    lines: list[str] = []
    lines.extend([
        "=== T55 HYPOTHESIS ===",
        "In the untouched live production loop, the entire continuation after",
        "RESULTS-EXECUTED is re-entered multiple times before one recursive cycle",
        "boundary. If true, TRACE-172/175/176 and the post-writer",
        "DIAG-CYCLE-START/END witnesses will multiply by the same factor.",
        "",
        "Variable measured: runtime continuation cardinality per completed response segment.",
        "No production files or AtomSpace state were changed by this observer.",
        "",
        "=== T55 CAPTURE CONTRACT ===",
        f"container: {args.container}",
        f"start UTC: {start}",
        f"requested RESULTS boundaries: {args.results}",
        f"maximum observation: {args.timeout}s",
        f"post-final-boundary grace: {args.grace}s",
        f"observed RESULTS boundaries: {len(result_positions)}",
        "startup/translation output: excluded by exact runtime-marker matching",
        "",
        "=== T55 DECISION RULE ===",
        "TRACE xN and DIAG START/END xN  -> whole continuation re-entered upstream.",
        "TRACE xN and DIAG START/END x1 -> multiplicity internal to writer corridor.",
        "All x1                         -> failure absent in that segment.",
        "",
        "=== T55 SEGMENT CARDINALITY MAP ===",
        "SEG  TRACE172 TRACE175 TRACE176 DIAG-START DIAG-END ITER POP RESULT",
        "-----------------------------------------------------------------",
    ])

    for s in summaries:
        c = s["counts"]
        lines.append(
            f"{s['index']:>3}  {c['TRACE172']:>8} {c['TRACE175']:>8} {c['TRACE176']:>8} "
            f"{c['DIAG_START']:>10} {c['DIAG_END']:>8} {c['ITERATION']:>4} "
            f"{c['POPULATOR']:>3} {c['RESULTS']:>6}  {s['verdict']}"
        )

    lines.extend(["", "=== T55 SEGMENT DETAILS ==="])
    for s in summaries:
        lines.extend([
            "",
            f"--- SEGMENT {s['index']} ---",
            f"verdict: {s['verdict']}",
            f"trace counts: {s['trace_counts']}",
            f"DIAG START values: {s['values']['DIAG_START']}",
            f"DIAG END values: {s['values']['DIAG_END']}",
            f"visible iteration values: {s['values']['ITERATION']}",
            f"populator cycle values: {s['values']['POPULATOR']}",
        ])

    lines.extend(["", "=== T55 ORDERED RUNTIME EVENTS ==="])
    for i, e in enumerate(captured, 1):
        lines.append(f"{i:5d}  {e['timestamp']}  {e['payload']}")

    decisive = [s for s in summaries if s["verdict"] == "WHOLE-CONTINUATION-REENTRY"]
    internal = [s for s in summaries if s["verdict"] == "WRITER-CORRIDOR-INTERNAL-MULTIPLICITY"]
    single = [s for s in summaries if s["verdict"] == "SINGLE-VALUED-THIS-SEGMENT"]

    lines.extend(["", "=== T55 VERDICT ==="])
    if decisive:
        ids = ", ".join(str(s["index"]) for s in decisive)
        lines.extend([
            f"SUPPORTED — WHOLE POST-RESULTS CONTINUATION RE-ENTRY in segment(s): {ids}.",
            "The balanced TRACE triplets and the diagnostics after the complete writer",
            "corridor multiplied together. Therefore no individual writer is the first",
            "multiplier; evaluation is re-entering the continuation upstream of",
            "clarity-soul-mutation-commit-clear! / populate-recent-action.",
            "",
            "NEXT CONSTRAINT:",
            "Localize the upstream binding whose result cardinality fans out into the",
            "post-results continuation. The next probe should compare the cardinality of",
            "$results, $results_final, and the RESULTS-EXECUTED continuation using live",
            "production-shaped inputs, without modifying loop.metta.",
        ])
    elif internal:
        ids = ", ".join(str(s["index"]) for s in internal)
        lines.extend([
            f"SUPPORTED — WRITER-CORRIDOR INTERNAL MULTIPLICITY in segment(s): {ids}.",
            "TRACE triplets multiplied but the post-corridor diagnostics did not.",
            "The next probe must localize the first writer binding that reconverges.",
        ])
    elif single and len(single) == len(summaries) and summaries:
        lines.extend([
            "NOT REPRODUCED — all observed segments were single-valued.",
            "No localization claim is made. Repeat during the known failure state.",
        ])
    else:
        lines.extend([
            "INCONCLUSIVE — mixed or missing cardinalities.",
            "The ordered event section above is the complete retained evidence; no",
            "positive localization claim is made.",
        ])

    lines.extend([
        "",
        "=== INVESTIGATION MAP UPDATE ===",
        "Previously proven:",
        "  F1. Genuine response cycles complete while visible iteration/populator remain 1.",
        "  F2. TRACE-172/175/176 are balanced and multiply after RESULTS-EXECUTED.",
        "  F3. Task-state remains bootstrap-frozen during completed cycles.",
        "  F4. Recursive tail arithmetic/order advances correctly in isolation (T53).",
        "  F5. The isolated cumulative post-results corridor is single-valued (T54).",
        "T55 determines whether live multiplicity spans the whole continuation or remains",
        "inside the writer corridor.",
        "",
        "=== T55 PRIMARY ARTIFACT ===",
        str(args.output),
        "",
        "=== T55 COMPLETE ===",
    ])

    evidence = "\n".join(lines) + "\n"
    args.output.write_text(evidence)
    print(evidence)

    if len(result_positions) < args.results:
        return 3
    if not summaries:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
