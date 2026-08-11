#!/usr/bin/env python3
"""v08.7 Durable Evolutionary Governance Protocol harness.

Static mode validates engine/ladder artifacts and semantic coverage.
Runtime mode can run MeTTa reductions inside clarity_omega. Filesystem modes can
inspect and prepare the v08.7 topology. No engine writes are performed.
"""
from __future__ import annotations
import argparse, dataclasses, hashlib, json, os, re, shlex, subprocess, sys, time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION = "v08.7-durable-evolutionary-governance-v01"
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
]

SEMANTIC_PROBES: List[Tuple[str, str, str]] = [
    ("canon eligibility runtime false", "!(q-evo-canon-eligible? runtime-observed)", "false"),
    ("canon eligibility soul approved", "!(q-evo-canon-eligible? soul-approved)", "canon-write-eligible"),
    ("illegal runtime to canon jump", "!(q-evo-lifecycle-next? runtime-observed durable-canon-active)", "blocked-illegal-jump"),
    ("validation not approval", "!(q-evo-lifecycle-next? validation-eligible durable-canon-active)", "blocked-no-soul-approval"),
    ("runtime surface not canon", "!(q-evo-surface-canon-status? memory-evolutionary-runtime runtime-observed)", "process-not-canon"),
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


def clean_result(stdout: str) -> str:
    s = ANSI_RE.sub("", stdout)
    lines = [ln.rstrip() for ln in s.splitlines()]
    kept=[]
    for ln in lines:
        t = ln.strip()
        if not t:
            continue
        if t.startswith("-->") or t.startswith(":-") or t.startswith("^"):
            continue
        if "prolog" in t.lower() or "metta function" in t.lower() or "metta sexpr" in t.lower() or "metta runnable" in t.lower():
            continue
        if t.startswith("'") and "(" in t:
            continue
        kept.append(t)
    return "\n".join(kept[-5:])


def run_docker_probe(container: str, engine: Path, expr: str, idx: int, name: str, raw_dir: Path, raw_mode: str, tail_chars: int) -> Tuple[bool, Dict[str, Any]]:
    temp = f"/tmp/_v08_7_durable_evo_{idx:03d}_{re.sub(r'[^a-zA-Z0-9]+','_', name)[:40]}.metta"
    payload = engine.read_text() + "\n" + expr + "\n"
    write_cmd = ["docker", "exec", "-i", container, "sh", "-c", f"cat > {shlex.quote(temp)}"]
    p = subprocess.run(write_cmd, input=payload, text=True, capture_output=True)
    if p.returncode != 0:
        return False, {"phase":"write", "returncode":p.returncode, "stderr":p.stderr[-tail_chars:]}
    run_cmd = ["docker", "exec", container, "sh", "-c", f"cd /PeTTa && ./run.sh {shlex.quote(temp)} 2>&1"]
    q = subprocess.run(run_cmd, text=True, capture_output=True)
    raw = q.stdout + q.stderr
    cleaned = clean_result(raw)
    raw_path = None
    if raw_mode == "all" or (raw_mode == "fail" and q.returncode != 0):
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = raw_dir / f"probe_{idx:03d}_{re.sub(r'[^a-zA-Z0-9]+','_', name)[:40]}.raw.txt"
        raw_path.write_text(raw)
    return q.returncode == 0, {
        "returncode": q.returncode,
        "actual_result_text": cleaned,
        "stdout_chars": len(q.stdout),
        "stdout_sha256": hashlib.sha256(q.stdout.encode()).hexdigest(),
        "stderr_chars": len(q.stderr),
        "stderr_sha256": hashlib.sha256(q.stderr.encode()).hexdigest(),
        "raw_sidecar_path": str(raw_path) if raw_path else None,
        "docker_run_command": " ".join(shlex.quote(x) for x in run_cmd),
        "temp_path": temp,
    }


def classify_line(line: str) -> str:
    if not line.isascii(): return "blocked-non-ascii-risk"
    if "\n" in line or "\r" in line: return "blocked-multiline-risk"
    if paren_balance(line) != 0: return "blocked-malformed-directive"
    if not line.strip().startswith("!(add-atom &self "): return "blocked-bad-directive-head"
    if "(!" in line or "(q-" not in line: pass
    return "serialization-valid"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", required=True)
    ap.add_argument("--ladder", required=True)
    ap.add_argument("--log-dir", default="v08_7_harness_logs")
    ap.add_argument("--runtime", action="store_true")
    ap.add_argument("--container", default="clarity_omega")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--inspect-topology", action="store_true")
    ap.add_argument("--prepare-topology", action="store_true", help="Create memory/evolutionary files and soul/durable.metta under repo-root if missing")
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
        dirs=[root/"memory/evolutionary", root/"memory/evolutionary/archive"]
        files=[root/"memory/evolutionary/README.metta", root/"memory/evolutionary/index.metta", root/"memory/evolutionary/runtime.metta", root/"memory/evolutionary/pending.metta", root/"memory/evolutionary/validation.metta", root/"memory/evolutionary/restart.metta", root/"memory/evolutionary/rejected.metta", root/"soul/durable.metta"]
        if ns.prepare_topology:
            for d in dirs: d.mkdir(parents=True, exist_ok=True)
            for f in files:
                if not f.exists():
                    f.parent.mkdir(parents=True, exist_ok=True)
                    if f.name == "durable.metta":
                        f.write_text(";; soul/durable.metta -- v08.7 durable canon placeholder\n(q-v08-7-durable-canon-file soul/durable.metta)\n")
                    elif f.name == "README.metta":
                        f.write_text(";; memory/evolutionary -- v08.7 process memory topology\n(q-v08-7-evolutionary-directory memory/evolutionary)\n")
                    else:
                        f.write_text(f";; {f.name} -- v08.7 process memory file\n")
        topo=[]
        for p in dirs+files:
            topo.append({"path": str(p), "exists": p.exists(), "is_dir": p.is_dir(), "size": p.stat().st_size if p.exists() and p.is_file() else None})
        missing=[x["path"] for x in topo if not x["exists"]]
        checks.append(Check("P0", "v08.7 topology inspected", "PASS" if not missing else "HOLD", f"missing={missing}", topo))
        valid_line='!(add-atom &self (q-v08-7-prebuild-durable-probe probe-001 active))'
        checks.append(Check("P1", "ground atom serialization sample", "PASS" if classify_line(valid_line)=="serialization-valid" else "FAIL", classify_line(valid_line), {"line": valid_line}))

    if ns.runtime:
        raw_dir=log_dir/"raw_probe_outputs"
        for idx,(name,expr,expected) in enumerate(SEMANTIC_PROBES,1):
            ok,data=run_docker_probe(ns.container, engine, expr, idx, name, raw_dir, ns.raw_mode, ns.raw_tail_chars)
            actual=data.get("actual_result_text","")
            match=expected in actual.split() or expected in actual
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
    lines=["# v08.7 Durable Evolutionary Governance Harness Trace", "", f"harness: `{VERSION}`", "", "## Summary", "", "```json", json.dumps(summary, indent=2, sort_keys=True), "```", "", "## Checks", ""]
    for c in checks:
        lines.append(f"- **{c.status}** `{c.tier}` {c.name}: {c.details}")
    mpath.write_text("\n".join(lines)+"\n")
    print(json.dumps({"summary":summary,"json":str(jpath),"markdown":str(mpath)}, indent=2))
    return 1 if summary.get("FAIL",0) else 0

if __name__ == "__main__":
    raise SystemExit(main())
