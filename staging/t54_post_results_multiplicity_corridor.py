#!/usr/bin/env python3
"""
T54 — Post-results multiplicity corridor harness

Single variable under test:
    Evaluation result cardinality as the production post-results writer chain
    is extended one binding at a time.

Why this test:
    Production proves completed response cycles while $k, task-state, and the
    populator cycle remain frozen at 1. TRACE-172/175/176 multiply after
    RESULTS-EXECUTED. T53 established that (+ 1 $k) and the tail operator order
    work in isolation. T54 therefore tests the causal corridor immediately
    before the recursive tail and identifies the first production binding that
    changes one continuation into multiple continuations (or zero).

Non-invasive:
    - edits no production file;
    - runs each stage in a fresh /PeTTa/run.sh process;
    - imports the local mounted ClarityOmega production closure only;
    - uses unique synthetic ordinals;
    - invokes no LLM/network service;
    - writes one complete evidence log.

Run from the ClarityOmega repository root:
    python3 staging/t54_post_results_multiplicity_corridor.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import textwrap

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_REPO = Path.cwd()
DEFAULT_SHARED = Path("shared_files")
DEFAULT_OUT = Path("/tmp/cg-v3-investigation/second-failure/t54")
TIMEOUT = 180

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
ERROR_RE = re.compile(
    r"Unknown procedure|Domain error|not_less_than_zero|"
    r"METTA_ARGUMENT_PARSE_ERROR|ERROR:|Traceback|Exception"
)

LOOP_NEEDLES = [
    "($_ (println! (RESULTS-EXECUTED)))",
    "($_ (clarity-soul-mutation-commit-clear!",
    "($_ (populate-recent-action $sexpr $msgnew $k))",
    "($_ (populate-state-delta $msgnew $results_nonempty $results_novel $k))",
    "($_ (populate-coupling-verdict $k))",
    "($_ (do-record-coupling-cycle! $metta_cmds $msgnew $k",
    "($_ (do-update-idle-pattern!))",
    "($_ (do-update-agency-balance!))",
    "($_d1 (println! (DIAG-CYCLE-START $k)))",
    "($_d9 (println! (DIAG-CYCLE-END $k)))",
    "(omegaclaw (+ 1 $k))",
]

# Every stage is cumulative and ends in a unique sentinel. If an earlier
# binding produces N results, the later continuation can be entered N times.
STAGES = [
    (
        "S0-CONTROL",
        5400,
        "(progn (println! (T54-IN S0-CONTROL)) (T54-SENTINEL S0-CONTROL))",
        "Baseline: one ordinary continuation must return exactly one value.",
    ),
    (
        "S1-COMMIT-CLEAR",
        5401,
        """(let* (($_0 (println! (T54-IN S1-COMMIT-CLEAR)))
                    ($_1 (clarity-soul-mutation-commit-clear! none proceed False)))
             (T54-SENTINEL S1-COMMIT-CLEAR))""",
        "Adds production line 172 only.",
    ),
    (
        "S2-RECENT-ACTION",
        5402,
        """(let* (($_0 (println! (T54-IN S2-RECENT-ACTION)))
                    ($_1 (clarity-soul-mutation-commit-clear! none proceed False))
                    ($_2 (populate-recent-action () False 5402)))
             (T54-SENTINEL S2-RECENT-ACTION))""",
        "Adds production line 173. This is the TRACE-172 producer.",
    ),
    (
        "S3-STATE-DELTA",
        5403,
        """(let* (($_0 (println! (T54-IN S3-STATE-DELTA)))
                    ($_1 (clarity-soul-mutation-commit-clear! none proceed False))
                    ($_2 (populate-recent-action () False 5403))
                    ($_3 (populate-state-delta False False False 5403)))
             (T54-SENTINEL S3-STATE-DELTA))""",
        "Adds production line 176. This is the TRACE-175 producer.",
    ),
    (
        "S4-COUPLING-VERDICT",
        5404,
        """(let* (($_0 (println! (T54-IN S4-COUPLING-VERDICT)))
                    ($_1 (clarity-soul-mutation-commit-clear! none proceed False))
                    ($_2 (populate-recent-action () False 5404))
                    ($_3 (populate-state-delta False False False 5404))
                    ($_4 (populate-coupling-verdict 5404)))
             (T54-SENTINEL S4-COUPLING-VERDICT))""",
        "Adds production line 177. This is the TRACE-176 producer.",
    ),
    (
        "S5-V3-RECORDER",
        5405,
        """(let* (($_0 (println! (T54-IN S5-V3-RECORDER)))
                    ($_1 (clarity-soul-mutation-commit-clear! none proceed False))
                    ($_2 (populate-recent-action () False 5405))
                    ($_3 (populate-state-delta False False False 5405))
                    ($_4 (populate-coupling-verdict 5405))
                    ($_5 (do-record-coupling-cycle! () False 5405 ())))
             (T54-SENTINEL S5-V3-RECORDER))""",
        "Adds production line 178, the v3 recorder.",
    ),
    (
        "S6-IDLE-UPDATE",
        5406,
        """(let* (($_0 (println! (T54-IN S6-IDLE-UPDATE)))
                    ($_1 (clarity-soul-mutation-commit-clear! none proceed False))
                    ($_2 (populate-recent-action () False 5406))
                    ($_3 (populate-state-delta False False False 5406))
                    ($_4 (populate-coupling-verdict 5406))
                    ($_5 (do-record-coupling-cycle! () False 5406 ()))
                    ($_6 (do-update-idle-pattern!)))
             (T54-SENTINEL S6-IDLE-UPDATE))""",
        "Adds production line 179.",
    ),
    (
        "S7-AGENCY-UPDATE",
        5407,
        """(let* (($_0 (println! (T54-IN S7-AGENCY-UPDATE)))
                    ($_1 (clarity-soul-mutation-commit-clear! none proceed False))
                    ($_2 (populate-recent-action () False 5407))
                    ($_3 (populate-state-delta False False False 5407))
                    ($_4 (populate-coupling-verdict 5407))
                    ($_5 (do-record-coupling-cycle! () False 5407 ()))
                    ($_6 (do-update-idle-pattern!))
                    ($_7 (do-update-agency-balance!)))
             (T54-SENTINEL S7-AGENCY-UPDATE))""",
        "Adds production line 180; completes the writer corridor.",
    ),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(text: str) -> str:
    return ANSI_RE.sub("", text or "")


def run(cmd: list[str], timeout: int = TIMEOUT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def extract_context(path: Path, patterns: list[str], radius: int = 2) -> str:
    if not path.is_file():
        return f"MISSING: {path}\n"
    lines = path.read_text(errors="replace").splitlines()
    wanted: set[int] = set()
    for idx, line in enumerate(lines):
        if any(p in line for p in patterns):
            wanted.update(range(max(0, idx-radius), min(len(lines), idx+radius+1)))
    out = []
    previous = -2
    for idx in sorted(wanted):
        if idx > previous + 1:
            out.append("    ...")
        out.append(f"{idx+1:5d}: {lines[idx]}")
        previous = idx
    return "\n".join(out) + "\n"


def source_audit(repo: Path) -> tuple[bool, str]:
    loop = repo / "src/loop.metta"
    manifest = repo / "lib_clarity_reasoning/lib_clarity_reasoning.metta"
    required = [loop, manifest]
    rows = ["=== T54 SOURCE AND CLOSURE AUDIT ===", f"repo: {repo}"]
    ok = True
    for path in required:
        exists = path.is_file()
        rows.append(f"{'PASS' if exists else 'FAIL'} file: {path.relative_to(repo)}")
        if exists:
            rows.append(f"      sha256: {sha256(path)}")
        ok &= exists
    if loop.is_file():
        text = loop.read_text(errors="replace")
        for needle in LOOP_NEEDLES:
            present = needle in text
            rows.append(f"{'PASS' if present else 'FAIL'} loop witness: {needle}")
            ok &= present
    if manifest.is_file():
        m = manifest.read_text(errors="replace")
        checks = {
            "canonical v8.7.2 engine imported": "lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY" in m,
            "recent-action imported": "./soul/recent_action_populator" in m,
            "state-delta writers imported": "./soul/corner_gap/state_delta_writer_writers" in m,
            "coupling detector writers imported": "./soul/corner_gap/coupling_integrity_detector_writers" in m,
            "v3 pure imported": "./soul/corner_gap/coupling_legibility" in m,
            "v3 writers imported": "./soul/corner_gap/coupling_legibility_writers" in m,
        }
        for label, passed in checks.items():
            rows.append(f"{'PASS' if passed else 'FAIL'} manifest: {label}")
            ok &= passed
    rows.append("")
    rows.append("Production corridor copied into cumulative test stages:")
    rows.append(extract_context(loop, ["RESULTS-EXECUTED", "clarity-soul-mutation-commit-clear!", "populate-recent-action", "populate-state-delta", "populate-coupling-verdict", "do-record-coupling-cycle!", "do-update-idle-pattern!", "do-update-agency-balance!", "DIAG-CYCLE-START", "DIAG-CYCLE-END", "omegaclaw (+ 1 $k)"], radius=0))
    return ok, "\n".join(rows) + "\n"


def probe_text(stage_name: str, expression: str) -> str:
    # Local production closure only. No git-import and no network.
    return f'''!(import! &self (library lib_import))
!(import! &self /PeTTa/repos/omegaclaw/lib_omegaclaw.metta)

;; Bootstrap the state families used by the production corridor.
!(do-bootstrap-task-state!)
!(do-bootstrap-coupling!)

(= (t54-stage) {expression})

!(let $vals (collapse (t54-stage))
   (println! (T54-RESULT {stage_name}
                         count (size-atom $vals)
                         values $vals)))
!(println! (T54-END {stage_name}))
'''


def execute_stage(container: str, shared: Path, out: Path, name: str, ordinal: int, expr: str) -> dict:
    safe = name.lower().replace("-", "_")
    host_probe = shared / f"t54_{safe}.metta"
    host_probe.write_text(probe_text(name, expr))
    container_probe = f"/tmp/{host_probe.name}"

    p = run([
        "docker", "exec", container, "sh", "-lc",
        f"cd /PeTTa && /PeTTa/run.sh {container_probe}",
    ])
    raw = clean((p.stdout or "") + (p.stderr or ""))
    (out / f"{safe}.raw.log").write_text(raw)

    # Runtime witnesses only; translation definitions are intentionally excluded.
    witnesses = []
    for line in raw.splitlines():
        if any(mark in line for mark in [
            "(T54-IN ", "(T54-RESULT ", "(T54-END ",
            "(POPULATOR-DIAG ", "(TRACE-172-EXIT)",
            "(TRACE-175-ENTRY)", "(TRACE-176-ENTRY)",
        ]):
            # Exclude translated source/prolog representations by requiring the
            # compact runtime line to begin with the witness.
            stripped = line.strip()
            if stripped.startswith("(T54-") or stripped.startswith("(POPULATOR-DIAG") or stripped in {
                "(TRACE-172-EXIT)", "(TRACE-175-ENTRY)", "(TRACE-176-ENTRY)"
            }:
                witnesses.append(stripped)

    count_match = re.search(
        rf"\(T54-RESULT\s+{re.escape(name)}\s+count\s+([0-9]+)\s+values\s+(.*?)\)\s*$",
        "\n".join(witnesses), re.M,
    )
    count = int(count_match.group(1)) if count_match else None
    errors = [line.strip() for line in raw.splitlines() if ERROR_RE.search(line)]
    # Remove static definitions containing error vocabulary; keep only late/runtime
    # errors if no decisive witness was produced.
    runtime_errors = errors[-20:] if count is None else []

    return {
        "name": name,
        "ordinal": ordinal,
        "rc": p.returncode,
        "count": count,
        "witnesses": witnesses,
        "errors": runtime_errors,
        "probe": str(host_probe),
        "raw": str(out / f"{safe}.raw.log"),
    }


def analyze(results: list[dict]) -> str:
    rows = [
        "=== T54 POST-RESULTS MULTIPLICITY MAP ===",
        "",
        "Question: At which cumulative production binding does one continuation",
        "become zero or multiple continuations?",
        "",
        f"{'STAGE':24s} {'RC':>3s} {'CARDINALITY':>11s}  INTERPRETATION",
        "-" * 86,
    ]
    first_divergence = None
    previous = 1
    for r in results:
        count = r["count"]
        if count is None:
            interp = "NO DECISIVE WITNESS"
        elif count == 1:
            interp = "single continuation"
        elif count == 0:
            interp = "continuation extinguished"
        else:
            interp = f"continuation multiplied x{count}"
        rows.append(f"{r['name']:24s} {r['rc']:>3d} {str(count):>11s}  {interp}")
        if first_divergence is None and count != 1:
            first_divergence = r
        previous = count if count is not None else previous

    rows += ["", "=== DECISIVE WITNESSES ==="]
    for r in results:
        rows.append(f"\n--- {r['name']} ---")
        if r["witnesses"]:
            rows.extend(r["witnesses"])
        else:
            rows.append("NO RUNTIME WITNESSES CAPTURED")
        if r["errors"]:
            rows.append("RUNTIME ERRORS:")
            rows.extend(r["errors"])

    rows += ["", "=== T54 VERDICT ==="]
    incomplete = [r for r in results if r["rc"] != 0 or r["count"] is None]
    if incomplete:
        rows.append("INCOMPLETE: at least one cumulative stage did not produce a cardinality witness.")
        rows.append("Do not infer localization from partial stages.")
        rows.append("Incomplete stages: " + ", ".join(r["name"] for r in incomplete))
    elif first_divergence:
        idx = results.index(first_divergence)
        prior = results[idx-1]["name"] if idx > 0 else "none"
        rows.append(
            f"LOCALIZED: cardinality first diverges from 1 at {first_divergence['name']} "
            f"(after proven-single stage {prior})."
        )
        rows.append(
            "The new binding introduced by that stage is the first demonstrated "
            "source of continuation extinction/multiplication in this corridor."
        )
    else:
        rows.append("NO MULTIPLICITY IN ISOLATED CORRIDOR: every cumulative stage returned exactly one continuation.")
        rows.append(
            "The production multiplication therefore requires live-cycle input/state "
            "or a binding before RESULTS-EXECUTED; it is not intrinsic to these writer "
            "calls under controlled empty-cycle inputs."
        )

    rows += ["", "=== INVESTIGATION MAP UPDATE ==="]
    rows.append("Already proven before T54:")
    rows.append("  F1. Genuine response cycles complete while visible iteration and populator cycle remain 1.")
    rows.append("  F2. TRACE-172/175/176 are balanced triplets and multiply after RESULTS-EXECUTED.")
    rows.append("  F3. Task-state remains bootstrap-frozen during those completed cycles.")
    rows.append("  F4. (+ 1 $k), sleep, cut, gc, and their tail order advance correctly in isolation (T53).")
    rows.append("T54 adds:")
    if incomplete:
        rows.append("  No durable localization fact; one or more stages were not observed.")
    elif first_divergence:
        rows.append(f"  F5. First post-results cardinality divergence: {first_divergence['name']}.")
    else:
        rows.append("  F5. Controlled post-results writer corridor is single-valued end to end.")
        rows.append("  Constraint: next probe must preserve real live-cycle inputs/state while measuring the same corridor.")

    return "\n".join(rows) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    ap.add_argument("--shared", type=Path, default=DEFAULT_SHARED)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    repo = args.repo.resolve()
    shared = (repo / args.shared).resolve() if not args.shared.is_absolute() else args.shared
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    shared.mkdir(parents=True, exist_ok=True)

    log_path = out / "t54-evidence.log"
    audit_ok, audit = source_audit(repo)

    header = [
        "=== T54 HYPOTHESIS ===",
        "The frozen-$k / multiplying-TRACE failure is caused by result multiplicity",
        "inside the production post-results writer corridor. Extending the exact",
        "corridor one binding at a time will reveal the first binding where one",
        "continuation becomes zero or multiple continuations.",
        "",
        "Variable measured: evaluation result cardinality.",
        "Everything else: fresh process, same local production closure, controlled",
        "empty-cycle input, unique ordinal per stage.",
        "",
        audit,
    ]

    if not audit_ok:
        text = "\n".join(header) + "T54 ABORT: source/closure audit failed. Nothing executed.\n"
        log_path.write_text(text)
        print(text, end="")
        return 2

    ps = run(["docker", "ps", "--filter", f"name=^{args.container}$", "--format", "{{.Names}}"])
    if args.container not in ps.stdout.splitlines():
        text = "\n".join(header) + f"T54 ABORT: container not running: {args.container}\n"
        log_path.write_text(text)
        print(text, end="")
        return 2

    results = []
    for name, ordinal, expr, purpose in STAGES:
        print(f"T54 running {name}: {purpose}")
        results.append(execute_stage(args.container, shared, out, name, ordinal, expr))

    report = "\n".join(header) + analyze(results)
    report += "\n=== T54 ARTIFACTS ===\n"
    report += f"ONE PRIMARY LOG: {log_path}\n"
    report += "Generated probes:\n"
    for r in results:
        report += f"  {r['probe']}\n"
    report += "Raw logs retained only for forensic fallback:\n"
    for r in results:
        report += f"  {r['raw']}\n"
    report += "\n=== T54 COMPLETE ===\n"

    log_path.write_text(report)
    print("\n" + report, end="")

    complete = all(r["rc"] == 0 and r["count"] is not None for r in results)
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
