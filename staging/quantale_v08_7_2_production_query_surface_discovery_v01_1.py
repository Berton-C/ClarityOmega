#!/usr/bin/env python3
"""
quantale_v08_7_2_production_query_surface_discovery_v01_1.py

Purpose
-------
Discovery harness for the remaining proof class:
  "Can we query the long-lived production SWI-Prolog / MeTTa atomspace?"

This does NOT attempt to prove v08.7.2 semantics. It inspects the live container's
boot path and command-handling surfaces so we can find the actual live query route
without confusing it with one-shot run.sh file evaluation.

It writes JSON and Markdown reports to --log-dir.
"""

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

TIMEOUT = 20
DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_CONTAINER_REPO_ROOT = "/PeTTa/repos/omegaclaw"
DEFAULT_LOG_DIR = "shared_files"

KEY_PATHS = [
    "/PeTTa/run.sh",
    "/PeTTa/src/main.pl",
    "/PeTTa/repos/omegaclaw/run.metta",
    "/PeTTa/repos/omegaclaw/lib_omegaclaw.metta",
    "/PeTTa/repos/omegaclaw/src/loop.metta",
    "/PeTTa/repos/omegaclaw/lib_llm_ext.py",
    "/PeTTa/repos/omegaclaw/channels/mattermost.py",
    "/PeTTa/repos/omegaclaw/channels/irc.py",
]

SEARCH_COMMANDS = {
    "proc_runtime_cmdlines": r"""
for p in /proc/[0-9]*; do
  pid=${p##*/}
  cmd=$(tr '\000' ' ' < "$p/cmdline" 2>/dev/null | cut -c1-500)
  [ -z "$cmd" ] && continue
  case "$cmd" in
    *swipl*|*run.sh*|*main.pl*|*mattermost*|*omega*|*clarity*|*python*|*node*|*server*)
      cwd=$(readlink "$p/cwd" 2>/dev/null || true)
      echo "PID=$pid CWD=$cwd CMD=$cmd"
      ;;
  esac
done | sort -n
""",
    "proc_runtime_fds": r"""
for p in /proc/[0-9]*; do
  pid=${p##*/}
  cmd=$(tr '\000' ' ' < "$p/cmdline" 2>/dev/null)
  case "$cmd" in
    *swipl*|*main.pl*|*run.sh*)
      echo "--- PID $pid FD ---"
      ls -la "$p/fd" 2>/dev/null | sed -n '1,120p'
      ;;
  esac
done
""",
    "proc_runtime_env": r"""
for p in /proc/[0-9]*; do
  pid=${p##*/}
  cmd=$(tr '\000' ' ' < "$p/cmdline" 2>/dev/null)
  case "$cmd" in
    *swipl*|*main.pl*|*run.sh*)
      echo "--- PID $pid ENV HITS ---"
      tr '\000' '\n' < "$p/environ" 2>/dev/null | grep -Ei 'METTA|HYPERON|OMEGA|CLARITY|MATTER|MM_|PORT|SOCKET|ATOM|QUERY|CHANNEL|COMM' || true
      ;;
  esac
done
""",
    "network_listeners": r"""
( ss -ltnup 2>/dev/null || netstat -ltnup 2>/dev/null || true ) | sed -n '1,200p'
""",
    "repo_query_surface_grep": r"""
cd /PeTTa/repos/omegaclaw 2>/dev/null || exit 0
LC_ALL=C grep -RInE \
  'query|debug|inspect|atomspace|AtomSpace|metta|MeTTa|eval|reduce|run!|commchannel|mattermost|MM_|webhook|socket|http|listen|stdin|read_line|read_term|message|skill|tool|shell|command' \
  run.metta lib_omegaclaw.metta src channels lib_llm_ext.py scripts 2>/dev/null | sed -n '1,400p'
""",
    "pettasrc_query_surface_grep": r"""
cd /PeTTa 2>/dev/null || exit 0
LC_ALL=C grep -RInE \
  'main\(|run\(|assert|dynamic|thread|socket|http|listen|stdin|read_line|read_term|eval|metta|MeTTa|atom|query|commchannel|mattermost|message' \
  src run.sh 2>/dev/null | sed -n '1,500p'
""",
    "mattermost_channel_impl": r"""
cd /PeTTa/repos/omegaclaw 2>/dev/null || exit 0
for f in channels/mattermost.py channels/irc.py lib_llm_ext.py; do
  [ -f "$f" ] || continue
  echo "===== $f ====="
  sed -n '1,260p' "$f"
done
""",
    "main_pl_head": r"""
for f in /PeTTa/run.sh /PeTTa/src/main.pl /PeTTa/repos/omegaclaw/run.metta /PeTTa/repos/omegaclaw/lib_omegaclaw.metta /PeTTa/repos/omegaclaw/src/loop.metta; do
  [ -f "$f" ] || continue
  echo "===== $f ====="
  sed -n '1,260p' "$f"
done
""",
}


