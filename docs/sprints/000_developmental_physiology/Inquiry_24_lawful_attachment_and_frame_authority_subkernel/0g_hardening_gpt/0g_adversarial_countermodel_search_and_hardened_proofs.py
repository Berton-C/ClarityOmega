#!/usr/bin/env python3
"""Adversarial countermodel search and first-order proof hardening for 0f.

This program is intentionally bounded to the exact theorem-bearing skeleton of
0f_Inquiry_24_Gate_B_Formal_Signature_and_Gate_C_Finite_Interpretation.md.
It does not survey or import another mathematical architecture.

It performs four jobs:
  1. freezes and hashes the exact source under attack;
  2. verifies the delivered positive Gate C model still passes;
  3. exhaustively searches small propositional abstractions for countermodels;
  4. cross-checks the hardened theorem schemas with PyProver.

The propositional abstractions do not replace the dependent K0-K17 theory.
They are adversarial unit models designed to expose missing premises, theorem
overstatement, and scope gaps before proof-assistant encoding.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import product
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

try:
    from pyprover import Prop, proves
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PyProver is required for proof hardening: {exc}")

ROOT = Path("/mnt/data")
TARGET = ROOT / "0f_Inquiry_24_Gate_B_Formal_Signature_and_Gate_C_Finite_Interpretation.md"
ALT_TARGET = ROOT / "0f_Inquiry_24_Gate_B_Formal_Kernel_Signature_and_Gate_C_Finite_Interpretation.md"
BASELINE_CHECKER = ROOT / "0f_gate_c_finite_model_check.py"
REPORT = ROOT / "0g_Adversarial_Countermodel_and_Proof_Hardening_Report.txt"
JSON_REPORT = ROOT / "0g_Adversarial_Countermodel_and_Proof_Hardening_Report.json"


def file_sha256(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def baseline_check() -> Tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(BASELINE_CHECKER)],
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


Assignment = Dict[str, bool]
Constraint = Callable[[Assignment], bool]


@dataclass(frozen=True)
class SearchResult:
    name: str
    category: str
    variables: Tuple[str, ...]
    model: Optional[Assignment]
    expected: str
    significance: str
    hardening: str

    @property
    def found(self) -> bool:
        return self.model is not None


def find_minimal_model(
    variables: Sequence[str],
    constraints: Iterable[Constraint],
    violation: Constraint,
) -> Optional[Assignment]:
    """Find a minimum-true finite Boolean countermodel, deterministic by order."""
    variables = tuple(variables)
    candidates: List[Assignment] = []
    for bits in product((False, True), repeat=len(variables)):
        a = dict(zip(variables, bits))
        if all(c(a) for c in constraints) and violation(a):
            candidates.append(a)
    if not candidates:
        return None
    candidates.sort(key=lambda a: (sum(a.values()), tuple(a[v] for v in variables)))
    return candidates[0]


def cm_branching_commit() -> SearchResult:
    vars_ = (
        "enabled_pre", "wf_tau1", "wf_tau2", "commit_tau1", "commit_tau2",
        "post1_has_e", "post2_has_e", "second_enabled_1", "second_enabled_2",
        "different_successors",
    )
    constraints = [
        lambda a: a["enabled_pre"],
        lambda a: (not a["commit_tau1"]) or (a["enabled_pre"] and a["wf_tau1"]),
        lambda a: (not a["commit_tau2"]) or (a["enabled_pre"] and a["wf_tau2"]),
        lambda a: (not a["commit_tau1"]) or a["post1_has_e"],
        lambda a: (not a["commit_tau2"]) or a["post2_has_e"],
        lambda a: (not a["post1_has_e"]) or (not a["second_enabled_1"]),
        lambda a: (not a["post2_has_e"]) or (not a["second_enabled_2"]),
    ]
    violation = lambda a: all([
        a["commit_tau1"], a["commit_tau2"], a["wf_tau1"], a["wf_tau2"],
        a["different_successors"],
    ])
    return SearchResult(
        "CM-C10-BRANCHING-COMMIT",
        "direct countermodel to theorem wording",
        vars_,
        find_minimal_model(vars_, constraints, violation),
        "C10 says at most one transition can extend the same pre-cut by event e.",
        "T7 blocks a second sequential commit after e is present, but does not prevent two distinct well-formed transactions from the same pre-state producing two branch successors.",
        "Replace C10 with branch-local atomicity, or add a separate commit-selection/linearity law. Do not force transaction determinism unless the kernel intends to erase genuine action choice.",
    )


def cm_contact_laundering() -> SearchResult:
    vars_ = (
        "generated_datum", "event_tagged_contact", "writer_allowed",
        "contact_record", "direct_contact_provenance", "external_contact_seal",
    )
    constraints = [
        lambda a: a["generated_datum"],
        lambda a: (not a["contact_record"]) or a["event_tagged_contact"],
        lambda a: (not a["contact_record"]) or a["writer_allowed"],
        lambda a: (not a["contact_record"]) or a["direct_contact_provenance"],
    ]
    violation = lambda a: a["contact_record"] and a["direct_contact_provenance"] and not a["external_contact_seal"]
    return SearchResult(
        "CM-K2-CONTACT-LAUNDERING",
        "direct adequacy countermodel / missing primitive",
        vars_,
        find_minimal_model(vars_, constraints, violation),
        "Only actual contact should be able to inhabit direct-contact provenance.",
        "The exact K2/K6/K17 text restricts the writer name and outer constructor, but it does not type direct contact with an unforgeable channel/contact witness. An internally generated datum can be passed to an allowed contact writer in a permissive doctrine.",
        "Add ContactSeal/ContactWitness as a required argument to foundInquiry, recordContact, and recoverContact; derive Contact(e) from committed sealed contact rather than treating an event tag as sufficient evidence.",
    )


def cm_opaque_materiality() -> SearchResult:
    vars_ = (
        "candidate", "witness", "tagged_contact", "outside_selfgen",
        "material_predicate", "doctrine_admits", "anchor_extension",
        "authoritative", "external_contact_seal", "semantically_relevant",
    )
    constraints = [
        lambda a: (not a["authoritative"]) or all([
            a["candidate"], a["witness"], a["tagged_contact"],
            a["outside_selfgen"], a["material_predicate"],
            a["doctrine_admits"], a["anchor_extension"],
        ]),
    ]
    violation = lambda a: a["authoritative"] and (not a["external_contact_seal"] or not a["semantically_relevant"])
    return SearchResult(
        "CM-K0-K11-OPAQUE-MATERIALITY",
        "parameter underdetermination",
        vars_,
        find_minimal_model(vars_, constraints, violation),
        "Authority should cite genuinely later, independent, materially relevant contact.",
        "MaterialTo and AdmitAuthority are primitive Soul-doctrine predicates. Without a doctrine soundness contract and a sealed contact witness, an instance can label irrelevant or internally manufactured material as sufficient.",
        "Introduce WellFormedSoulDoctrine laws: MaterialTo carries a ContactSeal and a relevance witness tied to a named attachment obligation; AdmitAuthority may eliminate only such evidence.",
    )


def cm_anchor_mutation() -> SearchResult:
    vars_ = (
        "old_anchor_present", "patch_same_key_different_value", "append_only_abstract",
        "conflict_free_abstract", "commit", "old_anchor_preserved",
    )
    constraints = [
        lambda a: a["old_anchor_present"],
        lambda a: (not a["commit"]) or (a["append_only_abstract"] and a["conflict_free_abstract"]),
    ]
    violation = lambda a: a["commit"] and a["patch_same_key_different_value"] and not a["old_anchor_preserved"]
    return SearchResult(
        "CM-C2-ABSTRACT-APPEND-ONLY",
        "under-specified predicate model",
        vars_,
        find_minimal_model(vars_, constraints, violation),
        "C2 claims exact preservation of every prior anchor component.",
        "AppendOnlyPatch, ConflictFree, and LocallyTyped are given kinds and prose meanings but not eliminable definitions. A model can interpret the predicates as true while commit mutates an old key.",
        "Make global key preservation an explicit field of WriterPatch/WellFormedTxn: old anchor lookup is definitionally equal in the post-state, and new components require fresh keys or identical values.",
    )


def global_loss_collision() -> SearchResult:
    # Search two frame-indexed states that collapse to the same global Lost bit.
    states = []
    for lost_f1, lost_f2 in product((False, True), repeat=2):
        global_lost = lost_f1 or lost_f2
        states.append(((lost_f1, lost_f2), global_lost))
    model: Optional[Assignment] = None
    for (s1, g1), (s2, g2) in product(states, repeat=2):
        if s1 != s2 and g1 == g2 and s1[0] and s2[0] and s1[1] != s2[1]:
            model = {
                "state_A_lost_in_Fevt": s1[0],
                "state_A_lost_in_Fnet": s1[1],
                "state_B_lost_in_Fevt": s2[0],
                "state_B_lost_in_Fnet": s2[1],
                "same_global_Lost": True,
            }
            break
    return SearchResult(
        "CM-K13-GLOBAL-LOSS-COLLISION",
        "type regression / information-loss countermodel",
        tuple(model.keys()) if model else tuple(),
        model,
        "A distinction may be lost in one frame or translation while available in another.",
        "The named 0f handoff declares LossRecord(d,F,e,...) but then defines Lost(d,e), erasing the frame/translation index. Distinct local-loss states collapse to the same global predicate.",
        "Restore LostIn(d, context, e) and RecoveredIn(d, context, e). Freeze the canonical 0f source by checksum before mechanization.",
    )


def cm_recovery_semantic_gap() -> SearchResult:
    vars_ = ("prior_loss", "recovery_record", "typed_witness", "distinction_available_after")
    constraints = [
        lambda a: (not a["recovery_record"]) or (a["prior_loss"] and a["typed_witness"]),
    ]
    violation = lambda a: a["recovery_record"] and a["typed_witness"] and not a["distinction_available_after"]
    return SearchResult(
        "CM-C5-RECORD-AVAILABILITY-GAP",
        "scope gap in theorem",
        vars_,
        find_minimal_model(vars_, constraints, violation),
        "The prose says reintroduce is availability-restoring.",
        "C5 proves only that every RecoveryRecord stores a witness. No formal AvailableIn relation is linked to the record, so a witnessed record can exist without semantic availability changing.",
        "Add AvailabilityIn(d,context,cut) and define reintroduce as the only constructor that changes unavailable to available, carrying the witness. Then prove the stronger transition theorem.",
    )


def cm_operational_sovereignty() -> SearchResult:
    vars_ = (
        "no_living_question_sort", "no_closure_writer", "carrier_controls_action",
        "countercontact_arrives", "carrier_ignores_countercontact",
    )
    constraints = [
        lambda a: a["no_living_question_sort"],
        lambda a: a["no_closure_writer"],
        lambda a: a["countercontact_arrives"],
    ]
    violation = lambda a: a["carrier_controls_action"] and a["carrier_ignores_countercontact"]
    return SearchResult(
        "CM-C8-OPERATIONAL-SOVEREIGNTY",
        "scope counterexample, not a syntactic countermodel",
        vars_,
        find_minimal_model(vars_, constraints, violation),
        "C8 is intended to protect the living inquiry from carrier sovereignty.",
        "The absence of a LivingQuestionClosed sort proves only that explicit exhaustion is unstateable. A runtime can still let carrier content monopolize action and ignore renewed contact while satisfying that syntactic absence.",
        "Reclassify C8 as a signature-audit theorem and add a Gate E operational non-sovereignty obligation: changed contact must remain capable of changing frame standing or action eligibility under controlled interventions.",
    )


def run_countermodel_searches() -> List[SearchResult]:
    return [
        cm_branching_commit(),
        cm_contact_laundering(),
        cm_opaque_materiality(),
        cm_anchor_mutation(),
        global_loss_collision(),
        cm_recovery_semantic_gap(),
        cm_operational_sovereignty(),
    ]


def proof_hardening() -> List[Tuple[str, bool, str]]:
    """Prove the hardened propositional cores with PyProver."""
    results: List[Tuple[str, bool, str]] = []

    Authority = Prop("Authority")
    Guard = Prop("Guard")
    Later = Prop("Later")
    Material = Prop("Material")
    Outside = Prop("OutsideSelfGen")
    ClosureOnly = Prop("ClosureOnly")
    ExternalBasis = Later & Material & Outside

    ok = proves(
        [Authority >> Guard, Guard >> ExternalBasis, ClosureOnly >> ~ExternalBasis],
        ClosureOnly >> ~Authority,
    )
    results.append(("H-C1 no authority from closure-only basis", ok,
                    "Authority→Guard; Guard→later∧material∧outside-selfgen; closure-only excludes that basis."))

    DirectProv = Prop("DirectContactProv")
    Seal = Prop("ContactSeal")
    Generated = Prop("Generated")
    ok = proves([DirectProv >> Seal, Generated >> ~Seal], Generated >> ~DirectProv)
    results.append(("H-C4 sealed direct-contact provenance", ok,
                    "Direct-contact provenance entails a seal; generated material cannot carry the seal."))

    Commit = Prop("Commit")
    PostHasEvent = Prop("PostHasEvent")
    EnabledPost = Prop("EnabledPost")
    SecondSequentialCommit = Prop("SecondSequentialCommit")
    ok = proves(
        [Commit >> PostHasEvent, PostHasEvent >> ~EnabledPost, SecondSequentialCommit >> EnabledPost],
        Commit >> ~SecondSequentialCommit,
    )
    results.append(("H-C10* branch-local no sequential recommit", ok,
                    "A commit puts e in the branch post-cut; enabled then fails; a sequential second commit would require enabled."))

    CommitA = Prop("CommitA")
    PreserveAnchor = Prop("PreserveAnchor")
    PatchWF = Prop("PatchWF")
    ok = proves([CommitA >> PatchWF, PatchWF >> PreserveAnchor], CommitA >> PreserveAnchor)
    results.append(("H-C2 explicit anchor preservation", ok,
                    "Well-formed patch is strengthened to contain a proof that every old anchor key/value is preserved."))

    CommitH = Prop("CommitH")
    PreserveHistory = Prop("PreserveHistory")
    HistoryPatchWF = Prop("HistoryPatchWF")
    ok = proves([CommitH >> HistoryPatchWF, HistoryPatchWF >> PreserveHistory], CommitH >> PreserveHistory)
    results.append(("H-C3 immutable historical inclusion", ok,
                    "Well-formed historical patch contains append-only inclusion; commit cannot remove or replace old records."))

    Recovery = Prop("Recovery")
    Witness = Prop("ReintroWitness")
    AvailableAfter = Prop("AvailableAfter")
    ReintroduceTransition = Prop("ReintroduceTransition")
    ok = proves(
        [AvailableAfter >> ReintroduceTransition, ReintroduceTransition >> Recovery,
         Recovery >> Witness],
        AvailableAfter >> Witness,
    )
    results.append(("H-C5 stronger availability recovery theorem", ok,
                    "Availability-after-loss factors through the sole reintroduce transition, whose recovery record carries a witness."))

    Durable = Prop("Durable")
    Authoritative = Prop("Authoritative")
    CandidateOrProbe = Prop("CandidateOrProbe")
    ok = proves([Durable >> Authoritative, Authoritative >> CandidateOrProbe],
                Durable >> CandidateOrProbe)
    results.append(("H-C7 lifecycle non-collapse", ok,
                    "Durability contains authority evidence; authority contains prior candidate-or-probe standing."))

    JointUse = Prop("JointUse")
    LocalCompat = Prop("LocalCompatibility")
    RetainedTension = Prop("RetainedTension")
    ok = proves([JointUse >> (LocalCompat | RetainedTension)],
                JointUse >> (LocalCompat | RetainedTension))
    results.append(("H-C9 scoped joint-use witness", ok,
                    "The sealed joint-use derivation exposes either local compatibility or an explicit retained-tension witness."))

    Reorg = Prop("ReorganizationEvidence")
    Exercised = Prop("ExercisedReach")
    ReturnedContact = Prop("ReturnedContact")
    Consequence = Prop("ConsequenceUptake")
    ok = proves([Reorg >> (Exercised & ReturnedContact & Consequence)],
                Reorg >> ReturnedContact)
    results.append(("H-K14 retrospective bite", ok,
                    "Reorganization evidence contains exercised reach, returned contact, and consequence uptake—not predicted reach alone."))

    Authority2 = Prop("Authority2")
    MaterialSeal = Prop("MaterialContactSeal")
    SemanticRelevance = Prop("SemanticRelevance")
    Outside2 = Prop("OutsideSelfGeneration")
    ok = proves([Authority2 >> (MaterialSeal & SemanticRelevance & Outside2)],
                Authority2 >> (MaterialSeal & Outside2))
    results.append(("H-K0/K11 doctrine soundness projection", ok,
                    "A well-formed doctrine may admit authority only from sealed, semantically relevant, independent contact."))

    return results


def hardened_no_countermodel_checks() -> List[Tuple[str, bool]]:
    """Bounded model checks showing selected hardening laws close their attacks."""
    checks: List[Tuple[str, bool]] = []

    # Contact laundering becomes impossible.
    vars_ = ("generated", "record", "direct", "seal")
    constraints = [
        lambda a: a["generated"],
        lambda a: (not a["record"]) or (a["direct"] and a["seal"]),
        lambda a: (not a["generated"]) or (not a["seal"]),
    ]
    attack = lambda a: a["record"] and a["direct"]
    checks.append(("sealed contact blocks laundering", find_minimal_model(vars_, constraints, attack) is None))

    # Explicit anchor preservation closes the abstract-predicate model.
    vars_ = ("commit", "wf", "preserve")
    constraints = [
        lambda a: (not a["commit"]) or a["wf"],
        lambda a: (not a["wf"]) or a["preserve"],
    ]
    attack = lambda a: a["commit"] and not a["preserve"]
    checks.append(("typed patch closes anchor mutation", find_minimal_model(vars_, constraints, attack) is None))

    # Material authority requires all three evidence conditions.
    vars_ = ("authority", "seal", "relevant", "outside")
    constraints = [lambda a: (not a["authority"]) or (a["seal"] and a["relevant"] and a["outside"])]
    attack = lambda a: a["authority"] and (not a["seal"] or not a["relevant"] or not a["outside"])
    checks.append(("doctrine contract closes opaque materiality", find_minimal_model(vars_, constraints, attack) is None))

    # Availability restoration requires a witness.
    vars_ = ("available", "transition", "recovery", "witness")
    constraints = [
        lambda a: (not a["available"]) or a["transition"],
        lambda a: (not a["transition"]) or a["recovery"],
        lambda a: (not a["recovery"]) or a["witness"],
    ]
    attack = lambda a: a["available"] and not a["witness"]
    checks.append(("availability transition closes recovery gap", find_minimal_model(vars_, constraints, attack) is None))

    return checks


def source_drift_findings() -> Dict[str, object]:
    target_text = TARGET.read_text(encoding="utf-8")
    alt_text = ALT_TARGET.read_text(encoding="utf-8") if ALT_TARGET.exists() else ""
    return {
        "target_sha256": file_sha256(TARGET),
        "alternative_sha256": file_sha256(ALT_TARGET) if ALT_TARGET.exists() else None,
        "same_bytes": target_text == alt_text,
        "target_has_global_lost": "\\operatorname{Lost}(d,e)" in target_text,
        "target_has_context_lost": "\\operatorname{LostIn}(d," in target_text,
        "alternative_has_context_lost": "\\operatorname{LostIn}(d," in alt_text,
        "target_lines": target_text.count("\n") + 1,
        "alternative_lines": alt_text.count("\n") + 1 if alt_text else 0,
    }


def render_report(
    baseline_ok: bool,
    baseline_output: str,
    drift: Mapping[str, object],
    cms: Sequence[SearchResult],
    proofs: Sequence[Tuple[str, bool, str]],
    hardened_checks: Sequence[Tuple[str, bool]],
) -> str:
    lines: List[str] = []
    lines.append("0g ADVERSARIAL COUNTERMODEL AND PROOF-HARDENING REPORT")
    lines.append("=" * 72)
    lines.append("")
    lines.append("EXACT TARGET")
    lines.append(f"  file: {TARGET.name}")
    lines.append(f"  sha256: {drift['target_sha256']}")
    lines.append(f"  lines: {drift['target_lines']}")
    lines.append("")
    lines.append("SOURCE IDENTITY AUDIT")
    lines.append(f"  alternate 0f sha256: {drift['alternative_sha256']}")
    lines.append(f"  byte-identical: {drift['same_bytes']}")
    lines.append(f"  named target uses global Lost(d,e): {drift['target_has_global_lost']}")
    lines.append(f"  named target uses LostIn(d,context,e): {drift['target_has_context_lost']}")
    lines.append(f"  alternate target uses LostIn(d,context,e): {drift['alternative_has_context_lost']}")
    lines.append("")
    lines.append("BASELINE POSITIVE MODEL")
    lines.append(f"  pass: {baseline_ok}")
    lines.extend(f"  {line}" for line in baseline_output.splitlines()[:8])
    lines.append("  ...")
    lines.append("")
    lines.append("ADVERSARIAL COUNTERMODELS")
    for cm in cms:
        lines.append(f"\n[{cm.name}] {cm.category}")
        lines.append(f"  found: {cm.found}")
        if cm.model is not None:
            for k, v in cm.model.items():
                lines.append(f"    {k} = {v}")
        lines.append(f"  expected: {cm.expected}")
        lines.append(f"  significance: {cm.significance}")
        lines.append(f"  hardening: {cm.hardening}")
    lines.append("")
    lines.append("PYPROVER HARDENED THEOREM SCHEMAS")
    for name, ok, rationale in proofs:
        lines.append(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        lines.append(f"         {rationale}")
    lines.append("")
    lines.append("BOUNDED POST-HARDENING COUNTERMODEL CHECKS")
    for name, ok in hardened_checks:
        lines.append(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    lines.append("")
    all_proofs = all(ok for _, ok, _ in proofs)
    all_hardened = all(ok for _, ok in hardened_checks)
    lines.append("AGGREGATE")
    lines.append(f"  baseline finite model passes: {baseline_ok}")
    lines.append(f"  adversarial models found: {sum(cm.found for cm in cms)} / {len(cms)}")
    lines.append(f"  hardened theorem schemas proved: {sum(ok for _, ok, _ in proofs)} / {len(proofs)}")
    lines.append(f"  bounded hardening closures pass: {sum(ok for _, ok in hardened_checks)} / {len(hardened_checks)}")
    lines.append(f"  proof-hardened core status: {'PASS' if all_proofs and all_hardened else 'FAIL'}")
    lines.append("  Gate E status: BLOCKED pending adoption of the 0g hardening delta and external Lean/Coq/Agda kernel check.")
    return "\n".join(lines) + "\n"


def main() -> int:
    if not TARGET.exists() or not BASELINE_CHECKER.exists():
        raise SystemExit("Required 0f target/checker missing")

    baseline_ok, baseline_output = baseline_check()
    drift = source_drift_findings()
    cms = run_countermodel_searches()
    proofs = proof_hardening()
    hardened_checks = hardened_no_countermodel_checks()

    report = render_report(baseline_ok, baseline_output, drift, cms, proofs, hardened_checks)
    REPORT.write_text(report, encoding="utf-8")

    payload = {
        "target": str(TARGET),
        "drift": dict(drift),
        "baseline_ok": baseline_ok,
        "countermodels": [
            {
                "name": cm.name,
                "category": cm.category,
                "found": cm.found,
                "model": cm.model,
                "expected": cm.expected,
                "significance": cm.significance,
                "hardening": cm.hardening,
            }
            for cm in cms
        ],
        "proofs": [
            {"name": name, "passed": ok, "rationale": rationale}
            for name, ok, rationale in proofs
        ],
        "hardened_checks": [
            {"name": name, "passed": ok} for name, ok in hardened_checks
        ],
    }
    JSON_REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print(report, end="")
    return 0 if baseline_ok and all(ok for _, ok, _ in proofs) and all(ok for _, ok in hardened_checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
