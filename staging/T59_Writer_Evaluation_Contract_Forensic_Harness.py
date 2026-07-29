#!/usr/bin/env python3
"""
T59 — Writer evaluation-contract forensic harness

Purpose
-------
Ground the current recent-action continuation leak against the established
singleton clearer contract used by state-delta and coupling-status writers.

This harness follows the ClarityOmega cold-harness discipline:

  * hands only: Python constructs probes, runs /PeTTa/run.sh, parses traces,
    and compares against independently stated expected cardinalities;
  * actual MeTTa bodies are inlined from the current host files;
  * each scenario runs in a fresh evaluator / AtomSpace;
  * the exact script and complete raw runtime trace are preserved;
  * raw output is shown before every verdict;
  * unreduced detection scans only actual result sections;
  * a timestamped artifact is written to host shared_files/ and container /tmp/;
  * no production file is modified.

Surfaces compared
-----------------
1. RA-CURRENT
   Exact production-shaped recent-action snapshot and uncollapsed drain.

2. RA-RECONVERGED
   Same intentional () sentinel snapshot, but the drain is collapse-wrapped
   and the function explicitly returns one ().

3. SD-CLEARER
   Actual do-clear-state-delta! definition, inlined from the live host file.

4. CP-CLEARER
   Actual do-clear-coupling-status! definition, inlined from the live host file.

For ZERO / ONE / MANY seeded atoms, each fresh probe records:
  * function return cardinality;
  * enclosing continuation cardinality;
  * separately match-verified post-state cardinality.

The full raw trace, not the summary, is the primary evidence.

Run from repository root:
    python3 staging/t59_writer_evaluation_contract_forensic.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_LOG_DIR = Path("shared_files")
RUN_SH = "./run.sh"
TIMEOUT = 45

HOST_FILES = {
    "recent_action": Path("soul/recent_action_populator.metta"),
    "state_delta": Path("soul/state_delta_writer_writers.metta"),
    "coupling": Path("soul/coupling_integrity_detector_writers.metta"),
}

LIB_IMPORT_LINE = "!(import! &self (library lib_import))"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


# ---------------------------------------------------------------------------
# Recorder
# ---------------------------------------------------------------------------

class Recorder:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def pr(self, text: str = "") -> None:
        print(text)
        self.lines.append(text)

    def log_only(self, text: str = "") -> None:
        self.lines.append(text)

    def text(self) -> str:
        return "\n".join(self.lines) + "\n"


REC = Recorder()


def pr(text: str = "") -> None:
    REC.pr(text)


# ---------------------------------------------------------------------------
# Runtime plumbing
# ---------------------------------------------------------------------------

def run(cmd: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        input=input_text,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


def strip_ansi(text: str | None) -> str:
    return ANSI_RE.sub("", text or "")


def container_running(container: str) -> bool:
    try:
        proc = run([
            "docker", "ps",
            "--filter", f"name={container}",
            "--format", "{{.Names}}",
        ])
        return proc.returncode == 0 and container in proc.stdout.splitlines()
    except subprocess.TimeoutExpired:
        return False


def evaluator_exists(container: str) -> bool:
    proc = run(["docker", "exec", container, "test", "-f", "/PeTTa/run.sh"])
    return proc.returncode == 0


def read_host_file(repo: Path, rel: Path) -> str:
    return (repo / rel).read_text(errors="replace")


def extract_definition(body: str, function_name: str) -> str:
    """
    Extract one top-level (= (function-name ...) ...) form with a small
    code-aware parenthesis scanner. This reads the current file body rather
    than recreating the established clearer definitions by hand.
    """
    anchor = f"(= ({function_name}"
    start = body.find(anchor)
    if start < 0:
        raise ValueError(f"definition not found: {function_name}")

    depth = 0
    in_string = False
    escaped = False
    in_comment = False

    for idx in range(start, len(body)):
        ch = body[idx]

        if in_comment:
            if ch == "\n":
                in_comment = False
            continue

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue

        if ch == ";":
            in_comment = True
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return body[start:idx + 1]

    raise ValueError(f"unbalanced definition: {function_name}")


def evaluate_script(
    container: str,
    script: str,
    label: str,
    timestamp: str,
) -> tuple[str, str | None, str]:
    """
    Write the exact combined script into container /tmp and evaluate it with
    the established run.sh path. Record the complete script and complete raw
    trace in the durable artifact.
    """
    safe = re.sub(r"[^a-zA-Z0-9_]+", "_", label).strip("_").lower()
    temp_path = f"/tmp/t59_{timestamp}_{safe}.metta"

    write = run(
        ["docker", "exec", "-i", container, "sh", "-c", f"cat > {temp_path}"],
        input_text=script,
    )
    if write.returncode != 0:
        raw = ""
        err = f"temp write failed: {write.stderr}"
    else:
        proc = run([
            "docker", "exec", container, "sh", "-c",
            f"cd /PeTTa && {RUN_SH} {temp_path} 2>&1",
        ])
        raw = strip_ansi(proc.stdout)
        err = None if proc.returncode == 0 else f"evaluator rc={proc.returncode}"

    REC.log_only("")
    REC.log_only("=" * 88)
    REC.log_only(f"PROBE: {label}")
    REC.log_only(f"TEMP FILE: {temp_path}")
    REC.log_only("=" * 88)
    REC.log_only("EXACT SCRIPT SENT:")
    REC.log_only(script)
    REC.log_only("COMPLETE RAW RUNTIME TRACE:")
    REC.log_only(raw if raw else f"(no output; error={err})")
    REC.log_only("END COMPLETE RAW RUNTIME TRACE")
    return raw, err, temp_path


# ---------------------------------------------------------------------------
# Raw parsing
# ---------------------------------------------------------------------------

def result_sections(raw: str) -> list[list[str]]:
    """
    Split evaluator output into actual result sections. Each run.sh ! evaluation
    ends below a caret-only separator. Source echo and prolog goal stay above.
    """
    lines = strip_ansi(raw).splitlines()
    sections: list[list[str]] = []
    current: list[str] = []
    saw_separator = False

    for line in lines:
        stripped = line.strip()
        if stripped and set(stripped) == {"^"}:
            if saw_separator and current:
                sections.append(current)
            current = []
            saw_separator = True
            continue
        if saw_separator and stripped and stripped != "true":
            current.append(stripped)

    if saw_separator and current:
        sections.append(current)
    return sections


def flattened_results(raw: str) -> list[str]:
    return [line for section in result_sections(raw) for line in section]


def is_unreduced(raw: str, function_name: str) -> bool:
    pattern = re.compile(
        r"\(\s*" + re.escape(function_name) + r"(?=\s|\))"
    )
    return any(pattern.search(line) for line in flattened_results(raw))


def marker_lines(raw: str, prefix: str) -> list[str]:
    return [
        line.strip()
        for line in raw.splitlines()
        if line.strip().startswith(prefix)
    ]


def parse_count(raw: str, marker: str, shape: str, case: str) -> int | None:
    pattern = re.compile(
        rf"^\({re.escape(marker)}\s+{re.escape(shape)}\s+{re.escape(case)}"
        rf"\s+count\s+(\d+)\b"
    )
    for line in raw.splitlines():
        stripped = line.strip()
        match = pattern.search(stripped)
        if match:
            return int(match.group(1))
    return None


def count_exact_marker(raw: str, marker: str, shape: str, case: str) -> int:
    prefix = f"({marker} {shape} {case})"
    return sum(1 for line in raw.splitlines() if line.strip() == prefix)


def show_raw_tail(raw: str, n: int = 18) -> None:
    lines = [line for line in strip_ansi(raw).splitlines() if line.strip()]
    if not lines:
        pr("    (no raw output)")
        return
    for line in lines[-n:]:
        pr("    " + line)


# ---------------------------------------------------------------------------
# Probe construction
# ---------------------------------------------------------------------------

CASES = {
    "ZERO": 0,
    "ONE": 1,
    "MANY": 3,
}


@dataclass(frozen=True)
class Shape:
    name: str
    function_name: str
    source_definition: str
    predicate: str
    seed_template: str
    read_pattern: str


def ra_definition(function_name: str, predicate: str, reconverged: bool) -> str:
    snapshot = f"""(collapse
          (match &self
            ({predicate} $old-id $t $d)
            (if (< $old-id 0)
                ({predicate} $old-id $t $d)
                ())))"""

    if not reconverged:
        drain = """(let $old (superpose $to-remove)
       (if (== $old ())
           ()
           (remove-atom &self $old)))"""
    else:
        drain = """(if (== $to-remove ())
         ()
         (let $_drained
              (collapse
                (let $old (superpose $to-remove)
                  (if (== $old ())
                      ()
                      (remove-atom &self $old))))
           ()))"""

    return f"""(= ({function_name})
   (let $to-remove
        {snapshot}
     {drain}))"""


def build_shapes(repo: Path) -> list[Shape]:
    sd_body = read_host_file(repo, HOST_FILES["state_delta"])
    cp_body = read_host_file(repo, HOST_FILES["coupling"])

    sd_definition = extract_definition(sd_body, "do-clear-state-delta!")
    cp_definition = extract_definition(cp_body, "do-clear-coupling-status!")

    return [
        Shape(
            name="RA-CURRENT",
            function_name="t59-ra-current!",
            source_definition=ra_definition(
                "t59-ra-current!", "t59-ra-current-atom", False
            ),
            predicate="t59-ra-current-atom",
            seed_template="(t59-ra-current-atom {id} retained desc-{id})",
            read_pattern="(t59-ra-current-atom $id $t $d)",
        ),
        Shape(
            name="RA-RECONVERGED",
            function_name="t59-ra-reconverged!",
            source_definition=ra_definition(
                "t59-ra-reconverged!", "t59-ra-reconverged-atom", True
            ),
            predicate="t59-ra-reconverged-atom",
            seed_template="(t59-ra-reconverged-atom {id} retained desc-{id})",
            read_pattern="(t59-ra-reconverged-atom $id $t $d)",
        ),
        Shape(
            name="SD-CLEARER",
            function_name="do-clear-state-delta!",
            source_definition=sd_definition,
            predicate="state-delta",
            seed_template="(state-delta {id} verdict-{id})",
            read_pattern="(state-delta $id $v)",
        ),
        Shape(
            name="CP-CLEARER",
            function_name="do-clear-coupling-status!",
            source_definition=cp_definition,
            predicate="coupling-status",
            seed_template="(coupling-status {id} verdict-{id})",
            read_pattern="(coupling-status $id $v)",
        ),
    ]


def seed_lines(shape: Shape, count: int) -> list[str]:
    return [
        f"!(add-atom &self {shape.seed_template.format(id=i + 1)})"
        for i in range(count)
    ]


def make_probe(shape: Shape, case: str, count: int) -> str:
    """
    One fresh evaluator invocation. Return cardinality and continuation
    cardinality use separate atom predicates for RA shapes. For established
    clearers, the state is re-seeded between calls because the first call clears.
    """
    lines = [
        LIB_IMPORT_LINE,
        "",
        ";; ===== ACTUAL / TESTED DEFINITION =====",
        shape.source_definition,
        "",
        f"!(println! (T59-BEGIN {shape.name} {case}))",
        "",
        ";; ===== RETURN CARDINALITY SEED =====",
    ]
    lines.extend(seed_lines(shape, count))
    lines.extend([
        "",
        f"!(let $returns (collapse ({shape.function_name}))",
        f"   (println! (T59-RETURN {shape.name} {case}",
        "                           count (size-atom $returns)",
        "                           values $returns)))",
        "",
        ";; ===== RE-SEED FOR CONTINUATION TEST WHEN CLEARER REMOVED STATE =====",
    ])

    if shape.name in ("SD-CLEARER", "CP-CLEARER"):
        lines.extend(seed_lines(shape, count))

    lines.extend([
        "",
        f"!(let* (($_call ({shape.function_name}))",
        f"         ($_after (println! (T59-CONTINUATION {shape.name} {case}))))",
        "   ())",
        "",
        ";; ===== POST-STATE READ, SEPARATE FROM WRITE RETURN =====",
        f"!(let $remaining (collapse (match &self {shape.read_pattern} $id))",
        f"   (println! (T59-POSTSTATE {shape.name} {case}",
        "                              count (size-atom $remaining)",
        "                              values $remaining)))",
        "",
        f"!(println! (T59-END {shape.name} {case}))",
        "",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Expected references and verdicts
# ---------------------------------------------------------------------------

def expected(shape: str, count: int) -> tuple[int, int, int]:
    """
    Python reference for checking only.

    RA-CURRENT:
      retained atoms map to explicit () snapshot members; superpose returns one
      result per member; no atom is removed.

    RA-RECONVERGED:
      same retained state, but the drain reconverges to one function result and
      one continuation.

    SD/CP:
      clearer returns one result and clears all stored atoms.
    """
    if shape == "RA-CURRENT":
        return count, count, count
    if shape == "RA-RECONVERGED":
        return 1, 1, count
    return 1, 1, 0


@dataclass
class ProbeResult:
    shape: str
    case: str
    seeded: int
    returns: int | None
    continuations: int
    poststate: int | None
    unreduced: bool
    error: str | None
    raw: str
    temp_path: str
    passed: bool


def run_probe(
    container: str,
    shape: Shape,
    case: str,
    count: int,
    timestamp: str,
) -> ProbeResult:
    label = f"{shape.name}/{case}"
    script = make_probe(shape, case, count)
    raw, error, temp_path = evaluate_script(
        container, script, label, timestamp
    )

    returns = parse_count(raw, "T59-RETURN", shape.name, case)
    continuations = count_exact_marker(
        raw, "T59-CONTINUATION", shape.name, case
    )
    poststate = parse_count(raw, "T59-POSTSTATE", shape.name, case)
    unreduced = is_unreduced(raw, shape.function_name)

    exp_returns, exp_cont, exp_post = expected(shape.name, count)
    passed = (
        error is None
        and returns == exp_returns
        and continuations == exp_cont
        and poststate == exp_post
        and not unreduced
        and any(
            line.strip() == f"(T59-END {shape.name} {case})"
            for line in raw.splitlines()
        )
    )

    return ProbeResult(
        shape=shape.name,
        case=case,
        seeded=count,
        returns=returns,
        continuations=continuations,
        poststate=poststate,
        unreduced=unreduced,
        error=error,
        raw=raw,
        temp_path=temp_path,
        passed=passed,
    )


# ---------------------------------------------------------------------------
# Artifact writing
# ---------------------------------------------------------------------------

def write_artifact(
    log_dir: Path,
    timestamp: str,
    container: str,
) -> tuple[str, str]:
    filename = f"t59_writer_contract_forensic_{timestamp}.log"
    text = REC.text()

    log_dir.mkdir(parents=True, exist_ok=True)
    host_path = log_dir / filename
    host_path.write_text(text)

    container_path = f"/tmp/{filename}"
    write = run(
        ["docker", "exec", "-i", container, "sh", "-c",
         f"cat > {container_path}"],
        input_text=text,
    )
    if write.returncode != 0:
        container_path = f"(container write failed: {write.stderr.strip()})"

    return str(host_path), container_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--container", default=DEFAULT_CONTAINER)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR)
    args = parser.parse_args()

    repo = args.repo.resolve()
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

    pr("=" * 88)
    pr("T59 WRITER EVALUATION-CONTRACT FORENSIC HARNESS")
    pr("=" * 88)
    pr(f"timestamp: {timestamp}")
    pr(f"repo: {repo}")
    pr(f"container: {args.container}")
    pr("")
    pr("MANDATORY PREFLIGHT QUESTIONS")
    pr("1. Soul-absent test:")
    pr("   Not applicable to the cognition boundary: this harness changes no")
    pr("   production reasoning, voice, navigation, or action. It only observes")
    pr("   MeTTa evaluation cardinality in a cold synthetic AtomSpace.")
    pr("2. Frame-discipline test:")
    pr("   Current-state claims are read now from the host production files and")
    pr("   from fresh container runtime traces. T58's conclusion is treated as")
    pr("   a hypothesis to retest, not as authority.")
    pr("")
    pr("WHAT THIS DOES NOT TEST")
    pr("  - live loop behavior after a repair")
    pr("  - boot/import registration")
    pr("  - recent_action_retriever duplicate-cycle nondeterminism")
    pr("  - any production edit")
    pr("")

    pr("PREFLIGHT")
    if not container_running(args.container):
        pr(f"  [FAIL] container not running: {args.container}")
        host, cont = write_artifact(args.log_dir, timestamp, args.container)
        pr(f"  host log: {host}")
        pr(f"  container log: {cont}")
        return 2
    pr(f"  [PASS] container running: {args.container}")

    if not evaluator_exists(args.container):
        pr("  [FAIL] evaluator missing: /PeTTa/run.sh")
        host, cont = write_artifact(args.log_dir, timestamp, args.container)
        pr(f"  host log: {host}")
        pr(f"  container log: {cont}")
        return 2
    pr("  [PASS] evaluator present: /PeTTa/run.sh")

    missing = [
        str(rel) for rel in HOST_FILES.values()
        if not (repo / rel).is_file()
    ]
    if missing:
        for path in missing:
            pr(f"  [FAIL] host source missing: {path}")
        host, cont = write_artifact(args.log_dir, timestamp, args.container)
        pr(f"  host log: {host}")
        pr(f"  container log: {cont}")
        return 2

    for rel in HOST_FILES.values():
        pr(f"  [PASS] host source present: {rel}")

    try:
        shapes = build_shapes(repo)
    except Exception as exc:
        pr(f"  [FAIL] source-definition extraction: {exc}")
        host, cont = write_artifact(args.log_dir, timestamp, args.container)
        pr(f"  host log: {host}")
        pr(f"  container log: {cont}")
        return 2
    pr("  [PASS] actual clearer definitions extracted from current host source")

    REC.log_only("")
    REC.log_only("SOURCE EXCERPTS USED")
    REC.log_only("-" * 88)
    REC.log_only("RECENT-ACTION CURRENT SHAPE")
    REC.log_only(shapes[0].source_definition)
    REC.log_only("")
    REC.log_only("RECENT-ACTION RECONVERGED DIFFERENTIAL")
    REC.log_only(shapes[1].source_definition)
    REC.log_only("")
    REC.log_only("ACTUAL do-clear-state-delta! EXTRACTED NOW")
    REC.log_only(shapes[2].source_definition)
    REC.log_only("")
    REC.log_only("ACTUAL do-clear-coupling-status! EXTRACTED NOW")
    REC.log_only(shapes[3].source_definition)

    results: list[ProbeResult] = []

    for shape in shapes:
        for case, count in CASES.items():
            pr("")
            pr("-" * 88)
            pr(f"PROBE {shape.name}/{case}: seeded atoms={count}")
            pr("-" * 88)
            result = run_probe(
                args.container, shape, case, count, timestamp
            )
            results.append(result)

            pr("RAW OUTPUT TAIL BEFORE VERDICT:")
            show_raw_tail(result.raw)

            exp_return, exp_cont, exp_post = expected(shape.name, count)
            pr("VERDICT:")
            pr(
                f"  observed returns={result.returns}, "
                f"continuations={result.continuations}, "
                f"poststate={result.poststate}, "
                f"unreduced={result.unreduced}"
            )
            pr(
                f"  expected returns={exp_return}, "
                f"continuations={exp_cont}, poststate={exp_post}"
            )
            if result.error:
                pr(f"  runtime error: {result.error}")
            pr(f"  {'PASS' if result.passed else 'FAIL'}")

    pr("")
    pr("=" * 88)
    pr("SUMMARY")
    pr("=" * 88)
    pr(
        f"{'SHAPE':16} {'CASE':6} {'SEED':>4} {'RET':>4} "
        f"{'CONT':>5} {'POST':>5} {'UNRED':>6} {'VERDICT':>8}"
    )
    pr("-" * 72)
    for r in results:
        pr(
            f"{r.shape:16} {r.case:6} {r.seeded:>4} "
            f"{str(r.returns):>4} {r.continuations:>5} "
            f"{str(r.poststate):>5} "
            f"{str(r.unreduced):>6} "
            f"{('PASS' if r.passed else 'FAIL'):>8}"
        )

    all_pass = all(r.passed for r in results)
    pr("")
    pr("INVESTIGATION INTERPRETATION")
    if all_pass:
        pr("  SUPPORTED:")
        pr("  - RA-CURRENT exposes snapshot cardinality as function returns and")
        pr("    as enclosing continuation count.")
        pr("  - RA-RECONVERGED preserves the intentional () sentinel and stored")
        pr("    atoms while returning one continuation.")
        pr("  - The actual state-delta and coupling clearers return one")
        pr("    continuation and clear their stored atoms.")
        pr("  - This grounds the minimal repair surface at the recent-action")
        pr("    drain/reconvergence boundary, not at the intentional filter branch.")
    else:
        pr("  NOT GROUNDED:")
        pr("  At least one raw runtime probe disagreed with the stated contract.")
        pr("  Read that probe's complete trace in the artifact before proposing")
        pr("  any production change.")

    pr("")
    pr("DEFERRED ISSUE REGISTER")
    pr("  RA-SECONDARY-01 remains open:")
    pr("  Duplicate recent-action atoms sharing one cycle ID may cause")
    pr("  recent_action_retriever to select arbitrarily through car-atom.")
    pr("  It is not tested or repaired by T59.")

    host_path, container_path = write_artifact(
        args.log_dir, timestamp, args.container
    )
    pr("")
    pr("RESULTS ARTIFACT")
    pr(f"  host:      {host_path}")
    pr(f"  container: {container_path}")
    pr("  The artifact contains every exact script and complete raw trace.")
    pr("")
    pr("T59 COMPLETE")

    # Re-write after artifact paths were printed so the host artifact contains
    # the final summary and path lines too.
    Path(host_path).write_text(REC.text())
    run(
        ["docker", "exec", "-i", args.container, "sh", "-c",
         f"cat > {container_path}"],
        input_text=REC.text(),
    )

    return 0 if all_pass else 3


if __name__ == "__main__":
    raise SystemExit(main())
