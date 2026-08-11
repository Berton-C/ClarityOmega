#!/usr/bin/env python3
"""
quantale_v08_5_canonical_integration_harness_v03_1_compact_forensic.py

Robust cold + runtime validation harness for canonical v08.5 alignment-pipeline engine:
  - lib_quantale_autopoietic_epistemic_dynamics_engine_v08_5_ALIGNMENT_PIPELINE_CANONICAL.metta
  - quantale_engine_validation_ladder_v08_5_ALIGNMENT_PIPELINE_CANONICAL.metta

Purpose:
  - verify v08.5 was built from the canonical promotion matrix commitments
  - validate inherited v08.1 TFS/self-seeing reductions remain present
  - validate new v08.5 canonical alignment-pipeline families are present and reducible
  - separate static presence checks, equation coverage, negative controls, and runtime reductions
  - produce JSON and Markdown traces for deep human read before any runtime wiring
  - v03 compact forensic runtime mode records exact probe evidence without embedding full repeated engine stdout in JSON

This harness does not wire adapters, mutate AtomSpace, or modify runtime files.
It only writes a temporary probe file under /tmp in the container when --runtime is used.
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

DEFAULT_ENGINE = "staging/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_5_ALIGNMENT_PIPELINE_CANONICAL.metta"
DEFAULT_LADDER = "staging/quantale_engine_validation_ladder_v08_5_ALIGNMENT_PIPELINE_CANONICAL.metta"
DEFAULT_CONTAINER = "clarity_omega"
TIMEOUT = 120

CANONICAL_GUIDANCE = [
    "soul-sovereignty",
    "alignment-pipeline-not-ontology-factory",
    "generative-amplification",
    "modal-reasoning-first-class",
    "hyperseed-math-as-capacity-amplifier",
    "contactable-surface-data",
    "reflexive-engine-self-application",
    "witness-without-warrant-inflation",
    "temporal-dependency-translation-discipline",
    "proven-substrate-physics",
    "daemon-callable-not-daemon-wired",
    "build-once-harness-hard",
]

PROMOTION_FAMILIES = [
    "contactable-surface-signal-protocol",
    "context-indexed-evidence-records",
    "two-channel-pbit-evidence-profiles",
    "dependency-support-records",
    "quantale-path-propagation-and-aggregation",
    "threshold-stability-and-hysteresis",
    "residual-inverse-threshold-gap-inquiry",
    "weakness-distinction-cost-coarsening-policy",
    "translation-morphism-transport-witnesses",
    "proto-time-and-pbit-temporal-evidence",
    "focus-fringe-intensity-field",
    "attention-gate-width-and-duration",
    "effort-resistance-overforcing-cost",
    "wu-wei-minimal-forcing-control",
    "alignment-path-checks-beyond-fixed-triplets",
    "eaoi-modal-pipe-geometry",
    "tfs-sns-pns-ssi-amplification-crosswalk",
    "generic-affective-orientation-surface",
    "witness-reputation-channel-without-warrant-inflation",
    "knowledge-question-inquiry-network",
    "capability-tool-action-effect-channels",
    "shared-world-intersubjective-support-sets",
    "realness-fulfillment-surprising-fulfillment",
    "reflexive-engine-self-application-and-rewiring-stability",
    "daemon-callable-interface-boundaries",
]

V08_5_SECTIONS = [
    "37. v08.5 canonical alignment pipeline promotion",
    "38. Contactable surface signal protocol",
    "39. Context, dependency, temporal evidence, and translation discipline",
    "40. Two-channel evidence, quantale path, threshold, residual, and weakness math",
    "41. Focus, attention gate, effort, forcing, and wu-wei control",
    "42. Alignment path algebra beyond fixed triplets",
    "43. E/A/O/I modal pipe geometry",
    "44. TFS / SNS-PNS / SSI amplification crosswalk",
    "45. Generic affective-orientation surface",
    "46. Witness-reputation without warrant inflation",
    "47. Knowledge, question, capability, tool, and shared-world surfaces",
    "48. Realness, fulfillment, surprising fulfillment, and future capacity",
    "49. Reflexive engine self-application and rewiring stability",
    "50. Daemon-callable interface boundaries",
    "51. v08.5 integrated pipeline demonstrations and negative controls",
]

# Minimum equation counts for v08.5 heads. Counts are deliberately conservative
# but nontrivial, and should fail if a family is only declared but not reducible.
V08_5_HEAD_MINIMUMS: Dict[str, int] = {
    # Section 38
    "q-contactable-surface?": 2,
    "q-surface-signal-accepted?": 4,
    "q-pipeline-flow-readiness?": 5,
    # Section 39
    "q-context-index-valid?": 3,
    "q-evidence-context-carry?": 3,
    "q-claim-support-status?": 3,
    "q-localized-revision?": 2,
    "q-temporal-evidence-status?": 4,
    "q-temporal-carry?": 3,
    "q-translation-witness-status?": 3,
    # Section 40
    "q-evidence-profile-status?": 4,
    "q-evidence-absence-vs-negation?": 3,
    "q-path-compose-kind?": 5,
    "q-load-bearing-chain-status?": 3,
    "q-threshold-hysteresis-status?": 4,
    "q-residual-threshold-gap?": 3,
    "q-weakness-policy?": 4,
    "q-distinction-cost-status?": 1,
    "q-coarsening-allowed?": 3,
    # Section 41
    "q-focus-fringe-status?": 4,
    "q-attention-gate-status?": 4,
    "q-genenergy-allocation-status?": 4,
    "q-effort-profile?": 4,
    "q-overforcing-risk?": 3,
    "q-wu-wei-control?": 4,
    # Section 42
    "q-alignment-path-status?": 8,
    "q-alignment-path-carry?": 4,
    "q-truthlike-emergence?": 4,
    # Section 43
    "q-modal-pipe-audit?": 12,
    "q-modal-pipe-complete?": 3,
    "q-modal-reasoning-reclaims-llm?": 3,
    # Section 44
    "q-cross-surface-amplification?": 12,
    "q-sns-pns-orientation-quality?": 6,
    "q-self-seeing-amplifies-pipeline?": 3,
    # Section 45
    "q-affective-region?": 9,
    "q-affective-orientation-candidate?": 8,
    "q-affective-channel-a-support?": 3,
    # Section 46
    "q-witness-independence?": 3,
    "q-witness-weight-candidate?": 5,
    "q-witness-salience-promotion?": 3,
    "q-witness-direct-warrant-inflation?": 3,
    # Section 47
    "q-epistemic-belief-profile?": 3,
    "q-question-node-status?": 4,
    "q-tool-affordance-status?": 3,
    "q-shared-world-support?": 4,
    # Section 48
    "q-realness-status?": 4,
    "q-fulfillment-status?": 4,
    "q-surprising-fulfillment?": 3,
    "q-future-capacity-gain?": 3,
    # Section 49
    "q-engine-self-surface?": 4,
    "q-engine-self-application?": 4,
    "q-engine-rewiring-stability?": 5,
    "q-engine-growth-mode?": 3,
    # Section 50
    "q-daemon-callable?": 6,
    "q-adapter-boundary?": 5,
    # Section 51
    "q-v08-5-integrated-pipeline?": 8,
    "q-v08-5-negative-control?": 8,
}

REQUIRED_V08_5_HARNESS_TARGETS = [
    "contactable-surface-signal-reduces",
    "context-indexed-evidence-reduces",
    "two-channel-evidence-reduces",
    "dependency-support-reduces",
    "path-propagation-reduces",
    "threshold-hysteresis-reduces",
    "residual-inquiry-reduces",
    "weakness-policy-reduces",
    "translation-witness-reduces",
    "temporal-evidence-reduces",
    "focus-fringe-reduces",
    "attention-gate-reduces",
    "effort-forcing-reduces",
    "wu-wei-control-reduces",
    "alignment-path-reduces",
    "modal-pipe-reduces",
    "tfs-sns-pns-ssi-crosswalk-reduces",
    "affective-orientation-reduces",
    "witness-reputation-reduces",
    "knowledge-question-tool-shared-world-reduces",
    "realness-fulfillment-reduces",
    "engine-self-application-reduces",
    "daemon-boundaries-reduce",
    "integrated-pipeline-reduces",
    "negative-controls-block",
]

# Runtime probe sets. Users can run all or a subset with --probe-set.
BASE_PROBES = [
    ("base: TFS tfs-0 still reduces", "!(match &self (q-tfs-layer tfs-0 $x) $x)", "direct-contact-field"),
    ("base: TFS tfs-3 still reduces", "!(match &self (q-tfs-layer tfs-3 $x) $x)", "flourishing-directed-development-field"),
    ("base: valid contact NACE", "!(q-tfs-valid-contact? nace)", "true"),
    ("base: invalid LLM poetic assertion", "!(q-tfs-invalid-contact? llm-poetic-assertion)", "true"),
    ("base: growth blocked without trace", "!(q-tfs-growth-claim-allowed? growth-signal-present soul-routing-present no-temporal-trace)", "blocked-no-trace"),
    ("base: self-seeing narration blocked", "!(q-llm-narration-alone-self-seeing? llm-says-i-learned no-trace no-orientation-shift)", "blocked-narration-only"),
]

CORE_PROBES = [
    ("core: contactable surface human-language", "!(q-contactable-surface? human-language)", "true"),
    ("core: contactable surface harness-log", "!(q-contactable-surface? harness-log)", "true"),
    ("core: no-surface blocked", "!(q-contactable-surface? no-surface)", "false"),
    ("core: accepted surface signal", "!(q-surface-signal-accepted? human-language provenance-present context-present)", "true"),
    ("core: narration-only blocked", "!(q-surface-signal-accepted? llm-narration-alone provenance-absent context-absent)", "blocked-narration-only"),
    ("core: full pipeline ready", "!(q-pipeline-flow-readiness? contactable orientation-qualified witness-scoped modal-audited alignment-checked self-visible soul-routed)", "pipeline-ready"),
    ("core: pipeline witness inflation blocked", "!(q-pipeline-flow-readiness? contactable orientation-qualified witness-inflated modal-audited alignment-checked self-visible soul-routed)", "blocked-witness-warrant-inflation"),
    ("core: context index valid", "!(q-context-index-valid? observer surface task-phase time-scope model-assumption)", "true"),
    ("core: context carry needs translation", "!(q-evidence-context-carry? same-claim source-context target-context translation-witness-absent)", "blocked-no-translation-witness"),
    ("core: support withdrawn requires revision", "!(q-claim-support-status? support-present support-withdrawn)", "revision-needed"),
    ("core: localized revision preserves unrelated", "!(q-localized-revision? claim support-withdrawn unrelated-claim)", "unrelated-claim-preserved"),
    ("core: temporal contested", "!(q-temporal-evidence-status? positive-support negative-support)", "temporally-contested"),
    ("core: temporal carry needs support", "!(q-temporal-carry? event-a event-b proto-time-evidence-present support-missing)", "blocked-no-support-record"),
    ("core: translation erasure blocked", "!(q-translation-witness-status? source-context target-context distinction-erased)", "blocked-distinction-erasure"),
]

EVIDENCE_PROBES = [
    ("evidence: paraconsistent profile", "!(q-evidence-profile-status? positive-support negative-support)", "paraconsistent-profile"),
    ("evidence: absence vs negation", "!(q-evidence-absence-vs-negation? absent-evidence)", "absence-of-evidence"),
    ("evidence: negative evidence", "!(q-evidence-absence-vs-negation? negative-evidence)", "evidence-of-absence"),
    ("evidence: sequential path uses q-mul", "!(q-path-compose-kind? sequential)", "use-q-mul"),
    ("evidence: repeated same source not independent", "!(q-path-compose-kind? repeated-same-source)", "not-independent-witness"),
    ("evidence: load-bearing chain requires composition", "!(q-load-bearing-chain-status? load-bearing supports-present)", "chain-composition-required"),
    ("evidence: hysteresis within band holds previous", "!(q-threshold-hysteresis-status? within-band)", "hold-previous-state"),
    ("evidence: oscillation risk blocked", "!(q-threshold-hysteresis-status? rapid-boundary-flip)", "blocked-oscillation-risk"),
    ("evidence: residual evidence needed", "!(q-residual-threshold-gap? current-support target-threshold residual-available)", "additional-evidence-needed"),
    ("evidence: weakness keeps weak signal in fringe", "!(q-weakness-policy? weak-signal low-cost high-possible-benefit)", "keep-in-fringe"),
    ("evidence: coarsen allowed", "!(q-coarsening-allowed? high-distinction-cost low-material-gain soul-risk-absent)", "coarsen-allowed"),
]

ATTENTION_PROBES = [
    ("attention: intensity below threshold is fringe", "!(q-focus-fringe-status? intensity-below-threshold)", "fringe"),
    ("attention: open adequate gate", "!(q-attention-gate-status? gate-open width-adequate duration-adequate)", "attention-channel-open"),
    ("attention: narrow gate", "!(q-attention-gate-status? gate-open width-too-narrow duration-adequate)", "attention-width-insufficient"),
    ("attention: allocate genenergy", "!(q-genenergy-allocation-status? salient contactable audit-ready)", "allocate-genenergy"),
    ("attention: blocked no audit", "!(q-genenergy-allocation-status? salient contactable audit-blocked)", "blocked-no-audit"),
    ("attention: efficient carry", "!(q-effort-profile? low-effort high-carry low-distortion)", "efficient-carry"),
    ("attention: overforced profile", "!(q-effort-profile? high-effort low-carry high-distortion)", "overforced"),
    ("attention: overforcing risk", "!(q-overforcing-risk? high-effort defensive-control low-aperture)", "overforcing-risk"),
    ("attention: wu-wei aligned", "!(q-wu-wei-control? minimal-forcing high-carry soul-aligned)", "wu-wei-aligned"),
    ("attention: overcontrol blocked", "!(q-wu-wei-control? high-forcing low-carry frame-preservation)", "blocked-overcontrol"),
]

ALIGNMENT_MODAL_PROBES = [
    ("alignment: all aligned", "!(q-alignment-path-status? aligned aligned aligned)", "integrating-alignment"),
    ("alignment: accidental landing", "!(q-alignment-path-status? drift drift aligned)", "accidental-landing-not-bankable"),
    ("alignment: carries", "!(q-alignment-path-carry? path-coherent context-carry-present temporal-trace-present)", "alignment-carries"),
    ("alignment: no temporal trace", "!(q-alignment-path-carry? path-coherent context-carry-present temporal-trace-absent)", "blocked-no-temporal-trace"),
    ("alignment: truthlike candidate", "!(q-truthlike-emergence? contact-grounded path-aligned low-capture soul-routed)", "truthlike-alignment-candidate"),
    ("alignment: symbolic capture blocks", "!(q-truthlike-emergence? contact-grounded path-aligned symbolic-capture soul-routed)", "blocked-symbolic-capture"),
    ("modal: E audit ready", "!(q-modal-pipe-audit? E contact-present evidence-profile-present support-present)", "epistemic-audit-ready"),
    ("modal: A audit strain", "!(q-modal-pipe-audit? A contact-present metabolization-impossible continuity-preserved)", "autopoietic-strain"),
    ("modal: O novelty theater blocked", "!(q-modal-pipe-audit? O novelty-present affordance-visible consequence-absent)", "blocked-novelty-theater"),
    ("modal: I tension collapse blocked", "!(q-modal-pipe-audit? I differentiated coherent live-tension-collapsed)", "blocked-tension-collapse"),
    ("modal: pipe complete", "!(q-modal-pipe-complete? epistemic-audit-ready autopoietic-audit-ready open-ended-audit-ready integration-audit-ready)", "modal-pipe-complete"),
    ("modal: reasoning reclaimed", "!(q-modal-reasoning-reclaims-llm? modal-pipe-complete soul-routed)", "reasoning-reclaimed-from-llm"),
]

AMPLIFICATION_AFFECTIVE_PROBES = [
    ("amplification: TFS amplifies E", "!(q-cross-surface-amplification? TFS E contact-grounded-warrant)", "tfs-amplifies-epistemology"),
    ("amplification: SNS-PNS amplifies O", "!(q-cross-surface-amplification? SNS-PNS O orientation-quality-novelty)", "orientation-amplifies-open-ended-intelligence"),
    ("amplification: SSI amplifies I", "!(q-cross-surface-amplification? SSI I self-visible-integration)", "ssi-amplifies-integration"),
    ("orientation: PNS compatible", "!(q-sns-pns-orientation-quality? high-valence moderate-arousal flexible-dominance contact-seeking)", "pns-compatible-orientation"),
    ("orientation: performative positivity risk", "!(q-sns-pns-orientation-quality? high-valence high-arousal high-dominance flattery-marker)", "sns-performative-positivity-risk"),
    ("orientation: distressed contactable", "!(q-sns-pns-orientation-quality? low-valence moderate-arousal preserved-dominance contact-seeking)", "distressed-but-contactable"),
    ("self-seeing: amplifies pipeline", "!(q-self-seeing-amplifies-pipeline? contact-visible orientation-visible audit-visible navigation-visible)", "self-seeing-amplifies-pipeline"),
    ("affective: warm grounded contact", "!(q-affective-region? high-valence low-arousal stable-dominance)", "warm-grounded-contact"),
    ("affective: shutdown risk", "!(q-affective-region? neutral-valence low-arousal low-dominance)", "shutdown-disengagement-risk"),
    ("affective: PNS orientation candidate", "!(q-affective-orientation-candidate? warm-grounded-contact tension-clear contactable)", "pns-orientation-candidate"),
    ("affective: tension vector audit needed", "!(q-affective-orientation-candidate? warm-grounded-contact tension-active contactable)", "needs-tension-vector-audit"),
    ("affective: Channel A support ready", "!(q-affective-channel-a-support? affective-orientation-candidate person-state-candidate modal-audited)", "channel-a-support-ready"),
    ("affective: no affective signal needs LLM semantic read", "!(q-affective-channel-a-support? no-affective-signal person-state-candidate modal-audited)", "needs-llm-semantic-read"),
]

WITNESS_SHARED_PROBES = [
    ("witness: independent", "!(q-witness-independence? source-a source-b distinct-sources)", "independent-witness"),
    ("witness: self-cert blocked", "!(q-witness-independence? self-invented self-invented same-source)", "blocked-self-certification"),
    ("witness: weight candidate", "!(q-witness-weight-candidate? weak-reliable repeated-independent cross-surface low-contradiction)", "witness-weight-candidate"),
    ("witness: not independent blocked", "!(q-witness-weight-candidate? weak-reliable repeated-same-source cross-surface low-contradiction)", "blocked-not-independent"),
    ("witness: direct frame inflation blocked", "!(q-witness-direct-warrant-inflation? weak-reliable-signal)", "blocked-direct-frame-inflation"),
    ("witness: popularity as truth blocked", "!(q-witness-direct-warrant-inflation? popularity-signal)", "blocked-popularity-as-truth"),
    ("knowledge: belief profile", "!(q-epistemic-belief-profile? claim positive-support negative-support support-record)", "belief-profile-ready"),
    ("question: supported inquiry", "!(q-question-node-status? question support-present answer-unknown)", "open-supported-question"),
    ("tool: affordance supported", "!(q-tool-affordance-status? tool action effect-channel-present risk-bounded)", "tool-affordance-supported"),
    ("shared-world: support candidate", "!(q-shared-world-support? claim multiple-agents independent-witness translation-witness-present)", "shared-world-support-candidate"),
    ("shared-world: authority theater blocked", "!(q-shared-world-support? claim authority-source-only independent-witness translation-witness-present)", "blocked-authority-theater"),
]

REALNESS_REFLEXIVE_DAEMON_PROBES = [
    ("realness: supported", "!(q-realness-status? prediction-loss-reduced contact-supported cross-context-carry)", "realness-supported"),
    ("realness: local only", "!(q-realness-status? prediction-loss-reduced contact-supported no-cross-context-carry)", "local-realness-only"),
    ("fulfillment: accidental not bankable", "!(q-fulfillment-status? expectation-met path-drift soul-routed)", "accidental-fulfillment-not-bankable"),
    ("surprising fulfillment candidate", "!(q-surprising-fulfillment? low-prior expectation-met contact-supported future-capacity-increased)", "surprising-fulfillment-candidate"),
    ("future capacity expanded", "!(q-future-capacity-gain? new-notice-capacity new-hold-capacity new-test-capacity new-integrate-capacity)", "future-capacity-expanded"),
    ("engine self-surface rule", "!(q-engine-self-surface? rule)", "true"),
    ("engine sovereign self rule false", "!(q-engine-self-surface? sovereign-self-rule)", "false"),
    ("engine self-application ready", "!(q-engine-self-application? engine-surface contactable modal-audited self-seeing soul-routed)", "engine-self-application-ready"),
    ("engine rewiring candidate", "!(q-engine-rewiring-stability? proposed-change trace-supported harness-supported soul-routed)", "rewiring-stability-candidate"),
    ("engine self-certified rewiring blocked", "!(q-engine-rewiring-stability? self-certified-change trace-supported harness-supported soul-routed)", "blocked-self-certification"),
    ("engine coherent growth", "!(q-engine-growth-mode? new-surface adapter-compatible pipeline-compatible)", "coherent-growth"),
    ("daemon callable pure", "!(q-daemon-callable? contactable-surface-signal pure-reduction no-writer)", "daemon-callable"),
    ("daemon wiring deferred", "!(q-daemon-callable? loop-hook live-runtime writer-needed)", "daemon-wiring-deferred"),
    ("adapter boundary VAD clean", "!(q-adapter-boundary? vad adapter-interface core-math-ready live-wiring-absent)", "adapter-boundary-clean"),
]

INTEGRATED_NEGATIVE_PROBES = [
    ("integrated: routable", "!(q-v08-5-integrated-pipeline? contactable pns-compatible-orientation witness-scoped modal-pipe-complete alignment-carries self-seeing-amplifies-pipeline soul-routed)", "v08-5-pipeline-routable"),
    ("integrated: no contact blocked", "!(q-v08-5-integrated-pipeline? contact-absent pns-compatible-orientation witness-scoped modal-pipe-complete alignment-carries self-seeing-amplifies-pipeline soul-routed)", "blocked-no-contact"),
    ("integrated: sns risk warning", "!(q-v08-5-integrated-pipeline? contactable sns-control-risk witness-scoped modal-pipe-complete alignment-carries self-seeing-amplifies-pipeline soul-routed)", "routed-with-sns-risk-warning"),
    ("integrated: witness inflation blocked", "!(q-v08-5-integrated-pipeline? contactable pns-compatible-orientation witness-inflated modal-pipe-complete alignment-carries self-seeing-amplifies-pipeline soul-routed)", "blocked-witness-inflation"),
    ("integrated: modal incomplete blocked", "!(q-v08-5-integrated-pipeline? contactable pns-compatible-orientation witness-scoped modal-pipe-incomplete alignment-carries self-seeing-amplifies-pipeline soul-routed)", "blocked-modal-incomplete"),
    ("integrated: no soul routing blocked", "!(q-v08-5-integrated-pipeline? contactable pns-compatible-orientation witness-scoped modal-pipe-complete alignment-carries self-seeing-amplifies-pipeline soul-absent)", "blocked-no-soul-routing"),
    ("negative: ontology factory blocked", "!(q-v08-5-negative-control? ontology-factory-drift)", "blocked-ontology-factory"),
    ("negative: LLM authorship blocked", "!(q-v08-5-negative-control? llm-narration-as-reasoning)", "blocked-llm-authorship"),
    ("negative: weak-signal warrant inflation blocked", "!(q-v08-5-negative-control? weak-signal-direct-warrant-inflation)", "blocked-witness-warrant-inflation"),
    ("negative: self-certifying rewiring blocked", "!(q-v08-5-negative-control? self-certifying-engine-rewiring)", "blocked-self-certification"),
    ("negative: reified disposition blocked", "!(q-v08-5-negative-control? reified-disposition-vector)", "blocked-reification"),
    ("negative: daemon wired in core blocked", "!(q-v08-5-negative-control? daemon-wired-in-core)", "blocked-premature-live-wiring"),
]

PROBE_SETS = {
    "base": BASE_PROBES,
    "core": CORE_PROBES,
    "evidence": EVIDENCE_PROBES,
    "attention": ATTENTION_PROBES,
    "modal": ALIGNMENT_MODAL_PROBES,
    "affective": AMPLIFICATION_AFFECTIVE_PROBES,
    "witness": WITNESS_SHARED_PROBES,
    "reflexive": REALNESS_REFLEXIVE_DAEMON_PROBES,
    "negative": INTEGRATED_NEGATIVE_PROBES,
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
    stamp: str = field(default_factory=lambda: dt.datetime.now().strftime("%Y%m%d_%H%M%S"))
    checks: List[Check] = field(default_factory=list)
    lines: List[str] = field(default_factory=list)

    @property
    def log_dir(self) -> Path:
        # Backward-compatible alias used by runtime sidecar writer.
        return self.out_dir

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
            if len(d) > 1600:
                d = d[:1600] + " ...<truncated>"
            self.lines.append(f"  data={d}")

    def raw_block(self, title: str, text: str, tail: int | None = 220) -> None:
        self.lines.append(f"### {title}")
        self.lines.append("```text")
        rows = text.splitlines()
        if tail is not None and len(rows) > tail:
            self.lines.append(f"... showing last {tail} of {len(rows)} lines ...")
            rows = rows[-tail:]
        self.lines.extend(rows)
        self.lines.append("```")

    def full_raw_block(self, title: str, text: str) -> None:
        # Full trace, no tail truncation. This is intentionally verbose because
        # the durable log artifact, not the console, is the source of truth.
        self.raw_block(title, text, tail=None)

    def write(self, meta: Dict[str, Any]) -> Tuple[Path, Path]:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        md = self.out_dir / f"v08_5_canonical_validation_trace_{self.stamp}.md"
        js = self.out_dir / f"v08_5_canonical_validation_trace_{self.stamp}.json"
        summary = summarize(self.checks)
        header = ["# v08.5 Canonical Integration Validation Trace", "", f"Timestamp: {self.stamp}", "", "## Summary", ""]
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


def equation_counts(atoms: List[List[str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for a in atoms:
        if len(a) >= 3 and a[0] == "=" and a[1].startswith("q-"):
            counts[a[1]] = counts.get(a[1], 0) + 1
    return counts


def run_cmd(cmd: List[str], input_text: str | None = None, timeout: int = TIMEOUT) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, input=input_text, text=True, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 999, "", repr(e)


def container_running(container: str) -> bool:
    rc, out, _ = run_cmd(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"])
    return rc == 0 and container in out.splitlines()



# ---------------------------------------------------------------------------
# Forensic runtime-output parsing
# ---------------------------------------------------------------------------

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')

def strip_ansi(t: str | None) -> str:
    return ANSI_RE.sub('', t or '')


def result_section(raw: str) -> List[str]:
    """Return only the actual MeTTa result section for one probe.

    run.sh usually prints three kinds of text: echoed source / metta-runnable,
    the prolog goal, and then the actual result after a caret separator. Older
    harnesses scanned the whole raw output and therefore could pass when the
    expected token appeared in an echoed source line or a different probe. This
    function deliberately reads only the final result segment for a single probe.
    """
    clean = strip_ansi(raw)
    lines = clean.splitlines()
    last_sep = -1
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s and set(s) == {'^'}:
            last_sep = i
    seg = lines[last_sep + 1:] if last_sep >= 0 else lines
    out: List[str] = []
    for ln in seg:
        s = ln.strip()
        if not s:
            continue
        # Preserve explicit true/false tokens as legitimate MeTTa results.
        # v03.2 incorrectly discarded 'true', causing false failures for
        # boolean predicates such as q-tfs-valid-contact? and q-context-index-valid?.
        out.append(s)
    return out


def expression_head(expr: str) -> str:
    m = re.search(r'!\(\s*([^\s()]+)', expr)
    return m.group(1) if m else ""


def is_unreduced(raw: str, expr: str) -> bool:
    head = expression_head(expr)
    if not head:
        return False
    for ln in result_section(raw):
        # PeTTa may render failed reductions as either:
        #   (q-head ...)
        #   (partial q-head (...))
        # Treat both as unreduced/partial because neither is the intended semantic token.
        if head in ln and (ln.strip().startswith('(') or 'partial' in ln):
            return True
    return False


def sha256_text(t: str | None) -> str:
    return hashlib.sha256((t or '').encode('utf-8', errors='replace')).hexdigest()


def tail_text(t: str | None, n: int) -> str:
    clean = strip_ansi(t or '')
    if n <= 0:
        return ''
    return clean[-n:] if len(clean) > n else clean


def token_in_result(raw: str, expected: str) -> bool:
    sec = result_section(raw)
    return any(expected in ln for ln in sec)


def token_in_raw_outside_result(raw: str, expected: str) -> bool:
    clean = strip_ansi(raw)
    sec_text = "\n".join(result_section(raw))
    return expected in clean and expected not in sec_text


def result_text(raw: str) -> str:
    return "\n".join(result_section(raw)).strip()


def section_text(engine: str, start_marker: str, next_marker: str | None = None) -> str:
    start = engine.find(start_marker)
    if start < 0:
        return ""
    end = len(engine)
    if next_marker:
        n = engine.find(next_marker, start + len(start_marker))
        if n >= 0:
            end = n
    return engine[start:end]


def static_validate(engine_path: Path, ladder_path: Path, rec: Recorder) -> Tuple[str, str, Dict[str, int]]:
    rec.section("Tier 0 - File discovery and identity")
    for p, label in [(engine_path, "v08.5 canonical engine"), (ladder_path, "v08.5 canonical validation ladder")]:
        if p.exists():
            rec.add("Tier 0", f"file present: {label}", "PASS", f"path={p} size={p.stat().st_size} sha256={sha256(p)}")
        else:
            rec.add("Tier 0", f"file present: {label}", "FAIL", f"path={p}")
    if not engine_path.exists() or not ladder_path.exists():
        return "", "", {}

    engine = engine_path.read_text(errors="replace")
    ladder = ladder_path.read_text(errors="replace")
    atoms = parse_atoms(engine)
    idx = index_by_head(atoms)
    counts = equation_counts(atoms)

    rec.section("Tier 1 - Syntax, parseability, inherited base, and v08.5 sections")
    for text, label in [(engine, "engine"), (ladder, "ladder")]:
        raw = paren_balance(text)
        code = paren_balance(strip_comments(text))
        raw_ok = raw == 0 or (label == "ladder" and code == 0)
        rec.add("Tier 1", f"{label} raw paren balance", "PASS" if raw_ok else "FAIL", f"balance={raw}")
        rec.add("Tier 1", f"{label} comment-stripped paren balance", "PASS" if code == 0 else "FAIL", f"balance={code}")
    rec.add("Tier 1", "engine parsed flat atoms", "PASS" if len(atoms) > 2500 else "FAIL", f"count={len(atoms)}")
    for section in ["33. TFS v0.3", "34. TFS v0.3 Reducible", "35. Soul-Visible Self-Seeing", "36. v08 stable"]:
        rec.add("Tier 1", f"inherited section present: {section}", "PASS" if section in engine else "FAIL")
    for section in V08_5_SECTIONS:
        rec.add("Tier 1", f"v08.5 section present: {section}", "PASS" if section in engine else "FAIL")

    rec.section("Tier 2 - Canonical guidance and promotion families")
    guidance = set(values_at(idx, "q-v08-5-guidance"))
    missing_guidance = [g for g in CANONICAL_GUIDANCE if g not in guidance]
    rec.add("Tier 2", "all 12 canonical guidance items present", "PASS" if not missing_guidance else "FAIL", f"missing={missing_guidance}")
    families = set(values_at(idx, "q-v08-5-promotion-family"))
    missing_families = [f for f in PROMOTION_FAMILIES if f not in families]
    rec.add("Tier 2", "all 25 canonical promotion families present", "PASS" if not missing_families else "FAIL", f"missing={missing_families}")
    boundaries = set(values_at(idx, "q-v08-5-engine-boundary"))
    for b in ["not-daemon-wired", "adapters-are-consumers-not-hardwired", "pure-primitives-before-writers", "soul-sovereignty-not-engine-sovereignty", "no-ontology-factory", "no-llm-authored-reasoning", "no-witness-warrant-inflation", "no-self-certifying-rewiring", "no-reified-disposition", "no-live-adapter-wiring-in-core"]:
        rec.add("Tier 2", f"boundary present: {b}", "PASS" if b in boundaries else "FAIL")

    rec.section("Tier 3 - Equation coverage for promoted v08.5 families")
    for head, minimum in sorted(V08_5_HEAD_MINIMUMS.items()):
        got = counts.get(head, 0)
        rec.add("Tier 3", f"equations present for {head}", "PASS" if got >= minimum else "FAIL", f"expected>={minimum} found={got}")

    rec.section("Tier 4 - Static semantic guard checks")
    v085 = section_text(engine, ";; 37. v08.5 canonical alignment pipeline promotion")
    rec.add("Tier 4", "v08.5 core is pure: no add-atom in promoted section", "PASS" if "add-atom" not in strip_comments(v085) else "FAIL")
    rec.add("Tier 4", "v08.5 core is pure: no remove-atom in promoted section", "PASS" if "remove-atom" not in strip_comments(v085) else "FAIL")
    rec.add("Tier 4", "v08.5 core is pure: no set-atom! in promoted section", "PASS" if "set-atom!" not in strip_comments(v085) else "FAIL")
    rec.add("Tier 4", "no q-self-seeing-disposition-vector head remains", "PASS" if "q-self-seeing-disposition-vector" not in engine else "FAIL")
    rec.add("Tier 4", "MORK remains declared surface, not live execution", "PASS" if "mork-live-proof" in engine and "adapter-required-not-core" in engine else "FAIL")
    rec.add("Tier 4", "VAD remains adapter-ready, not live lookup", "PASS" if "vad adapter-interface core-math-ready live-wiring-absent" in engine else "FAIL")
    rec.add("Tier 4", "NACE live revision remains adapter-required, not core", "PASS" if "nace-live-revision" in engine and "adapter-required-not-core" in engine else "FAIL")
    rec.add("Tier 4", "witness direct warrant inflation explicitly blocked", "PASS" if "q-witness-direct-warrant-inflation?" in engine and "blocked-direct-frame-inflation" in engine else "FAIL")
    rec.add("Tier 4", "self-certifying engine rewiring explicitly blocked", "PASS" if "self-certified-change" in engine and "blocked-self-certification" in engine else "FAIL")
    rec.add("Tier 4", "E/A/O/I as modal pipe geometry present", "PASS" if all(x in engine for x in ["q-modal-pipe-mode E", "q-modal-pipe-mode A", "q-modal-pipe-mode O", "q-modal-pipe-mode I"]) else "FAIL")

    rec.section("Tier 5 - Ladder shape and harness obligations")
    rec.add("Tier 5", "ladder includes Tier 5J", "PASS" if "Tier 5J" in ladder else "FAIL")
    rec.add("Tier 5", "ladder contains v08.5 canonical guidance checks", "PASS" if "q-v08-5-guidance" in ladder and "generative-amplification" in ladder else "FAIL")
    rec.add("Tier 5", "ladder contains representative promoted family check", "PASS" if "q-v08-5-promotion-family" in ladder else "FAIL")
    ladder_family_hits = sum(1 for fam in PROMOTION_FAMILIES if fam in ladder)
    rec.add("Tier 5", "ladder direct family coverage", "PASS" if ladder_family_hits >= len(PROMOTION_FAMILIES) else "INSPECT", f"direct_family_hits={ladder_family_hits}/{len(PROMOTION_FAMILIES)}; harness covers all families even if ladder has representative examples")
    rec.add("Tier 5", "ladder contains negative controls", "PASS" if "q-v08-5-negative-control?" in ladder and "blocked-llm-authorship" in ladder else "FAIL")
    rec.add("Tier 5", "ladder contains runtime-reduction examples", "PASS" if "q-v08-5-integrated-pipeline?" in ladder and "q-engine-rewiring-stability?" in ladder else "FAIL")
    targets = set(values_at(idx, "q-v08-5-harness-target"))
    missing_targets = [t for t in REQUIRED_V08_5_HARNESS_TARGETS if t not in targets]
    rec.add("Tier 5", "all v08.5 harness targets present", "PASS" if not missing_targets else "FAIL", f"missing={missing_targets}")
    commented_tests = sum(1 for line in ladder.splitlines() if line.strip().startswith(";; !("))
    rec.add("Tier 5", "ladder tests are commented documentation, harness supplies execution", "INSPECT" if commented_tests else "PASS", f"commented_test_lines={commented_tests}")

    rec.section("Tier 6 - Static negative controls against harness blindness")
    mut_missing_guidance = engine.replace("(q-v08-5-guidance generative-amplification)", "", 1)
    rec.add("Tier 6", "negative control detects missing canonical guidance", "PASS" if "generative-amplification" not in set(values_at(index_by_head(parse_atoms(mut_missing_guidance)), "q-v08-5-guidance")) else "FAIL")
    mut_missing_family = engine.replace("(q-v08-5-promotion-family witness-reputation-channel-without-warrant-inflation)", "", 1)
    rec.add("Tier 6", "negative control detects missing promotion family", "PASS" if "witness-reputation-channel-without-warrant-inflation" not in set(values_at(index_by_head(parse_atoms(mut_missing_family)), "q-v08-5-promotion-family")) else "FAIL")
    mut_reified = engine + "\n(q-self-seeing-disposition-vector fake)\n"
    rec.add("Tier 6", "negative control detects reified disposition vector", "PASS" if "q-self-seeing-disposition-vector" in mut_reified and "q-self-seeing-disposition-vector" not in engine else "FAIL")
    mut_live = engine.replace("(= (q-daemon-callable? loop-hook live-runtime writer-needed) daemon-wiring-deferred)", "(= (q-daemon-callable? loop-hook live-runtime writer-needed) daemon-callable)", 1)
    rec.add("Tier 6", "negative control detects daemon live wiring promotion risk", "PASS" if "daemon-wiring-deferred" in engine and "daemon-wiring-deferred" not in mut_live else "FAIL")
    mut_warrant = engine.replace("(= (q-witness-direct-warrant-inflation? weak-reliable-signal) blocked-direct-frame-inflation)", "(= (q-witness-direct-warrant-inflation? weak-reliable-signal) allowed-direct-frame-inflation)", 1)
    rec.add("Tier 6", "negative control detects weak signal warrant inflation mutation", "PASS" if "allowed-direct-frame-inflation" in mut_warrant and "allowed-direct-frame-inflation" not in engine else "FAIL")

    return engine, ladder, counts


def selected_runtime_probes(probe_set: str) -> List[Tuple[str, str, str]]:
    if probe_set == "all":
        out: List[Tuple[str, str, str]] = []
        for key in ["base", "core", "evidence", "attention", "modal", "affective", "witness", "reflexive", "negative"]:
            out.extend(PROBE_SETS[key])
        return out
    if probe_set not in PROBE_SETS:
        raise ValueError(f"unknown probe set {probe_set}; choose all or one of {sorted(PROBE_SETS)}")
    return PROBE_SETS[probe_set]


def selected_runtime_probes(probe_set: str) -> List[Tuple[str, str, str]]:
    if probe_set == "all":
        out: List[Tuple[str, str, str]] = []
        for key in ["base", "core", "evidence", "attention", "modal", "affective", "witness", "reflexive", "negative"]:
            out.extend(PROBE_SETS[key])
        return out
    if probe_set not in PROBE_SETS:
        raise ValueError(f"unknown probe set {probe_set}; choose all or one of {sorted(PROBE_SETS)}")
    return PROBE_SETS[probe_set]


def runtime_probe(engine_path: Path, container: str, probe_set: str, rec: Recorder, stop_on_fail: bool = False, raw_mode: str = 'fail', raw_tail_chars: int = 3000) -> None:
    """Run each runtime probe in isolation and record compact forensic evidence.

    Best-practice sources used:
      - corner_gap_pipeline_harness.py: raw output before verdict, unreduced detection,
        fresh space per call, and import/symbol/reduce distinction.
      - capability_registry_diagnostic.py: combined input written to /tmp and evaluated
        through run.sh, with exact sections and conservative parsing.
      - verify_nace_substrate.py: show substrate value against expected reference.

    v03 improvement beyond v02 and examples:
      - every JSON check carries exact expression, return code, parsed result section,
        unreduced flag, expected-token-in-result flag, expected-token-outside-result flag,
        stdout/stderr hashes, bounded tails, and optional raw sidecar paths.
      - full repeated PeTTa engine echo is not embedded in every JSON record.
    """
    rec.section(f"Tier 7 - Runtime reduction probe set: {probe_set} (v03 compact forensic per-probe)")
    if not container_running(container):
        rec.add("Tier 7", "container running", "SKIP", f"container {container} not running or docker unavailable")
        return

    engine_text = engine_path.read_text(errors="replace")
    engine_hash = hashlib.sha256(engine_text.encode("utf-8", errors="replace")).hexdigest()
    probes = selected_runtime_probes(probe_set)
    raw_dir = rec.log_dir / "raw_probe_outputs"
    if raw_mode in ("fail", "all"):
        raw_dir.mkdir(parents=True, exist_ok=True)
    rec.add("Tier 7", "runtime forensic mode active", "PASS", f"planned_probes={len(probes)} engine_sha256={engine_hash}; each probe is isolated; JSON stores compact evidence; raw_mode={raw_mode}; raw_tail_chars={raw_tail_chars}")

    for i, (name, expr, expected) in enumerate(probes, 1):
        label_slug = re.sub(r'[^A-Za-z0-9_.-]+', '_', name).strip('_')[:80]
        temp_path = f"/tmp/_v08_5_canonical_probe_v02_{i:03d}_{label_slug}.metta"
        script = engine_text + "\n" + expr + "\n"
        write_cmd = ["docker", "exec", "-i", container, "sh", "-c", f"cat > {temp_path}"]
        rcw, outw, errw = run_cmd(write_cmd, input_text=script, timeout=180)
        command = f"cd /PeTTa && ./run.sh {temp_path} 2>&1"
        run_invocation = ["docker", "exec", container, "sh", "-c", command]

        if rcw != 0:
            data = {
                "probe_index": i,
                "expression": expr,
                "expected_token": expected,
                "temp_path": temp_path,
                "write_returncode": rcw,
                "write_stdout_chars": len(outw or ""),
                "write_stderr_chars": len(errw or ""),
                "write_stdout_tail": tail_text(outw, raw_tail_chars),
                "write_stderr_tail": tail_text(errw, raw_tail_chars),
            }
            rec.add("Tier 7", name, "FAIL", "could not write isolated probe script", data)
            if stop_on_fail:
                break
            continue

        rcr, outr, errr = run_cmd(run_invocation, timeout=180)
        raw = (outr or "") + (errr or "")
        sec = result_section(raw)
        unreduced = is_unreduced(raw, expr)
        local_match = token_in_result(raw, expected)
        global_match_outside = token_in_raw_outside_result(raw, expected)
        status = "PASS" if (rcr == 0 and local_match and not unreduced) else "FAIL"
        details = (
            f"expected={expected}; local_result_match={local_match}; "
            f"unreduced={unreduced}; returncode={rcr}; "
            f"raw_contains_expected_outside_result={global_match_outside}"
        )
        raw_sidecar = None
        if raw_mode == "all" or (raw_mode == "fail" and status == "FAIL"):
            sidecar_name = f"probe_{i:03d}_{label_slug}.raw.txt"
            sidecar_path = raw_dir / sidecar_name
            sidecar_path.write_text(strip_ansi(raw), encoding="utf-8")
            raw_sidecar = str(sidecar_path)

        data = {
            "probe_index": i,
            "probe_name": name,
            "expression": expr,
            "expression_head": expression_head(expr),
            "expected_token": expected,
            "actual_result_section": sec,
            "actual_result_text": "\n".join(sec),
            "local_result_match": local_match,
            "unreduced": unreduced,
            "raw_contains_expected_outside_result": global_match_outside,
            "returncode": rcr,
            "temp_path": temp_path,
            "docker_write_command": " ".join(write_cmd[:-1]) + " 'cat > " + temp_path + "'",
            "docker_run_command": " ".join(run_invocation[:-1]) + " '" + command + "'",
            "script_body_lines_only": [expr],
            "script_engine_omitted_from_log": True,
            "script_engine_sha256": engine_hash,
            "actual_result_empty": len(sec) == 0,
            "stdout_chars": len(outr or ""),
            "stderr_chars": len(errr or ""),
            "stdout_sha256": sha256_text(outr),
            "stderr_sha256": sha256_text(errr),
            # Keep normal JSON compact: result section + hashes are primary evidence.
            # Include stdout/stderr tails only for failures or when raw_mode=all.
            "stdout_tail": tail_text(outr, raw_tail_chars) if (status == "FAIL" or raw_mode == "all") else "",
            "stderr_tail": tail_text(errr, raw_tail_chars) if (status == "FAIL" or raw_mode == "all") else "",
            "raw_sidecar_path": raw_sidecar,
        }

        rec.add("Tier 7", name, status, details, data)
        rec.full_raw_block(f"PARSED RESULT SECTION probe {i:03d}: {name}", "\n".join(sec) if sec else "(empty result section)")
        if status == "FAIL":
            rec.full_raw_block(f"STDOUT TAIL probe {i:03d}: {name}", tail_text(outr, raw_tail_chars))
            if errr:
                rec.full_raw_block(f"STDERR TAIL probe {i:03d}: {name}", tail_text(errr, raw_tail_chars))
        if status == "FAIL" and stop_on_fail:
            break


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default=DEFAULT_ENGINE)
    ap.add_argument("--ladder", default=DEFAULT_LADDER)
    ap.add_argument("--log-dir", default="shared_files")
    ap.add_argument("--runtime", action="store_true")
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--probe-set", default="all", choices=["all"] + sorted(PROBE_SETS.keys()), help="Runtime probe subset to run when --runtime is used")
    ap.add_argument("--stop-on-fail", action="store_true", help="Stop runtime probing after the first failing isolated probe")
    ap.add_argument("--raw-mode", default="fail", choices=["none", "fail", "all"], help="Write raw sidecar files for no probes, failed probes, or all probes. JSON stores bounded tails and hashes only.")
    ap.add_argument("--raw-tail-chars", type=int, default=3000, help="Max characters of stripped stdout/stderr tail stored in JSON/Markdown per probe.")
    args = ap.parse_args()

    rec = Recorder(Path(args.log_dir))
    engine_path = Path(args.engine)
    ladder_path = Path(args.ladder)
    static_validate(engine_path, ladder_path, rec)
    # Harness-regression self-check: runtime forensic sidecars require Recorder.log_dir.
    rec.add("Tier 0", "harness recorder exposes log_dir for raw sidecars", "PASS" if hasattr(rec, "log_dir") else "FAIL", f"log_dir={getattr(rec, 'log_dir', None)}")
    if args.runtime:
        runtime_probe(engine_path, args.container, args.probe_set, rec, stop_on_fail=args.stop_on_fail, raw_mode=args.raw_mode, raw_tail_chars=args.raw_tail_chars)
    else:
        rec.section("Tier 7 - Runtime reduction probe")
        rec.add("Tier 7", "optional MeTTa runtime probe", "SKIP", "run with --runtime to probe clarity_omega; use --probe-set for chunks")
    md, js = rec.write({
        "harness_version": "v08.5-canonical-integration-v03.3-compact-forensic",
        "cwd": str(Path.cwd()),
        "engine": str(engine_path),
        "ladder": str(ladder_path),
        "runtime": bool(args.runtime),
        "container": args.container,
        "probe_set": args.probe_set,
        "raw_mode": args.raw_mode,
        "raw_tail_chars": args.raw_tail_chars,
    })
    print(f"TRACE_MD {md}")
    print(f"TRACE_JSON {js}")
    summary = summarize(rec.checks)
    print(f"SUMMARY {summary}")
    return 1 if any(c.status == "FAIL" for c in rec.checks) else 0

if __name__ == "__main__":
    raise SystemExit(main())
