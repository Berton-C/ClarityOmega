#!/usr/bin/env python3
"""
quantale_v08_7_2_live_body_runtime_harness_v01_4.py

Purpose
-------
Validate v08.7.2 using the established one-shot run.sh transport discipline:
inline the ACTUAL LIVE FILE BODIES read from inside the running container, then
run query probes.

This is intentionally different from the failed live-import query-only harnesses:
  - one-shot run.sh probes do not reliably register import!-ed library rules for
    top-level ! evaluation;
  - therefore this harness does NOT claim to prove the production loop booted the
    import graph;
  - it DOES prove the mounted live files visible inside the container are exactly
    the files under test and reduce correctly when their bodies are loaded into a
    fresh one-shot AtomSpace.

Evidence discipline
-------------------
  1. Host files present and syntactically sane.
  2. Container-visible live files exist and SHA-match host files.
  3. Probe payload is assembled from container-read live file bodies, not local
     candidate bytes and not /tmp staged substitutes.
  4. Runtime probes execute with /PeTTa/run.sh.

Author: generated with ChatGPT for Berton Bennett / ClarityOmega.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

HARNESS_VERSION = "v08.7.2-live-body-runtime-v01.4-container-cat-inline-bodies"
DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_CONTAINER_REPO_ROOT = "/PeTTa/repos/omegaclaw"
RUN_SH_ROOT = "/PeTTa"
RUN_SH = "./run.sh"
LIB_IMPORT_LINE = "!(import! &self (library lib_import))"

ENGINE_REL = "lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta"
LADDER_REL = "staging/quantale_engine_validation_ladder_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta"
LIVE_BODY_RELS = [
    "lib_clarity_reasoning/lib_clarity_reasoning.metta",
    ENGINE_REL,
    "soul/soul_kernel.metta",
    "soul/evolutionary/README.metta",
    "soul/evolutionary/archive/README.metta",
    "soul/evolutionary/index.metta",
    "soul/evolutionary/runtime.metta",
    "soul/evolutionary/pending.metta",
    "soul/evolutionary/validation.metta",
    "soul/evolutionary/restart.metta",
    "soul/evolutionary/rejected.metta",
    "soul/durable.metta",
]

SERIALIZED_REL_FILES = [
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

REQUIRED_IMPORT_SUBSTRINGS = [
    "lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY",
    "./soul/evolutionary/README",
    "./soul/evolutionary/archive/README",
    "./soul/evolutionary/index",
    "./soul/evolutionary/runtime",
    "./soul/evolutionary/pending",
    "./soul/evolutionary/validation",
    "./soul/evolutionary/restart",
    "./soul/evolutionary/rejected",
    "./soul/durable",
]

REQUIRED_KERNEL_CLASS_LINES = [
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/runtime.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/pending.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/validation.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/restart.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/rejected.metta" journal))',
]

TOPOLOGY_PROBES: List[Tuple[str, str, str]] = [
    ("live body topology README", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-README loaded) live-readme-present)", "live-readme-present"),
    ("live body topology archive README", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-archive-README loaded) live-archive-readme-present)", "live-archive-readme-present"),
    ("live body topology index", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-index loaded) live-index-present)", "live-index-present"),
    ("live body topology runtime", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-runtime loaded) live-runtime-present)", "live-runtime-present"),
    ("live body topology pending", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-pending loaded) live-pending-present)", "live-pending-present"),
    ("live body topology validation", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-validation loaded) live-validation-present)", "live-validation-present"),
    ("live body topology restart", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-restart loaded) live-restart-present)", "live-restart-present"),
    ("live body topology rejected", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-rejected loaded) live-rejected-present)", "live-rejected-present"),
    ("live body durable", "!(match &self (q-v08-7-2-topology-file soul-durable-metta loaded) live-durable-present)", "live-durable-present"),
    ("live body durable probe", "!(match &self (q-v08-7-2-durable-probe probe-durable active) live-durable-probe-present)", "live-durable-probe-present"),
    ("live body runtime observation", "!(match &self (q-v08-7-2-runtime-observation probe-runtime observation-present) live-runtime-observation-present)", "live-runtime-observation-present"),
    ("live body pending candidate", "!(match &self (q-v08-7-2-pending-candidate probe-candidate pending-validation) live-pending-candidate-present)", "live-pending-candidate-present"),
    ("live body validation evidence", "!(match &self (q-v08-7-2-validation-evidence probe-candidate evidence-present) live-validation-evidence-present)", "live-validation-evidence-present"),
    ("live body restart evidence", "!(match &self (q-v08-7-2-restart-evidence probe-candidate restored) live-restart-evidence-present)", "live-restart-evidence-present"),
    ("live body rejected candidate", "!(match &self (q-v08-7-2-rejected-candidate probe-rejected audit-required) live-rejected-candidate-present)", "live-rejected-candidate-present"),
]

SEMANTIC_PROBES: List[Tuple[str, str, str]] = [
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

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(s: str) -> str:
    return ANSI_RE.sub("", s or "")


def run_cmd(cmd: List[str], input_text: Optional[str] = None, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, input=input_text, text=True, capture_output=True, timeout=timeout)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def file_sha(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def paren_balance(text: str) -> int:
    # Simple balance after stripping semicolon comments. Enough for regression checks.
    bal = 0
    for line in text.splitlines():
        body = line.split(";", 1)[0]
        bal += body.count("(") - body.count(")")
    return bal


def add_check(checks: List[Dict[str, Any]], name: str, status: str, tier: str, details: str = "", data: Any = None) -> None:
    checks.append({"name": name, "status": status, "tier": tier, "details": details, "data": data})


def container_exists(container: str) -> bool:
    p = run_cmd(["docker", "inspect", container], timeout=20)
    return p.returncode == 0


def container_cat(container: str, path: str) -> Tuple[Optional[str], str, int]:
    p = run_cmd(["docker", "exec", container, "sh", "-c", "cat " + shell_quote(path)], timeout=60)
    if p.returncode != 0:
        return None, p.stderr, p.returncode
    return p.stdout, p.stderr, p.returncode


def shell_quote(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"


def validate_serialized_file(text: str) -> Dict[str, Any]:
    bad = []
    checked = 0
    skipped = 0
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith(";"):
            skipped += 1
            continue
        checked += 1
        if not (stripped.startswith("!(add-atom &self ") and stripped.endswith(")")):
            bad.append({"line": i, "text": stripped, "verdict": "blocked-not-add-atom-directive"})
            continue
        if paren_balance(stripped) != 0:
            bad.append({"line": i, "text": stripped, "verdict": "blocked-unbalanced-directive"})
    return {"checked_lines": checked, "skipped_lines": skipped, "bad": bad}


def assemble_container_bodies(container: str, container_repo_root: str, checks: List[Dict[str, Any]]) -> Tuple[Optional[str], List[Dict[str, Any]]]:
    parts = [LIB_IMPORT_LINE]
    manifest = []
    for rel in LIVE_BODY_RELS:
        cpath = container_repo_root.rstrip("/") + "/" + rel
        body, stderr, rc = container_cat(container, cpath)
        if rc != 0 or body is None:
            add_check(checks, f"container cat live body: {rel}", "FAIL", "B0", f"rc={rc} stderr={stderr}")
            return None, manifest
        sha = sha256_text(body)
        manifest.append({"rel": rel, "container_path": cpath, "bytes": len(body.encode("utf-8")), "sha256": sha})
        parts.append(f"\n; BEGIN LIVE BODY {rel}\n")
        parts.append(body)
        parts.append(f"\n; END LIVE BODY {rel}\n")
    add_check(checks, "live body payload assembled from container cat", "PASS", "B0", f"files={len(manifest)}", manifest)
    return "\n".join(parts), manifest


def write_probe_to_container(container: str, script: str, probe_path: str) -> Tuple[bool, str]:
    p = run_cmd(["docker", "exec", "-i", container, "sh", "-c", "cat > " + shell_quote(probe_path)], input_text=script, timeout=90)
    if p.returncode != 0:
        return False, p.stderr
    return True, ""


def run_probe(container: str, probe_path: str, timeout: int) -> subprocess.CompletedProcess[str]:
    cmd = f"cd {shell_quote(RUN_SH_ROOT)} && {RUN_SH} {shell_quote(probe_path)} 2>&1"
    return run_cmd(["docker", "exec", container, "sh", "-c", cmd], timeout=timeout)


def output_tail(stdout: str, n: int = 10) -> List[str]:
    lines = [ln for ln in strip_ansi(stdout).splitlines() if ln.strip()]
    return lines[-n:]


def run_runtime_probe(
    container: str,
    base_payload: str,
    probe_dir: str,
    idx: int,
    name: str,
    expression: str,
    expected: str,
    checks: List[Dict[str, Any]],
    raw_dir: Path,
    timeout: int,
    raw_mode: str,
    raw_tail_chars: int,
) -> None:
    safe = re.sub(r"[^A-Za-z0-9_]+", "_", name).strip("_")[:80]
    probe_path = probe_dir.rstrip("/") + f"/_v08_7_2_live_body_{idx:03d}_{safe}.metta"
    script = base_payload + "\n\n; BEGIN PROBE\n" + expression + "\n; END PROBE\n"
    ok, err = write_probe_to_container(container, script, probe_path)
    if not ok:
        add_check(checks, name, "FAIL", "R1", "probe write failed", {"probe_path": probe_path, "stderr": err})
        return
    p = run_probe(container, probe_path, timeout)
    stdout = strip_ansi(p.stdout)
    stderr = strip_ansi(p.stderr)
    present = expected in stdout
    raw_sidecar_path = None
    if raw_mode == "all" or (raw_mode == "fail" and not present):
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_sidecar = raw_dir / (Path(probe_path).name + ".out.txt")
        raw_sidecar.write_text(stdout, encoding="utf-8")
        raw_sidecar_path = str(raw_sidecar)
    status = "PASS" if (p.returncode == 0 and present) else "FAIL"
    data = {
        "expression": expression,
        "expected_token": expected,
        "expected_present_in_stdout": present,
        "probe_path": probe_path,
        "docker_run_command": f"docker exec {container} sh -c 'cd {RUN_SH_ROOT} && {RUN_SH} {probe_path} 2>&1'",
        "returncode": p.returncode,
        "stdout_chars": len(stdout),
        "stdout_sha256": sha256_text(stdout),
        "stderr_chars": len(stderr),
        "stderr_sha256": sha256_text(stderr),
        "actual_tail": output_tail(stdout),
        "raw_sidecar_path": raw_sidecar_path,
    }
    if status == "FAIL" and raw_tail_chars > 0:
        data["raw_tail_chars"] = stdout[-raw_tail_chars:]
    add_check(checks, name, status, "R1", f"expected={expected}; present={present}; returncode={p.returncode}", data)


def summarize(checks: List[Dict[str, Any]]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for c in checks:
        out[c["status"]] = out.get(c["status"], 0) + 1
    return out


def write_markdown(path: Path, trace: Dict[str, Any]) -> None:
    lines = []
    lines.append(f"# {HARNESS_VERSION}")
    lines.append("")
    lines.append("## Summary")
    for k, v in sorted(trace["summary"].items()):
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("This harness inlines live file bodies read from the container. It proves live-mounted file bodies reduce under one-shot run.sh transport. It does not prove the production loop boot/import graph loaded them.")
    lines.append("")
    lines.append("## Checks")
    for c in trace["checks"]:
        lines.append(f"- `{c['tier']}` **{c['status']}** — {c['name']}: {c.get('details','')}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="v08.7.2 live body runtime harness")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--container-repo-root", default=DEFAULT_CONTAINER_REPO_ROOT)
    ap.add_argument("--probe-container-dir", default="/tmp")
    ap.add_argument("--log-dir", default="shared_files")
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--raw-mode", choices=["none", "fail", "all"], default="fail")
    ap.add_argument("--raw-tail-chars", type=int, default=3000)
    args = ap.parse_args()

    repo = Path(args.repo_root)
    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = log_dir / "raw_live_body_probe_outputs"
    checks: List[Dict[str, Any]] = []

    if container_exists(args.container):
        add_check(checks, "container exists", "PASS", "L0")
    else:
        add_check(checks, "container exists", "FAIL", "L0", f"container={args.container}")
        trace = {"meta": vars(args) | {"harness_version": HARNESS_VERSION}, "summary": summarize(checks), "checks": checks}
        _write_outputs(log_dir, trace)
        print(json.dumps({"summary": trace["summary"], "json": trace.get("json"), "markdown": trace.get("markdown")}, indent=2))
        return 1

    # Host file checks.
    host_shas: Dict[str, str] = {}
    for rel in sorted(set(LIVE_BODY_RELS + [LADDER_REL])):
        path = repo / rel
        if path.exists():
            sha = file_sha(path)
            host_shas[rel] = sha
            add_check(checks, f"host file present: {rel}", "PASS", "L1", f"size={path.stat().st_size} sha256={sha}")
        else:
            add_check(checks, f"host file present: {rel}", "FAIL", "L1", "missing")

    for rel in ["lib_clarity_reasoning/lib_clarity_reasoning.metta", ENGINE_REL, "soul/soul_kernel.metta"]:
        p = repo / rel
        if p.exists():
            bal = paren_balance(p.read_text(encoding="utf-8"))
            add_check(checks, f"paren balance: {rel}", "PASS" if bal == 0 else "FAIL", "L1", f"balance={bal}")

    lib_text = (repo / "lib_clarity_reasoning/lib_clarity_reasoning.metta").read_text(encoding="utf-8") if (repo / "lib_clarity_reasoning/lib_clarity_reasoning.metta").exists() else ""
    missing_imports = [s for s in REQUIRED_IMPORT_SUBSTRINGS if s not in lib_text]
    add_check(checks, "live import block contains required imports", "PASS" if not missing_imports else "FAIL", "L1", f"missing={missing_imports}")

    kernel_text = (repo / "soul/soul_kernel.metta").read_text(encoding="utf-8") if (repo / "soul/soul_kernel.metta").exists() else ""
    missing_classes = [s for s in REQUIRED_KERNEL_CLASS_LINES if s not in kernel_text]
    add_check(checks, "soul_kernel contains v08.7.2 journal class declarations", "PASS" if not missing_classes else "FAIL", "L1", f"missing={missing_classes}")

    for rel in SERIALIZED_REL_FILES:
        p = repo / rel
        if p.exists():
            v = validate_serialized_file(p.read_text(encoding="utf-8"))
            add_check(checks, f"serialization valid: {rel}", "PASS" if not v["bad"] else "FAIL", "L1", f"checked={v['checked_lines']} bad={len(v['bad'])}", {"path": rel, **v})

    # Container SHA visibility checks.
    for rel in LIVE_BODY_RELS:
        cpath = args.container_repo_root.rstrip("/") + "/" + rel
        body, stderr, rc = container_cat(args.container, cpath)
        if rc != 0 or body is None:
            add_check(checks, f"container live file visible and sha-matched: {rel}", "FAIL", "L2", f"rc={rc} stderr={stderr}", {"container_path": cpath})
            continue
        csha = sha256_text(body)
        hsha = host_shas.get(rel)
        add_check(
            checks,
            f"container live file visible and sha-matched: {rel}",
            "PASS" if hsha == csha else "FAIL",
            "L2",
            f"container={cpath} sha_match={hsha == csha}",
            {"container_path": cpath, "container_sha256": csha, "host_sha256": hsha, "returncode": rc, "stderr": stderr},
        )

    base_payload, manifest = assemble_container_bodies(args.container, args.container_repo_root, checks)
    if base_payload:
        payload_sha = sha256_text(base_payload)
        add_check(checks, "assembled live body payload sha", "PASS", "B0", f"bytes={len(base_payload.encode('utf-8'))} sha256={payload_sha}", {"sha256": payload_sha, "bytes": len(base_payload.encode("utf-8"))})
        probes = TOPOLOGY_PROBES + SEMANTIC_PROBES
        for i, (name, expr, expected) in enumerate(probes, 1):
            run_runtime_probe(args.container, base_payload, args.probe_container_dir, i, name, expr, expected, checks, raw_dir, args.timeout, args.raw_mode, args.raw_tail_chars)

    meta = {
        "harness_version": HARNESS_VERSION,
        "mode": "container-cat-live-body-inline-run-sh",
        "repo_root": args.repo_root,
        "container": args.container,
        "container_repo_root": args.container_repo_root,
        "probe_container_dir": args.probe_container_dir,
        "ephemeral_engine_concat": False,
        "ephemeral_topology_concat": False,
        "live_body_inline_transport": True,
        "production_boot_import_proof": False,
        "transport_note": "one-shot run.sh uses container-cat live file bodies; import!-only probes are known not to register rules for top-level ! evaluation",
    }
    trace = {"meta": meta, "summary": summarize(checks), "checks": checks}
    _write_outputs(log_dir, trace)
    print(json.dumps({"summary": trace["summary"], "json": trace["json"], "markdown": trace["markdown"]}, indent=2))
    return 0 if trace["summary"].get("FAIL", 0) == 0 else 1


def _write_outputs(log_dir: Path, trace: Dict[str, Any]) -> None:
    ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = log_dir / f"v08_7_2_live_body_runtime_trace_{ts}.json"
    md_path = log_dir / f"v08_7_2_live_body_runtime_trace_{ts}.md"
    trace["json"] = str(json_path)
    trace["markdown"] = str(md_path)
    json_path.write_text(json.dumps(trace, indent=2, sort_keys=False), encoding="utf-8")
    write_markdown(md_path, trace)


if __name__ == "__main__":
    raise SystemExit(main())
