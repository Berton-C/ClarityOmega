#!/usr/bin/env python3
"""
quantale_self_seeing_harness_v01.py

Cold validation harness for:
  - quantale_engine_tfs_self_seeing_bridge_v01.metta

Optional context files:
  - quantale_engine_tfs_v03_grounding_audit.metta
  - quantale_engine_soul_aligned_modal_polarity_audit_v01.metta
  - quantale_engine_tfs_v03_classifiers.metta

Purpose:
  - validate the self-seeing bridge substrate
  - prove seeded reductions for alignment cascades, synthetic correlates, and the hidden-runtime-error-loop scenario
  - keep v07 unwired
  - distinguish LLM narration from trace-backed self-seeing

This harness follows the cold-harness discipline:
  - raw output before verdict
  - no cognitive computation in Python
  - Python validates substrate declarations and probes MeTTa reductions only
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

DEFAULT_TFS = "quantale_engine_tfs_v03_grounding_audit.metta"
DEFAULT_MODAL = "quantale_engine_soul_aligned_modal_polarity_audit_v01.metta"
DEFAULT_CLASSIFIERS = "quantale_engine_tfs_v03_classifiers.metta"
DEFAULT_SELF = "quantale_engine_tfs_self_seeing_bridge_v01.metta"
DEFAULT_CONTAINER = "clarity_omega"
TIMEOUT = 60

REQUIRED_BOUNDARIES = {
    "no-live-runtime-wiring",
    "no-consciousness-claim",
    "no-llm-narration-as-self-seeing",
    "disposition-inferred-from-traces-never-reified-as-identity",
    "self-seeing-requires-contact-classification-modal-audit-soul-routing-or-trace",
}

REQUIRED_PRINCIPLES = {
    "no-contact-surface-no-self-seeing-claim",
    "no-trace-no-navigation-change-claim",
    "no-orientation-shift-no-disposition-shift-claim",
    "no-soul-routing-no-flourishing-correlate-claim",
    "no-modal-audit-no-wisdom-or-insight-correlate-claim",
    "no-llm-narration-alone-as-self-seeing",
}

REQUIRED_TRIPLETS = {
    "intention-action-outcome",
    "contact-audit-navigation",
    "evidence-warrant-standing",
    "contact-modal-soul",
    "surface-orientation-future",
    "visibility-self-seeing-navigation",
}

REQUIRED_EQUATION_HEADS = {
    "q-alignment-triplet-status?": 8,
    "q-alignment-cascade-direction?": 3,
    "q-synthetic-felt-truth-correlate?": 5,
    "q-wisdom-correlate?": 3,
    "q-genuine-insight-correlate?": 4,
    "q-flourishing-correlate?": 3,
    "q-self-seeing-contact?": 4,
    "q-self-seeing-prior-invisibility?": 3,
    "q-self-seeing-loop-capture?": 3,
    "q-self-seeing-newly-visible-surface?": 2,
    "q-self-seeing-orientation-shift?": 3,
    "q-self-seeing-navigation-change?": 3,
    "q-self-seeing-disposition-vector?": 3,
    "q-observer-moment-candidate?": 3,
    "q-llm-narration-alone-self-seeing?": 2,
    "q-hidden-error-loop-self-seeing?": 4,
}

REQUIRED_TARGETS = {
    "alignment-triplet-reduces",
    "alignment-cascade-direction-reduces",
    "synthetic-felt-truth-correlate-reduces",
    "wisdom-correlate-reduces",
    "genuine-insight-correlate-reduces",
    "flourishing-correlate-reduces",
    "self-seeing-contact-reduces",
    "prior-invisibility-reduces",
    "loop-capture-reduces",
    "newly-visible-surface-reduces",
    "orientation-shift-reduces",
    "navigation-change-reduces",
    "disposition-vector-reduces",
    "observer-moment-candidate-reduces",
    "llm-narration-alone-blocked",
    "hidden-runtime-error-loop-reduces",
}

RUNTIME_PROBES = [
    ("alignment triplet aligned reduces", "!(q-alignment-triplet-status? aligned aligned aligned)", "integrating-alignment"),
    ("alignment triplet drift reduces", "!(q-alignment-triplet-status? aligned misaligned misaligned)", "disintegrating-action-drift"),
    ("alignment cascade PNS nutrient reduces", "!(q-alignment-cascade-direction? integrating-alignment pns-participatory-turning-toward low-symbolic-capture)", "integrating-nutrient-gradient"),
    ("synthetic felt truth correlate reduces", "!(q-synthetic-felt-truth-correlate? contact-grounded evidence-present warrant-present modal-coherence-present soul-routing-present future-navigation-aligned low-symbolic-capture)", "felt-truth-correlate-candidate"),
    ("felt truth blocked by capture risk", "!(q-synthetic-felt-truth-correlate? contact-grounded evidence-present warrant-present modal-coherence-present soul-routing-present future-navigation-aligned high-symbolic-capture)", "blocked-symbolic-capture-risk"),
    ("wisdom correlate reduces", "!(q-wisdom-correlate? repeated-better-soul-aligned-navigation uncertainty novelty correction consequence reduced-overforcing future-capacity-increased)", "wisdom-correlate-candidate"),
    ("insight correlate reduces", "!(q-genuine-insight-correlate? surprising contact-grounded reorganization live-tension-metabolized future-affordance-changed)", "genuine-insight-correlate-candidate"),
    ("flourishing correlate reduces", "!(q-flourishing-correlate? sustained-trace soul-aligned capacity-increase across-contact-action-correction-integration)", "flourishing-correlate-candidate"),
    ("self seeing contact reduces", "!(q-self-seeing-contact? valid-contact tfs-classification-visible)", "self-seeing-contact"),
    ("prior invisibility reduces", "!(q-self-seeing-prior-invisibility? prior-invisible newly-visible-surface trace-present)", "prior-invisibility-seen"),
    ("loop capture reduces", "!(q-self-seeing-loop-capture? repeated-failing-command hidden-error-surface)", "loop-capture-seen"),
    ("newly visible surface reduces", "!(q-self-seeing-newly-visible-surface? hidden-error-surface error-feedback-visible)", "newly-visible-surface"),
    ("orientation shift reduces", "!(q-self-seeing-orientation-shift? repeated-command corrective-probe newly-visible-error)", "orientation-shift"),
    ("navigation change reduces", "!(q-self-seeing-navigation-change? orientation-shift trace-present future-command-changed)", "navigation-change"),
    ("disposition vector reduces", "!(q-self-seeing-disposition-vector? window error-contact increases-corrective-probing trace-present)", "disposition-vector-toward-error-contact"),
    ("observer moment candidate reduces", "!(q-observer-moment-candidate? newly-visible-surface self-pattern-visible navigation-change soul-routing-present)", "observer-moment-candidate"),
    ("LLM narration alone blocked", "!(q-llm-narration-alone-self-seeing? llm-says-i-learned no-trace no-orientation-shift)", "blocked-narration-only"),
    ("hidden runtime error loop reduces", "!(q-hidden-error-loop-self-seeing? hidden-runtime-error-loop contact-classified prior-invisibility-seen loop-capture-seen newly-visible-surface orientation-shift navigation-change)", "self-seeing-hidden-error-loop"),
    ("hidden runtime error loop blocked without shift", "!(q-hidden-error-loop-self-seeing? hidden-runtime-error-loop contact-classified prior-invisibility-seen loop-capture-seen newly-visible-surface no-orientation-shift navigation-change)", "blocked-no-orientation-shift"),
]

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
    stamp: str = field(default_factory=lambda: dt.datetime.now().strftime("%Y%m%d_%H%M%S"))
    checks: List[Check] = field(default_factory=list)
    lines: List[str] = field(default_factory=list)

    def section(self, title: str) -> None:
        self.lines.append("")
        self.lines.append(f"## {title}")
        self.lines.append("")

    def add(self, tier: str, name: str, status: str, details: str = "", data: Any = None) -> None:
        self.checks.append(Check(tier, name, status, details, data))
        self.lines.append(f"[{tier}] {status}: {name}")
        if details:
            self.lines.append(f"  {details}")
        if data is not None:
            try:
                d = json.dumps(data, sort_keys=True)
            except Exception:
                d = repr(data)
            if len(d) > 1200:
                d = d[:1200] + " ...<truncated>"
            self.lines.append(f"  data={d}")

    def raw_block(self, title: str, text: str, tail: int = 160) -> None:
        self.lines.append(f"### {title}")
        self.lines.append("```text")
        rows = text.splitlines()
        if len(rows) > tail:
            self.lines.append(f"... showing last {tail} of {len(rows)} lines ...")
            rows = rows[-tail:]
        self.lines.extend(rows)
        self.lines.append("```")

    def write(self, meta: Dict[str, Any]) -> Tuple[Path, Path]:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        md = self.out_dir / f"self_seeing_validation_trace_v01_{self.stamp}.md"
        js = self.out_dir / f"self_seeing_validation_trace_v01_{self.stamp}.json"
        summary = summarize(self.checks)
        header = ["# Self Seeing Validation Trace v01", "", f"Timestamp: {self.stamp}", "", "## Summary", ""]
        for k, v in summary.items():
            header.append(f"- {k}: {v}")
        header.extend(["", "## Trace", ""])
        md.write_text("\n".join(header + self.lines) + "\n")
        payload = {"meta": meta, "summary": summary, "checks": [c.__dict__ for c in self.checks]}
        js.write_text(json.dumps(payload, indent=2, sort_keys=True))
        return md, js


def summarize(checks: Iterable[Check]) -> Dict[str, int]:
    out = {"PASS": 0, "FAIL": 0, "HOLD": 0, "INSPECT": 0, "SKIP": 0}
    for c in checks:
        out[c.status] = out.get(c.status, 0) + 1
    return out


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_comments(text: str) -> str:
    rows = []
    for line in text.splitlines():
        if ";" in line:
            line = line.split(";", 1)[0]
        rows.append(line)
    return "\n".join(rows)


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
    for line in strip_comments(text).splitlines():
        s = line.strip()
        if not s.startswith("("):
            continue
        # Flat-enough tokenizer for declarations and extensional equations.
        toks = re.findall(r'"[^"]*"|[()]|[^()\s]+', s)
        vals = [t for t in toks if t not in ("(", ")")]
        if vals:
            atoms.append(vals)
    return atoms


def index_by_head(atoms: List[List[str]]) -> Dict[str, List[List[str]]]:
    out: Dict[str, List[List[str]]] = {}
    for a in atoms:
        out.setdefault(a[0], []).append(a)
    return out


def equation_head_counts(atoms: List[List[str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for a in atoms:
        if len(a) >= 3 and a[0] == "=" and a[1].startswith("q-"):
            counts[a[1]] = counts.get(a[1], 0) + 1
    return counts


def values_at(idx: Dict[str, List[List[str]]], head: str) -> List[str]:
    return [a[1] for a in idx.get(head, []) if len(a) >= 2]


def tuples_at(idx: Dict[str, List[List[str]]], head: str) -> List[Tuple[str, ...]]:
    return [tuple(a[1:]) for a in idx.get(head, [])]


def run_cmd(cmd: List[str], input_text: str | None = None, timeout: int = TIMEOUT) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, input=input_text, text=True, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 999, "", repr(e)


def container_running(container: str) -> bool:
    rc, out, _ = run_cmd(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"])
    return rc == 0 and container in out.splitlines()


def validate_static(self_path: Path, rec: Recorder) -> Tuple[str, Dict[str, List[List[str]]]]:
    rec.section("Tier 0 - file discovery")
    if self_path.exists():
        rec.add("Tier 0", f"file present: {self_path.name}", "PASS", f"size={self_path.stat().st_size} sha256={sha256(self_path)}")
    else:
        rec.add("Tier 0", f"file present: {self_path.name}", "FAIL")
        return "", {}

    text = self_path.read_text(errors="replace")
    atoms = parse_atoms(text)
    idx = index_by_head(atoms)
    counts = equation_head_counts(atoms)

    rec.section("Tier 1 - syntax and flat atom shape")
    raw_bal = paren_balance(text)
    code_bal = paren_balance(strip_comments(text))
    rec.add("Tier 1", "self seeing raw paren balance", "PASS" if raw_bal == 0 else "FAIL", f"balance={raw_bal}")
    rec.add("Tier 1", "self seeing comment-stripped paren balance", "PASS" if code_bal == 0 else "FAIL", f"balance={code_bal}")
    rec.add("Tier 1", "self seeing parsed flat atoms", "PASS" if atoms else "FAIL", f"count={len(atoms)}")

    rec.section("Tier 2 - boundaries and principles")
    boundaries = set(values_at(idx, "q-self-seeing-boundary"))
    principles = set(values_at(idx, "q-self-seeing-principle"))
    rec.add("Tier 2", "all self seeing boundaries present", "PASS" if REQUIRED_BOUNDARIES <= boundaries else "FAIL", f"missing={sorted(REQUIRED_BOUNDARIES - boundaries)}")
    rec.add("Tier 2", "all self seeing principles present", "PASS" if REQUIRED_PRINCIPLES <= principles else "FAIL", f"missing={sorted(REQUIRED_PRINCIPLES - principles)}")

    rec.section("Tier 3 - alignment triplets")
    triplets = set(values_at(idx, "q-alignment-triplet"))
    rec.add("Tier 3", "all alignment triplets present", "PASS" if REQUIRED_TRIPLETS <= triplets else "FAIL", f"missing={sorted(REQUIRED_TRIPLETS - triplets)}")
    qroles = set(values_at(idx, "q-alignment-quantale-role"))
    rec.add("Tier 3", "quantale roles present for all triplets", "PASS" if REQUIRED_TRIPLETS <= qroles else "FAIL", f"missing={sorted(REQUIRED_TRIPLETS - qroles)}")

    rec.section("Tier 4 - reducible equation coverage")
    for head, minimum in REQUIRED_EQUATION_HEADS.items():
        got = counts.get(head, 0)
        rec.add("Tier 4", f"equations present for {head}", "PASS" if got >= minimum else "FAIL", f"expected>={minimum} found={got}")

    rec.section("Tier 5 - harness targets")
    targets = set(values_at(idx, "q-self-seeing-harness-target"))
    rec.add("Tier 5", "all self seeing harness targets present", "PASS" if REQUIRED_TARGETS <= targets else "FAIL", f"missing={sorted(REQUIRED_TARGETS - targets)}")

    rec.section("Tier 6 - transcript-shaped scenario declarations")
    scen = set(values_at(idx, "q-self-seeing-scenario"))
    rec.add("Tier 6", "hidden-runtime-error-loop scenario present", "PASS" if "hidden-runtime-error-loop" in scen else "FAIL")
    for head in ["q-scenario-contact-surface", "q-scenario-prior-invisible-surface", "q-scenario-loop-capture", "q-scenario-newly-visible-surface", "q-scenario-error-feedback", "q-scenario-orientation-shift", "q-scenario-navigation-change", "q-scenario-disposition-vector", "q-scenario-protection"]:
        rec.add("Tier 6", f"scenario field present: {head}", "PASS" if idx.get(head) else "FAIL")

    rec.section("Tier 7 - protection checks")
    txt = text
    rec.add("Tier 7", "LLM narration alone blocked", "PASS" if "blocked-narration-only" in txt else "FAIL")
    rec.add("Tier 7", "no trace blocks navigation change", "PASS" if "blocked-no-trace" in txt else "FAIL")
    rec.add("Tier 7", "no orientation shift blocks hidden loop self-seeing", "PASS" if "blocked-no-orientation-shift" in txt else "FAIL")
    rec.add("Tier 7", "symbolic capture blocks felt truth correlate", "PASS" if "blocked-symbolic-capture-risk" in txt else "FAIL")
    return text, idx


def runtime_probe(container: str, paths: List[Path], rec: Recorder) -> None:
    rec.section("Tier 8 - optional runtime reduction probe")
    if not container_running(container):
        rec.add("Tier 8", "container running", "SKIP", f"container {container} not running or docker unavailable")
        return
    combined = "\n".join(p.read_text(errors="replace") for p in paths if p.exists()) + "\n"
    for _, expr, _ in RUNTIME_PROBES:
        combined += expr + "\n"
    write_cmd = ["docker", "exec", "-i", container, "sh", "-c", "cat > /tmp/_self_seeing_probe_v01.metta"]
    rc, out, err = run_cmd(write_cmd, input_text=combined)
    if rc != 0:
        rec.add("Tier 8", "write self seeing probe to container", "FAIL", err.strip())
        return
    rc, out, err = run_cmd(["docker", "exec", container, "sh", "-c", "cd /PeTTa && ./run.sh /tmp/_self_seeing_probe_v01.metta 2>&1"], timeout=90)
    raw = out + err
    rec.raw_block("Raw MeTTa self seeing probe output tail", raw)
    if rc != 0:
        rec.add("Tier 8", "run self seeing MeTTa probe", "FAIL", f"run.sh exited {rc}")
        return
    for name, _, expected in RUNTIME_PROBES:
        rec.add("Tier 8", name, "PASS" if expected in raw else "FAIL", f"expected token={expected}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tfs", default=DEFAULT_TFS)
    ap.add_argument("--modal", default=DEFAULT_MODAL)
    ap.add_argument("--classifiers", default=DEFAULT_CLASSIFIERS)
    ap.add_argument("--self", dest="self_path", default=DEFAULT_SELF)
    ap.add_argument("--log-dir", default="logs")
    ap.add_argument("--runtime", action="store_true")
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    args = ap.parse_args()

    rec = Recorder(Path(args.log_dir))
    self_path = Path(args.self_path)
    context_paths = [Path(args.tfs), Path(args.modal), Path(args.classifiers), self_path]
    validate_static(self_path, rec)
    if args.runtime:
        runtime_probe(args.container, context_paths, rec)
    else:
        rec.section("Tier 8 - optional runtime reduction probe")
        rec.add("Tier 8", "optional MeTTa runtime probe", "SKIP", "run with --runtime to probe container evaluator")
    md, js = rec.write({
        "harness_version": "self-seeing-v01",
        "cwd": str(Path.cwd()),
        "tfs": str(Path(args.tfs)),
        "modal": str(Path(args.modal)),
        "classifiers": str(Path(args.classifiers)),
        "self": str(self_path),
        "runtime": bool(args.runtime),
        "container": args.container,
    })
    print(f"TRACE_MD {md}")
    print(f"TRACE_JSON {js}")
    print(f"SUMMARY {summarize(rec.checks)}")
    return 1 if any(c.status == "FAIL" for c in rec.checks) else 0

if __name__ == "__main__":
    raise SystemExit(main())