def sh(cmd: List[str], timeout: int = TIMEOUT, input_text: Optional[str] = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, input=input_text, capture_output=True, text=True, timeout=timeout)


def docker_sh(container: str, script: str, timeout: int = TIMEOUT) -> Dict[str, Any]:
    try:
        p = sh(["docker", "exec", container, "sh", "-lc", script], timeout=timeout)
        out = (p.stdout or "") + (("\nSTDERR:\n" + p.stderr) if p.stderr else "")
        return {
            "returncode": p.returncode,
            "stdout": p.stdout or "",
            "stderr": p.stderr or "",
            "chars": len(out),
            "sha256": hashlib.sha256(out.encode()).hexdigest(),
            "tail": "\n".join(out.splitlines()[-80:]),
        }
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") + (e.stderr or "")
        if isinstance(out, bytes):
            out = out.decode(errors="replace")
        return {
            "returncode": None,
            "timeout": True,
            "stdout": e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""),
            "stderr": e.stderr.decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or ""),
            "chars": len(out or ""),
            "sha256": hashlib.sha256((out or "").encode()).hexdigest(),
            "tail": "\n".join((out or "").splitlines()[-80:]),
        }


def container_running(container: str) -> bool:
    try:
        p = sh(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"])
        return p.returncode == 0 and container in p.stdout.splitlines()
    except Exception:
        return False


def classify_findings(outputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    text = "\n".join((v.get("stdout", "") + "\n" + v.get("stderr", "")) for v in outputs.values())
    findings: List[str] = []
    holds: List[str] = []
    candidates: List[str] = []

    if re.search(r"swipl .*main\.pl", text):
        findings.append("Production runtime is a long-lived SWI-Prolog process launched via /PeTTa/src/main.pl.")
    if "commchannel=mattermost" in text or "MM_CHANNEL_ID" in text:
        findings.append("Mattermost is the configured production communication channel.")
    if re.search(r"socket|listen|http|webhook", text, re.I):
        candidates.append("Source contains possible socket/http/webhook terms; inspect matched lines for a query/debug surface.")
    if re.search(r"read_line|read_term|stdin", text, re.I):
        candidates.append("Source contains stdin/read terms; inspect whether the running SWI process exposes an interactive command stream.")
    if re.search(r"query|debug|inspect|atomspace", text, re.I):
        candidates.append("Source contains query/debug/atomspace terms; inspect whether any are reachable through Mattermost/tool commands.")
    if not candidates:
        holds.append("No obvious live query surface identified by keyword discovery. Need manual source read or instrumented route.")

    holds.append("Do not use one-shot /PeTTa/run.sh as production atomspace proof unless it is shown to attach to PID 9's long-lived atomspace.")

    return {"findings": findings, "candidate_surfaces": candidates, "holds": holds}


def add(checks: List[Dict[str, Any]], name: str, status: str, tier: str, details: str = "", data: Any = None):
    checks.append({"name": name, "status": status, "tier": tier, "details": details, "data": data})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--container-repo-root", default=DEFAULT_CONTAINER_REPO_ROOT)
    ap.add_argument("--log-dir", default=DEFAULT_LOG_DIR)
    ap.add_argument("--raw-tail-chars", type=int, default=5000)
    args = ap.parse_args()

    checks: List[Dict[str, Any]] = []
    outputs: Dict[str, Dict[str, Any]] = {}

    if container_running(args.container):
        add(checks, "container exists", "PASS", "D0", args.container)
    else:
        add(checks, "container exists", "FAIL", "D0", args.container)
        summary = {"FAIL": 1}
        report = {"meta": vars(args), "summary": summary, "checks": checks}
        print(json.dumps(report, indent=2))
        return 1

    for path in KEY_PATHS:
        q = "test -f {p} && (wc -c < {p}; sha256sum {p}; sed -n '1,80p' {p}) || true".format(p=path)
        r = docker_sh(args.container, q, timeout=TIMEOUT)
        outputs[f"file_head:{path}"] = r
        status = "PASS" if r["stdout"].strip() else "HOLD"
        add(checks, f"source file snapshot: {path}", status, "S0", f"chars={r['chars']} sha256={r['sha256']}", {"tail": r["tail"]})

    for label, script in SEARCH_COMMANDS.items():
        r = docker_sh(args.container, script, timeout=TIMEOUT)
        outputs[label] = r
        # grep commands may return 1 when no hits; that is HOLD, not FAIL
        status = "PASS" if r.get("chars", 0) > 0 else "HOLD"
        add(checks, f"discovery: {label}", status, "S1", f"returncode={r.get('returncode')} chars={r.get('chars')} sha256={r.get('sha256')}", {"tail": r.get("tail", "")})

    classification = classify_findings(outputs)
    add(checks, "classification: discovered production shape", "PASS", "S2", "; ".join(classification["findings"]) or "no strong production-shape finding", classification)

    # This harness is discovery-only. It should end in HOLD until an actual query surface is known.
    add(checks, "production query surface selected", "HOLD", "Q0", "Discovery completed. Select or implement the live atomspace query surface before semantic production probes.", {
        "recommended_next_step": "Use findings to inspect Mattermost command path or SWI-Prolog internals; then pass the exact live query transport to the production boot atomspace harness.",
        "not_a_solution": "one-shot run.sh file evaluation",
    })

    summary: Dict[str, int] = {}
    for c in checks:
        summary[c["status"]] = summary.get(c["status"], 0) + 1

    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = log_dir / f"v08_7_2_query_surface_discovery_trace_{stamp}.json"
    md_path = log_dir / f"v08_7_2_query_surface_discovery_trace_{stamp}.md"

    report = {
        "meta": {
            "harness_version": "v08.7.2-production-query-surface-discovery-v01.1",
            "mode": "inspect-run-sh-main-pl-mattermost-command-path",
            "container": args.container,
            "container_repo_root": args.container_repo_root,
            "one_shot_run_sh_import_proof": False,
            "live_body_inline_transport": False,
            "production_semantic_probe_attempted": False,
        },
        "summary": summary,
        "checks": checks,
        "json": str(json_path),
        "markdown": str(md_path),
    }

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_lines = ["# v08.7.2 Production Query Surface Discovery", "", f"Summary: `{summary}`", ""]
    for c in checks:
        md_lines.append(f"## {c['status']} [{c['tier']}] {c['name']}")
        md_lines.append(c.get("details", ""))
        data = c.get("data")
        if data is not None:
            snippet = json.dumps(data, indent=2)[:12000]
            md_lines.append("```json")
            md_lines.append(snippet)
            md_lines.append("```")
        md_lines.append("")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(json.dumps({"summary": summary, "json": str(json_path), "markdown": str(md_path)}, indent=2))
    return 0 if summary.get("FAIL", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
