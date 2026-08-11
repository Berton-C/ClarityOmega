#!/usr/bin/env python3
"""v08.7 Durable Evolutionary Governance Protocol harness.

Static mode validates engine/ladder artifacts and semantic coverage.
Runtime mode stages the cold engine/ladder artifacts into the container /tmp,
verifies their hashes there, then runs MeTTa reductions inside clarity_omega from
those container-resident bytes. Filesystem modes can inspect the v08.7 topology.
No runtime project files are modified unless --prepare-topology is explicitly used.
"""
from __future__ import annotations
import argparse, dataclasses, hashlib, json, os, re, shlex, subprocess, sys, time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION = "v08.7.2-soul-evolutionary-topology-v01.6-container-tmp-ephemeral-topology"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
WRITER_TERMS = ["(add-atom", "(remove-atom", "(set-atom!", "(append-file", "(write-file", "(sqlite3", "(chromadb"]

REQUIRED_LAWS = [
    "runtime-observation-is-not-growth",
    "finding-is-not-growth",
    "persistent-trace-is-not-growth",
    "recurrence-is-not-reinforcement-without-metabolization",
    "validation-is-not-soul-approval",
    "restart-survival-is-not-canon",
    "chroma-retrieval-is-not-durable-norm",
    "promotions-status-is-not-durable-canon",
    "history-survival-is-not-approved-growth",
    "genesis-encounter-output-is-not-durable-canon-without-lifecycle-passage",
    "only-soul-durable-metta-establishes-durable-canon",
    "evolutionary-memory-is-process-not-canon",
    "durable-canon-must-be-imported-and-queryable",
    "durable-canon-requires-ground-atom-serialization",
    "malformed-imported-line-is-boot-risk",
    "engine-stays-pure-harness-and-adapters-write",
    "durable-file-class-v1-is-journal-mechanical-only",
    "durability-is-structural-persistence-not-file-survival",
    "durable-growth-is-observer-relative-and-context-indexed",
    "durable-growth-is-graded-not-crisp-absolute-truth",
    "durable-growth-allows-paraconsistent-evidence-vectors",
    "reinforcement-requires-proto-time-not-static-presence",
    "continuity-requires-structural-signature-and-degree",
    "artifact-lineage-is-required-for-externalized-canon",
    "cross-context-transfer-requires-resonance-not-copying",
    "attention-and-maintenance-costs-must-be-visible",
    "approximate-preservation-is-valid-when-degradation-is-known",
    "hyperseed-threshold-must-pass-before-runtime-import-candidate",
    "no-runtime-file-mutation-in-completion-engine",
]

REQUIRED_FAMILIES = [
    "q-v08-7-evolutionary-path",
    "q-v08-7-durable-canon-path",
    "q-v08-7-surface-role?",
    "q-v08-7-required-surface?",
    "q-evo-lifecycle-next?",
    "q-evo-canon-eligible?",
    "q-evo-surface-canon-status?",
    "q-evo-candidate-route?",
    "q-evo-validation-status?",
    "q-evo-restart-proof-status?",
    "q-evo-soul-approval-status?",
    "q-evo-durable-canon-status?",
    "q-tfs2-polarity-trajectory?",
    "q-tfs2-trace-verdict?",
    "q-tfs2-trace-eligibility?",
    "q-tfs2-trace-durability?",
    "q-evo-suspicion-delta?",
    "q-evo-suspicion-route?",
    "q-v08-7-file-class-status?",
    "q-v08-7-path-discipline?",
    "q-v08-7-write-operation-status?",
    "q-v08-7-serialization-status?",
    "q-v08-7-import-liveness?",
    "q-v08-7-boot-safety?",
    "q-v08-7-support-surface-status?",
    "q-v08-7-negative-control?",
    "q-hyperseed-context-status?",
    "q-hyperseed-evidence-pbit-status?",
    "q-hyperseed-proto-time-status?",
    "q-hyperseed-structural-signature-status?",
    "q-hyperseed-continuity-degree-status?",
    "q-hyperseed-artifact-lineage-status?",
    "q-hyperseed-resource-cost-status?",
    "q-hyperseed-cross-context-transfer-status?",
    "q-hyperseed-approximation-status?",
    "q-v08-7-2-hyperseed-field-status?",
    "q-v08-7-2-durable-growth-threshold?",
    "q-v08-7-2-import-candidate-status?",
    "q-v08-7-2-support-evidence-role?",
    "q-v08-7-2-negative-control?",
]

