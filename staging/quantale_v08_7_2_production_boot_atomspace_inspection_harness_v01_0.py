#!/usr/bin/env python3
"""
quantale_v08_7_2_production_boot_atomspace_inspection_harness_v01_0.py

Production boot / long-lived atomspace inspection harness for v08.7.2.

This is intentionally NOT a one-shot run.sh reduction harness.
It does NOT inline live file bodies.
It does NOT assume that a one-shot import! line registers library rules.

Purpose
-------
Answer the remaining question honestly:

    Did the production boot/import graph load v08.7.2 into the long-lived
    runtime atomspace that the running Clarity/Omega process actually uses?

This harness has two phases:

1. Discovery / inventory phase
   - confirms container is running
   - inventories running processes, cwd/env hints, sockets/ports, boot files
   - verifies the live v08.7.2 files and wiring are present/sha-visible
   - searches for possible atomspace/query surfaces

2. Direct live-query proof phase
   - runs semantic probes ONLY against a configured/discovered live query surface
   - never falls back to inlining bodies or one-shot import proof

If no live query surface is configured/discovered, the result is HOLD, not FAIL.
That is a truthful result: the files may be green and the live-body harness may be
green, but production atomspace proof still needs the actual query transport.

Supported direct-query transports
---------------------------------
A. --query-command-template
   Shell command executed inside the container for each expression.
   Use {expr} for the MeTTa expression and {label} for a probe label.
   Example shape, if such a CLI exists in your repo:

     --query-command-template 'cd /PeTTa/repos/omegaclaw && ./clarity_query --expr "{expr}"'

B. --host-query-command-template
   Shell command executed on the host for each expression.
   Use {expr}, {label}, {container}.

C. --query-file-command-template
   Writes the expression to a temp file inside the container, then executes the
   command template. Use {file}, {label}. This is for a production query CLI that
   reads an expression file but queries the long-lived atomspace, NOT run.sh.

   Example shape:
     --query-file-command-template 'cd /PeTTa/repos/omegaclaw && ./live_query --file {file}'

Important: Do not point these templates at /PeTTa/run.sh unless the command
actually talks to the running long-lived runtime. run.sh one-shot probes are a
separate proof class and already covered by the live-body harness.

Outputs
-------
Writes JSON and Markdown traces to --log-dir.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_CONTAINER_REPO_ROOT = "/PeTTa/repos/omegaclaw"
TIMEOUT = 45

LIVE_FILES = [
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
    '(soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" journal)',
    '(soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/runtime.metta" journal)',
    '(soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/pending.metta" journal)',
    '(soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/validation.metta" journal)',
    '(soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/restart.metta" journal)',
    '(soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/rejected.metta" journal)',
]

# Deliberately compact representative semantic probes. The live-body harness covers
# all 80. Here we need enough to prove the long-lived boot atomspace has v08.7.2
# vocabulary, topology atoms, and key negative controls.
LIVE_PROBES = [
    ("topology durable loaded", "!(match &self (q-v08-7-2-topology-file soul-durable-metta loaded) live-durable-present)", "live-durable-present"),
    ("topology runtime loaded", "!(match &self (q-v08-7-2-topology-file soul-evolutionary-runtime loaded) live-runtime-present)", "live-runtime-present"),
    ("canon eligibility runtime false", "!(q-evo-canon-eligible? runtime-observed)", "false"),
    ("canon eligibility soul approved", "!(q-evo-canon-eligible? soul-approved)", "canon-write-eligible"),
    ("illegal runtime to canon jump", "!(q-evo-lifecycle-next? runtime-observed durable-canon-active)", "blocked-illegal-jump"),
    ("journal class v1 accepted", "!(q-v08-7-file-class-status? soul-durable-metta journal-class semantic-gates-present)", "v1-accepted-mechanical-append-class"),
    ("append allowed", "!(q-v08-7-write-operation-status? append-file canonical-allowlisted journal-class approved)", "append-route-allowed"),
    ("write blocked", "!(q-v08-7-write-operation-status? write-file canonical-allowlisted journal-class approved)", "blocked-truncate-risk"),
    ("hyperseed threshold pass", "!(q-v08-7-2-durable-growth-threshold? context-valid pbit-evidence-valid proto-time-valid structural-signature-valid continuity-valid artifact-lineage-valid resource-cost-valid approximation-valid)", "hyperseed-durability-threshold-pass"),
    ("hyperseed import candidate ready", "!(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-green hyperseed-threshold-pass)", "import-candidate-ready"),
    ("governance open hold", "!(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-open hyperseed-threshold-pass)", "hold-governance-not-green"),
    ("contextless negative", "!(q-v08-7-2-negative-control? contextless-claim durable-growth-claimed)", "blocked-context-missing"),
]

@dataclass
class Check:
    name: str
    status: str
    tier: str
    details: str = ""
    data: Any = None


def now_stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def run_cmd(cmd: List[str], timeout: int = TIMEOUT, input_text: Optional[str] = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, input=input_text, capture_output=True, text=True, timeout=timeout)


def sh(cmd: str, timeout: int = TIMEOUT) -> subprocess.CompletedProcess:
    return run_cmd(["bash", "-lc", cmd], timeout=timeout)


def docker_exec(container: str, command: str, timeout: int = TIMEOUT, input_text: Optional[str] = None) -> subprocess.CompletedProcess:
    return run_cmd(["docker", "exec", "-i", container, "sh", "-lc", command], timeout=timeout, input_text=input_text)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def paren_balance(text: str) -> int:
    # Simple raw balance; prior harnesses also used raw/comment-stripped variants.
    return text.count("(") - text.count(")")


def strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", text or "")


def tail_lines(text: str, n: int = 20) -> List[str]:
    lines = [ln for ln in strip_ansi(text).splitlines() if ln.strip()]
    return lines[-n:]


def add(checks: List[Check], name: str, status: str, tier: str, details: str = "", data: Any = None) -> None:
    checks.append(Check(name=name, status=status, tier=tier, details=details, data=data))


def container_exists(container: str) -> bool:
    try:
        p = run_cmd(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"])
        return p.returncode == 0 and container in p.stdout.splitlines()
    except Exception:
        return False


def container_cat(container: str, path: str) -> Tuple[Optional[str], str]:
    p = docker_exec(container, "cat " + shlex.quote(path))
    if p.returncode == 0:
        return p.stdout, ""
    return None, p.stderr or p.stdout


def write_container_file(container: str, path: str, content: str) -> Tuple[bool, str]:
    p = docker_exec(container, "cat > " + shlex.quote(path), input_text=content)
    return p.returncode == 0, p.stderr or p.stdout


def host_file_checks(checks: List[Check], repo_root: Path) -> Dict[str, Dict[str, Any]]:
    facts: Dict[str, Dict[str, Any]] = {}
    for rel in LIVE_FILES:
        path = repo_root / rel
        if not path.exists():
            add(checks, f"host file present: {rel}", "FAIL", "L1", "missing")
            facts[rel] = {"exists": False}
            continue
        text = path.read_text(errors="replace")
        digest = sha256_file(path)
        facts[rel] = {"exists": True, "size": path.stat().st_size, "sha256": digest, "paren_balance": paren_balance(text)}
        add(checks, f"host file present: {rel}", "PASS", "L1", f"size={path.stat().st_size} sha256={digest}")
        if rel.endswith(".metta") and rel in [
            "lib_clarity_reasoning/lib_clarity_reasoning.metta",
            "lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta",
            "soul/soul_kernel.metta",
        ]:
            bal = paren_balance(text)
            add(checks, f"paren balance: {rel}", "PASS" if bal == 0 else "FAIL", "L1", f"balance={bal}")

    lib_path = repo_root / "lib_clarity_reasoning/lib_clarity_reasoning.metta"
    if lib_path.exists():
        lib = lib_path.read_text(errors="replace")
        missing = [s for s in REQUIRED_IMPORT_SUBSTRINGS if s not in lib]
        add(checks, "live import block contains required imports", "PASS" if not missing else "FAIL", "L1", f"missing={missing}", {"missing": missing})

    kernel_path = repo_root / "soul/soul_kernel.metta"
    if kernel_path.exists():
        kernel = kernel_path.read_text(errors="replace")
        missing = [s for s in REQUIRED_KERNEL_CLASS_LINES if s not in kernel]
        add(checks, "soul_kernel contains v08.7.2 journal class declarations", "PASS" if not missing else "FAIL", "L1", f"missing={missing}", {"missing": missing})
    return facts


def container_sha_checks(checks: List[Check], container: str, container_repo_root: str, host_facts: Dict[str, Dict[str, Any]]) -> None:
    for rel, fact in host_facts.items():
        if not fact.get("exists"):
            continue
        cpath = container_repo_root.rstrip("/") + "/" + rel
        body, err = container_cat(container, cpath)
        if body is None:
            add(checks, f"container live file visible and sha-matched: {rel}", "FAIL", "L2", f"cat failed: {err[:300]}")
            continue
        cdigest = sha256_text(body)
        match = cdigest == fact["sha256"]
        add(checks, f"container live file visible and sha-matched: {rel}", "PASS" if match else "FAIL", "L2", f"container={cpath} sha_match={match}", {
            "container_path": cpath,
            "container_sha256": cdigest,
            "host_sha256": fact["sha256"],
            "bytes": len(body.encode("utf-8")),
        })


def inventory_runtime(checks: List[Check], container: str, container_repo_root: str, raw_tail_chars: int) -> Dict[str, Any]:
    inv: Dict[str, Any] = {}

    commands = {
        "processes": "ps -eo pid,ppid,stat,args 2>/dev/null | sed -n '1,220p'",
        "network_tcp": "(ss -ltnp 2>/dev/null || netstat -ltnp 2>/dev/null || true)",
        "network_unix": "(ss -lxnp 2>/dev/null || netstat -lxnp 2>/dev/null || true) | sed -n '1,220p'",
        "repo_top": f"find {shlex.quote(container_repo_root)} -maxdepth 2 -type f | sed -n '1,220p'",
        "candidate_query_files": f"find {shlex.quote(container_repo_root)} /tmp /var/run -maxdepth 4 \( -type f -o -type s \) 2>/dev/null | grep -Ei 'query|atom|space|socket|rpc|api|server|clarity|omega|metta' | sed -n '1,220p'",
        "grep_query_terms": f"grep -RInE 'atomspace|query|live_query|clarity_query|socket|server|FastAPI|Flask|uvicorn|websocket|zmq|rpc|run.sh|import!' {shlex.quote(container_repo_root)} 2>/dev/null | sed -n '1,260p'",
    }

    for key, cmd in commands.items():
        p = docker_exec(container, cmd, timeout=TIMEOUT)
        text = strip_ansi((p.stdout or "") + (p.stderr or ""))
        inv[key] = {"returncode": p.returncode, "chars": len(text), "sha256": sha256_text(text), "tail": text[-raw_tail_chars:]}
        status = "PASS" if p.returncode == 0 else "HOLD"
        add(checks, f"runtime inventory: {key}", status, "P0", f"returncode={p.returncode} chars={len(text)} sha256={sha256_text(text)}", inv[key])

    # Process cwd/env hints for non-trivial processes.
    proc_script = r'''
for p in /proc/[0-9]*; do
  pid=${p##*/}
  cmd=$(tr '\0' ' ' < "$p/cmdline" 2>/dev/null | cut -c1-260)
  [ -z "$cmd" ] && continue
  case "$cmd" in
    *python*|*metta*|*run.sh*|*omega*|*clarity*|*server*|*uvicorn*|*node*|*npm*)
      cwd=$(readlink "$p/cwd" 2>/dev/null || true)
      envhit=$(tr '\0' '\n' < "$p/environ" 2>/dev/null | grep -Ei 'METTA|HYPERON|OMEGA|CLARITY|PORT|SOCKET|ATOM|QUERY' | tr '\n' ';' | cut -c1-500)
      echo "PID=$pid CWD=$cwd CMD=$cmd ENVHIT=$envhit"
      ;;
  esac
done | sed -n '1,220p'
'''
    p = docker_exec(container, proc_script, timeout=TIMEOUT)
    text = strip_ansi((p.stdout or "") + (p.stderr or ""))
    inv["process_cwd_env_hints"] = {"returncode": p.returncode, "chars": len(text), "sha256": sha256_text(text), "tail": text[-raw_tail_chars:]}
    add(checks, "runtime inventory: process cwd/env hints", "PASS" if p.returncode == 0 else "HOLD", "P0", f"returncode={p.returncode} chars={len(text)} sha256={sha256_text(text)}", inv["process_cwd_env_hints"])
    return inv


def format_template(template: str, expr: str, label: str, container: str, file_path: Optional[str] = None) -> str:
    return template.format(
        expr=shlex.quote(expr),
        expr_raw=expr,
        label=shlex.quote(label),
        label_raw=label,
        container=shlex.quote(container),
        file=shlex.quote(file_path or ""),
        file_raw=file_path or "",
    )


def run_live_probe_container_template(container: str, template: str, label: str, expr: str, timeout: int) -> Tuple[int, str, str, str]:
    cmd = format_template(template, expr, label, container)
    p = docker_exec(container, cmd, timeout=timeout)
    out = strip_ansi((p.stdout or "") + (p.stderr or ""))
    return p.returncode, out, "docker-exec-template", cmd


def run_live_probe_host_template(template: str, container: str, label: str, expr: str, timeout: int) -> Tuple[int, str, str, str]:
    cmd = format_template(template, expr, label, container)
    p = sh(cmd, timeout=timeout)
    out = strip_ansi((p.stdout or "") + (p.stderr or ""))
    return p.returncode, out, "host-template", cmd


def run_live_probe_file_template(container: str, template: str, label: str, expr: str, timeout: int, tmp_dir: str = "/tmp") -> Tuple[int, str, str, str]:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", label)[:80]
    fpath = f"{tmp_dir.rstrip('/')}/_v08_7_2_production_boot_probe_{safe}.metta"
    ok, msg = write_container_file(container, fpath, expr + "\n")
    if not ok:
        return 99, msg, "query-file-write", f"write {fpath}"
    cmd = format_template(template, expr, label, container, fpath)
    p = docker_exec(container, cmd, timeout=timeout)
    out = strip_ansi((p.stdout or "") + (p.stderr or ""))
    return p.returncode, out, "docker-file-template", cmd


def direct_live_query_phase(checks: List[Check], args: argparse.Namespace) -> None:
    transports = []
    if args.query_command_template:
        transports.append(("container", args.query_command_template))
    if args.host_query_command_template:
        transports.append(("host", args.host_query_command_template))
    if args.query_file_command_template:
        transports.append(("file", args.query_file_command_template))

    if not transports:
        add(checks, "production live query surface configured", "HOLD", "Q0", "No --query-command-template, --host-query-command-template, or --query-file-command-template supplied. Discovery complete, but semantic production atomspace proof not attempted.", {
            "required_next_step": "Supply the exact Clarity/Omega live atomspace query transport. Do not use one-shot run.sh unless it queries the long-lived atomspace.",
            "probe_count_waiting": len(LIVE_PROBES),
        })
        return

    add(checks, "production live query surface configured", "PASS", "Q0", f"transports={[t[0] for t in transports]}")

    # Run all probes against first configured transport by default; if multiple, all must pass.
    for mode, template in transports:
        for label, expr, expected in LIVE_PROBES:
            try:
                if mode == "container":
                    rc, out, transport, cmd = run_live_probe_container_template(args.container, template, label, expr, args.query_timeout)
                elif mode == "host":
                    rc, out, transport, cmd = run_live_probe_host_template(template, args.container, label, expr, args.query_timeout)
                else:
                    rc, out, transport, cmd = run_live_probe_file_template(args.container, template, label, expr, args.query_timeout, args.query_file_tmp_dir)
            except subprocess.TimeoutExpired as e:
                add(checks, f"production atomspace probe: {label} [{mode}]", "FAIL", "Q1", f"timeout after {args.query_timeout}s", {"expression": expr, "expected": expected})
                continue
            present = expected in out
            unreduced = expr.replace("!", "").strip() in out or expr.strip() in out
            status = "PASS" if rc == 0 and present and not unreduced else "FAIL"
            details = f"expected={expected}; present={present}; returncode={rc}; unreduced_echo={unreduced}"
            add(checks, f"production atomspace probe: {label} [{mode}]", status, "Q1", details, {
                "transport": transport,
                "command": cmd,
                "expression": expr,
                "expected_token": expected,
                "expected_present_in_stdout": present,
                "returncode": rc,
                "stdout_chars": len(out),
                "stdout_sha256": sha256_text(out),
                "actual_tail": tail_lines(out, args.raw_tail_lines),
                "unreduced_echo_detected": unreduced,
            })


def summarize(checks: List[Check]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for c in checks:
        out[c.status] = out.get(c.status, 0) + 1
    return out


def write_outputs(checks: List[Check], args: argparse.Namespace, stamp: str) -> Tuple[Path, Path]:
    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    summary = summarize(checks)
    meta = {
        "harness_version": "v08.7.2-production-boot-atomspace-inspection-v01.0",
        "mode": "production-boot-long-lived-atomspace-discovery-and-direct-query",
        "repo_root": args.repo_root,
        "container": args.container,
        "container_repo_root": args.container_repo_root,
        "one_shot_run_sh_import_proof": False,
        "live_body_inline_transport": False,
        "production_boot_import_proof_attempted": bool(args.query_command_template or args.host_query_command_template or args.query_file_command_template),
        "query_command_template_supplied": bool(args.query_command_template),
        "host_query_command_template_supplied": bool(args.host_query_command_template),
        "query_file_command_template_supplied": bool(args.query_file_command_template),
        "transport_note": "This harness only passes Q1 semantic probes if they are answered through a configured live query surface for the long-lived runtime atomspace. Discovery-only runs end with HOLD, not FAIL.",
    }
    payload = {
        "meta": meta,
        "summary": summary,
        "checks": [asdict(c) for c in checks],
    }
    json_path = log_dir / f"v08_7_2_production_boot_atomspace_trace_{stamp}.json"
    md_path = log_dir / f"v08_7_2_production_boot_atomspace_trace_{stamp}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = []
    lines.append("# v08.7.2 production boot atomspace inspection trace")
    lines.append("")
    lines.append("## Summary")
    for k in sorted(summary):
        lines.append(f"- {k}: {summary[k]}")
    lines.append("")
    lines.append("## Interpretation guardrail")
    lines.append("This is not a one-shot `run.sh` import proof and not a live-body inline proof. Semantic PASS checks require a configured live query transport into the long-lived runtime atomspace. If Q0 is HOLD, discovery completed but production atomspace proof is still open.")
    lines.append("")
    lines.append("## Checks")
    for c in checks:
        lines.append(f"- **{c.status}** `{c.tier}` {c.name}: {c.details}")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    ap = argparse.ArgumentParser(description="v08.7.2 production boot atomspace inspection harness")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--container-repo-root", default=DEFAULT_CONTAINER_REPO_ROOT)
    ap.add_argument("--log-dir", default="shared_files")
    ap.add_argument("--raw-tail-chars", type=int, default=3000)
    ap.add_argument("--raw-tail-lines", type=int, default=20)
    ap.add_argument("--query-timeout", type=int, default=45)
    ap.add_argument("--query-command-template", default=None, help="Command executed inside container. Use {expr}/{expr_raw} and {label}.")
    ap.add_argument("--host-query-command-template", default=None, help="Command executed on host. Use {expr}/{expr_raw}, {label}, {container}.")
    ap.add_argument("--query-file-command-template", default=None, help="Command executed inside container after writing expr to {file}. Must query live atomspace, not one-shot run.sh.")
    ap.add_argument("--query-file-tmp-dir", default="/tmp")
    args = ap.parse_args()

    checks: List[Check] = []
    stamp = now_stamp()
    repo_root = Path(args.repo_root).resolve()

    if container_exists(args.container):
        add(checks, "container exists", "PASS", "L0", args.container)
    else:
        add(checks, "container exists", "FAIL", "L0", args.container)
        json_path, md_path = write_outputs(checks, args, stamp)
        print(json.dumps({"summary": summarize(checks), "json": str(json_path), "markdown": str(md_path)}, indent=2))
        return 2

    host_facts = host_file_checks(checks, repo_root)
    container_sha_checks(checks, args.container, args.container_repo_root, host_facts)
    inventory_runtime(checks, args.container, args.container_repo_root, args.raw_tail_chars)
    direct_live_query_phase(checks, args)

    json_path, md_path = write_outputs(checks, args, stamp)
    print(json.dumps({"summary": summarize(checks), "json": str(json_path), "markdown": str(md_path)}, indent=2))

    # Exit nonzero only on FAIL. HOLD is a truthful incomplete proof, not an execution error.
    return 1 if summarize(checks).get("FAIL", 0) else 0


if __name__ == "__main__":
    sys.exit(main())
