#!/usr/bin/env python3
"""v08.7.2 live import/runtime harness.

This harness is intentionally stricter than the candidate/ephemeral topology harness:

- It does NOT concatenate the engine into probe payloads.
- It does NOT stage substitute soul/evolutionary files into /tmp for semantic proof.
- Probe files import only the live project entrypoint, then run query-only checks.
- The engine and topology files are never concatenated into probes.
- Therefore reductions pass only if the live entrypoint import graph imports
  the v08.7.2 engine and the live soul/evolutionary + soul/durable files.

It writes temporary query files inside the live repo tree by default, because library import resolution may be contextual to the repo/library root. It still does not concatenate engine or topology contents into the probes.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import re
import shlex
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

VERSION = "v08.7.2-live-import-runtime-v01.2-repo-local-probe-entrypoint-query"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

LIVE_ENTRYPOINT_IMPORT = "!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_clarity_reasoning))"

SEMANTIC_PROBES = [
    ("canon eligibility runtime false", "!(q-evo-canon-eligible? runtime-observed)", "false"),
    ("canon eligibility soul approved", "!(q-evo-canon-eligible? soul-approved)", "canon-write-eligible"),
    ("illegal runtime to canon jump", "!(q-evo-lifecycle-next? runtime-observed durable-canon-active)", "blocked-illegal-jump"),
    ("validation not approval", "!(q-evo-lifecycle-next? validation-eligible durable-canon-active)", "blocked-no-soul-approval"),
    ("runtime surface not canon", "!(q-evo-surface-canon-status? soul-evolutionary-runtime runtime-observed)", "process-not-canon"),
    ("soul durable active canon", "!(q-evo-surface-canon-status? soul-durable-metta durable-canon-active)", "durable-canon-active"),
    ("finding no explicit route blocked", "!(q-evo-candidate-route? finding-present no-explicit-route trace-present)", "blocked-finding-is-not-growth"),
    ("genesis no explicit route blocked", "!(q-evo-candidate-route? genesis-output no-explicit-route trace-present)", "blocked-genesis-output-not-canon"),
    ("hand authored verdict blocked", "!(q-evo-validation-status? candidate observations-present preloaded-verdict-only harness-pass)", "blocked-hand-authored-verdict"),
    ("dark file blocked", "!(q-evo-restart-proof-status? candidate before-present after-restored not-imported-queryable)", "blocked-dark-file"),
    ("approval absent blocked", "!(q-evo-soul-approval-status? candidate validation-eligible restart-restored approval-absent)", "blocked-no-soul-approval"),
    ("durable canon active", "!(q-evo-durable-canon-status? candidate ground-atom import-live soul-approved revision-path-present)", "durable-canon-active"),
    ("unreduced storage blocked", "!(q-evo-durable-canon-status? candidate unreduced-expression import-live soul-approved revision-path-present)", "blocked-unreduced-storage"),
    ("trace A verdict", "!(q-tfs2-trace-verdict? same-start metabolizing-transition metabolized-protection)", "metabolization-candidate"),
    ("trace B verdict", "!(q-tfs2-trace-verdict? same-start stuck-recurrence-warning defensive-fixation-risk)", "blocked-defensive-fixation"),
    ("repetition without metabolization blocked", "!(q-tfs2-trace-verdict? same-start repeated-same-state repeated-same-state)", "blocked-repetition-without-metabolization"),
    ("Trace A eligibility", "!(q-tfs2-trace-eligibility? metabolization-candidate)", "validation-eligible"),
    ("Trace B audit", "!(q-tfs2-trace-eligibility? blocked-defensive-fixation)", "audit-required"),
    ("suspicion decays on metabolization", "!(q-evo-suspicion-delta? metabolization contactability-rises warrant-rises recurrence-supported)", "suspicion-decays"),
    ("suspicion rises on stuck recurrence", "!(q-evo-suspicion-delta? stuck-recurrence contactability-flat warrant-flat recurrence-repeated)", "suspicion-rises"),
    ("high protection alone not penalized", "!(q-evo-suspicion-delta? protection-high contactability-available warrant-rising recurrence-supported)", "no-suspicion-penalty"),
    ("journal class v1 accepted", "!(q-v08-7-file-class-status? soul-durable-metta journal-class semantic-gates-present)", "v1-accepted-mechanical-append-class"),
    ("unsupported durable class blocked", "!(q-v08-7-file-class-status? soul-durable-metta durable-canon-class rank-ladder-absent)", "blocked-unsupported-new-class"),
    ("canonical path accepted", "!(q-v08-7-path-discipline? canonical-absolute-soul-path allowlisted)", "path-accepted"),
    ("relative path blocked", "!(q-v08-7-path-discipline? relative-soul-path allowlisted)", "blocked-wrong-path-form"),
    ("append allowed", "!(q-v08-7-write-operation-status? append-file canonical-allowlisted journal-class approved)", "append-route-allowed"),
    ("write blocked", "!(q-v08-7-write-operation-status? write-file canonical-allowlisted journal-class approved)", "blocked-truncate-risk"),
    ("serialization valid", "!(q-v08-7-serialization-status? one-balanced-ground-directive ascii-safe)", "serialization-valid"),
    ("unreduced serialization blocked", "!(q-v08-7-serialization-status? unreduced-call-form ascii-safe)", "blocked-unreduced-storage"),
    ("import live", "!(q-v08-7-import-liveness? file-exists imported queryable-after-restart)", "import-live"),
    ("not imported blocked", "!(q-v08-7-import-liveness? file-exists not-imported queryable-after-restart)", "blocked-dark-file"),
    ("boot safe", "!(q-v08-7-boot-safety? valid-lines-only recovery-documented)", "boot-safe"),
    ("malformed recovery unknown blocked", "!(q-v08-7-boot-safety? malformed-line recovery-unknown)", "blocked-boot-poison-risk"),
    ("findings absent compatible", "!(q-v08-7-support-surface-status? soul-findings-metta absent explicit-route)", "no-op-compatible-absent"),
    ("finding without route blocked", "!(q-v08-7-support-surface-status? soul-findings-metta finding-present no-explicit-route)", "blocked-finding-not-growth"),
    ("chroma no route blocked", "!(q-v08-7-support-surface-status? chromadb retrieved no-explicit-route)", "blocked-retrieval-not-canon"),
    ("promotions no route blocked", "!(q-v08-7-support-surface-status? promotions-db active-flag no-explicit-route)", "blocked-status-flag-not-canon"),
    ("negative runtime claim blocked", "!(q-v08-7-negative-control? runtime-observation durable-canon-claimed)", "blocked-runtime-observation-is-not-growth"),
    ("negative validation claim blocked", "!(q-v08-7-negative-control? validation-pass durable-canon-claimed)", "blocked-validation-is-not-approval"),
    ("negative genesis claim blocked", "!(q-v08-7-negative-control? genesis-output durable-canon-claimed)", "blocked-genesis-output-not-canon"),
    ("hyperseed context valid", "!(q-hyperseed-context-status? context-present observer-bound aspect-indexed)", "context-valid"),
    ("hyperseed context missing blocked", "!(q-hyperseed-context-status? context-absent observer-bound aspect-indexed)", "blocked-context-missing"),
    ("hyperseed pbit evidence valid", "!(q-hyperseed-evidence-pbit-status? support-opposition-present confidence-graded contradiction-visible)", "pbit-evidence-valid"),
    ("hyperseed crisp certainty blocked", "!(q-hyperseed-evidence-pbit-status? support-opposition-present confidence-crisp contradiction-visible)", "blocked-crisp-certainty"),
    ("hyperseed proto time valid", "!(q-hyperseed-proto-time-status? window-present recurrence-observed interval-known)", "proto-time-valid"),
    ("hyperseed static presence blocked", "!(q-hyperseed-proto-time-status? window-present static-presence interval-known)", "blocked-static-presence-not-habit"),
    ("hyperseed structural signature valid", "!(q-hyperseed-structural-signature-status? signature-present invariant-named degradation-measured)", "structural-signature-valid"),
    ("hyperseed missing structural signature blocked", "!(q-hyperseed-structural-signature-status? signature-absent invariant-named degradation-measured)", "blocked-no-structural-signature"),
    ("hyperseed continuity valid", "!(q-hyperseed-continuity-degree-status? degree-present above-threshold degradation-known)", "continuity-valid"),
    ("hyperseed continuity too low blocked", "!(q-hyperseed-continuity-degree-status? degree-present below-threshold degradation-known)", "blocked-continuity-too-low"),
    ("hyperseed artifact lineage valid", "!(q-hyperseed-artifact-lineage-status? source-present approval-present revision-path-present)", "artifact-lineage-valid"),
    ("hyperseed approval lineage missing blocked", "!(q-hyperseed-artifact-lineage-status? source-present approval-absent revision-path-present)", "blocked-approval-lineage-missing"),
    ("hyperseed resource cost valid", "!(q-hyperseed-resource-cost-status? cost-visible sustainable bounded)", "resource-cost-valid"),
    ("hyperseed unbounded maintenance blocked", "!(q-hyperseed-resource-cost-status? cost-visible sustainable unbounded)", "blocked-unbounded-maintenance"),
    ("hyperseed transfer compatible", "!(q-hyperseed-cross-context-transfer-status? source-context target-context resonance-evidence-present)", "transfer-compatible"),
    ("hyperseed transfer without resonance blocked", "!(q-hyperseed-cross-context-transfer-status? source-context target-context resonance-evidence-absent)", "blocked-copy-without-resonance"),
    ("hyperseed approximation valid", "!(q-hyperseed-approximation-status? approximation-bound-present loss-known use-safe)", "approximation-valid"),
    ("hyperseed unsafe approximation blocked", "!(q-hyperseed-approximation-status? approximation-bound-present loss-known use-unsafe)", "blocked-unsafe-approximation"),
    ("hyperseed threshold pass", "!(q-v08-7-2-durable-growth-threshold? context-valid pbit-evidence-valid proto-time-valid structural-signature-valid continuity-valid artifact-lineage-valid resource-cost-valid approximation-valid)", "hyperseed-durability-threshold-pass"),
    ("hyperseed threshold context blocked", "!(q-v08-7-2-durable-growth-threshold? blocked-context-missing pbit-evidence-valid proto-time-valid structural-signature-valid continuity-valid artifact-lineage-valid resource-cost-valid approximation-valid)", "blocked-context-missing"),
    ("hyperseed import candidate ready", "!(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-green hyperseed-threshold-pass)", "import-candidate-ready"),
    ("hyperseed governance open hold", "!(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-open hyperseed-threshold-pass)", "hold-governance-not-green"),
    ("hyperseed file survival negative", "!(q-v08-7-2-negative-control? file-survival durable-growth-claimed)", "blocked-file-survival-not-structural-durability"),
    ("hyperseed contextless negative", "!(q-v08-7-2-negative-control? contextless-claim durable-growth-claimed)", "blocked-context-missing"),
    ("hyperseed cross context copy negative", "!(q-v08-7-2-negative-control? cross-context-copy transfer-claimed)", "blocked-copy-without-resonance"),
]

LIVE_REQUIRED_HOST_FILES = [
    "lib_clarity_reasoning/lib_clarity_reasoning.metta",
    "lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta",
    "soul/soul_kernel.metta",
    "soul/durable.metta",
    "soul/evolutionary/README.metta",
    "soul/evolutionary/archive/README.metta",
    "soul/evolutionary/index.metta",
    "soul/evolutionary/runtime.metta",
    "soul/evolutionary/pending.metta",
    "soul/evolutionary/validation.metta",
    "soul/evolutionary/restart.metta",
    "soul/evolutionary/rejected.metta",
]

LIB_REQUIRED_SNIPPETS = [
    "!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/README))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/index))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/runtime))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/pending))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/validation))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/restart))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/rejected))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/archive/README))",
    "!(import! &self (library omegaclaw ./soul/durable))",
]

KERNEL_REQUIRED_CLASS_LINES = [
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/runtime.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/pending.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/validation.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/restart.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/rejected.metta" journal))',
]

LIVE_TOPOLOGY_PROBES: List[Tuple[str, str, str]] = [
    ("live topology README imported", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-README loaded) live-readme-present)", "live-readme-present"),
    ("live topology archive README imported", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-archive-README loaded) live-archive-readme-present)", "live-archive-readme-present"),
    ("live topology index imported", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-index loaded) live-index-present)", "live-index-present"),
    ("live topology runtime imported", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-runtime loaded) live-runtime-present)", "live-runtime-present"),
    ("live topology pending imported", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-pending loaded) live-pending-present)", "live-pending-present"),
    ("live topology validation imported", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-validation loaded) live-validation-present)", "live-validation-present"),
    ("live topology restart imported", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-restart loaded) live-restart-present)", "live-restart-present"),
    ("live topology rejected imported", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-rejected loaded) live-rejected-present)", "live-rejected-present"),
    ("live durable imported", "!(match &self (q-v08-7-2-topology-file soul-durable-metta loaded) live-durable-present)", "live-durable-present"),
    ("live durable probe imported", "!(match &self (q-v08-7-2-durable-probe probe-durable active) live-durable-probe-present)", "live-durable-probe-present"),
    ("live runtime observation imported", "!(match &self (q-v08-7-2-runtime-observation probe-runtime observation-present) live-runtime-observation-present)", "live-runtime-observation-present"),
    ("live pending candidate imported", "!(match &self (q-v08-7-2-pending-candidate probe-candidate pending-validation) live-pending-candidate-present)", "live-pending-candidate-present"),
    ("live validation evidence imported", "!(match &self (q-v08-7-2-validation-evidence probe-candidate evidence-present) live-validation-evidence-present)", "live-validation-evidence-present"),
    ("live restart evidence imported", "!(match &self (q-v08-7-2-restart-evidence probe-candidate restored) live-restart-evidence-present)", "live-restart-evidence-present"),
    ("live rejected candidate imported", "!(match &self (q-v08-7-2-rejected-candidate probe-rejected audit-required) live-rejected-candidate-present)", "live-rejected-candidate-present"),
]

@dataclasses.dataclass
class Check:
    tier: str
    name: str
    status: str
    details: str = ""
    data: Any = None


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paren_balance(text: str) -> int:
    return text.count("(") - text.count(")")


def classify_line(s: str) -> str:
    if not s or s.startswith(";;"):
        return "skip-comment-or-empty"
    if not s.startswith("!(add-atom &self "):
        if s.startswith("(") and s.endswith(")"):
            return "blocked-bare-atom-not-boot-directive"
        return "blocked-non-add-atom-line"
    if s.count("(") != s.count(")"):
        return "blocked-unbalanced-directive"
    try:
        s.encode("ascii")
    except UnicodeEncodeError:
        return "blocked-non-ascii-line"
    return "serialization-valid"


def docker_exec(container: str, command: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["docker", "exec", container, "sh", "-c", command], input=stdin, text=True, capture_output=True)


def clean_output(text: str) -> str:
    return ANSI_RE.sub("", text or "")


def extract_tail(stdout: str, tail_lines: int = 12) -> List[str]:
    lines = [ln.strip() for ln in clean_output(stdout).splitlines() if ln.strip()]
    return lines[-tail_lines:]


def make_probe_name(probe_container_dir: str, idx: int, name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_")[:80]
    return f"{probe_container_dir.rstrip('/')}/_v08_7_2_live_import_{idx:03d}_{safe}.metta"


def run_query_probe(container: str, probe_container_dir: str, idx: int, name: str, expr: str, expected: str, raw_dir: Path, raw_mode: str, tail_chars: int) -> Check:
    mkdir = docker_exec(container, f"mkdir -p {shlex.quote(probe_container_dir)}")
    if mkdir.returncode != 0:
        return Check("L3", name, "FAIL", f"could not create probe dir: {mkdir.stderr.strip()}", {"probe_container_dir": probe_container_dir})
    probe_path = make_probe_name(probe_container_dir, idx, name)
    body = ";; v08.7.2 live entrypoint query probe\n"
    body += ";; No engine or topology files are concatenated here.\n"
    body += ";; This imports the live project entrypoint only, then asks the query.\n"
    body += LIVE_ENTRYPOINT_IMPORT + "\n"
    body += expr.rstrip() + "\n"
    w = docker_exec(container, f"cat > {shlex.quote(probe_path)}", body)
    if w.returncode != 0:
        return Check("L3", name, "FAIL", f"could not write query probe: {w.stderr.strip()}", {"probe_path": probe_path})
    run_cmd = f"cd /PeTTa && ./run.sh {shlex.quote(probe_path)} 2>&1"
    r = docker_exec(container, run_cmd)
    stdout = clean_output(r.stdout)
    stderr = clean_output(r.stderr)
    tail = extract_tail(stdout)
    expected_present = expected in stdout
    status = "PASS" if r.returncode == 0 and expected_present else "FAIL"
    raw_sidecar = None
    if raw_mode == "all" or (raw_mode == "fail" and status != "PASS"):
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_sidecar = raw_dir / (Path(probe_path).name + ".out.txt")
        raw_sidecar.write_text(stdout[-tail_chars:] if tail_chars > 0 else stdout)
    return Check(
        "L3",
        name,
        status,
        f"expected={expected}; present={expected_present}; returncode={r.returncode}",
        {
            "probe_path": probe_path,
            "docker_run_command": f"docker exec {container} sh -c {run_cmd!r}",
            "live_entrypoint_import": LIVE_ENTRYPOINT_IMPORT,
            "expression": expr,
            "expected_token": expected,
            "expected_present_in_stdout": expected_present,
            "actual_tail": tail,
            "returncode": r.returncode,
            "stderr_chars": len(stderr),
            "stdout_chars": len(stdout),
            "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
            "raw_sidecar_path": str(raw_sidecar) if raw_sidecar else None,
        },
    )


def validate_serialization(path: Path) -> Tuple[str, Dict[str, Any]]:
    if not path.exists():
        return "FAIL", {"path": str(path), "exists": False}
    bad=[]; checked=0; skipped=0
    for i,line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        verdict = classify_line(line.strip())
        if verdict.startswith("skip-"):
            skipped += 1
            continue
        checked += 1
        if verdict != "serialization-valid":
            bad.append({"line": i, "verdict": verdict, "text": line[:200]})
    return ("PASS" if not bad else "FAIL"), {"path": str(path), "checked_lines": checked, "skipped_lines": skipped, "bad": bad}


def main() -> int:
    ap = argparse.ArgumentParser(description="v08.7.2 live import/runtime query-only harness")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--container", default="clarity_omega")
    ap.add_argument("--container-repo-root", default="/PeTTa/repos/omegaclaw")
    ap.add_argument("--log-dir", default="shared_files")
    ap.add_argument("--raw-mode", choices=["none", "fail", "all"], default="fail")
    ap.add_argument("--raw-tail-chars", type=int, default=3000)
    ap.add_argument("--probe-container-dir", default="/PeTTa/repos/omegaclaw/shared_files/live_import_probes", help="Container directory where temporary query probes are written. Default is inside the live repo tree, not /tmp, to match library import context.")
    ns = ap.parse_args()

    root = Path(ns.repo_root)
    log_dir = Path(ns.log_dir); log_dir.mkdir(parents=True, exist_ok=True)
    checks: List[Check] = []
    meta = {
        "harness_version": VERSION,
        "mode": "repo-local-live-entrypoint-import-query-only",
        "container": ns.container,
        "repo_root": str(root),
        "container_repo_root": ns.container_repo_root,
        "ephemeral_engine_concat": False,
        "ephemeral_topology_concat": False,
        "live_entrypoint_import": LIVE_ENTRYPOINT_IMPORT,
        "probe_container_dir": ns.probe_container_dir,
    }

    inspect = subprocess.run(["docker", "inspect", ns.container], text=True, capture_output=True)
    checks.append(Check("L0", "container exists", "PASS" if inspect.returncode == 0 else "FAIL", inspect.stderr.strip()[:300]))
    if inspect.returncode != 0:
        return write_report(log_dir, checks, meta)

    for rel in LIVE_REQUIRED_HOST_FILES:
        p = root / rel
        checks.append(Check("L1", f"host file present: {rel}", "PASS" if p.exists() else "FAIL", f"size={p.stat().st_size} sha256={sha256_path(p)}" if p.exists() else "missing"))
    if any(c.status == "FAIL" for c in checks):
        return write_report(log_dir, checks, meta)

    lib = (root / "lib_clarity_reasoning/lib_clarity_reasoning.metta").read_text(errors="replace")
    kernel = (root / "soul/soul_kernel.metta").read_text(errors="replace")
    checks.append(Check("L1", "lib_clarity_reasoning paren balance", "PASS" if paren_balance(lib) == 0 else "FAIL", f"balance={paren_balance(lib)}"))
    checks.append(Check("L1", "soul_kernel paren balance", "PASS" if paren_balance(kernel) == 0 else "FAIL", f"balance={paren_balance(kernel)}"))
    missing_lib = [s for s in LIB_REQUIRED_SNIPPETS if s not in lib]
    checks.append(Check("L1", "live import block contains required imports", "PASS" if not missing_lib else "FAIL", f"missing={missing_lib}"))
    missing_classes = [s for s in KERNEL_REQUIRED_CLASS_LINES if s not in kernel]
    checks.append(Check("L1", "soul_kernel contains v08.7.2 journal class declarations", "PASS" if not missing_classes else "FAIL", f"missing={missing_classes}"))

    for rel in ["soul/durable.metta", "soul/evolutionary/README.metta", "soul/evolutionary/archive/README.metta", "soul/evolutionary/index.metta", "soul/evolutionary/runtime.metta", "soul/evolutionary/pending.metta", "soul/evolutionary/validation.metta", "soul/evolutionary/restart.metta", "soul/evolutionary/rejected.metta"]:
        status, data = validate_serialization(root / rel)
        checks.append(Check("L1", f"serialization valid: {rel}", status, f"checked={data.get('checked_lines')} bad={len(data.get('bad', []))}", data))

    for rel in LIVE_REQUIRED_HOST_FILES:
        host_path = root / rel
        container_path = f"{ns.container_repo_root.rstrip('/')}/{rel}"
        cmd = f"test -f {shlex.quote(container_path)} && sha256sum {shlex.quote(container_path)} | awk '{{print $1}}'"
        r = docker_exec(ns.container, cmd)
        host_sha = sha256_path(host_path)
        container_sha = r.stdout.strip().splitlines()[-1] if r.returncode == 0 and r.stdout.strip() else ""
        ok = r.returncode == 0 and container_sha == host_sha
        checks.append(Check("L2", f"container live file visible and sha-matched: {rel}", "PASS" if ok else "FAIL", f"container={container_path} sha_match={ok}", {"host_sha256": host_sha, "container_sha256": container_sha, "container_path": container_path, "returncode": r.returncode, "stderr": r.stderr.strip()}))

    raw_dir = log_dir / "raw_live_import_probe_outputs"
    idx = 1
    for name, expr, expected in LIVE_TOPOLOGY_PROBES:
        checks.append(run_query_probe(ns.container, ns.probe_container_dir, idx, name, expr, expected, raw_dir, ns.raw_mode, ns.raw_tail_chars)); idx += 1

    for name, expr, expected in SEMANTIC_PROBES:
        checks.append(run_query_probe(ns.container, ns.probe_container_dir, idx, f"live semantic: {name}", expr, expected, raw_dir, ns.raw_mode, ns.raw_tail_chars)); idx += 1

    return write_report(log_dir, checks, meta)


def write_report(log_dir: Path, checks: List[Check], meta: Dict[str, Any]) -> int:
    summary: Dict[str, int] = {}
    for c in checks:
        summary[c.status] = summary.get(c.status, 0) + 1
    report = {"meta": meta, "summary": summary, "checks": [dataclasses.asdict(c) for c in checks]}
    ts = time.strftime("%Y%m%d_%H%M%S")
    jpath = log_dir / f"v08_7_2_live_import_runtime_trace_{ts}.json"
    mpath = log_dir / f"v08_7_2_live_import_runtime_trace_{ts}.md"
    jpath.write_text(json.dumps(report, indent=2, sort_keys=True))
    lines = ["# v08.7.2 Live Entrypoint Runtime Harness Trace", "", f"harness: `{VERSION}`", "", "## Summary", "", "```json", json.dumps(summary, indent=2, sort_keys=True), "```", "", "## Checks", ""]
    for c in checks:
        lines.append(f"- **{c.status}** `{c.tier}` {c.name}: {c.details}")
    mpath.write_text("\n".join(lines) + "\n")
    print(json.dumps({"summary": summary, "json": str(jpath), "markdown": str(mpath)}, indent=2))
    return 1 if summary.get("FAIL", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
