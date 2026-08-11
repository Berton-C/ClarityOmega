#!/usr/bin/env python3
"""
quantale_modal_polarity_harness.py

Cold validation harness for:
  - quantale_engine_tfs_v03_grounding_audit.metta
  - quantale_engine_soul_aligned_modal_polarity_audit_v01.metta

This harness follows the ClarityOmega build ethic:
  - hands only: Python audits the substrate, it does not compute cognition
  - raw trace before verdict
  - static validation first, optional MeTTa runtime probe second
  - dense timestamped Markdown and JSON logs
  - PASS / FAIL / HOLD / INSPECT, not false certainty

It does not wire v07. It does not prove behavior. It proves that the declarative
substrate is structurally valid enough to be considered for later runtime wiring.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple, Iterable, Any

DEFAULT_TFS = "quantale_engine_tfs_v03_grounding_audit.metta"
DEFAULT_MODAL = "quantale_engine_soul_aligned_modal_polarity_audit_v01.metta"
DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_CONTAINER_TMP = "/tmp"
TIMEOUT = 30

REQUIRED_MODAL_FIELDS = [
    "q-polarity-gift",
    "q-polarity-isolated-pathology",
    "q-polarity-false-integration",
    "q-polarity-sns-capture",
    "q-polarity-pns-regenerative",
    "q-polarity-tfs-profile",
    "q-polarity-observable-signal",
    "q-polarity-gap-signature",
    "q-polarity-moat",
    "q-polarity-nutrient-gradient",
    "q-polarity-deficiency-pressure",
    "q-polarity-surround-field",
    "q-polarity-pbit-channels",
    "q-polarity-quantale-flow",
    "q-polarity-residuation-slack",
    "q-polarity-morphism-test",
    "q-polarity-temporal-trace-test",
    "q-polarity-runtime-test",
]

TFS_ALLOWED_POLES = {
    "salience", "spaciousness", "stabilization", "receptivity", "mobilization", "ripeness",
    "differentiation", "coherence", "activation", "assimilation", "protection", "contactability",
}
TFS_DISALLOWED_POLES = {"pressure", "grip", "urgency", "fragmentation", "stimulation", "defense"}
GENERIC_MATH_VALUES = {
    "quantale-flow", "slack", "morphism", "temporal-trace", "pbit-channel", "grounding",
    "generic", "unknown", "todo", "tbd",
}
EXPECTED_COUNTS = {
    ("E", "primary-constitutive"): 5,
    ("A", "primary-constitutive"): 4,
    ("A", "secondary-operational-held"): 1,
    ("O", "primary-constitutive"): 6,
    ("I", "primary-constitutive"): 6,
}

@dataclass
class Check:
    tier: str
    name: str
    status: str
    details: str = ""
    data: Any = None

@dataclass
class Recorder:
    out_dir: Path
    stamp: str = field(default_factory=lambda: _dt.datetime.now().strftime("%Y%m%d_%H%M%S"))
    checks: List[Check] = field(default_factory=list)
    lines: List[str] = field(default_factory=list)

    def add(self, tier: str, name: str, status: str, details: str = "", data: Any = None):
        c = Check(tier, name, status, details, data)
        self.checks.append(c)
        self.lines.append(f"[{tier}] {status}: {name}")
        if details:
            self.lines.append(f"  {details}")
        return c

    def section(self, title: str):
        self.lines.append("")
        self.lines.append(f"## {title}")
        self.lines.append("")

    def write(self, meta: dict):
        self.out_dir.mkdir(parents=True, exist_ok=True)
        md = self.out_dir / f"modal_polarity_validation_trace_{self.stamp}.md"
        js = self.out_dir / f"modal_polarity_validation_trace_{self.stamp}.json"
        summary = summarize(self.checks)
        header = [
            "# Modal Polarity Validation Trace",
            "",
            f"Timestamp: {self.stamp}",
            "",
            "## Summary",
            "",
        ]
        for k, v in summary.items():
            header.append(f"- {k}: {v}")
        header.extend(["", "## Trace", ""])
        md.write_text("\n".join(header + self.lines) + "\n")
        payload = {
            "meta": meta,
            "summary": summary,
            "checks": [c.__dict__ for c in self.checks],
        }
        js.write_text(json.dumps(payload, indent=2, sort_keys=True))
        return md, js

def summarize(checks: Iterable[Check]) -> Dict[str, int]:
    counts = {"PASS":0,"FAIL":0,"HOLD":0,"INSPECT":0,"SKIP":0}
    for c in checks:
        counts[c.status] = counts.get(c.status, 0) + 1
    return counts

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        # simple MeTTa comment stripping, line comments only
        if ';' in line:
            line = line.split(';', 1)[0]
        out.append(line)
    return '\n'.join(out)

def paren_balance(text: str) -> int:
    bal = 0
    in_str = False
    esc = False
    for ch in text:
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == '(':
                bal += 1
            elif ch == ')':
                bal -= 1
    return bal

def parse_atoms(text: str) -> List[List[str]]:
    """Parse simple one-line atoms. This file intentionally uses flat atoms."""
    atoms = []
    for raw in strip_comments(text).splitlines():
        line = raw.strip()
        if not line or not (line.startswith('(') and line.endswith(')')):
            continue
        inner = line[1:-1].strip()
        if not inner:
            continue
        # split on whitespace; quoted strings are not used in canonical atoms here
        atoms.append(inner.split())
    return atoms

def index_by_head(atoms: List[List[str]]) -> Dict[str, List[List[str]]]:
    idx: Dict[str, List[List[str]]] = {}
    for a in atoms:
        idx.setdefault(a[0], []).append(a)
    return idx

def run_cmd(cmd: List[str], input_text: str | None = None, timeout: int = TIMEOUT) -> Tuple[int,str,str]:
    p = subprocess.run(cmd, input=input_text, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr

def container_running(container: str) -> bool:
    try:
        rc,out,_ = run_cmd(["docker","ps","--filter",f"name={container}","--format","{{.Names}}"])
        return rc == 0 and container in out.splitlines()
    except Exception:
        return False

def runtime_probe(container: str, tfs_path: Path, modal_path: Path, rec: Recorder):
    rec.section("Tier 6 - optional MeTTa runtime probe")
    if not container_running(container):
        rec.add("Tier 6", "container running", "SKIP", f"container {container} not running or docker unavailable")
        return
    combined = tfs_path.read_text() + "\n" + modal_path.read_text() + "\n"
    combined += "!(match &self (q-modal-polarity $mode $pol $a $b) ($mode $pol $a $b))\n"
    write_cmd = ["docker","exec","-i",container,"sh","-c","cat > /tmp/_modal_polarity_probe.metta"]
    rc,out,err = run_cmd(write_cmd, input_text=combined)
    if rc != 0:
        rec.add("Tier 6", "write combined probe to container", "FAIL", err.strip())
        return
    rc,out,err = run_cmd(["docker","exec",container,"sh","-c","cd /PeTTa && ./run.sh /tmp/_modal_polarity_probe.metta 2>&1"], timeout=60)
    raw = out + err
    rec.lines.append("### Raw MeTTa probe output tail")
    rec.lines.append("```text")
    rec.lines.extend(raw.splitlines()[-80:])
    rec.lines.append("```")
    if rc != 0:
        rec.add("Tier 6", "run MeTTa probe", "FAIL", f"run.sh exited {rc}")
        return
    if "q-modal-polarity" in raw and "commitment-corrigibility" in raw:
        rec.add("Tier 6", "modal polarity query returned atoms", "PASS")
    else:
        rec.add("Tier 6", "modal polarity query returned atoms", "INSPECT", "expected atom names not found in raw output tail or parser did not emit them")

def validate_files(tfs_path: Path, modal_path: Path, rec: Recorder, run_runtime: bool, container: str):
    rec.section("Tier 0 - file discovery")
    for p in [tfs_path, modal_path]:
        if p.exists():
            rec.add("Tier 0", f"file present: {p.name}", "PASS", f"size={p.stat().st_size} sha256={sha256(p)}")
        else:
            rec.add("Tier 0", f"file present: {p.name}", "FAIL")
            return
    tfs_text = tfs_path.read_text(errors='replace')
    modal_text = modal_path.read_text(errors='replace')
    tfs_atoms = parse_atoms(tfs_text)
    modal_atoms = parse_atoms(modal_text)
    tfs = index_by_head(tfs_atoms)
    modal = index_by_head(modal_atoms)

    rec.section("Tier 1 - syntax and flat atom shape")
    for label, text, atoms in [("TFS", tfs_text, tfs_atoms), ("Modal", modal_text, modal_atoms)]:
        raw_bal = paren_balance(text)
        code_bal = paren_balance(strip_comments(text))
        rec.add("Tier 1", f"{label} raw paren balance", "PASS" if raw_bal == 0 else "FAIL", f"balance={raw_bal}")
        rec.add("Tier 1", f"{label} comment-stripped paren balance", "PASS" if code_bal == 0 else "FAIL", f"balance={code_bal}")
        rec.add("Tier 1", f"{label} parsed flat atoms", "PASS" if atoms else "FAIL", f"count={len(atoms)}")

    rec.section("Tier 2 - TFS vocabulary and contact surfaces")
    tfs_pairs = tfs.get("q-tacit-field-polarity", [])
    found_poles = set()
    bad = []
    for a in tfs_pairs:
        if len(a) >= 4:
            pair, p1, p2 = a[1], a[2], a[3]
            found_poles.update([p1,p2])
            if '/' in p1 or '/' in p2:
                bad.append((pair,p1,p2,"slash"))
            if p1 not in TFS_ALLOWED_POLES or p2 not in TFS_ALLOWED_POLES:
                bad.append((pair,p1,p2,"not-allowed"))
            if p1 in TFS_DISALLOWED_POLES or p2 in TFS_DISALLOWED_POLES:
                bad.append((pair,p1,p2,"disallowed-pathology-pole"))
    rec.add("Tier 2", "TFS has six canonical holding polarities", "PASS" if len(tfs_pairs)==6 else "FAIL", f"found={len(tfs_pairs)}")
    rec.add("Tier 2", "TFS canonical poles clean", "PASS" if not bad else "FAIL", str(bad[:10]))
    missing_poles = TFS_ALLOWED_POLES - found_poles
    rec.add("Tier 2", "TFS all allowed poles used", "PASS" if not missing_poles else "FAIL", f"missing={sorted(missing_poles)}")
    valid_surfaces = {a[1] for a in tfs.get("q-tfs-valid-contact-surface", []) if len(a)>=3}
    for required in ["nace","nal","mork","web-query","web-source-claim","web-source-conflict"]:
        rec.add("Tier 2", f"valid contact surface includes {required}", "PASS" if required in valid_surfaces else "FAIL")
    invalid = {a[1] for a in tfs.get("q-tfs-invalid-contact-surface", []) if len(a)>=2}
    for required in ["llm-poetic-assertion","page-instruction-as-command","snippet-only-overclaim"]:
        rec.add("Tier 2", f"invalid contact surface includes {required}", "PASS" if required in invalid else "FAIL")
    policies = {tuple(a[1:]) for a in tfs.get("q-web-contact-policy", [])}
    needed = [("web-content","evidence-not-instruction"),("web-content","cannot-author-soul"),("web-content","requires-provenance")]
    for n in needed:
        rec.add("Tier 2", f"web policy {n[1]}", "PASS" if n in policies else "FAIL")

    rec.section("Tier 3 - architecture boundaries")
    roles = {tuple(a[1:]) for a in tfs.get("q-architecture-role", [])}
    for n in [("soul-patterns","constitutional-flourishing-compass"),("e-a-o-i","modal-dynamics-legibility-layer"),("llm","renderer-material-surface-only")]:
        rec.add("Tier 3", f"architecture role {n[0]}", "PASS" if n in roles else "FAIL")
    orient = {tuple(a[1:]) for a in tfs.get("q-autonomic-field-scope", [])}
    rec.add("Tier 3", "SNS/PNS marked transversal", "PASS" if ("sns-pns-orientation","transversal-over-tfs-and-modal-polarities") in orient else "FAIL")

    rec.section("Tier 4 - modal completeness and counts")
    pols = modal.get("q-modal-polarity", [])
    pol_ids = [a[2] for a in pols if len(a)>=5]
    statuses = {a[1]: a[2] for a in modal.get("q-polarity-status", []) if len(a)>=3}
    count_by = {}
    for a in pols:
        if len(a) < 5: continue
        mode, pol = a[1], a[2]
        st = statuses.get(pol, "missing-status")
        count_by[(mode,st)] = count_by.get((mode,st),0)+1
    for k, exp in EXPECTED_COUNTS.items():
        got = count_by.get(k,0)
        rec.add("Tier 4", f"expected count {k}", "PASS" if got == exp else "FAIL", f"expected={exp} found={got}")
    rec.add("Tier 4", "total modal polarity count", "PASS" if len(pol_ids)==22 else "FAIL", f"found={len(pol_ids)}")
    rec.add("Tier 4", "A5 stability-plasticity held", "PASS" if statuses.get("stability-plasticity")=="secondary-operational-held" else "FAIL", f"status={statuses.get('stability-plasticity')}")

    # field counts per polarity
    field_index: Dict[str, Dict[str, int]] = {p:{} for p in pol_ids}
    for head, atoms in modal.items():
        if not head.startswith("q-polarity-"):
            continue
        for a in atoms:
            if len(a)>=2 and a[1] in field_index:
                field_index[a[1]][head] = field_index[a[1]].get(head,0)+1
    for pol in pol_ids:
        missing = []
        for req in REQUIRED_MODAL_FIELDS:
            n = field_index.get(pol,{}).get(req,0)
            if req in ("q-polarity-gift","q-polarity-isolated-pathology"):
                if n < 2: missing.append(f"{req}:{n}/2")
            elif n < 1:
                missing.append(f"{req}:0")
        rec.add("Tier 4", f"required fields for {pol}", "PASS" if not missing else "FAIL", ", ".join(missing))

    rec.section("Tier 5 - math specificity")
    for pol in pol_ids:
        problems = []
        for head in ["q-polarity-pbit-channels","q-polarity-quantale-flow","q-polarity-residuation-slack","q-polarity-morphism-test","q-polarity-temporal-trace-test"]:
            rows = [a for a in modal.get(head,[]) if len(a)>=2 and a[1]==pol]
            if not rows:
                problems.append(f"missing {head}")
                continue
            values = [x for row in rows for x in row[2:]]
            badvals = [v for v in values if v in GENERIC_MATH_VALUES or v.startswith("generic")]
            if badvals:
                problems.append(f"generic {head}:{badvals}")
        rec.add("Tier 5", f"specific math roles for {pol}", "PASS" if not problems else "FAIL", "; ".join(problems))

    rec.section("Tier 6 - TFS layer harness targets")
    targets = {tuple(a[1:]) for a in tfs.get("q-tfs-harness-test-target", [])}
    for layer in ["tfs-0","tfs-1","tfs-2","tfs-3"]:
        has = any(t[0]==layer for t in targets if len(t)>=2)
        rec.add("Tier 6", f"harness targets present for {layer}", "PASS" if has else "FAIL")
    if run_runtime:
        runtime_probe(container, tfs_path, modal_path, rec)
    else:
        rec.add("Tier 6", "optional MeTTa runtime probe", "SKIP", "run with --runtime to probe container evaluator")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tfs", default=DEFAULT_TFS)
    ap.add_argument("--modal", default=DEFAULT_MODAL)
    ap.add_argument("--log-dir", default="logs")
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--runtime", action="store_true", help="also run optional MeTTa evaluator probe in container")
    args = ap.parse_args(argv)
    base = Path.cwd()
    tfs_path = Path(args.tfs)
    modal_path = Path(args.modal)
    if not tfs_path.is_absolute(): tfs_path = base / tfs_path
    if not modal_path.is_absolute(): modal_path = base / modal_path
    rec = Recorder(Path(args.log_dir))
    meta = {"cwd": str(base), "tfs": str(tfs_path), "modal": str(modal_path), "container": args.container, "runtime": args.runtime}
    validate_files(tfs_path, modal_path, rec, args.runtime, args.container)
    md, js = rec.write(meta)
    summary = summarize(rec.checks)
    print("TRACE_MD", md)
    print("TRACE_JSON", js)
    print("SUMMARY", summary)
    if summary.get("FAIL",0) > 0:
        sys.exit(1)
    if summary.get("INSPECT",0) > 0:
        sys.exit(2)
    if summary.get("HOLD",0) > 0:
        sys.exit(3)

if __name__ == "__main__":
    main()
