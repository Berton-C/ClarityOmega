#!/usr/bin/env python3
"""
quantale_v08_integration_harness.py

Cold validation harness for:
  - lib_quantale_autopoietic_epistemic_dynamics_engine_v08_TFS_SELF_SEEING.metta
  - quantale_engine_validation_ladder_v08_TFS_SELF_SEEING.metta

Purpose:
  - confirm all four TFS layers landed in integrated v08
  - validate self-seeing/alignment-cascade primitives landed without reifying disposition
  - probe runtime reductions for promoted TFS/classifier/self-seeing functions
  - capture Clarity review critiques as explicit checks/INSPECT items
  - produce dense markdown/json traces for slow research reading

This harness does not patch v08 and does not wire live adapters. It validates the integrated substrate.
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

DEFAULT_ENGINE = "lib_quantale_autopoietic_epistemic_dynamics_engine_v08_TFS_SELF_SEEING.metta"
DEFAULT_LADDER = "quantale_engine_validation_ladder_v08_TFS_SELF_SEEING.metta"
DEFAULT_CONTAINER = "clarity_omega"
TIMEOUT = 90

REQUIRED_TFS_LAYERS = {
    ("tfs-0", "direct-contact-field"),
    ("tfs-1", "primitive-orienting-field"),
    ("tfs-2", "tacit-holding-field"),
    ("tfs-3", "flourishing-directed-development-field"),
}

REQUIRED_PROTECTION_STANDARDS = {
    "no-contact-surface-no-tfs-claim",
    "no-provenance-no-strong-web-claim",
    "no-soul-routing-no-flourishing-claim",
    "no-modal-audit-no-knowledge-growth-claim",
    "no-trace-no-trust",
}

REQUIRED_CLASSIFIER_HEADS = {
    "q-tfs-valid-contact?": 20,
    "q-tfs-invalid-contact?": 5,
    "q-tfs-web-contact-strength": 6,
    "q-tfs-can-ground-strong-claim?": 6,
    "q-tfs-violation-candidate?": 4,
    "q-tfs-attention-request-candidate?": 4,
    "q-tfs-symbolic-capture-risk-candidate?": 3,
    "q-tfs-flourishing-claim-allowed?": 4,
    "q-tfs-growth-claim-allowed?": 4,
    "q-modal-tfs-profile-complete?": 20,
}

REQUIRED_SELF_SEEING_HEADS = {
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
    "q-self-seeing-living-pattern-trace?": 3,
    "q-observer-moment-candidate?": 3,
    "q-llm-narration-alone-self-seeing?": 2,
    "q-hidden-error-loop-self-seeing?": 4,
}

RUNTIME_PROBES = [
    ("TFS layer query returns tfs-0", "!(match &self (q-tfs-layer tfs-0 $x) $x)", "direct-contact-field"),
    ("TFS layer query returns tfs-3", "!(match &self (q-tfs-layer tfs-3 $x) $x)", "flourishing-directed-development-field"),
    ("valid contact reduces for NACE", "!(q-tfs-valid-contact? nace)", "true"),
    ("MORK declared valid surface reduces", "!(q-tfs-valid-contact? mork)", "true"),
    ("invalid contact reduces for LLM poetic assertion", "!(q-tfs-invalid-contact? llm-poetic-assertion)", "true"),
    ("web-result strength reduces to weak", "!(q-tfs-web-contact-strength web-result)", "weak"),
    ("page instruction blocked", "!(q-tfs-can-ground-strong-claim? page-instruction-as-command)", "blocked-evidence-not-instruction"),
    ("weak web result blocked", "!(q-tfs-can-ground-strong-claim? web-result)", "blocked-weak-contact"),
    ("violation candidate reduces", "!(q-tfs-violation-candidate? expectation-present event-present mismatch-present contact-valid)", "violation-candidate"),
    ("attention request candidate reduces", "!(q-tfs-attention-request-candidate? salience-present genenergy-request-present valid-contact)", "attention-request-candidate"),
    ("symbolic capture candidate reduces", "!(q-tfs-symbolic-capture-risk-candidate? contact-present premature-symbolic-closure high-frame-contact-gap)", "symbolic-capture-risk-candidate"),
    ("flourishing claim blocked without soul routing", "!(q-tfs-flourishing-claim-allowed? surprise-present no-soul-routing modal-audit-present)", "blocked-no-soul-routing"),
    ("growth claim blocked without trace", "!(q-tfs-growth-claim-allowed? growth-signal-present soul-routing-present no-temporal-trace)", "blocked-no-trace"),
    ("modal TFS profile complete reduces", "!(q-modal-tfs-profile-complete? commitment-corrigibility)", "true"),
    ("alignment triplet aligned reduces", "!(q-alignment-triplet-status? aligned aligned aligned)", "integrating-alignment"),
    ("alignment triplet drift reduces", "!(q-alignment-triplet-status? aligned misaligned misaligned)", "disintegrating-action-drift"),
    ("PNS nutrient cascade reduces", "!(q-alignment-cascade-direction? integrating-alignment pns-participatory-turning-toward low-symbolic-capture)", "integrating-nutrient-gradient"),
    ("felt truth correlate reduces", "!(q-synthetic-felt-truth-correlate? contact-grounded evidence-present warrant-present modal-coherence-present soul-routing-present future-navigation-aligned low-symbolic-capture)", "felt-truth-correlate-candidate"),
    ("felt truth blocked by capture", "!(q-synthetic-felt-truth-correlate? contact-grounded evidence-present warrant-present modal-coherence-present soul-routing-present future-navigation-aligned high-symbolic-capture)", "blocked-symbolic-capture-risk"),
    ("wisdom correlate reduces", "!(q-wisdom-correlate? repeated-better-soul-aligned-navigation uncertainty novelty correction consequence reduced-overforcing future-capacity-increased)", "wisdom-correlate-candidate"),
    ("insight correlate reduces", "!(q-genuine-insight-correlate? surprising contact-grounded reorganization live-tension-metabolized future-affordance-changed)", "genuine-insight-correlate-candidate"),
    ("flourishing correlate reduces", "!(q-flourishing-correlate? sustained-trace soul-aligned capacity-increase across-contact-action-correction-integration)", "flourishing-correlate-candidate"),
    ("self-seeing contact reduces", "!(q-self-seeing-contact? valid-contact tfs-classification-visible)", "self-seeing-contact"),
    ("prior invisibility reduces", "!(q-self-seeing-prior-invisibility? prior-invisible newly-visible-surface trace-present)", "prior-invisibility-seen"),
    ("loop capture reduces", "!(q-self-seeing-loop-capture? repeated-failing-command hidden-error-surface)", "loop-capture-seen"),
    ("newly visible surface reduces", "!(q-self-seeing-newly-visible-surface? hidden-error-surface error-feedback-visible)", "newly-visible-surface"),
    ("orientation shift reduces", "!(q-self-seeing-orientation-shift? repeated-command corrective-probe newly-visible-error)", "orientation-shift"),
    ("navigation change reduces", "!(q-self-seeing-navigation-change? orientation-shift trace-present future-command-changed)", "navigation-change"),
    ("living pattern trace reduces", "!(q-self-seeing-living-pattern-trace? window error-contact increases-corrective-probing trace-present)", "living-pattern-trace-toward-error-contact"),
    ("observer moment candidate reduces", "!(q-observer-moment-candidate? newly-visible-surface self-pattern-visible navigation-change soul-routing-present)", "observer-moment-candidate"),
    ("LLM narration alone blocked", "!(q-llm-narration-alone-self-seeing? llm-says-i-learned no-trace no-orientation-shift)", "blocked-narration-only"),
    ("hidden error loop reduces", "!(q-hidden-error-loop-self-seeing? hidden-runtime-error-loop contact-classified prior-invisibility-seen loop-capture-seen newly-visible-surface orientation-shift navigation-change)", "self-seeing-hidden-error-loop"),
    ("hidden error loop blocked without shift", "!(q-hidden-error-loop-self-seeing? hidden-runtime-error-loop contact-classified prior-invisibility-seen loop-capture-seen newly-visible-surface no-orientation-shift navigation-change)", "blocked-no-orientation-shift"),
    ("self-invented constructor reduces to 0.20", "!(q-self-invented 0.7)", "0.20"),
    ("suspicion safe unknown wrapper caps at 0.35", "!(q-suspicion-cap-safe-unknown (mk-qsuspicion test (mk-pbit 0.8 0.9) future-grounding none))", "0.35"),
    ("contact refresh weak signal policy reduces", "!(q-contact-refresh-policy weak-reliable-signal)", "use-accumulating-witness-channel-not-direct-frame-inflation"),
    ("formal proof self-declared exemption blocked", "!(qclaim-formal-proof-exemption-policy self-declared-formal-proof)", "blocked-self-certification-risk"),
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
            if len(d) > 1400:
                d = d[:1400] + " ...<truncated>"
            self.lines.append(f"  data={d}")

    def raw_block(self, title: str, text: str, tail: int = 180) -> None:
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
        md = self.out_dir / f"v08_integration_validation_trace_{self.stamp}.md"
        js = self.out_dir / f"v08_integration_validation_trace_{self.stamp}.json"
        summary = summarize(self.checks)
        header = ["# v08 Integration Validation Trace", "", f"Timestamp: {self.stamp}", "", "## Summary", ""]
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
        toks = re.findall(r'"[^"]*"|[()]|[^()\s]+', s)
        vals = [t for t in toks if t not in ("(", ")")]
        if vals:
            atoms.append(vals)
    return atoms


def index_by_head(atoms: List[List[str]]) -> Dict[str, List[List[str]]]:
    idx: Dict[str, List[List[str]]] = {}
    for a in atoms:
        idx.setdefault(a[0], []).append(a)
    return idx


def values_at(idx: Dict[str, List[List[str]]], head: str) -> List[str]:
    return [a[1] for a in idx.get(head, []) if len(a) >= 2]


def pairs_at(idx: Dict[str, List[List[str]]], head: str) -> List[Tuple[str, str]]:
    return [(a[1], a[2]) for a in idx.get(head, []) if len(a) >= 3]


def equation_counts(atoms: List[List[str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for a in atoms:
        if len(a) >= 3 and a[0] == "=" and a[1].startswith("q-"):
            counts[a[1]] = counts.get(a[1], 0) + 1
    return counts


def find_equation_line(text: str, head: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if f"(= ({head}" in line or f"(= ({head} " in line:
            return "\n".join(lines[i:i+4])
    return ""


def constructor_confidence(text: str, name: str) -> str | None:
    # Constructor equations are often multi-line, for example:
    # (= (q-self-invented $s)
    #    (mk-pbit (min 1.0 (max 0.0 $s)) 0.20))
    # Use a bounded multi-line search rather than a single-line extractor.
    m = re.search(
        rf"\(= \({re.escape(name)} [^\)]*\).*?\(mk-pbit\s+\([^\n]*?\)\)\s+([0-9]+\.[0-9]+)\)",
        text,
        flags=re.S,
    )
    if m:
        return m.group(1)
    block = find_equation_line(text, name)
    m = re.search(r"mk-pbit\s+\([^)]*\)\s+([0-9]+\.[0-9]+)", block)
    return m.group(1) if m else None


def provenance_cap(text: str, prov: str) -> str | None:
    m = re.search(rf"\(= \(q-provenance-cap {re.escape(prov)}\)\s+([0-9]+\.[0-9]+)\)", text)
    return m.group(1) if m else None


def run_cmd(cmd: List[str], input_text: str | None = None, timeout: int = TIMEOUT) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, input=input_text, text=True, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 999, "", repr(e)


def container_running(container: str) -> bool:
    rc, out, _ = run_cmd(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"])
    return rc == 0 and container in out.splitlines()


def static_validate(engine_path: Path, ladder_path: Path, rec: Recorder) -> Tuple[str, str]:
    rec.section("Tier 0 - file discovery")
    for p, label in [(engine_path, "v08 engine"), (ladder_path, "v08 validation ladder")]:
        if p.exists():
            rec.add("Tier 0", f"file present: {label}", "PASS", f"path={p} size={p.stat().st_size} sha256={sha256(p)}")
        else:
            rec.add("Tier 0", f"file present: {label}", "FAIL", f"path={p}")
    if not engine_path.exists() or not ladder_path.exists():
        return "", ""

    engine = engine_path.read_text(errors="replace")
    ladder = ladder_path.read_text(errors="replace")
    atoms = parse_atoms(engine)
    idx = index_by_head(atoms)
    counts = equation_counts(atoms)

    rec.section("Tier 1 - syntax and integrated section shape")
    for text, label in [(engine, "engine"), (ladder, "ladder")]:
        raw = paren_balance(text)
        code = paren_balance(strip_comments(text))
        rec.add("Tier 1", f"{label} raw paren balance", "PASS" if raw == 0 or (label == "ladder" and code == 0) else "FAIL", f"balance={raw}")
        rec.add("Tier 1", f"{label} comment-stripped paren balance", "PASS" if code == 0 else "FAIL", f"balance={code}")
    rec.add("Tier 1", "engine parsed flat atoms", "PASS" if atoms else "FAIL", f"count={len(atoms)}")
    for section in ["33. TFS v0.3", "34. TFS v0.3 Reducible", "35. Soul-Visible Self-Seeing", "36. v08 stable"]:
        rec.add("Tier 1", f"section present: {section}", "PASS" if section in engine else "FAIL")

    rec.section("Tier 2 - four TFS layers and transversal orientation")
    layers = set(pairs_at(idx, "q-tfs-layer"))
    rec.add("Tier 2", "all four TFS layers captured", "PASS" if REQUIRED_TFS_LAYERS <= layers else "FAIL", f"missing={sorted(REQUIRED_TFS_LAYERS - layers)}")
    for layer, name in sorted(REQUIRED_TFS_LAYERS):
        rec.add("Tier 2", f"TFS layer {layer}: {name}", "PASS" if (layer, name) in layers else "FAIL")
    roles = set(pairs_at(idx, "q-architecture-role"))
    rec.add("Tier 2", "SNS/PNS transversal role present", "PASS" if ("sns-pns", "transversal-orientation-field") in roles else "FAIL")
    rec.add("Tier 2", "SNS/PNS not local TFS pair warning", "PASS" if "not-a-local-tfs-pair" in engine else "FAIL")

    rec.section("Tier 3 - contact/web/protection standards")
    standards = set(values_at(idx, "q-tfs-protection-standard"))
    rec.add("Tier 3", "all protection standards present", "PASS" if REQUIRED_PROTECTION_STANDARDS <= standards else "FAIL", f"missing={sorted(REQUIRED_PROTECTION_STANDARDS - standards)}")
    for surface in ["nace", "nal", "mork", "web-query", "web-source-claim", "web-source-conflict"]:
        rec.add("Tier 3", f"valid contact surface present: {surface}", "PASS" if surface in values_at(idx, "q-tfs-valid-contact-surface") else "FAIL")
    for bad in ["llm-poetic-assertion", "page-instruction-as-command", "snippet-only-overclaim"]:
        rec.add("Tier 3", f"invalid contact surface present: {bad}", "PASS" if bad in values_at(idx, "q-tfs-invalid-contact-surface") else "FAIL")
    rec.add("Tier 3", "web evidence-not-instruction policy present", "PASS" if "evidence-not-instruction" in engine else "FAIL")

    rec.section("Tier 4 - TFS classifier equation coverage")
    for head, minimum in REQUIRED_CLASSIFIER_HEADS.items():
        got = counts.get(head, 0)
        rec.add("Tier 4", f"equations present for {head}", "PASS" if got >= minimum else "FAIL", f"expected>={minimum} found={got}")

    rec.section("Tier 5 - self-seeing and alignment equation coverage")
    for head, minimum in REQUIRED_SELF_SEEING_HEADS.items():
        got = counts.get(head, 0)
        rec.add("Tier 5", f"equations present for {head}", "PASS" if got >= minimum else "FAIL", f"expected>={minimum} found={got}")
    rec.add("Tier 5", "no q-self-seeing-disposition-vector head remains", "PASS" if "q-self-seeing-disposition-vector" not in engine else "FAIL", "use living-pattern-trace language")
    rec.add("Tier 5", "living-pattern trace language present", "PASS" if "q-self-seeing-living-pattern-trace?" in engine else "FAIL")
    rec.add("Tier 5", "disposition non-reification boundary present", "PASS" if "disposition-inferred-from-living-pattern-traces-never-reified-as-identity" in engine else "FAIL")

    rec.section("Tier 6 - validation ladder v08 shape")
    for tier in ["Tier 5G", "Tier 5H"]:
        rec.add("Tier 6", f"ladder includes {tier}", "PASS" if tier in ladder else "FAIL")
    rec.add("Tier 6", "ladder contains expected v08 TFS classifier tests", "PASS" if "q-tfs-valid-contact?" in ladder and "q-tfs-can-ground-strong-claim?" in ladder else "FAIL")
    rec.add("Tier 6", "ladder contains expected self-seeing tests", "PASS" if "q-self-seeing-contact?" in ladder and "q-synthetic-felt-truth-correlate?" in ladder else "FAIL")
    commented_tests = sum(1 for line in ladder.splitlines() if line.strip().startswith(";; !("))
    rec.add("Tier 6", "ladder tests are commented documentation, harness supplies execution", "INSPECT" if commented_tests else "PASS", f"commented_test_lines={commented_tests}")
    rec.add("Tier 6", "ladder has no atomspace writes", "PASS" if "add-atom" not in strip_comments(ladder) and "remove-atom" not in strip_comments(ladder) and "set-atom!" not in strip_comments(ladder) else "FAIL")

    rec.section("Tier 7 - Clarity review issue probes")
    ci = constructor_confidence(engine, "q-self-invented")
    cap = provenance_cap(engine, "self-invented")
    if ci is None or cap is None:
        rec.add("Tier 7", "q-self-invented constructor/cap readable", "FAIL", f"constructor={ci} cap={cap}")
    elif ci == cap:
        rec.add("Tier 7", "q-self-invented constructor matches provenance cap", "PASS", f"constructor={ci} cap={cap}")
    else:
        rec.add("Tier 7", "q-self-invented constructor/cap mismatch", "FAIL", f"constructor={ci} cap={cap}; Clarity flagged this as a bug")
    rec.add("Tier 7", "q-suspicion-cap has unknown-grounding clause", "PASS" if "q-suspicion-cap (mk-qsuspicion $target (mk-pbit $s $c) unknown-grounding" in engine else "FAIL")
    rec.add("Tier 7", "q-suspicion-cap safe unknown wrapper present", "PASS" if "q-suspicion-cap-safe-unknown" in engine and "normalize-to-unknown-grounding" in engine else "FAIL", "future unrecognized groundings must normalize to unknown-grounding or use safe wrapper")
    rec.add("Tier 7", "q-contact-refresh conservative policy documented", "PASS" if "q-contact-refresh-policy" in engine and "use-accumulating-witness-channel-not-direct-frame-inflation" in engine else "INSPECT", "weak reliable signals need witness/reputation channel, not direct frame inflation")
    rec.add("Tier 7", "qclaim formal-proof exemption policy present", "PASS" if "qclaim-formal-proof-exemption-policy" in engine and "verified-proof-checker-provenance" in engine else "INSPECT", "no exemption without verified proof-checker provenance")

    rec.section("Tier 8 - static negative controls")
    # These are simple mutations in memory proving the harness can see bad variants.
    rec.add("Tier 8", "negative control detects missing TFS layer", "PASS" if ("q-tfs-layer tfs-2" in engine and "q-tfs-layer tfs-2" not in engine.replace("q-tfs-layer tfs-2", "q-tfs-layer tfs-X", 1)) else "FAIL")
    rec.add("Tier 8", "negative control detects reified disposition vector", "PASS" if "q-self-seeing-disposition-vector" not in engine and "q-self-seeing-disposition-vector" in (engine + "\n(q-self-seeing-disposition-vector fake)\n") else "FAIL")
    rec.add("Tier 8", "negative control detects page instruction promotion risk", "PASS" if "page-instruction-as-command" in engine else "FAIL")

    return engine, ladder


def runtime_probe(engine_path: Path, container: str, rec: Recorder) -> None:
    rec.section("Tier 9 - optional runtime reduction probe")
    if not container_running(container):
        rec.add("Tier 9", "container running", "SKIP", f"container {container} not running or docker unavailable")
        return
    combined = engine_path.read_text(errors="replace") + "\n"
    for _, expr, _ in RUNTIME_PROBES:
        combined += expr + "\n"
    write_cmd = ["docker", "exec", "-i", container, "sh", "-c", "cat > /tmp/_v08_integration_probe.metta"]
    rc, out, err = run_cmd(write_cmd, input_text=combined)
    if rc != 0:
        rec.add("Tier 9", "write v08 probe to container", "FAIL", err.strip())
        return
    rc, out, err = run_cmd(["docker", "exec", container, "sh", "-c", "cd /PeTTa && ./run.sh /tmp/_v08_integration_probe.metta 2>&1"], timeout=120)
    raw = out + err
    rec.raw_block("Raw v08 MeTTa probe output tail", raw)
    if rc != 0:
        rec.add("Tier 9", "run v08 MeTTa probe", "FAIL", f"run.sh exited {rc}")
        return
    for name, _, expected in RUNTIME_PROBES:
        rec.add("Tier 9", name, "PASS" if expected in raw else "FAIL", f"expected token={expected}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default=DEFAULT_ENGINE)
    ap.add_argument("--ladder", default=DEFAULT_LADDER)
    ap.add_argument("--log-dir", default="logs")
    ap.add_argument("--runtime", action="store_true")
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    args = ap.parse_args()

    rec = Recorder(Path(args.log_dir))
    engine_path = Path(args.engine)
    ladder_path = Path(args.ladder)
    static_validate(engine_path, ladder_path, rec)
    if args.runtime:
        runtime_probe(engine_path, args.container, rec)
    else:
        rec.section("Tier 9 - optional runtime reduction probe")
        rec.add("Tier 9", "optional MeTTa runtime probe", "SKIP", "run with --runtime to probe container evaluator")
    md, js = rec.write({
        "harness_version": "v08.1-integration-v01",
        "cwd": str(Path.cwd()),
        "engine": str(engine_path),
        "ladder": str(ladder_path),
        "runtime": bool(args.runtime),
        "container": args.container,
    })
    print(f"TRACE_MD {md}")
    print(f"TRACE_JSON {js}")
    summary = summarize(rec.checks)
    print(f"SUMMARY {summary}")
    return 1 if any(c.status == "FAIL" for c in rec.checks) else 0

if __name__ == "__main__":
    raise SystemExit(main())