HARNESS_TARGETS = [
    "topology-declared",
    "lifecycle-reduces",
    "candidate-canon-separation-reduces",
    "soul-approval-gate-reduces",
    "tfs2-polarity-dynamics-reduces",
    "suspicion-dynamics-reduces",
    "file-class-v1-decision-reduces",
    "path-discipline-reduces",
    "write-operation-boundary-reduces",
    "serialization-contract-reduces",
    "import-liveness-reduces",
    "boot-safety-reduces",
    "support-surface-boundaries-reduce",
    "negative-controls-block",
    "engine-purity-preserved",
    "hyperseed-fields-present",
    "context-status-reduces",
    "pbit-evidence-reduces",
    "proto-time-reduces",
    "structural-signature-reduces",
    "continuity-degree-reduces",
    "artifact-lineage-reduces",
    "resource-cost-reduces",
    "cross-context-transfer-reduces",
    "approximation-bound-reduces",
    "hyperseed-threshold-reduces",
    "import-candidate-status-reduces",
    "hyperseed-negative-controls-block",
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


def strip_comments(text: str) -> str:
    out=[]
    for line in text.splitlines():
        if line.lstrip().startswith(";;"):
            continue
        out.append(line)
    return "\n".join(out)


def section_55(text: str) -> str:
    marker = ";; 55. v08.7 Durable evolutionary governance protocol"
    idx = text.find(marker)
    return text[idx:] if idx >= 0 else ""



def clean_runtime_lines(stdout: str) -> List[str]:
    """Strip ANSI and common PeTTa/Prolog scaffolding, preserving semantic tokens."""
    s = ANSI_RE.sub("", stdout)
    out: List[str] = []
    for ln in s.splitlines():
        t = ln.strip()
        if not t:
            continue
        if t.startswith("-->") or t.startswith(":-") or t.startswith("^"):
            continue
        low = t.lower()
        if any(x in low for x in ["prolog goal", "metta function", "metta sexpr", "metta runnable"]):
            continue
        if t in {"A),", "_).", "A).", "_)."}:
            continue
        if re.fullmatch(r"'[^']+',?", t):
            continue
        if t.startswith("!(q-"):
            continue
        if t.startswith("(q-v08-7-harness-target "):
            continue
        out.append(t)
    return out


def extract_result(stdout: str, expected: str) -> Tuple[str, List[str], bool]:
    """Return a concise semantic result token plus cleaned tail."""
    lines = clean_runtime_lines(stdout)
    token_match = any(ln == expected or expected in ln.split() for ln in lines)
    token = expected if token_match else (lines[-1] if lines else "")
    return token, lines[-8:], token_match


def docker_exec(container: str, command: str, input_text: Optional[str] = None, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    """Run a shell command in the container. Input is optional text."""
    return subprocess.run(
        ["docker", "exec", "-i", container, "sh", "-c", command],
        input=input_text,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def stage_artifacts_to_container(container: str, engine: Path, ladder: Path, tmp_dir: str) -> Tuple[bool, Dict[str, Any]]:
    """Copy engine and ladder into container tmp and verify hashes there.

    This is intentionally modeled after the corner-gap harness discipline:
    the cold artifact bytes are placed inside the live runtime container first,
    then all runtime probes are assembled from those in-container bytes.
    That catches host/container drift and validates against the real run.sh
    environment without mutating project runtime files.
    """
    tmp_dir_q = shlex.quote(tmp_dir.rstrip("/"))
    engine_dst = f"{tmp_dir.rstrip('/')}/v08_7_2_engine_under_test.metta"
    ladder_dst = f"{tmp_dir.rstrip('/')}/v08_7_2_ladder_under_test.metta"
    mk = docker_exec(container, f"mkdir -p {tmp_dir_q}")
    if mk.returncode != 0:
        return False, {"phase": "mkdir", "stderr": mk.stderr, "tmp_dir": tmp_dir}
    artifacts = [("engine", engine, engine_dst), ("ladder", ladder, ladder_dst)]
    copied = []
    for label, src, dst in artifacts:
        w = docker_exec(container, f"cat > {shlex.quote(dst)}", src.read_text())
        if w.returncode != 0:
            return False, {"phase": f"copy-{label}", "stderr": w.stderr, "dst": dst}
        h = docker_exec(container, f"sha256sum {shlex.quote(dst)} | awk '{{print $1}}'")
        if h.returncode != 0:
            return False, {"phase": f"hash-{label}", "stderr": h.stderr, "dst": dst}
        host_sha = sha256_path(src)
        container_sha = h.stdout.strip().splitlines()[-1] if h.stdout.strip() else ""
        copied.append({
            "label": label,
            "host_path": str(src),
            "container_path": dst,
            "host_sha256": host_sha,
            "container_sha256": container_sha,
            "sha_match": host_sha == container_sha,
            "bytes": src.stat().st_size,
        })
        if host_sha != container_sha:
            return False, {"phase": f"sha-mismatch-{label}", "artifacts": copied}
    return True, {"tmp_dir": tmp_dir, "engine_container_path": engine_dst, "ladder_container_path": ladder_dst, "artifacts": copied}


def run_docker_probe(container: str, engine: Path, expr: str, expected: str,
                     idx: int, name: str, raw_dir: Path, raw_mode: str, tail_chars: int,
                     container_engine_path: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
    temp = f"/tmp/_v08_7_durable_evo_{idx:03d}_{re.sub(r'[^a-zA-Z0-9]+','_', name)[:40]}.metta"
    if container_engine_path:
        # Assemble the probe FROM the in-container engine copy. This validates the
        # exact bytes staged in /tmp against the live runtime's run.sh.
        append_expr = f"printf '\\n%s\\n' {shlex.quote(expr)} >> {shlex.quote(temp)}"
        assemble_cmd = f"cat {shlex.quote(container_engine_path)} > {shlex.quote(temp)} && {append_expr}"
        p = docker_exec(container, assemble_cmd)
        write_phase = "assemble-from-container-engine"
    else:
        payload = engine.read_text() + "\n" + expr + "\n"
        p = docker_exec(container, f"cat > {shlex.quote(temp)}", payload)
        write_phase = "write-host-concatenated-payload"
    if p.returncode != 0:
        return False, {"phase": write_phase, "returncode":p.returncode, "stderr":p.stderr[-tail_chars:], "temp_path": temp, "container_engine_path": container_engine_path}
    run_cmd = ["docker", "exec", container, "sh", "-c", f"cd /PeTTa && ./run.sh {shlex.quote(temp)} 2>&1"]
    q = subprocess.run(run_cmd, text=True, capture_output=True)
    raw = q.stdout + q.stderr
    result_token, result_section, token_match = extract_result(raw, expected)
    raw_path = None
    if raw_mode == "all" or (raw_mode == "fail" and (q.returncode != 0 or not token_match)):
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = raw_dir / f"probe_{idx:03d}_{re.sub(r'[^a-zA-Z0-9]+','_', name)[:40]}.raw.txt"
        raw_path.write_text(raw)
    return q.returncode == 0, {
        "returncode": q.returncode,
        "actual_result_text": result_token,
        "actual_result_section": result_section,
        "stdout_chars": len(q.stdout),
        "stdout_sha256": hashlib.sha256(q.stdout.encode()).hexdigest(),
        "stderr_chars": len(q.stderr),
        "stderr_sha256": hashlib.sha256(q.stderr.encode()).hexdigest(),
        "raw_sidecar_path": str(raw_path) if raw_path else None,
        "docker_run_command": " ".join(shlex.quote(x) for x in run_cmd),
        "temp_path": temp,
        "probe_assembly_phase": write_phase,
        "container_engine_path": container_engine_path,
    }


def classify_line(line: str) -> str:
    s = line.strip()
    if not s:
        return "skip-empty"
    if s.startswith(";;"):
        return "skip-comment"
    if not s.isascii():
        return "blocked-non-ascii-risk"
    if "\n" in s or "\r" in s:
        return "blocked-multiline-risk"
    if paren_balance(s) != 0:
        return "blocked-malformed-directive"
    if not s.startswith("!(add-atom &self "):
        if s.startswith("(") and s.endswith(")"):
            return "blocked-bare-atom-not-boot-directive"
        return "blocked-bad-directive-head"
    if re.search(r'\(!|\(\s*eval|\(\s*let|\(\s*match|\(\s*collapse|\(\s*superpose', s):
        return "blocked-unreduced-storage"
    return "serialization-valid"



def read_text_if_exists(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() and path.is_file() else ""


def inspect_governance(root: Path, manifest: Optional[str]) -> List[Check]:
    checks: List[Check] = []
    kernel = root / "soul" / "soul_kernel.metta"
    ktxt = read_text_if_exists(kernel)
    durable_abs = "/PeTTa/repos/omegaclaw/soul/durable.metta"
    durable_line = f'(soul-file-class "{durable_abs}" journal)'
    durable_add_atom_line = f'!(add-atom &self {durable_line})'
    class_atoms = re.findall(r'\(soul-file-class\s+"([^"]+)"\s+([^)]+)\)', ktxt)
    classes = sorted(set(cls.strip() for _, cls in class_atoms))
    if not ktxt:
        checks.append(Check("G0", "soul kernel readable", "HOLD", f"missing={kernel}",
                            {"recommended_kernel_line": durable_add_atom_line}))
        return checks
    checks.append(Check(
        "G0",
        "soul kernel readable",
        "PASS",
        f"path={kernel} class_atoms={len(class_atoms)} classes={classes}",
        {"class_atoms": class_atoms[:20], "classes": classes, "recommended_kernel_line": durable_add_atom_line},
    ))
    checks.append(Check(
        "G1",
        "durable.metta journal class declaration",
        "PASS" if durable_line in ktxt else "HOLD",
        "present" if durable_line in ktxt else f"missing expected class declaration for {durable_abs}",
        {
            "expected_substring": durable_line,
            "recommended_kernel_line": durable_add_atom_line,
            "interpretation": "journal is mechanical append permission; durable-canon status remains semantic",
        },
    ))
    checks.append(Check(
        "G1",
        "soul file class default-deny visible",
        "PASS" if "runtime-soul" in ktxt and "soul-file-class-of" in ktxt else "HOLD",
        "runtime-soul fallback visible" if "runtime-soul" in ktxt and "soul-file-class-of" in ktxt else "fallback not found",
    ))
    candidates: List[Path] = []
    if manifest:
        candidates.append(root / manifest)
        candidates.append(Path(manifest))
    for pat in [
        "**/lib_clarity_reasoning*.metta",
        "**/*manifest*.metta",
        "**/*reasoning*.metta",
        "**/*import*.metta",
        "**/*bootstrap*.metta",
        "**/*init*.metta",
        "**/*.metta",
    ]:
        candidates.extend(root.glob(pat))
    seen=set(); candidates=[p for p in candidates if not (str(p) in seen or seen.add(str(p)))]
    import_hits=[]
    searched=[]
    for p in candidates[:300]:
        searched.append(str(p))
        body=read_text_if_exists(p)
        if "durable.metta" in body or durable_abs in body:
            import_hits.append(str(p))
    checks.append(Check(
        "G2",
        "durable.metta import-chain reference",
        "PASS" if import_hits else "HOLD",
        f"import_hits={import_hits[:10]}" if import_hits else "no durable.metta import reference found in searched manifest candidates",
        {
            "searched_count": len(candidates),
            "searched_sample": searched[:40],
            "import_hits": import_hits[:20],
            "recommended_import_target": "/PeTTa/repos/omegaclaw/soul/durable.metta",
            "recommended_import_line_hint": "Add the project-standard import/include form used by the active boot manifest for /PeTTa/repos/omegaclaw/soul/durable.metta.",
        },
    ))
    return checks


def validate_serialization_file(path: Path) -> Tuple[str, Dict[str, Any]]:
    if not path.exists():
        return "HOLD", {
            "path": str(path),
            "exists": False,
            "recommended_minimal_file": [
                ";; v08.7 soul durable canon append surface",
                ";; append-only; one !(add-atom &self (...)) directive per durable canon line",
            ],
        }
    bad=[]
    checked=0
    skipped=0
    for i,line in enumerate(path.read_text(errors="replace").splitlines(),1):
        s=line.strip()
        verdict = classify_line(s)
        if verdict.startswith("skip-"):
            skipped += 1
            continue
        checked += 1
        if verdict != "serialization-valid":
            recommendation = None
            if verdict == "blocked-bare-atom-not-boot-directive":
                recommendation = f"!(add-atom &self {s})"
            bad.append({"line": i, "verdict": verdict, "text": s[:200], "recommended_rewrite": recommendation})
    return ("PASS" if not bad else "FAIL"), {
        "path": str(path),
        "checked_lines": checked,
        "skipped_lines": skipped,
        "bad": bad[:20],
        "format_contract": "Boot-imported durable files must use one balanced ASCII !(add-atom &self (...)) directive per non-comment line.",
    }



EPHEMERAL_TOPOLOGY_FILES: Dict[str, str] = {
    "soul/evolutionary/README.metta": ";; v08.7.2 ephemeral soul/evolutionary README\n!(add-atom &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-README loaded))\n",
    "soul/evolutionary/index.metta": ";; v08.7.2 ephemeral evolutionary index\n!(add-atom &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-index loaded))\n",
    "soul/evolutionary/runtime.metta": ";; v08.7.2 ephemeral runtime observations\n!(add-atom &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-runtime loaded))\n!(add-atom &self (q-v08-7-2-runtime-observation probe-runtime observation-present))\n",
    "soul/evolutionary/pending.metta": ";; v08.7.2 ephemeral pending candidates\n!(add-atom &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-pending loaded))\n!(add-atom &self (q-v08-7-2-pending-candidate probe-candidate pending))\n",
    "soul/evolutionary/validation.metta": ";; v08.7.2 ephemeral validation evidence\n!(add-atom &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-validation loaded))\n!(add-atom &self (q-v08-7-2-validation-evidence probe-candidate evidence-present))\n",
    "soul/evolutionary/restart.metta": ";; v08.7.2 ephemeral restart evidence\n!(add-atom &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-restart loaded))\n!(add-atom &self (q-v08-7-2-restart-evidence probe-candidate restored))\n",
    "soul/evolutionary/rejected.metta": ";; v08.7.2 ephemeral rejected candidates\n!(add-atom &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-rejected loaded))\n!(add-atom &self (q-v08-7-2-rejected-candidate probe-rejected audit-required))\n",
    "soul/durable.metta": ";; v08.7.2 ephemeral soul durable canon test surface\n;; one balanced ASCII !(add-atom &self (...)) directive per non-comment line\n!(add-atom &self (q-v08-7-2-ephemeral-topology-file soul-durable-metta loaded))\n!(add-atom &self (q-v08-7-2-ephemeral-durable-probe probe-durable active))\n",
}

EPHEMERAL_EXPECTED_TOKENS = [
    "readme-present",
    "index-present",
    "runtime-present",
    "pending-present",
    "validation-present",
    "restart-present",
    "rejected-present",
    "durable-present",
    "durable-probe-present",
    "runtime-observation-present",
    "pending-candidate-present",
    "validation-evidence-present",
    "restart-evidence-present",
    "rejected-candidate-present",
]


def stage_ephemeral_topology_to_container(container: str, tmp_dir: str) -> Tuple[bool, Dict[str, Any]]:
    """Create an isolated v08.7.2 topology under container /tmp.

    This intentionally does NOT touch /PeTTa/repos/omegaclaw or any bind-mounted
    runtime project file. It gives us container-visible .metta files with the same
    relative surfaces v08.7 will eventually use, so the runtime can parse/load
    representative durable/process files before implementation.
    """
    base = f"{tmp_dir.rstrip('/')}/v08_7_2_ephemeral_topology_under_test"
    rm = docker_exec(container, f"rm -rf {shlex.quote(base)} && mkdir -p {shlex.quote(base)}/soul/evolutionary/archive {shlex.quote(base)}/soul")
    if rm.returncode != 0:
        return False, {"phase": "mkdir-ephemeral-topology", "stderr": rm.stderr, "base": base}
    files=[]
    for rel, body in EPHEMERAL_TOPOLOGY_FILES.items():
        path = f"{base}/{rel}"
        verdicts=[]
        for line in body.splitlines():
            v=classify_line(line.strip())
            if not v.startswith('skip-'):
                verdicts.append(v)
        if any(v != 'serialization-valid' for v in verdicts):
            return False, {"phase": "local-serialization-contract", "rel": rel, "verdicts": verdicts}
        w = docker_exec(container, f"mkdir -p $(dirname {shlex.quote(path)}) && cat > {shlex.quote(path)}", body)
        if w.returncode != 0:
            return False, {"phase": f"write-{rel}", "stderr": w.stderr, "path": path}
        h = docker_exec(container, f"sha256sum {shlex.quote(path)} | awk '{{print $1}}'")
        files.append({"rel": rel, "container_path": path, "bytes": len(body.encode()), "sha256": h.stdout.strip().splitlines()[-1] if h.stdout.strip() else "", "serialization_verdicts": verdicts})
    return True, {"base": base, "files": files, "archive_dir": f"{base}/soul/evolutionary/archive"}


def run_ephemeral_topology_probe(container: str, container_engine_path: str, topology_base: str,
                                 raw_dir: Path, raw_mode: str, tail_chars: int) -> Tuple[bool, Dict[str, Any]]:
    """Run a composite runtime probe assembled from container engine + container topology files.

    This is a pre-implementation verification path. It does not claim the project
    boot manifest imports these files. It proves the representative files are in
    the container, boot-safe at line level, and executable under /PeTTa/run.sh when
    assembled as a topology payload.
    """
    composite = "/tmp/_v08_7_2_ephemeral_topology_composite_probe.metta"
    paths = [f"{topology_base}/{rel}" for rel in EPHEMERAL_TOPOLOGY_FILES.keys()]
    query_lines = [
        "!(match &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-README loaded) readme-present)",
        "!(match &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-index loaded) index-present)",
        "!(match &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-runtime loaded) runtime-present)",
        "!(match &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-pending loaded) pending-present)",
        "!(match &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-validation loaded) validation-present)",
        "!(match &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-restart loaded) restart-present)",
        "!(match &self (q-v08-7-2-ephemeral-topology-file soul-evolutionary-rejected loaded) rejected-present)",
        "!(match &self (q-v08-7-2-ephemeral-topology-file soul-durable-metta loaded) durable-present)",
        "!(match &self (q-v08-7-2-ephemeral-durable-probe probe-durable active) durable-probe-present)",
        "!(match &self (q-v08-7-2-runtime-observation probe-runtime observation-present) runtime-observation-present)",
        "!(match &self (q-v08-7-2-pending-candidate probe-candidate pending) pending-candidate-present)",
        "!(match &self (q-v08-7-2-validation-evidence probe-candidate evidence-present) validation-evidence-present)",
        "!(match &self (q-v08-7-2-restart-evidence probe-candidate restored) restart-evidence-present)",
        "!(match &self (q-v08-7-2-rejected-candidate probe-rejected audit-required) rejected-candidate-present)",
    ]
    cat_cmd = "cat " + " ".join(shlex.quote(p) for p in [container_engine_path] + paths) + f" > {shlex.quote(composite)}"
    add_queries = "\n".join(query_lines) + "\n"
    a = docker_exec(container, cat_cmd)
    if a.returncode != 0:
        return False, {"phase": "assemble-composite", "stderr": a.stderr, "composite": composite, "included_paths": paths}
    q = docker_exec(container, f"cat >> {shlex.quote(composite)}", add_queries)
    if q.returncode != 0:
        return False, {"phase": "append-queries", "stderr": q.stderr, "composite": composite}
    run_cmd = ["docker", "exec", container, "sh", "-c", f"cd /PeTTa && ./run.sh {shlex.quote(composite)} 2>&1"]
    r = subprocess.run(run_cmd, text=True, capture_output=True)
    raw = r.stdout + r.stderr
    present = {tok: (tok in raw) for tok in EPHEMERAL_EXPECTED_TOKENS}
    missing = [tok for tok, ok in present.items() if not ok]
    raw_path = None
    if raw_mode == "all" or (raw_mode == "fail" and (r.returncode != 0 or missing)):
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = raw_dir / "ephemeral_topology_composite_probe.raw.txt"
        raw_path.write_text(raw)
    return r.returncode == 0 and not missing, {
        "composite_path": composite,
        "included_paths": paths,
        "query_count": len(query_lines),
        "expected_tokens": EPHEMERAL_EXPECTED_TOKENS,
        "missing_tokens": missing,
        "present": present,
        "returncode": r.returncode,
        "stdout_chars": len(r.stdout),
        "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
        "stderr_chars": len(r.stderr),
        "stderr_sha256": hashlib.sha256(r.stderr.encode()).hexdigest(),
        "raw_sidecar_path": str(raw_path) if raw_path else None,
        "docker_run_command": " ".join(shlex.quote(x) for x in run_cmd),
        "meaning": "Container-visible ephemeral topology files parsed and queried under /PeTTa/run.sh without touching runtime project files.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", required=True)
    ap.add_argument("--ladder", required=True)
    ap.add_argument("--log-dir", default="v08_7_harness_logs")
    ap.add_argument("--runtime", action="store_true")
    ap.add_argument("--container", default="clarity_omega")
    ap.add_argument("--container-tmp-dir", default="/tmp", help="Container tmp dir where engine/ladder are staged for runtime probes")
    ap.add_argument("--runtime-host-concat", action="store_true", help="Legacy runtime mode: concatenate host engine text into each probe instead of staging artifacts in container /tmp")
    ap.add_argument("--ephemeral-topology-runtime", action="store_true", help="Stage soul/evolutionary/* and soul/durable.metta under container /tmp and run a composite runtime probe without touching project runtime files")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--inspect-topology", action="store_true")
    ap.add_argument("--prepare-topology", action="store_true", help="Create soul/evolutionary files and soul/durable.metta under repo-root if missing")
    ap.add_argument("--inspect-governance", action="store_true", help="Inspect soul_kernel file-class and manifest/import references for soul/durable.metta")
    ap.add_argument("--manifest", default=None, help="Optional manifest/import file to inspect relative to repo-root or as an absolute path")
    ap.add_argument("--validate-durable-file", action="store_true", help="Validate existing soul/durable.metta serialization lines")
    ap.add_argument("--raw-mode", choices=["none", "fail", "all"], default="fail")
    ap.add_argument("--raw-tail-chars", type=int, default=3000)
    ns = ap.parse_args()

    engine=Path(ns.engine); ladder=Path(ns.ladder); log_dir=Path(ns.log_dir); log_dir.mkdir(parents=True, exist_ok=True)
    checks: List[Check] = []
    meta = {"harness_version": VERSION, "engine": str(engine), "ladder": str(ladder), "runtime": ns.runtime, "container": ns.container}

    for label, path in [("engine", engine), ("ladder", ladder)]:
        if path.exists(): checks.append(Check("S0", f"file present: {label}", "PASS", f"path={path} size={path.stat().st_size} sha256={sha256_path(path)}"))
        else: checks.append(Check("S0", f"file present: {label}", "FAIL", f"missing={path}"))
    if not engine.exists() or not ladder.exists():
        return write_report(log_dir, checks, meta)
    etxt=engine.read_text(); ltxt=ladder.read_text()
    checks.append(Check("S1", "engine raw paren balance", "PASS" if paren_balance(etxt)==0 else "FAIL", f"balance={paren_balance(etxt)}"))
    checks.append(Check("S1", "engine comment-stripped paren balance", "PASS" if paren_balance(strip_comments(etxt))==0 else "FAIL", f"balance={paren_balance(strip_comments(etxt))}"))
    checks.append(Check("S1", "ladder comment-stripped paren balance", "PASS" if paren_balance(strip_comments(ltxt))==0 else "FAIL", f"balance={paren_balance(strip_comments(ltxt))}"))
    sec=section_55(etxt)
    checks.append(Check("S2", "v08.7 section present", "PASS" if sec else "FAIL", "section 55 located" if sec else "missing section 55"))
    missing_fam=[f for f in REQUIRED_FAMILIES if f not in etxt]
    checks.append(Check("S2", "all v08.7 primitive families present", "PASS" if not missing_fam else "FAIL", f"missing={missing_fam}"))
    missing_laws=[l for l in REQUIRED_LAWS if l not in etxt]
    checks.append(Check("S2", "all v08.7 laws present", "PASS" if not missing_laws else "FAIL", f"missing={missing_laws}"))
    missing_targets=[t for t in HARNESS_TARGETS if (f"q-v08-7-harness-target {t}" not in etxt or f"q-v08-7-harness-target {t}" not in ltxt)]
    checks.append(Check("S2", "engine and ladder expose all v08.7 harness targets", "PASS" if not missing_targets else "FAIL", f"missing={missing_targets}"))
    writer_found=[w for w in WRITER_TERMS if w in sec]
    checks.append(Check("S3", "v08.7 engine section remains pure", "PASS" if not writer_found else "FAIL", f"writer_terms_found={writer_found}"))
    for tok in ["v1-accepted-mechanical-append-class", "blocked-truncate-risk", "blocked-unreduced-storage", "blocked-dark-file", "blocked-boot-poison-risk", "blocked-genesis-output-not-canon"]:
        checks.append(Check("S3", f"critical token present: {tok}", "PASS" if tok in etxt else "FAIL"))
    # local expression coverage by token presence in equations
    for idx,(name,expr,expected) in enumerate(SEMANTIC_PROBES,1):
        checks.append(Check("S4", f"static probe planned: {name}", "PASS" if expected in etxt else "FAIL", f"expected={expected}"))

    if ns.inspect_topology or ns.prepare_topology:
        root=Path(ns.repo_root)
        dirs=[root/"soul/evolutionary", root/"soul/evolutionary/archive"]
        files=[root/"soul/evolutionary/README.metta", root/"soul/evolutionary/index.metta", root/"soul/evolutionary/runtime.metta", root/"soul/evolutionary/pending.metta", root/"soul/evolutionary/validation.metta", root/"soul/evolutionary/restart.metta", root/"soul/evolutionary/rejected.metta", root/"soul/durable.metta"]
        if ns.prepare_topology:
            for d in dirs: d.mkdir(parents=True, exist_ok=True)
            for f in files:
                if not f.exists():
                    f.parent.mkdir(parents=True, exist_ok=True)
                    if f.name == "durable.metta":
                        f.write_text(";; soul/durable.metta -- v08.7 durable canon placeholder\n(q-v08-7-durable-canon-file soul/durable.metta)\n")
                    elif f.name == "README.metta":
                        f.write_text(";; soul/evolutionary -- v08.7 process memory topology\n(q-v08-7-evolutionary-directory soul/evolutionary)\n")
                    else:
                        f.write_text(f";; {f.name} -- v08.7 process memory file\n")
        topo=[]
        for p in dirs+files:
            topo.append({"path": str(p), "exists": p.exists(), "is_dir": p.is_dir(), "size": p.stat().st_size if p.exists() and p.is_file() else None})
        missing=[x["path"] for x in topo if not x["exists"]]
        checks.append(Check("P0", "v08.7 topology inspected", "PASS" if not missing else "HOLD", f"missing={missing}", topo))
        valid_line='!(add-atom &self (q-v08-7-prebuild-durable-probe probe-001 active))'
        checks.append(Check("P1", "ground atom serialization sample", "PASS" if classify_line(valid_line)=="serialization-valid" else "FAIL", classify_line(valid_line), {"line": valid_line}))


    if ns.inspect_governance:
        checks.extend(inspect_governance(Path(ns.repo_root), ns.manifest))

    if ns.validate_durable_file:
        status, data = validate_serialization_file(Path(ns.repo_root) / "soul/durable.metta")
        checks.append(Check("G3", "durable.metta serialization file validation", status,
                            f"checked_lines={data.get('checked_lines')} bad={len(data.get('bad', []))}", data))

    if ns.runtime:
        raw_dir=log_dir/"raw_probe_outputs"
        container_engine_path: Optional[str] = None
        if ns.runtime_host_concat:
            checks.append(Check("R0", "runtime artifact staging to container tmp", "SKIP", "legacy --runtime-host-concat mode requested"))
        else:
            staged_ok, staged_data = stage_artifacts_to_container(ns.container, engine, ladder, ns.container_tmp_dir)
            checks.append(Check(
                "R0",
                "runtime artifacts staged in container tmp",
                "PASS" if staged_ok else "FAIL",
                "container engine/ladder sha256 verified" if staged_ok else f"staging failed at {staged_data.get('phase')}",
                staged_data,
            ))
            if staged_ok:
                container_engine_path = staged_data.get("engine_container_path")
                if ns.ephemeral_topology_runtime:
                    topo_ok, topo_data = stage_ephemeral_topology_to_container(ns.container, ns.container_tmp_dir)
                    checks.append(Check(
                        "R0",
                        "ephemeral v08.7 topology staged in container tmp",
                        "PASS" if topo_ok else "FAIL",
                        "soul/evolutionary/* and soul/durable.metta staged under container tmp" if topo_ok else f"ephemeral staging failed at {topo_data.get('phase')}",
                        topo_data,
                    ))
                    if topo_ok and container_engine_path:
                        ep_ok, ep_data = run_ephemeral_topology_probe(ns.container, container_engine_path, topo_data["base"], raw_dir, ns.raw_mode, ns.raw_tail_chars)
                        checks.append(Check(
                            "R0",
                            "ephemeral topology runtime composite probe",
                            "PASS" if ep_ok else "FAIL",
                            "all staged topology atoms queryable" if ep_ok else f"missing={ep_data.get('missing_tokens')}",
                            ep_data,
                        ))
        for idx,(name,expr,expected) in enumerate(SEMANTIC_PROBES,1):
            ok,data=run_docker_probe(ns.container, engine, expr, expected, idx, name, raw_dir, ns.raw_mode, ns.raw_tail_chars, container_engine_path=container_engine_path)
            actual=data.get("actual_result_text","")
            match=(data.get("actual_result_text") == expected) or (expected in data.get("actual_result_section", []))
            status="PASS" if ok and match else "FAIL"
            data.update({"expression":expr,"expected_token":expected,"local_result_match":match})
            checks.append(Check("R1", name, status, f"expected={expected}; actual={actual!r}; local={match}; returncode={data.get('returncode')}", data))
    else:
        checks.append(Check("R0", "runtime semantic probes not requested", "SKIP", "use --runtime"))

    return write_report(log_dir, checks, meta)


def write_report(log_dir: Path, checks: List[Check], meta: Dict[str, Any]) -> int:
    summary: Dict[str,int] = {}
    for c in checks: summary[c.status]=summary.get(c.status,0)+1
    report={"meta":meta,"summary":summary,"checks":[dataclasses.asdict(c) for c in checks]}
    ts=time.strftime("%Y%m%d_%H%M%S")
    jpath=log_dir/f"v08_7_durable_evolutionary_governance_trace_{ts}.json"
    mpath=log_dir/f"v08_7_durable_evolutionary_governance_trace_{ts}.md"
    jpath.write_text(json.dumps(report, indent=2, sort_keys=True))
    lines=["# v08.7.2 Hyperseed Durability Completion Harness Trace", "", f"harness: `{VERSION}`", "", "## Summary", "", "```json", json.dumps(summary, indent=2, sort_keys=True), "```", "", "## Checks", ""]
    for c in checks:
        lines.append(f"- **{c.status}** `{c.tier}` {c.name}: {c.details}")
    mpath.write_text("\n".join(lines)+"\n")
    print(json.dumps({"summary":summary,"json":str(jpath),"markdown":str(mpath)}, indent=2))
    return 1 if summary.get("FAIL",0) else 0

if __name__ == "__main__":
    raise SystemExit(main())
