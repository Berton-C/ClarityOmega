#!/usr/bin/env python3
"""
T56 — Live command-cardinality / continuation-multiplicity correlation

Purpose
-------
Test one meaningful variable through the untouched ClarityOmega production loop:

    Does the number of balanced TRACE-172/175/176 triplets in a completed
    runtime segment equal POPULATOR-DIAG sexpr-len for that segment?

Why this matters
----------------
T54 proved the isolated post-results writer corridor is single-valued.
Production observations repeatedly show multiple balanced TRACE triplets before
the next visible iteration boundary. If triplet multiplicity tracks sexpr-len,
the strongest localization is that the post-results continuation is being
evaluated once per superposed command/result branch, rather than once per loop
cycle.

This harness:
  * edits no production file;
  * invokes no v3 function;
  * ignores startup/translation output;
  * retains only exact timestamped runtime events;
  * never stores the CHARS_SENT payload;
  * captures enough RESULTS boundaries to form complete segments;
  * produces one primary, readable evidence log.

Run from the ClarityOmega repository root:
    python3 staging/t56_live_command_multiplicity_correlation.py

Optional:
    --container clarity_omega
    --segments 4
    --wait-first 240
    --timeout 420
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import selectors
import signal
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


TS_RE = re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2}T\S+Z)\s+(?P<body>.*)$")
ITER_RE = re.compile(r"^\(---------iteration\s+(?P<n>-?\d+)\)")
POP_RE = re.compile(
    r"^\(POPULATOR-DIAG\s+cycle-id\s+(?P<cycle>\S+)\s+"
    r"msgnew\s+(?P<msgnew>\S+)\s+sexpr-len\s+(?P<len>\d+)\s+"
    r"action-type\s+(?P<action>\S+)"
)
CHARS_RE = re.compile(r"^\(CHARS_SENT:\s+(?P<n>\d+)\b")
ALIVE_RE = re.compile(r"^\(ALIVENESS_VERDICT:\s+(?P<v>\S+)")
TASK_RE = re.compile(
    r"^\(TASK-STATE(?:-DIAG)?\b.*?"
    r"(?:cycles-since-input\s+(?P<cycles>-?\d+))?.*?"
    r"(?:last-activity\s+(?P<last>[0-9.]+))?.*?"
    r"(?:task-phase\s+(?P<phase>[^\s\)]+))?"
)


@dataclass
class Event:
    ts: str
    kind: str
    detail: str = ""


@dataclass
class Segment:
    number: int
    start_result_ts: str
    events: list[Event] = field(default_factory=list)
    end_result_ts: Optional[str] = None
    sexpr_len: Optional[int] = None
    pop_cycle: Optional[str] = None
    msgnew: Optional[str] = None
    action_type: Optional[str] = None
    trace172: int = 0
    trace175: int = 0
    trace176: int = 0
    iterations: list[int] = field(default_factory=list)
    idle_count: int = 0
    aliveness: list[str] = field(default_factory=list)
    chars_sent: list[int] = field(default_factory=list)
    silent_count: int = 0
    task_states: list[str] = field(default_factory=list)

    def add(self, ev: Event) -> None:
        self.events.append(ev)
        if ev.kind == "POPULATOR":
            parts = dict(item.split("=", 1) for item in ev.detail.split() if "=" in item)
            self.pop_cycle = parts.get("cycle")
            self.msgnew = parts.get("msgnew")
            self.action_type = parts.get("action")
            try:
                self.sexpr_len = int(parts["sexpr_len"])
            except (KeyError, ValueError):
                pass
        elif ev.kind == "TRACE-172":
            self.trace172 += 1
        elif ev.kind == "TRACE-175":
            self.trace175 += 1
        elif ev.kind == "TRACE-176":
            self.trace176 += 1
        elif ev.kind == "ITERATION":
            try:
                self.iterations.append(int(ev.detail))
            except ValueError:
                pass
        elif ev.kind == "IDLE":
            self.idle_count += 1
        elif ev.kind == "ALIVENESS":
            self.aliveness.append(ev.detail)
        elif ev.kind == "CHARS":
            try:
                self.chars_sent.append(int(ev.detail))
            except ValueError:
                pass
        elif ev.kind == "SILENT":
            self.silent_count += 1
        elif ev.kind == "TASK-STATE":
            self.task_states.append(ev.detail)


def parse_runtime_event(line: str) -> Optional[Event]:
    m = TS_RE.match(line.rstrip("\n"))
    if not m:
        return None

    ts = m.group("ts")
    body = m.group("body").strip()

    # Exact runtime markers only. Translation/source echoes are excluded because
    # their body does not begin with the runtime S-expression marker.
    if body == "(RESULTS-EXECUTED)":
        return Event(ts, "RESULTS")
    if body == "(TRACE-172-EXIT)":
        return Event(ts, "TRACE-172")
    if body == "(TRACE-175-ENTRY)":
        return Event(ts, "TRACE-175")
    if body == "(TRACE-176-ENTRY)":
        return Event(ts, "TRACE-176")
    if body.startswith("(IDLE_DIRECTIVE_RAW:"):
        return Event(ts, "IDLE")
    if body == "(SILENT_CYCLE)":
        return Event(ts, "SILENT")

    m2 = ITER_RE.match(body)
    if m2:
        return Event(ts, "ITERATION", m2.group("n"))

    m2 = POP_RE.match(body)
    if m2:
        detail = (
            f"cycle={m2.group('cycle')} "
            f"msgnew={m2.group('msgnew')} "
            f"sexpr_len={m2.group('len')} "
            f"action={m2.group('action')}"
        )
        return Event(ts, "POPULATOR", detail)

    m2 = ALIVE_RE.match(body)
    if m2:
        return Event(ts, "ALIVENESS", m2.group("v"))

    m2 = CHARS_RE.match(body)
    if m2:
        # Deliberately retain only the reported character count.
        return Event(ts, "CHARS", m2.group("n"))

    if body.startswith("(TASK-STATE"):
        # Keep at most a compact prefix; never retain prompt/history payloads.
        compact = " ".join(body[:240].split())
        return Event(ts, "TASK-STATE", compact)

    return None


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def duration_seconds(a: str, b: str) -> Optional[float]:
    try:
        aa = dt.datetime.fromisoformat(a.replace("Z", "+00:00"))
        bb = dt.datetime.fromisoformat(b.replace("Z", "+00:00"))
        return (bb - aa).total_seconds()
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default="clarity_omega")
    ap.add_argument("--segments", type=int, default=4,
                    help="Number of complete RESULTS-to-RESULTS segments required")
    ap.add_argument("--wait-first", type=int, default=240,
                    help="Seconds allowed for first runtime RESULTS marker")
    ap.add_argument("--timeout", type=int, default=420,
                    help="Absolute maximum capture duration")
    args = ap.parse_args()

    outdir = Path("/tmp/cg-v3-investigation/second-failure/t56")
    outdir.mkdir(parents=True, exist_ok=True)
    evidence = outdir / "t56-evidence.log"

    start_utc = iso_now()
    cmd = [
        "docker", "logs", "--timestamps",
        "--since", start_utc, "--follow", args.container
    ]

    header = [
        "=== T56 HYPOTHESIS ===",
        "In the untouched production loop, balanced TRACE-172/175/176 triplet",
        "multiplicity equals POPULATOR-DIAG sexpr-len within each completed",
        "RESULTS-to-RESULTS segment.",
        "",
        "Expected learning:",
        "  MATCH across segments -> continuation is likely evaluated once per",
        "  superposed command/result branch, localizing the defect above the",
        "  isolated writer corridor and below/within result-branch evaluation.",
        "  NO MATCH -> command cardinality is not the controlling variable.",
        "",
        "=== CAPTURE CONTRACT ===",
        f"Container: {args.container}",
        f"Start UTC: {start_utc}",
        f"Required complete segments: {args.segments}",
        "Production files edited: none",
        "v3 functions directly invoked: none",
        "Startup/translation output retained: no",
        "CHARS_SENT payload retained: no (character count only)",
        "",
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        preexec_fn=os.setsid,
    )

    if proc.stdout is None:
        raise RuntimeError("docker logs stdout unavailable")

    sel = selectors.DefaultSelector()
    sel.register(proc.stdout, selectors.EVENT_READ)

    segments: list[Segment] = []
    current: Optional[Segment] = None
    all_events: list[Event] = []
    first_result_monotonic: Optional[float] = None
    started = time.monotonic()
    stop_reason = ""

    try:
        while True:
            now = time.monotonic()
            if now - started > args.timeout:
                stop_reason = "absolute timeout"
                break
            if first_result_monotonic is None and now - started > args.wait_first:
                stop_reason = "first RESULTS marker timeout"
                break
            if len(segments) >= args.segments:
                stop_reason = f"captured {args.segments} complete segments"
                break

            ready = sel.select(timeout=0.5)
            if not ready:
                if proc.poll() is not None:
                    stop_reason = f"docker logs exited rc={proc.returncode}"
                    break
                continue

            line = proc.stdout.readline()
            if not line:
                if proc.poll() is not None:
                    stop_reason = f"docker logs exited rc={proc.returncode}"
                    break
                continue

            ev = parse_runtime_event(line)
            if ev is None:
                continue

            all_events.append(ev)

            if ev.kind == "RESULTS":
                if first_result_monotonic is None:
                    first_result_monotonic = time.monotonic()

                if current is not None:
                    current.end_result_ts = ev.ts
                    segments.append(current)

                current = Segment(
                    number=len(segments) + 1,
                    start_result_ts=ev.ts,
                    events=[ev],
                )
                continue

            if current is not None:
                current.add(ev)

    finally:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait(timeout=5)

    lines = list(header)
    lines += [
        "=== CAPTURE RESULT ===",
        f"Stop reason: {stop_reason}",
        f"Complete segments captured: {len(segments)}",
        f"Normalized runtime events retained: {len(all_events)}",
        "",
        "=== SEGMENT SUMMARY ===",
        (
            "SEG  SEXPR  POP-CYCLE  T172 T175 T176  BALANCED  "
            "TRIPLETS=SEXPR  ITERATIONS  IDLE ALIVE SEND/SILENT  DURATION"
        ),
        "-" * 118,
    ]

    decisive_rows = 0
    exact_matches = 0
    balanced_rows = 0

    for s in segments:
        balanced = s.trace172 == s.trace175 == s.trace176
        triplets = s.trace172 if balanced else None
        comparable = balanced and s.sexpr_len is not None
        match = comparable and triplets == s.sexpr_len
        if comparable:
            decisive_rows += 1
        if balanced:
            balanced_rows += 1
        if match:
            exact_matches += 1

        dur = duration_seconds(s.start_result_ts, s.end_result_ts or "")
        duration_text = f"{dur:.3f}s" if dur is not None else "n/a"
        iter_text = ",".join(str(x) for x in s.iterations) or "-"
        send_text = (
            f"{len(s.chars_sent)}/{s.silent_count}"
            if s.chars_sent or s.silent_count else "-"
        )
        lines.append(
            f"{s.number:>3}  "
            f"{str(s.sexpr_len) if s.sexpr_len is not None else '-':>5}  "
            f"{str(s.pop_cycle or '-'):>9}  "
            f"{s.trace172:>4} {s.trace175:>4} {s.trace176:>4}  "
            f"{('YES' if balanced else 'NO'):>8}  "
            f"{('YES' if match else ('NO' if comparable else 'N/A')):>14}  "
            f"{iter_text:<10}  "
            f"{s.idle_count:>4} {len(s.aliveness):>5} {send_text:>11}  "
            f"{duration_text}"
        )

    lines += ["", "=== ORDERED NORMALIZED EVENTS ==="]
    for s in segments:
        lines.append(f"--- SEGMENT {s.number}: RESULTS {s.start_result_ts} -> {s.end_result_ts} ---")
        for ev in s.events:
            detail = f" {ev.detail}" if ev.detail else ""
            lines.append(f"{ev.ts}  {ev.kind}{detail}")

    lines += ["", "=== T56 VERDICT ==="]

    if decisive_rows >= 3 and exact_matches == decisive_rows:
        verdict = (
            "SUPPORTED — in every comparable completed segment, the balanced "
            "TRACE-triplet count exactly equals POPULATOR-DIAG sexpr-len."
        )
        constraint = (
            "Durable constraint: the production multiplicity factor is command "
            "cardinality, not intrinsic writer branching. The next investigation "
            "must inspect the result-command superposition/evaluation boundary and "
            "where the post-results continuation remains inside that branch."
        )
    elif decisive_rows >= 3 and exact_matches < decisive_rows:
        verdict = (
            "NOT SUPPORTED — command cardinality does not consistently determine "
            "the balanced TRACE-triplet multiplicity."
        )
        constraint = (
            "Durable constraint: do not localize to command superposition from "
            "sexpr-len. The next test must compare another live cardinality at the "
            "same boundary."
        )
    else:
        verdict = (
            "INSUFFICIENT EVIDENCE — fewer than three complete comparable segments "
            "contained both POPULATOR sexpr-len and balanced TRACE counts."
        )
        constraint = (
            "No localization claim. Re-run with a longer timeout or more active "
            "completed response cycles; the parser itself retained only exact "
            "runtime witnesses."
        )

    lines += [
        verdict,
        "",
        f"Comparable segments: {decisive_rows}",
        f"Exact sexpr/triplet matches: {exact_matches}",
        f"Balanced TRACE segments: {balanced_rows}",
        "",
        constraint,
        "",
        "=== INVESTIGATION MAP ===",
        "F1. Genuine response cycles complete while visible iteration/populator remain 1.",
        "F2. TRACE-172/175/176 are balanced and multiply before the next cycle boundary.",
        "F3. Task-state remains bootstrap-frozen during completed cycles.",
        "F4. Recursive tail arithmetic/order advances correctly in isolation (T53).",
        "F5. Isolated cumulative post-results corridor is single-valued (T54).",
        "T56 tests whether the live multiplication factor is the command count itself.",
        "",
        f"Primary evidence log: {evidence}",
        "=== T56 COMPLETE ===",
    ]

    text = "\n".join(lines) + "\n"
    evidence.write_text(text)
    print(text, end="")

    return 0 if decisive_rows >= 3 else 2


if __name__ == "__main__":
    raise SystemExit(main())
