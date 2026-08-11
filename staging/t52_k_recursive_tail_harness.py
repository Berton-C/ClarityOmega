#!/usr/bin/env python3
"""
t52_k_recursive_tail_harness.py

Non-invasive production-runtime harness for the ClarityOmega v3 investigation.

Single variable under test
--------------------------
$k across the recursive tail of src/loop.metta.

Hypothesis
----------
Completed response work is occurring while the loop-carried $k does not
advance across the recursive tail.

The harness does NOT edit loop.metta, does NOT patch any production file,
and does NOT invoke any corner-gate/v3 function directly.

It uses independent $k witnesses already present in the production runtime:
  - DIAG-CYCLE-DISPATCH invocation-id: $k   (getContext entry)
  - ---------iteration $k                   (visible loop entry)
  - POPULATOR-DIAG cycle-id $k              (post-results writer)
  - DIAG-CYCLE-START $k
  - DIAG-CYCLE-END $k                       (end of post-results diagnostics)

RESULTS-EXECUTED is used only as the completed-work boundary.

Termination
-----------
Primary:
  TARGET_RESULTS completed RESULTS-EXECUTED boundaries followed by the next
  DIAG-CYCLE-DISPATCH witness, so the transition across the recursive tail can
  be evaluated.

Safety:
  MAX_SECONDS after the first genuine runtime $k witness.

Artifacts
---------
Writes into:
  /tmp/cg-v3-investigation/second-failure/t52/

  raw.log
  events.txt
  analysis.txt
  source-audit.txt

Usage
-----
From the ClarityOmega repository root:

  python3 staging/t52_k_recursive_tail_harness.py --start

Options:
  --container clarity_omega
  --target-results 3
  --max-seconds 360
  --start
  --stop-after
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import re
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_OUT = Path("/tmp/cg-v3-investigation/second-failure/t52")
DEFAULT_TARGET_RESULTS = 3
DEFAULT_MAX_SECONDS = 360

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

PATTERNS = {
    "DISPATCH": re.compile(r"\(DIAG-CYCLE-DISPATCH invocation-id:\s*([0-9]+)"),
    "ITERATION": re.compile(r"\(---------iteration\s+([0-9]+)\)"),
    "RESULTS": re.compile(r"\(RESULTS-EXECUTED\)"),
    "POPULATOR": re.compile(r"\(POPULATOR-DIAG cycle-id\s+([0-9]+)\b"),
    "CYCLE_START": re.compile(r"\(DIAG-CYCLE-START\s+([0-9]+)\)"),
    "CYCLE_END": re.compile(r"\(DIAG-CYCLE-END\s+([0-9]+)\)"),
}

ERROR_RE = re.compile(
    r"Unknown procedure|Domain error|not_less_than_zero|"
    r"METTA_ARGUMENT_PARSE_ERROR|ERROR:|Traceback|Exception"
)

TIMESTAMP_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)\s+(?P<body>.*)$"
)


@dataclass
class Event:
    seq: int
    kind: str
    value: Optional[int]
    timestamp: str
    line: str
    results_before: int


def run(cmd: list[str], timeout: int = 120, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=check,
    )


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text or "")


def container_running(container: str) -> bool:
    p = run([
        "docker", "ps",
        "--filter", f"name=^{container}$",
        "--format", "{{.Names}}",
    ])
    return p.returncode == 0 and container in p.stdout.splitlines()


def source_audit(loop_path: Path) -> tuple[bool, str]:
    lines = []
    ok = True

    if not loop_path.exists():
        return False, f"FAIL: missing {loop_path}\n"

    text = loop_path.read_text(errors="replace")
    digest = hashlib.sha256(text.encode()).hexdigest()

    checks = [
        ("recursive function head", "(= (omegaclaw $k)" in text),
        ("getContext receives $k", "(getContext $k)" in text),
        ("visible iteration prints $k", "(println! (---------iteration $k))" in text),
        ("populator receives $k", "(populate-recent-action $sexpr $msgnew $k)" in text),
        ("cycle-start prints $k", "(println! (DIAG-CYCLE-START $k))" in text),
        ("cycle-end prints $k", "(println! (DIAG-CYCLE-END $k))" in text),
        ("recursive tail requests k+1", "(omegaclaw (+ 1 $k))" in text),
    ]

    lines.append(f"path: {loop_path}")
    lines.append(f"sha256: {digest}")
    lines.append("")

    for label, passed in checks:
        lines.append(f"{'PASS' if passed else 'FAIL'}: {label}")
        ok = ok and passed

    lines.append("")
    lines.append(
        "Source audit establishes that all runtime witnesses and the recursive "
        "tail are present in the production source. It does not claim that the "
        "tail evaluates correctly."
    )

    return ok, "\n".join(lines) + "\n"


def terminate_process(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    try:
        proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
            proc.wait(timeout=5)
        except Exception:
            pass


def parse_runtime_line(clean: str):
    ts_match = TIMESTAMP_RE.match(clean)
    if not ts_match:
        return None

    timestamp = ts_match.group("ts")
    body = ts_match.group("body")

    for kind, pattern in PATTERNS.items():
        m = pattern.search(body)
        if m:
            value = int(m.group(1)) if m.lastindex else None
            return kind, value, timestamp, body

    if ERROR_RE.search(body):
        return "ERROR", None, timestamp, body

    return None


def prior_event(events: list[Event], idx: int, kind: str) -> Optional[Event]:
    for event in reversed(events[:idx]):
        if event.kind == kind:
            return event
    return None


def next_event(events: list[Event], idx: int, kind: str) -> Optional[Event]:
    for event in events[idx + 1:]:
        if event.kind == kind:
            return event
    return None


def analyze(events: list[Event], stop_reason: str, target_results: int, max_seconds: int) -> str:
    counts = {key: 0 for key in list(PATTERNS) + ["ERROR"]}
    values = {key: [] for key in ["DISPATCH", "ITERATION", "POPULATOR", "CYCLE_START", "CYCLE_END"]}

    for event in events:
        counts[event.kind] = counts.get(event.kind, 0) + 1
        if event.kind in values and event.value is not None:
            values[event.kind].append(event.value)

    out = []
    out.append("=== T52 $k RECURSIVE-TAIL ANALYSIS ===")
    out.append("")
    out.append(f"stop reason:                 {stop_reason}")
    out.append(f"target result boundaries:    {target_results}")
    out.append(f"safety ceiling seconds:      {max_seconds}")
    out.append("")
    out.append(f"DISPATCH witnesses:          {counts['DISPATCH']}")
    out.append(f"VISIBLE ITERATIONS:          {counts['ITERATION']}")
    out.append(f"RESULTS-EXECUTED:            {counts['RESULTS']}")
    out.append(f"POPULATOR witnesses:         {counts['POPULATOR']}")
    out.append(f"DIAG-CYCLE-START:            {counts['CYCLE_START']}")
    out.append(f"DIAG-CYCLE-END:              {counts['CYCLE_END']}")
    out.append(f"ERROR EVENTS:                {counts['ERROR']}")
    out.append("")

    for kind, label in [
        ("DISPATCH", "dispatch progression"),
        ("ITERATION", "visible iteration progression"),
        ("POPULATOR", "populator cycle progression"),
        ("CYCLE_START", "cycle-start progression"),
        ("CYCLE_END", "cycle-end progression"),
    ]:
        seq = values[kind]
        if not seq:
            verdict = "not-observed"
        elif len(set(seq)) == 1:
            verdict = f"constant-at-{seq[0]}"
        else:
            verdict = " -> ".join(str(v) for v in seq)
        out.append(f"{label:30s} {verdict}")

    out.append("")
    out.append("=== TRANSITIONS ACROSS COMPLETED RESULTS ===")

    result_indexes = [i for i, e in enumerate(events) if e.kind == "RESULTS"]
    transition_rows = []
    for ordinal, idx in enumerate(result_indexes, start=1):
        before_dispatch = prior_event(events, idx, "DISPATCH")
        before_iteration = prior_event(events, idx, "ITERATION")
        after_populator = next_event(events, idx, "POPULATOR")
        after_start = next_event(events, idx, "CYCLE_START")
        after_end = next_event(events, idx, "CYCLE_END")
        next_dispatch = next_event(events, idx, "DISPATCH")

        current_k = None
        for candidate in [before_dispatch, before_iteration, after_populator, after_start, after_end]:
            if candidate and candidate.value is not None:
                current_k = candidate.value
                break

        next_k = next_dispatch.value if next_dispatch else None
        expected = current_k + 1 if current_k is not None else None
        advanced = (
            current_k is not None
            and next_k is not None
            and next_k == expected
        )

        row = {
            "ordinal": ordinal,
            "dispatch": before_dispatch.value if before_dispatch else None,
            "iteration": before_iteration.value if before_iteration else None,
            "populator": after_populator.value if after_populator else None,
            "start": after_start.value if after_start else None,
            "end": after_end.value if after_end else None,
            "next_dispatch": next_k,
            "expected": expected,
            "advanced": advanced,
        }
        transition_rows.append(row)

        out.append(
            f"result {ordinal}: "
            f"dispatch={row['dispatch']} "
            f"iteration={row['iteration']} "
            f"populator={row['populator']} "
            f"cycle-start={row['start']} "
            f"cycle-end={row['end']} "
            f"next-dispatch={row['next_dispatch']} "
            f"expected-next={row['expected']} "
            f"advanced={'YES' if advanced else 'NO/UNPROVEN'}"
        )

    out.append("")
    out.append("=== DECISION ===")

    comparable = [
        row for row in transition_rows
        if row["expected"] is not None and row["next_dispatch"] is not None
    ]

    all_constant_one = all(
        not seq or all(v == 1 for v in seq)
        for seq in values.values()
    )

    completed_end_then_same_dispatch = any(
        row["end"] is not None
        and row["next_dispatch"] is not None
        and row["end"] == row["next_dispatch"]
        for row in comparable
    )

    if comparable and all(row["advanced"] for row in comparable):
        verdict = (
            "NOT SUPPORTED: every observed completed-result transition advanced "
            "$k to the expected next value."
        )
    elif completed_end_then_same_dispatch:
        verdict = (
            "SUPPORTED, STRONG FORM: a completed post-results cycle reached "
            "DIAG-CYCLE-END at k=N, but the next production dispatch re-entered "
            "with the same k=N rather than N+1."
        )
    elif comparable and all_constant_one:
        verdict = (
            "SUPPORTED: independent production witnesses remain fixed at k=1 "
            "across completed RESULTS boundaries and subsequent dispatches. "
            "The recursive advance is not becoming the next observed invocation."
        )
    elif comparable:
        verdict = (
            "MIXED: at least one completed-result transition failed to show the "
            "expected k+1, but the witnesses are not uniformly constant. Inspect "
            "the transition rows and raw events."
        )
    else:
        verdict = (
            "UNRESOLVED: the capture did not include both a completed RESULTS "
            "boundary and a subsequent DISPATCH witness."
        )

    out.append(verdict)
    out.append("")
    out.append(
        "Interpretation boundary: this harness localizes the failure to the "
        "production transition between one completed invocation and the next. "
        "It does not yet identify whether the cause is AtomSpace multiplicity, "
        "evaluation/backtracking, cut placement, or arithmetic reduction."
    )

    return "\n".join(out) + "\n"


def write_events(events: list[Event], path: Path) -> None:
    lines = []
    for e in events:
        value = "" if e.value is None else f" value={e.value}"
        lines.append(
            f"{e.seq:6d}  RDONE={e.results_before:<3d}  "
            f"{e.kind:<13s}{value:<12s}  {e.timestamp} {e.line}"
        )
    path.write_text("\n".join(lines) + ("\n" if lines else ""))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--target-results", type=int, default=DEFAULT_TARGET_RESULTS)
    ap.add_argument("--max-seconds", type=int, default=DEFAULT_MAX_SECONDS)
    ap.add_argument("--start", action="store_true",
                    help="run docker compose up -d before capture")
    ap.add_argument("--stop-after", action="store_true",
                    help="stop the production container after capture")
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    for name in ["raw.log", "events.txt", "analysis.txt", "source-audit.txt"]:
        p = out_dir / name
        if p.exists():
            p.unlink()

    print("=== T52 HYPOTHESIS ===")
    print("Completed production response work is occurring while the loop-carried")
    print("$k does not advance across the recursive tail.")
    print()
    print("This harness:")
    print("  - edits no production file")
    print("  - invokes no v3 function directly")
    print("  - observes only existing $k witnesses and RESULTS boundaries")
    print()

    audit_ok, audit_text = source_audit(Path("src/loop.metta"))
    (out_dir / "source-audit.txt").write_text(audit_text)
    print("=== T52 SOURCE AUDIT ===")
    print(audit_text, end="")
    if not audit_ok:
        print("T52 ABORT: source audit failed.")
        return 2

    if args.start:
        print("Starting local production container with docker compose up -d ...")
        p = run(["docker", "compose", "up", "-d"], timeout=300)
        if p.returncode != 0:
            print(strip_ansi(p.stdout + p.stderr))
            print("T52 ABORT: docker compose up failed.")
            return 3

    if not container_running(args.container):
        print(f"T52 ABORT: container '{args.container}' is not running.")
        print("Start it or rerun with --start.")
        return 4

    start_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"Container: {args.container}")
    print(f"Capture start UTC: {start_utc}")
    print(
        f"Termination: {args.target_results} RESULTS boundaries plus the next "
        f"DISPATCH, or {args.max_seconds}s after the first runtime $k witness."
    )
    print()

    proc = subprocess.Popen(
        [
            "docker", "logs",
            "--timestamps",
            "--since", start_utc,
            "--follow",
            args.container,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    events: list[Event] = []
    raw_lines: list[str] = []
    runtime_started = False
    first_runtime_monotonic: Optional[float] = None
    results_count = 0
    dispatch_count_at_target: Optional[int] = None
    stop_reason = "log-stream-ended"

    try:
        assert proc.stdout is not None
        while True:
            if runtime_started and first_runtime_monotonic is not None:
                if time.monotonic() - first_runtime_monotonic >= args.max_seconds:
                    stop_reason = "safety-ceiling-reached"
                    break

            line = proc.stdout.readline()
            if line == "":
                if proc.poll() is not None:
                    stop_reason = "log-stream-ended"
                    break
                time.sleep(0.05)
                continue

            clean = strip_ansi(line.rstrip("\n"))
            raw_lines.append(clean)

            parsed = parse_runtime_line(clean)
            if parsed is None:
                continue

            kind, value, timestamp, body = parsed

            if kind in {"DISPATCH", "ITERATION"} and not runtime_started:
                runtime_started = True
                first_runtime_monotonic = time.monotonic()
                print(f"T52 readiness: first runtime $k witness observed: {body}")

            if not runtime_started:
                continue

            event = Event(
                seq=len(raw_lines),
                kind=kind,
                value=value,
                timestamp=timestamp,
                line=body,
                results_before=results_count,
            )
            events.append(event)

            if kind == "RESULTS":
                results_count += 1
                event.results_before = results_count
                if results_count >= args.target_results and dispatch_count_at_target is None:
                    dispatch_count_at_target = sum(1 for e in events if e.kind == "DISPATCH")
                    print(
                        f"T52 progress: target RESULTS count {results_count} reached; "
                        "waiting for the next DISPATCH witness."
                    )

            if (
                dispatch_count_at_target is not None
                and kind == "DISPATCH"
                and sum(1 for e in events if e.kind == "DISPATCH") > dispatch_count_at_target
            ):
                stop_reason = "target-results-plus-next-dispatch"
                break

    except KeyboardInterrupt:
        stop_reason = "user-interrupted"
    finally:
        terminate_process(proc)

    (out_dir / "raw.log").write_text("\n".join(raw_lines) + ("\n" if raw_lines else ""))
    write_events(events, out_dir / "events.txt")

    analysis = analyze(
        events,
        stop_reason=stop_reason,
        target_results=args.target_results,
        max_seconds=args.max_seconds,
    )
    (out_dir / "analysis.txt").write_text(analysis)

    print()
    print(analysis, end="")
    print()
    print("=== T52 ORDERED EVENTS ===")
    print((out_dir / "events.txt").read_text(), end="")
    print()
    print("=== T52 ARTIFACTS ===")
    for name in ["source-audit.txt", "raw.log", "events.txt", "analysis.txt"]:
        print(out_dir / name)

    if args.stop_after:
        print()
        print(f"Stopping container {args.container} ...")
        run(["docker", "stop", args.container], timeout=60)

    print()
    print("=== T52 COMPLETE ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
