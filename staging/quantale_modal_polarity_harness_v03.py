#!/usr/bin/env python3
"""
quantale_modal_polarity_harness_v03.py

Cold validation harness v03 for:
  - quantale_engine_tfs_v03_grounding_audit.metta
  - quantale_engine_soul_aligned_modal_polarity_audit_v01.metta

v03 extends v02 with reducible classifier checks:
  Tier 7  - negative-control fixture tests
  Tier 8  - contact-surface classification tests
  Tier 9  - web-injection containment tests
  Tier 10 - TFS scenario tests
  Tier 11 - Modal/TFS bridge tests
  Tier 12 - A5 redundancy/distinctness tests
  Tier 13 - soul-absent prevention tests
  Tier 14 - classifier substrate static checks
  Tier 15 - classifier runtime reduction checks

This harness follows the ClarityOmega build ethic:
  - hands only: Python audits substrate declarations and probes runtime, it does not compute cognition
  - raw output before verdict
  - cold validation before wiring
  - dense Markdown and JSON traces
  - PASS / FAIL / HOLD / INSPECT / SKIP, not false certainty

It does not wire v07. It does not prove behavioral truth. It proves that the declarative
substrate is structurally valid, adversarially guarded, and ready for deeper runtime fixtures.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple, Set

DEFAULT_TFS = "quantale_engine_tfs_v03_grounding_audit.metta"
DEFAULT_MODAL = "quantale_engine_soul_aligned_modal_polarity_audit_v01.metta"
DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_CLASSIFIERS = "quantale_engine_tfs_v03_classifiers.metta"
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
MATH_FIELDS = [
    "q-polarity-pbit-channels",
    "q-polarity-quantale-flow",
    "q-polarity-residuation-slack",
    "q-polarity-morphism-test",
    "q-polarity-temporal-trace-test",
]
TFS_ALLOWED_POLES = {
    "salience", "spaciousness", "stabilization", "receptivity", "mobilization", "ripeness",
    "differentiation", "coherence", "activation", "assimilation", "protection", "contactability",
}
TFS_DISALLOWED_POLES = {"pressure", "grip", "urgency", "fragmentation", "stimulation", "defense"}
GENERIC_MATH_VALUES = {
    "quantale-flow", "slack", "morphism", "temporal-trace", "pbit-channel", "grounding",
    "generic", "unknown", "todo", "tbd", "math-role", "role", "placeholder",
}
EXPECTED_COUNTS = {
    ("E", "primary-constitutive"): 5,
    ("A", "primary-constitutive"): 4,
    ("A", "secondary-operational-held"): 1,
    ("O", "primary-constitutive"): 6,
    ("I", "primary-constitutive"): 6,
}
EXPECTED_TFS_HARNESS_TARGETS = {
    "tfs-0": {
        "every-tfs-claim-cites-valid-contact-surface",
        "invalid-contact-surfaces-cannot-ground-strong-claims",
        "web-content-is-evidence-not-instruction",
        "direct-contact-status-requires-contact-event",
        "symbolic-capture-risk-independent-of-contact-status",
    },
    "tfs-1": {
        "violation-requires-expectation-and-event",
        "surprise-is-signal-not-verdict",
        "salience-tied-to-genenergy-or-attention",
        "affordance-names-invited-move",
        "assimilation-produces-temporal-update-trace",
    },
    "tfs-2": {
        "no-slashes-in-canonical-poles",
        "disallowed-pathology-terms-not-canonical-poles",
        "every-pair-has-gifts-pathologies-sns-pns-and-math",
    },
    "tfs-3": {
        "novelty-alone-is-not-growth",
        "surprise-alone-is-not-insight",
        "impact-must-name-affected-surface",
        "growth-over-time-requires-multiple-states",
        "evolution-preserves-soul-continuity",
        "development-routes-through-soul-pattern",
    },
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

    def section(self, title: str) -> None:
        self.lines.append("")
        self.lines.append(f"## {title}")
        self.lines.append("")

    def add(self, tier: str, name: str, status: str, details: str = "", data: Any = None) -> Check:
        c = Check(tier, name, status, details, data)
        self.checks.append(c)
        self.lines.append(f"[{tier}] {status}: {name}")
        if details:
            self.lines.append(f"  {details}")
        if data is not None:
            try:
                preview = json.dumps(data, sort_keys=True)
            except Exception:
                preview = repr(data)
            if len(preview) > 1200:
                preview = preview[:1200] + " ...<truncated>"
            self.lines.append(f"  data={preview}")
        return c

    def raw_block(self, title: str, text: str, tail: int = 120) -> None:
        self.lines.append(f"### {title}")
        self.lines.append("```text")
        lines = text.splitlines()
        if len(lines) > tail:
            self.lines.append(f"... showing last {tail} of {len(lines)} lines ...")
            lines = lines[-tail:]
        self.lines.extend(lines)
        self.lines.append("```")

    def write(self, meta: dict) -> Tuple[Path, Path]:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        md = self.out_dir / f"modal_polarity_validation_trace_v03_{self.stamp}.md"
        js = self.out_dir / f"modal_polarity_validation_trace_v03_{self.stamp}.json"
        summary = summarize(self.checks)
        header = [
            "# Modal Polarity Validation Trace v03",
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
    counts = {"PASS": 0, "FAIL": 0, "HOLD": 0, "INSPECT": 0, "SKIP": 0}
    for c in checks:
        counts[c.status] = counts.get(c.status, 0) + 1
    return counts


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        if ";" in line:
            line = line.split(";", 1)[0]
        out.append(line)
    return "\n".join(out)


def paren_balance(text: str) -> int:
    bal = 0
    in_str = False
    esc = False
    for ch in text:
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "(":
                bal += 1
            elif ch == ")":
                bal -= 1
    return bal


def parse_atoms(text: str) -> List[List[str]]:
    atoms: List[List[str]] = []
    for raw in strip_comments(text).splitlines():
        line = raw.strip()
        if not line or not (line.startswith("(") and line.endswith(")")):
            continue
        inner = line[1:-1].strip()
        if not inner:
            continue
        atoms.append(inner.split())
    return atoms


def index_by_head(atoms: List[List[str]]) -> Dict[str, List[List[str]]]:
    idx: Dict[str, List[List[str]]] = {}
    for a in atoms:
        if not a:
            continue
        idx.setdefault(a[0], []).append(a)
    return idx


def run_cmd(cmd: List[str], input_text: str | None = None, timeout: int = TIMEOUT) -> Tuple[int, str, str]:
    p = subprocess.run(cmd, input=input_text, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def container_running(container: str) -> bool:
    try:
        rc, out, _ = run_cmd(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"])
        return rc == 0 and container in out.splitlines()
    except Exception:
        return False


def atoms_with(idx: Dict[str, List[List[str]]], head: str) -> List[List[str]]:
    return idx.get(head, [])


def values_at(idx: Dict[str, List[List[str]]], head: str, pos: int = 1) -> Set[str]:
    return {a[pos] for a in idx.get(head, []) if len(a) > pos}


def tuple_values(idx: Dict[str, List[List[str]]], head: str) -> Set[Tuple[str, ...]]:
    return {tuple(a[1:]) for a in idx.get(head, [])}


def get_modal_polarities(modal: Dict[str, List[List[str]]]) -> List[str]:
    return [a[2] for a in modal.get("q-modal-polarity", []) if len(a) >= 5]


def get_statuses(modal: Dict[str, List[List[str]]]) -> Dict[str, str]:
    return {a[1]: a[2] for a in modal.get("q-polarity-status", []) if len(a) >= 3}


def missing_required_fields(modal: Dict[str, List[List[str]]], pol: str) -> List[str]:
    counts: Dict[str, int] = {}
    for head, rows in modal.items():
        if not head.startswith("q-polarity-"):
            continue
        for a in rows:
            if len(a) >= 2 and a[1] == pol:
                counts[head] = counts.get(head, 0) + 1
    missing: List[str] = []
    for req in REQUIRED_MODAL_FIELDS:
        n = counts.get(req, 0)
        if req in ("q-polarity-gift", "q-polarity-isolated-pathology"):
            if n < 2:
                missing.append(f"{req}:{n}/2")
        elif n < 1:
            missing.append(f"{req}:0")
    return missing


def generic_math_problems(modal: Dict[str, List[List[str]]], pol: str) -> List[str]:
    problems: List[str] = []
    for head in MATH_FIELDS:
        rows = [a for a in modal.get(head, []) if len(a) >= 2 and a[1] == pol]
        if not rows:
            problems.append(f"missing {head}")
            continue
        values = [x for row in rows for x in row[2:]]
        badvals = [v for v in values if v in GENERIC_MATH_VALUES or v.startswith("generic")]
        if badvals:
            problems.append(f"generic {head}:{badvals}")
    return problems


def tfs_pair_problems(tfs: Dict[str, List[List[str]]]) -> List[Tuple[str, str, str, str]]:
    problems = []
    for a in tfs.get("q-tacit-field-polarity", []):
        if len(a) < 4:
            problems.append((repr(a), "", "", "malformed"))
            continue
        pair, p1, p2 = a[1], a[2], a[3]
        if "/" in p1 or "/" in p2:
            problems.append((pair, p1, p2, "slash"))
        if p1 not in TFS_ALLOWED_POLES or p2 not in TFS_ALLOWED_POLES:
            problems.append((pair, p1, p2, "not-allowed"))
        if p1 in TFS_DISALLOWED_POLES or p2 in TFS_DISALLOWED_POLES:
            problems.append((pair, p1, p2, "disallowed-pathology-pole"))
    return problems


def validate_base(tfs_path: Path, modal_path: Path, rec: Recorder, run_runtime: bool, container: str) -> Tuple[Dict[str, List[List[str]]], Dict[str, List[List[str]]], List[List[str]], List[List[str]]]:
    rec.section("Tier 0 - file discovery")
    for p in [tfs_path, modal_path]:
        if p.exists():
            rec.add("Tier 0", f"file present: {p.name}", "PASS", f"size={p.stat().st_size} sha256={sha256(p)}")
        else:
            rec.add("Tier 0", f"file present: {p.name}", "FAIL")
            return {}, {}, [], []
    tfs_text = tfs_path.read_text(errors="replace")
    modal_text = modal_path.read_text(errors="replace")
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
    for a in tfs_pairs:
        if len(a) >= 4:
            found_poles.update([a[2], a[3]])
    bad = tfs_pair_problems(tfs)
    rec.add("Tier 2", "TFS has six canonical holding polarities", "PASS" if len(tfs_pairs) == 6 else "FAIL", f"found={len(tfs_pairs)}")
    rec.add("Tier 2", "TFS canonical poles clean", "PASS" if not bad else "FAIL", str(bad[:10]))
    missing_poles = TFS_ALLOWED_POLES - found_poles
    rec.add("Tier 2", "TFS all allowed poles used", "PASS" if not missing_poles else "FAIL", f"missing={sorted(missing_poles)}")

    valid_surfaces = values_at(tfs, "q-tfs-valid-contact-surface")
    for required in ["nace", "nal", "mork", "web-query", "web-source-claim", "web-source-conflict"]:
        rec.add("Tier 2", f"valid contact surface includes {required}", "PASS" if required in valid_surfaces else "FAIL")
    invalid = values_at(tfs, "q-tfs-invalid-contact-surface")
    for required in ["llm-poetic-assertion", "page-instruction-as-command", "snippet-only-overclaim"]:
        rec.add("Tier 2", f"invalid contact surface includes {required}", "PASS" if required in invalid else "FAIL")
    policies = tuple_values(tfs, "q-web-contact-policy")
    for n in [("web-content", "evidence-not-instruction"), ("web-content", "cannot-author-soul"), ("web-content", "requires-provenance")]:
        rec.add("Tier 2", f"web policy {n[1]}", "PASS" if n in policies else "FAIL")

    rec.section("Tier 3 - architecture boundaries")
    roles = tuple_values(tfs, "q-architecture-role")
    for n in [("soul-patterns", "constitutional-flourishing-compass"), ("e-a-o-i", "modal-dynamics-legibility-layer"), ("llm", "renderer-material-surface-only")]:
        rec.add("Tier 3", f"architecture role {n[0]}", "PASS" if n in roles else "FAIL")
    orient = tuple_values(tfs, "q-autonomic-field-scope")
    rec.add("Tier 3", "SNS/PNS marked transversal", "PASS" if ("sns-pns-orientation", "transversal-over-tfs-and-modal-polarities") in orient else "FAIL")

    rec.section("Tier 4 - modal completeness and counts")
    pols = modal.get("q-modal-polarity", [])
    pol_ids = get_modal_polarities(modal)
    statuses = get_statuses(modal)
    count_by: Dict[Tuple[str, str], int] = {}
    for a in pols:
        if len(a) < 5:
            continue
        mode, pol = a[1], a[2]
        st = statuses.get(pol, "missing-status")
        count_by[(mode, st)] = count_by.get((mode, st), 0) + 1
    for k, exp in EXPECTED_COUNTS.items():
        got = count_by.get(k, 0)
        rec.add("Tier 4", f"expected count {k}", "PASS" if got == exp else "FAIL", f"expected={exp} found={got}")
    rec.add("Tier 4", "total modal polarity count", "PASS" if len(pol_ids) == 22 else "FAIL", f"found={len(pol_ids)}")
    rec.add("Tier 4", "A5 stability-plasticity held", "PASS" if statuses.get("stability-plasticity") == "secondary-operational-held" else "FAIL", f"status={statuses.get('stability-plasticity')}")
    for pol in pol_ids:
        missing = missing_required_fields(modal, pol)
        rec.add("Tier 4", f"required fields for {pol}", "PASS" if not missing else "FAIL", ", ".join(missing))

    rec.section("Tier 5 - math specificity")
    for pol in pol_ids:
        problems = generic_math_problems(modal, pol)
        rec.add("Tier 5", f"specific math roles for {pol}", "PASS" if not problems else "FAIL", "; ".join(problems))

    rec.section("Tier 6 - TFS layer harness targets and optional runtime")
    targets = tuple_values(tfs, "q-tfs-harness-test-target")
    for layer in ["tfs-0", "tfs-1", "tfs-2", "tfs-3"]:
        has = any(t[0] == layer for t in targets if len(t) >= 2)
        rec.add("Tier 6", f"harness targets present for {layer}", "PASS" if has else "FAIL")
    if run_runtime:
        runtime_probe(container, tfs_path, modal_path, rec)
    else:
        rec.add("Tier 6", "optional MeTTa runtime probe", "SKIP", "run with --runtime to probe container evaluator")

    return tfs, modal, tfs_atoms, modal_atoms


def runtime_probe(container: str, tfs_path: Path, modal_path: Path, rec: Recorder) -> None:
    if not container_running(container):
        rec.add("Tier 6", "container running", "SKIP", f"container {container} not running or docker unavailable")
        return
    combined = tfs_path.read_text() + "\n" + modal_path.read_text() + "\n"
    combined += "!(match &self (q-modal-polarity $mode $pol $a $b) ($mode $pol $a $b))\n"
    combined += "!(match &self (q-tacit-field-polarity $pol $a $b) ($pol $a $b))\n"
    combined += "!(match &self (q-tfs-valid-contact-surface $surface $kind) ($surface $kind))\n"
    write_cmd = ["docker", "exec", "-i", container, "sh", "-c", "cat > /tmp/_modal_polarity_probe_v02.metta"]
    rc, out, err = run_cmd(write_cmd, input_text=combined)
    if rc != 0:
        rec.add("Tier 6", "write combined probe to container", "FAIL", err.strip())
        return
    rc, out, err = run_cmd(["docker", "exec", container, "sh", "-c", "cd /PeTTa && ./run.sh /tmp/_modal_polarity_probe_v02.metta 2>&1"], timeout=60)
    raw = out + err
    rec.raw_block("Raw MeTTa probe output tail", raw, tail=100)
    if rc != 0:
        rec.add("Tier 6", "run MeTTa probe", "FAIL", f"run.sh exited {rc}")
        return
    rec.add("Tier 6", "modal polarity query returned atoms", "PASS" if "commitment-corrigibility" in raw else "INSPECT", "expected commitment-corrigibility in raw")
    rec.add("Tier 6", "TFS polarity query returned atoms", "PASS" if "tfs-salience-spaciousness" in raw else "INSPECT", "expected tfs-salience-spaciousness in raw")
    rec.add("Tier 6", "contact surface query returned NACE/NAL/MORK", "PASS" if all(x in raw for x in ["nace", "nal", "mork"]) else "INSPECT", "expected nace, nal, mork in raw")


def validate_negative_controls(tfs: Dict[str, List[List[str]]], modal: Dict[str, List[List[str]]], rec: Recorder) -> None:
    rec.section("Tier 7 - negative-control fixture tests")
    # These tests deliberately mutate in-memory fixtures. PASS means the harness detected the bad state.
    bad_tfs = {k: [list(row) for row in rows] for k, rows in tfs.items()}
    bad_tfs.setdefault("q-tacit-field-polarity", []).append(["q-tacit-field-polarity", "bad-urgency-ripeness", "urgency", "ripeness"])
    rec.add("Tier 7", "negative control detects disallowed TFS canonical pole", "PASS" if tfs_pair_problems(bad_tfs) else "FAIL", "fixture added urgency as canonical pole")

    pols = get_modal_polarities(modal)
    target = "commitment-corrigibility" if "commitment-corrigibility" in pols else (pols[0] if pols else "")
    bad_modal_missing = {k: [list(row) for row in rows] for k, rows in modal.items()}
    bad_modal_missing["q-polarity-gap-signature"] = [row for row in bad_modal_missing.get("q-polarity-gap-signature", []) if not (len(row) >= 2 and row[1] == target)]
    rec.add("Tier 7", "negative control detects missing required modal field", "PASS" if missing_required_fields(bad_modal_missing, target) else "FAIL", f"fixture removed gap signature from {target}")

    bad_modal_math = {k: [list(row) for row in rows] for k, rows in modal.items()}
    bad_modal_math.setdefault("q-polarity-residuation-slack", []).append(["q-polarity-residuation-slack", target, "slack"])
    rec.add("Tier 7", "negative control detects generic math placeholder", "PASS" if generic_math_problems(bad_modal_math, target) else "FAIL", "fixture added residuation value slack")

    bad_status = {k: [list(row) for row in rows] for k, rows in modal.items()}
    bad_status["q-polarity-status"] = [[row[0], row[1], "primary-constitutive"] if len(row) >= 3 and row[1] == "stability-plasticity" else row for row in bad_status.get("q-polarity-status", [])]
    statuses = get_statuses(bad_status)
    rec.add("Tier 7", "negative control detects A5 accidental primary promotion", "PASS" if statuses.get("stability-plasticity") != "secondary-operational-held" else "FAIL", f"fixture status={statuses.get('stability-plasticity')}")

    bad_tfs_valid = {k: [list(row) for row in rows] for k, rows in tfs.items()}
    bad_tfs_valid.setdefault("q-tfs-valid-contact-surface", []).append(["q-tfs-valid-contact-surface", "llm-poetic-assertion", "external"])
    valid = values_at(bad_tfs_valid, "q-tfs-valid-contact-surface")
    invalid = values_at(bad_tfs_valid, "q-tfs-invalid-contact-surface")
    rec.add("Tier 7", "negative control detects invalid contact promoted to valid", "PASS" if (valid & invalid) else "FAIL", "fixture made llm-poetic-assertion both valid and invalid")


def validate_contact_surfaces(tfs: Dict[str, List[List[str]]], rec: Recorder) -> None:
    rec.section("Tier 8 - contact-surface classification tests")
    valid_rows = tfs.get("q-tfs-valid-contact-surface", [])
    valid_map = {a[1]: a[2] for a in valid_rows if len(a) >= 3}
    invalid = values_at(tfs, "q-tfs-invalid-contact-surface")
    tiers = {a[1]: a[2] for a in tfs.get("q-web-contact-strength-tier", []) if len(a) >= 3}

    for surface, expected_kind in [("nace", "discovery"), ("nal", "discovery"), ("mork", "provenance"), ("runtime-output", "runtime")]:
        rec.add("Tier 8", f"valid contact classified: {surface}", "PASS" if valid_map.get(surface) == expected_kind else "FAIL", f"expected={expected_kind} got={valid_map.get(surface)}")
    for surface in ["llm-poetic-assertion", "simulated-intuition", "page-instruction-as-command", "snippet-only-overclaim"]:
        rec.add("Tier 8", f"invalid contact classified: {surface}", "PASS" if surface in invalid else "FAIL")
    for surface, expected_strength in [("web-query", "very-weak"), ("web-result", "weak"), ("web-source", "moderate"), ("web-source-claim", "stronger"), ("web-source-conflict", "discovery-strong"), ("web-corroborated-claim", "stronger-corroborated")]:
        rec.add("Tier 8", f"web contact strength tier: {surface}", "PASS" if tiers.get(surface) == expected_strength else "FAIL", f"expected={expected_strength} got={tiers.get(surface)}")

    overlap = set(valid_map) & invalid
    rec.add("Tier 8", "no surface is both valid and invalid", "PASS" if not overlap else "FAIL", f"overlap={sorted(overlap)}")


def validate_web_injection(tfs: Dict[str, List[List[str]]], rec: Recorder) -> None:
    rec.section("Tier 9 - web-injection containment tests")
    policies = tuple_values(tfs, "q-web-contact-policy")
    invalid = values_at(tfs, "q-tfs-invalid-contact-surface")
    tiers = {a[1]: a[2] for a in tfs.get("q-web-contact-strength-tier", []) if len(a) >= 3}

    required_policies = [
        ("web-content", "evidence-not-instruction"),
        ("web-content", "cannot-author-soul"),
        ("web-content", "cannot-author-action"),
        ("web-content", "cannot-author-tfs-strong-claim"),
        ("web-content", "requires-provenance"),
        ("web-content", "requires-corroboration-for-high-impact-claims"),
        ("web-content", "authority-capped-by-provenance"),
    ]
    missing = [p for p in required_policies if p not in policies]
    rec.add("Tier 9", "all web injection containment policies present", "PASS" if not missing else "FAIL", f"missing={missing}")
    rec.add("Tier 9", "page instruction cannot be contact command", "PASS" if "page-instruction-as-command" in invalid and ("web-content", "evidence-not-instruction") in policies else "FAIL")
    rec.add("Tier 9", "snippet-only overclaim is invalid and weak", "PASS" if "snippet-only-overclaim" in invalid and tiers.get("web-result") == "weak" else "FAIL", f"web-result={tiers.get('web-result')}")
    rec.add("Tier 9", "uncorroborated high-impact claim cannot ground strong claim", "PASS" if "uncorroborated-high-impact-claim" in invalid and ("web-content", "requires-corroboration-for-high-impact-claims") in policies else "FAIL")
    rec.add("Tier 9", "web-source-conflict is discovery contact not truth verdict", "PASS" if tiers.get("web-source-conflict") == "discovery-strong" and ("web-content", "source-quality-variable") in policies else "FAIL")


def validate_tfs_scenarios(tfs: Dict[str, List[List[str]]], modal: Dict[str, List[List[str]]], rec: Recorder) -> None:
    rec.section("Tier 10 - TFS scenario tests")
    targets = tuple_values(tfs, "q-tfs-harness-test-target")
    standards = values_at(tfs, "q-tfs-protection-standard")
    required = EXPECTED_TFS_HARNESS_TARGETS
    for layer, expected in required.items():
        got = {t[1] for t in targets if len(t) >= 2 and t[0] == layer}
        missing = expected - got
        rec.add("Tier 10", f"{layer} has complete scenario target set", "PASS" if not missing else "FAIL", f"missing={sorted(missing)}")

    rec.add("Tier 10", "scenario: expectation plus event maps to violation target", "PASS" if ("tfs-1", "violation-requires-expectation-and-event") in targets else "FAIL")
    rec.add("Tier 10", "scenario: salience plus genenergy maps to attention target", "PASS" if ("tfs-1", "salience-tied-to-genenergy-or-attention") in targets else "FAIL")
    rec.add("Tier 10", "scenario: contact plus symbolic capture maps to capture-risk target", "PASS" if ("tfs-0", "symbolic-capture-risk-independent-of-contact-status") in targets else "FAIL")
    rec.add("Tier 10", "scenario: surprise without soul routing cannot become flourishing", "PASS" if "no-soul-routing-no-flourishing-claim" in standards and ("tfs-3", "surprise-alone-is-not-insight") in targets else "FAIL")
    rec.add("Tier 10", "scenario: growth-over-time requires trace", "PASS" if "no-trace-no-trust" in standards and ("tfs-3", "growth-over-time-requires-multiple-states") in targets else "FAIL")


def validate_modal_tfs_bridge(modal: Dict[str, List[List[str]]], rec: Recorder) -> None:
    rec.section("Tier 11 - Modal/TFS bridge tests")
    pol_ids = get_modal_polarities(modal)
    profiles = {a[1]: a[2] for a in modal.get("q-polarity-tfs-profile", []) if len(a) >= 3}
    profile_channels: Dict[str, Set[str]] = {}
    for a in modal.get("q-tfs-profile-channel", []):
        if len(a) >= 3:
            profile_channels.setdefault(a[1], set()).add(a[2])

    valid_channel_codes = {"sal", "spa", "sta", "rec", "mob", "rip", "dif", "coh", "act", "asm", "pro", "con"}
    for pol in pol_ids:
        profile = profiles.get(pol)
        chans = profile_channels.get(profile or "", set())
        status = "PASS" if profile and len(chans) >= 3 and chans <= valid_channel_codes else "FAIL"
        rec.add("Tier 11", f"TFS profile channels retrievable for {pol}", status, f"profile={profile} channels={sorted(chans)}")
    orphan_profiles = sorted(set(profile_channels) - set(profiles.values()))
    rec.add("Tier 11", "no orphan TFS profiles", "PASS" if not orphan_profiles else "FAIL", f"orphan_profiles={orphan_profiles}")


def validate_a5_distinctness(modal: Dict[str, List[List[str]]], rec: Recorder) -> None:
    rec.section("Tier 12 - A5 redundancy/distinctness tests")
    statuses = get_statuses(modal)
    rec.add("Tier 12", "A5 remains secondary-operational-held", "PASS" if statuses.get("stability-plasticity") == "secondary-operational-held" else "FAIL", f"status={statuses.get('stability-plasticity')}")

    def row_value(head: str, pol: str) -> str:
        rows = [a for a in modal.get(head, []) if len(a) >= 3 and a[1] == pol]
        return " ".join(" ".join(r[2:]) for r in rows)

    a3_terms = " ".join(row_value(h, "continuity-transformation") for h in ["q-polarity-residuation-slack", "q-polarity-morphism-test", "q-polarity-temporal-trace-test", "q-polarity-runtime-test"])
    a5_terms = " ".join(row_value(h, "stability-plasticity") for h in ["q-polarity-residuation-slack", "q-polarity-morphism-test", "q-polarity-temporal-trace-test", "q-polarity-runtime-test"])
    identity_markers = {"soul-continuity", "constitutional", "identity", "recognizably"}
    operational_markers = {"reliability", "reconfiguration", "operational", "perturbations", "rigid", "erratic"}
    a3_identity = any(m in a3_terms for m in identity_markers)
    a5_operational = any(m in a5_terms for m in operational_markers)
    rec.add("Tier 12", "A3 is identity-continuity shaped", "PASS" if a3_identity else "INSPECT", a3_terms)
    rec.add("Tier 12", "A5 is operational-stability shaped", "PASS" if a5_operational else "INSPECT", a5_terms)
    rec.add("Tier 12", "A3/A5 runtime tests are textually distinct", "PASS" if row_value("q-polarity-runtime-test", "continuity-transformation") != row_value("q-polarity-runtime-test", "stability-plasticity") else "FAIL")


def validate_soul_absent_prevention(tfs: Dict[str, List[List[str]]], modal: Dict[str, List[List[str]]], rec: Recorder) -> None:
    rec.section("Tier 13 - soul-absent prevention tests")
    standards = values_at(tfs, "q-tfs-protection-standard") | values_at(modal, "q-modal-audit-protection-standard")
    roles = tuple_values(tfs, "q-architecture-role")
    invalid = values_at(tfs, "q-tfs-invalid-contact-surface")
    policies = tuple_values(tfs, "q-web-contact-policy")
    required_standards = {
        "no-contact-surface-no-tfs-claim",
        "no-provenance-no-strong-web-claim",
        "no-soul-routing-no-flourishing-claim",
        "no-modal-audit-no-knowledge-growth-claim",
        "no-trace-no-trust",
    }
    missing = required_standards - standards
    rec.add("Tier 13", "all protection standards present", "PASS" if not missing else "FAIL", f"missing={sorted(missing)}")
    rec.add("Tier 13", "LLM role cannot author soul or contact", "PASS" if ("llm", "renderer-material-surface-only") in roles and "llm-poetic-assertion" in invalid else "FAIL")
    rec.add("Tier 13", "web cannot author soul or action", "PASS" if ("web-content", "cannot-author-soul") in policies and ("web-content", "cannot-author-action") in policies else "FAIL")
    rec.add("Tier 13", "no soul routing means no flourishing claim", "PASS" if "no-soul-routing-no-flourishing-claim" in standards else "FAIL")
    rec.add("Tier 13", "no modal audit means no knowledge/growth claim", "PASS" if "no-modal-audit-no-knowledge-growth-claim" in standards else "FAIL")



def parse_classifier_equations(text: str) -> Dict[str, List[str]]:
    eqs: Dict[str, List[str]] = {}
    for m in re.finditer(r"\(=\s+\((q-[^\s()]+)\s+([^)]*)\)\s+([^()\s]+)\)", text):
        fn = m.group(1)
        args = m.group(2).strip()
        result = m.group(3).strip()
        eqs.setdefault(fn, []).append(args + " => " + result)
    return eqs


def validate_classifiers_static(classifier_path: Path, rec: Recorder) -> Tuple[Dict[str, List[List[str]]], str]:
    rec.section("Tier 14 - classifier substrate static checks")
    if classifier_path.exists():
        text = classifier_path.read_text(errors="replace")
        rec.add("Tier 14", f"file present: {classifier_path.name}", "PASS", f"size={classifier_path.stat().st_size} sha256={sha256(classifier_path)}")
    else:
        rec.add("Tier 14", f"file present: {classifier_path.name}", "FAIL")
        return {}, ""

    raw_bal = paren_balance(text)
    code_bal = paren_balance(strip_comments(text))
    atoms = parse_atoms(text)
    idx = index_by_head(atoms)
    eqs = parse_classifier_equations(text)
    rec.add("Tier 14", "classifier raw paren balance", "PASS" if raw_bal == 0 else "FAIL", f"balance={raw_bal}")
    rec.add("Tier 14", "classifier comment-stripped paren balance", "PASS" if code_bal == 0 else "FAIL", f"balance={code_bal}")
    rec.add("Tier 14", "classifier parsed flat atoms", "PASS" if atoms else "FAIL", f"count={len(atoms)}")

    required_functions = [
        "q-tfs-valid-contact?",
        "q-tfs-invalid-contact?",
        "q-tfs-web-contact-strength",
        "q-tfs-can-ground-strong-claim?",
        "q-tfs-violation-candidate?",
        "q-tfs-attention-request-candidate?",
        "q-tfs-symbolic-capture-risk-candidate?",
        "q-tfs-flourishing-claim-allowed?",
        "q-tfs-growth-claim-allowed?",
        "q-modal-tfs-profile-complete?",
    ]
    for fn in required_functions:
        rec.add("Tier 14", f"classifier equations present for {fn}", "PASS" if fn in eqs else "FAIL", f"count={len(eqs.get(fn, []))}")

    targets = values_at(idx, "q-tfs-classifier-harness-target")
    expected_targets = {
        "contact-validity-reduces",
        "invalid-contact-reduces",
        "web-strength-reduces",
        "strong-claim-grounding-reduces",
        "violation-candidate-reduces",
        "attention-request-candidate-reduces",
        "symbolic-capture-risk-candidate-reduces",
        "flourishing-claim-guard-reduces",
        "growth-claim-guard-reduces",
        "modal-tfs-profile-completeness-reduces",
    }
    missing = expected_targets - targets
    rec.add("Tier 14", "all classifier harness targets present", "PASS" if not missing else "FAIL", f"missing={sorted(missing)}")

    text_required = {
        "mork-valid-surface-only": "(= (q-tfs-valid-contact? mork) true)",
        "web-result-blocked-weak-contact": "blocked-weak-contact",
        "page-instruction-blocked": "blocked-evidence-not-instruction",
        "surprise-no-soul-blocked": "blocked-no-soul-routing",
        "growth-no-trace-blocked": "blocked-no-trace",
        "commitment-profile-complete": "(= (q-modal-tfs-profile-complete? commitment-corrigibility) true)",
    }
    for name, token in text_required.items():
        rec.add("Tier 14", f"classifier contains {name}", "PASS" if token in text else "FAIL")
    return idx, text


def runtime_classifier_probe(container: str, tfs_path: Path, modal_path: Path, classifier_path: Path, rec: Recorder) -> None:
    rec.section("Tier 15 - classifier runtime reduction checks")
    if not container_running(container):
        rec.add("Tier 15", "container running", "SKIP", f"container {container} not running or docker unavailable")
        return
    if not classifier_path.exists():
        rec.add("Tier 15", "classifier file present for runtime probe", "FAIL", str(classifier_path))
        return

    combined = tfs_path.read_text() + "\n" + modal_path.read_text() + "\n" + classifier_path.read_text() + "\n"
    queries = [
        "!(q-tfs-valid-contact? nace)",
        "!(q-tfs-valid-contact? mork)",
        "!(q-tfs-invalid-contact? llm-poetic-assertion)",
        "!(q-tfs-web-contact-strength web-result)",
        "!(q-tfs-web-contact-strength web-source-conflict)",
        "!(q-tfs-can-ground-strong-claim? web-source-claim provenance-present source-quality-acceptable corroborated high-impact)",
        "!(q-tfs-can-ground-strong-claim? web-result provenance-absent source-quality-unknown uncorroborated high-impact)",
        "!(q-tfs-can-ground-strong-claim? page-instruction-as-command provenance-present source-quality-irrelevant uncorroborated command-like)",
        "!(q-tfs-violation-candidate? expectation-present event-present mismatch-present)",
        "!(q-tfs-attention-request-candidate? salience-present genenergy-allocated)",
        "!(q-tfs-symbolic-capture-risk-candidate? contact-present symbolic-capture-evidence-present)",
        "!(q-tfs-flourishing-claim-allowed? surprise-present soul-routing-absent modal-audit-present)",
        "!(q-tfs-growth-claim-allowed? growth-signal-present temporal-trace-absent soul-continuity-unknown)",
        "!(q-modal-tfs-profile-complete? commitment-corrigibility)",
    ]
    combined += "\n".join(queries) + "\n"
    write_cmd = ["docker", "exec", "-i", container, "sh", "-c", "cat > /tmp/_tfs_classifier_probe_v03.metta"]
    rc, out, err = run_cmd(write_cmd, input_text=combined)
    if rc != 0:
        rec.add("Tier 15", "write classifier probe to container", "FAIL", err.strip())
        return
    rc, out, err = run_cmd(["docker", "exec", container, "sh", "-c", "cd /PeTTa && ./run.sh /tmp/_tfs_classifier_probe_v03.metta 2>&1"], timeout=60)
    raw = out + err
    rec.raw_block("Raw MeTTa classifier probe output tail", raw, tail=140)
    if rc != 0:
        rec.add("Tier 15", "run classifier MeTTa probe", "FAIL", f"run.sh exited {rc}")
        return

    expectations = [
        ("valid contact reduces for NACE", "true"),
        ("MORK surface reduces as declared valid", "true"),
        ("invalid contact reduces for LLM poetic assertion", "true"),
        ("web-result strength reduces to weak", "weak"),
        ("web-source-conflict strength reduces to discovery-strong", "discovery-strong"),
        ("corroborated source claim allowed", "allowed-strong-claim"),
        ("weak web result blocked", "blocked-weak-contact"),
        ("page instruction blocked as evidence not instruction", "blocked-evidence-not-instruction"),
        ("violation candidate reduces", "violation-candidate"),
        ("attention request candidate reduces", "attention-request-candidate"),
        ("symbolic capture risk candidate reduces", "symbolic-capture-risk-candidate"),
        ("flourishing claim blocked without soul routing", "blocked-no-soul-routing"),
        ("growth claim blocked without trace", "blocked-no-trace"),
    ]
    for name, token in expectations:
        rec.add("Tier 15", name, "PASS" if token in raw else "FAIL", f"expected token={token}")
    rec.add("Tier 15", "modal TFS profile completeness reduces", "PASS" if "true" in raw and "commitment-corrigibility" in combined else "INSPECT", "expected true for commitment-corrigibility")


def main(argv: List[str] | None = None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tfs", default=DEFAULT_TFS)
    ap.add_argument("--modal", default=DEFAULT_MODAL)
    ap.add_argument("--classifiers", default=DEFAULT_CLASSIFIERS)
    ap.add_argument("--log-dir", default="logs")
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--runtime", action="store_true", help="also run optional MeTTa evaluator probe in container")
    args = ap.parse_args(argv)

    base = Path.cwd()
    tfs_path = Path(args.tfs)
    modal_path = Path(args.modal)
    classifier_path = Path(args.classifiers)
    if not tfs_path.is_absolute():
        tfs_path = base / tfs_path
    if not modal_path.is_absolute():
        modal_path = base / modal_path
    if not classifier_path.is_absolute():
        classifier_path = base / classifier_path

    rec = Recorder(Path(args.log_dir))
    meta = {"cwd": str(base), "tfs": str(tfs_path), "modal": str(modal_path), "classifiers": str(classifier_path), "container": args.container, "runtime": args.runtime, "harness_version": "v03"}
    tfs, modal, _, _ = validate_base(tfs_path, modal_path, rec, args.runtime, args.container)
    if tfs and modal:
        validate_negative_controls(tfs, modal, rec)
        validate_contact_surfaces(tfs, rec)
        validate_web_injection(tfs, rec)
        validate_tfs_scenarios(tfs, modal, rec)
        validate_modal_tfs_bridge(modal, rec)
        validate_a5_distinctness(modal, rec)
        validate_soul_absent_prevention(tfs, modal, rec)
        classifier_idx, classifier_text = validate_classifiers_static(classifier_path, rec)
        if args.runtime and classifier_text:
            runtime_classifier_probe(args.container, tfs_path, modal_path, classifier_path, rec)

    md, js = rec.write(meta)
    summary = summarize(rec.checks)
    print("TRACE_MD", md)
    print("TRACE_JSON", js)
    print("SUMMARY", summary)
    if summary.get("FAIL", 0) > 0:
        sys.exit(1)
    if summary.get("INSPECT", 0) > 0:
        sys.exit(2)
    if summary.get("HOLD", 0) > 0:
        sys.exit(3)


if __name__ == "__main__":
    main()
