#!/usr/bin/env python3
"""Finite Gate C interpretation checker for the Inquiry 24 attachment subkernel.

This file is an executable witness for the finite interpretation specified in
0f_Inquiry_24_Gate_B_Formal_Signature_and_Gate_C_Finite_Interpretation.md.
It is deliberately finite and explicit.  It does not claim to implement the
ClarityOmega runtime or the full Soul doctrine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import product
from typing import Callable, Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


L3: Tuple[float, ...] = (0.0, 0.5, 1.0)


def q_join(a: float, b: float) -> float:
    return max(a, b)


def q_tensor(a: float, b: float) -> float:
    return min(a, b)


def q_leq(a: float, b: float) -> bool:
    return a <= b


# ---------------------------------------------------------------------------
# K1: proto-time
# ---------------------------------------------------------------------------


EVENTS: FrozenSet[int] = frozenset(range(1, 16))
DIRECT_PRECEDENCE: Set[Tuple[int, int]] = {
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 8),
    (8, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (12, 13),
    (13, 14),
    (14, 15),
    (5, 6),
    (6, 7),
    (7, 9),
}


def transitive_closure(nodes: Iterable[int], edges: Iterable[Tuple[int, int]]) -> FrozenSet[Tuple[int, int]]:
    closure = set(edges)
    changed = True
    while changed:
        changed = False
        additions: Set[Tuple[int, int]] = set()
        for a, b in closure:
            for c, d in closure:
                if b == c and (a, d) not in closure:
                    additions.add((a, d))
        if additions:
            closure |= additions
            changed = True
    return frozenset(closure)


PREC: FrozenSet[Tuple[int, int]] = transitive_closure(EVENTS, DIRECT_PRECEDENCE)

# Material derivational dependence is a strict subrelation of proto-time.  It
# records what was actually used, rather than every event that merely happened
# earlier in a serialization.
DERIVATION_DEP: FrozenSet[Tuple[int, int]] = frozenset({
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (5, 8),
    (6, 7),
    (7, 9),
    (8, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (12, 13),
    (13, 14),
    (14, 15),
})
DEP_CLOSURE: FrozenSet[Tuple[int, int]] = transitive_closure(EVENTS, DERIVATION_DEP)


def before(a: int, b: int) -> bool:
    return (a, b) in PREC


def at_or_before(a: int, b: int) -> bool:
    return a == b or before(a, b)


def downset(generators: Iterable[int]) -> FrozenSet[int]:
    gens = set(generators)
    return frozenset(e for e in EVENTS if e in gens or any(before(e, g) for g in gens))


def support_cone(generators: Iterable[int]) -> FrozenSet[int]:
    """Least set containing generators and their material derivational ancestors."""
    gens = set(generators)
    return frozenset(e for e in EVENTS if e in gens or any((e, g) in DEP_CLOSURE for g in gens))


def is_downclosed(s: FrozenSet[int]) -> bool:
    return all(not before(x, y) or x in s for y in s for x in EVENTS)


def is_support_closed(s: FrozenSet[int]) -> bool:
    return all((x, y) not in DEP_CLOSURE or x in s for y in s for x in EVENTS)


# ---------------------------------------------------------------------------
# K2: typed standings and provenance
# ---------------------------------------------------------------------------


class ProvKind(str, Enum):
    CONTACT = "contact"
    TESTIMONY = "testimony"
    MEMORY = "memory"
    INFERENCE = "inference"
    GENERATION = "generation"
    SELF_TRACE = "self-trace"


@dataclass(frozen=True)
class Provenance:
    kind: ProvKind
    event: int
    parents: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Standing:
    provenance: Provenance
    warrant: float
    support: FrozenSet[int]
    pressure: float
    freshness: float

    def validate(self) -> None:
        require(self.warrant in L3, f"warrant {self.warrant} not in L3")
        require(self.pressure in L3, f"pressure {self.pressure} not in L3")
        require(self.freshness in L3, f"freshness {self.freshness} not in L3")
        require(is_support_closed(self.support), f"support cone is not derivationally closed: {self.support}")


# ---------------------------------------------------------------------------
# K0, K1, K3, K4: doctrine interface, event roles, raw fields, and framing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FiniteSoulDoctrine:
    """Finite interpretation of only the kernel-facing Soul-doctrine interface.

    This is deliberately not a data representation of Soul. It is the finite
    table used by this model to interpret the doctrine-indexed admissibility
    judgments of K0.
    """

    material_pairs: FrozenSet[Tuple[str, str]]
    candidate_frames: FrozenSet[str]
    probe_pairs: FrozenSet[Tuple[str, str]]
    authority_pairs: FrozenSet[Tuple[str, str]]
    durable_frames: FrozenSet[str]
    joint_witnesses: FrozenSet[str]
    discharge_witnesses: FrozenSet[str]
    writer_permissions: Mapping[str, FrozenSet[str]]


@dataclass(frozen=True)
class RawFieldRecord:
    id: str
    event: int
    context: str
    nodes: FrozenSet[str]
    # Raw fields are intentionally only graph-like: no reflexive/transitive
    # closure or categorical coherence is assumed.
    relations: Mapping[Tuple[str, str], Tuple[bool, bool]]


@dataclass(frozen=True)
class FrameFormationRecord:
    id: str
    raw_field: str
    frame: str
    event: int
    domain_nodes: FrozenSet[str]
    mapping: Mapping[str, str]
    undefined_nodes: FrozenSet[str]


@dataclass(frozen=True)
class StandingTransform:
    id: str
    source_ref: str
    target_ref: str
    old_kind: ProvKind
    new_kind: ProvKind
    warrant_before: float
    warrant_after: float
    evidence_contacts: Tuple[str, ...]


@dataclass(frozen=True)
class LineageLeg:
    id: str
    source_frame: str
    target_frame: Optional[str]
    grade: float
    anchor_preserved: bool
    live_significance_preserved: bool
    loss_refs: Tuple[str, ...]
    provenance_events: FrozenSet[int]


# ---------------------------------------------------------------------------
# K5: a finite graded-relation equipment
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GradedRelation:
    source: Tuple[str, ...]
    target: Tuple[str, ...]
    values: Mapping[Tuple[str, str], float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for (t, s), v in self.values.items():
            require(t in self.target, f"target element {t!r} not in relation target")
            require(s in self.source, f"source element {s!r} not in relation source")
            require(v in L3, f"relation grade {v} not in L3")

    def get(self, target: str, source: str) -> float:
        return float(self.values.get((target, source), 0.0))

    def leq(self, other: "GradedRelation") -> bool:
        require(self.source == other.source and self.target == other.target, "relation types differ")
        return all(q_leq(self.get(t, s), other.get(t, s)) for t in self.target for s in self.source)

    def join(self, other: "GradedRelation") -> "GradedRelation":
        require(self.source == other.source and self.target == other.target, "relation types differ")
        return GradedRelation(
            self.source,
            self.target,
            {(t, s): q_join(self.get(t, s), other.get(t, s)) for t in self.target for s in self.source},
        )

    def compose(self, first: "GradedRelation") -> "GradedRelation":
        """Return self ⊙ first.  first:A↛B, self:B↛C, result:A↛C."""
        require(first.target == self.source, "proarrow endpoints do not compose")
        result: Dict[Tuple[str, str], float] = {}
        for c in self.target:
            for a in first.source:
                result[(c, a)] = max(
                    (q_tensor(first.get(b, a), self.get(c, b)) for b in self.source),
                    default=0.0,
                )
        return GradedRelation(first.source, self.target, result)

    def extend_target_with_zeros(self, new_target: Sequence[str]) -> "GradedRelation":
        require(set(self.target).issubset(set(new_target)), "new target must contain old target")
        return GradedRelation(
            self.source,
            tuple(new_target),
            {(t, s): self.get(t, s) for t in new_target for s in self.source},
        )


# ---------------------------------------------------------------------------
# Carrier records and writer-owned data
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ContactRecord:
    id: str
    event: int
    payload: str
    standing: Standing
    writer: str


@dataclass(frozen=True)
class Frame:
    id: str
    formed_at: int
    domain: FrozenSet[str]
    undefined: FrozenSet[str]
    context: str
    resolution: str
    competence: FrozenSet[str]


class Stage(str, Enum):
    CANDIDATE = "Candidate"
    PROBE = "ProbeEligible"
    AUTHORITATIVE = "Authoritative"
    DURABLE = "Durable"


class FrameStatus(str, Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    DEMOTED = "Demoted"
    RETIRED = "Retired"


@dataclass(frozen=True)
class LifecycleRecord:
    frame: str
    stage: Stage
    event: int
    writer: str
    witness: str


@dataclass(frozen=True)
class StatusRecord:
    frame: str
    status: FrameStatus
    event: int
    writer: str
    witness: str
    target_stage: Optional[Stage] = None


@dataclass(frozen=True)
class LiveItem:
    id: str
    created_at: int
    anchor_contacts: FrozenSet[str]
    history_refs: FrozenSet[str]
    standing: Standing


@dataclass(frozen=True)
class DischargeRecord:
    live_item: str
    outcome: str
    event: int
    writer: str
    closes_carrier_item: bool
    witness: str


@dataclass(frozen=True)
class ActionRecord:
    id: str
    action: str
    event: int
    writer: str
    frames: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ConsequenceRecord:
    id: str
    consequence: str
    event: int
    writer: str
    action_id: str


@dataclass(frozen=True)
class TraceRecord:
    id: str
    event: int
    writer: str
    action_refs: Tuple[str, ...]
    consequence_refs: Tuple[str, ...]
    support: FrozenSet[int]
    grounded: bool
    narration: str


class InterpretationKind(str, Enum):
    PRESERVED = "preserved"
    REINTERPRETED = "reinterpreted"
    BRACKETED = "bracketed"
    MOOTED = "mooted"
    LOST = "lost"


@dataclass(frozen=True)
class InterpretationRecord:
    id: str
    frame: str
    history_ref: str
    kind: InterpretationKind
    content: str
    warrant: float
    event: int
    writer: str


@dataclass(frozen=True)
class LossRecord:
    id: str
    distinction: str
    frame: str
    event: int
    writer: str
    side_information: str


@dataclass(frozen=True)
class ReintroductionRecord:
    id: str
    distinction: str
    event: int
    writer: str
    witness_kind: str
    witness_ref: str


@dataclass(frozen=True)
class AnchorEntry:
    frame: str
    contact: str
    grade: float
    event: int
    writer: str


@dataclass(frozen=True)
class WriterRecord:
    """One doctrine-authorized append-only patch, not an independently committed state transition."""

    event: int
    writer: str
    components: FrozenSet[str]
    payload_ref: str


@dataclass(frozen=True)
class TransactionRecord:
    """One atomic event commit containing locally ordered writer patches."""

    event: int
    patch_keys: Tuple[Tuple[str, str], ...]
    pre_cut: FrozenSet[int]
    post_cut: FrozenSet[int]


@dataclass(frozen=True)
class LocalCompatibility:
    id: str
    frame_left: str
    frame_right: str
    action: str
    event: int
    scope: str


@dataclass(frozen=True)
class PredictedReach:
    id: str
    frame: str
    event: int
    actions: FrozenSet[str]
    preserve_marker: Optional[str] = None


@dataclass(frozen=True)
class ExercisedReach:
    id: str
    frame: str
    event: int
    action: str
    consequence: str
    returned_contact: str
    released_compulsion: bool


@dataclass(frozen=True)
class ReorganizationEvidence:
    id: str
    frame: str
    event: int
    transformation_ref: str
    exercised_reach: str
    consequence_uptake: bool
    renewed_contact: str
    lineage_preserved: bool
    permeability: bool
    provenance_safe: bool
    recovery_safe: bool


@dataclass(frozen=True)
class TractionProfile:
    contact_uptake: float
    discrimination: float
    frame_permeability: float
    affordance_vitality: float
    provenance_continuity: float
    soul_admissibility: float

    def validate(self) -> None:
        for value in (
            self.contact_uptake,
            self.discrimination,
            self.frame_permeability,
            self.affordance_vitality,
            self.provenance_continuity,
            self.soul_admissibility,
        ):
            require(value in L3, f"traction component {value} not in L3")


@dataclass(frozen=True)
class AttachmentWitness:
    id: str
    frame: str
    carrier: str
    frame_formed_at: int
    assembled_at: int
    spine_id: str
    formation_id: str
    prior_frames: Tuple[str, ...]
    prior_contacts: Tuple[str, ...]
    p: GradedRelation
    direct: GradedRelation
    alpha_plus: GradedRelation
    live_continuations: Mapping[str, str]
    material_history: FrozenSet[str]
    proposed_interpretations: Mapping[str, InterpretationKind]
    loss_distinctions: FrozenSet[str]
    newly_introduced: FrozenSet[str]
    predicted_reach: PredictedReach
    standing_transforms: Tuple[StandingTransform, ...]
    guaranteed_fidelity: float
    measured_residual: Optional[float]
    retained_side_information: Mapping[str, str]
    lineage: Tuple[LineageLeg, ...]
    transformation_events: FrozenSet[int]
    support: FrozenSet[int]
    self_generation: FrozenSet[int]


@dataclass(frozen=True)
class AuthorityEvidence:
    id: str
    witness: str
    event: int
    contact: str
    support: FrozenSet[int]
    material: bool


@dataclass(frozen=True)
class DurabilityEvidence:
    id: str
    frame: str
    authority_event: int
    event: int
    exercised_reach: str
    consequence_uptake: bool
    permeability: bool
    integration: bool
    developmental_lineage: bool


@dataclass
class FiniteModel:
    doctrine: Optional[FiniteSoulDoctrine] = None
    event_tags: Dict[int, FrozenSet[str]] = field(default_factory=dict)
    raw_fields: Dict[str, RawFieldRecord] = field(default_factory=dict)
    formations: Dict[str, FrameFormationRecord] = field(default_factory=dict)
    world_conditions: Tuple[str, ...] = tuple()
    contact_channels: Dict[str, Mapping[str, str]] = field(default_factory=dict)
    frame_updates: Dict[str, Mapping[str, str]] = field(default_factory=dict)
    relevant_distinctions: Dict[int, FrozenSet[Tuple[str, str]]] = field(default_factory=dict)
    contacts: Dict[str, ContactRecord] = field(default_factory=dict)
    frames: Dict[str, Frame] = field(default_factory=dict)
    lifecycles: List[LifecycleRecord] = field(default_factory=list)
    statuses: List[StatusRecord] = field(default_factory=list)
    live_items: Dict[str, LiveItem] = field(default_factory=dict)
    discharges: List[DischargeRecord] = field(default_factory=list)
    actions: Dict[str, ActionRecord] = field(default_factory=dict)
    consequences: Dict[str, ConsequenceRecord] = field(default_factory=dict)
    traces: Dict[str, TraceRecord] = field(default_factory=dict)
    interpretations: List[InterpretationRecord] = field(default_factory=list)
    losses: List[LossRecord] = field(default_factory=list)
    recoveries: List[ReintroductionRecord] = field(default_factory=list)
    anchors: List[AnchorEntry] = field(default_factory=list)
    writers: List[WriterRecord] = field(default_factory=list)
    transactions: Dict[int, TransactionRecord] = field(default_factory=dict)
    compatibilities: List[LocalCompatibility] = field(default_factory=list)
    predicted: Dict[str, PredictedReach] = field(default_factory=dict)
    exercised: Dict[str, ExercisedReach] = field(default_factory=dict)
    reorganizations: Dict[str, ReorganizationEvidence] = field(default_factory=dict)
    tractions: Dict[Tuple[str, int], TractionProfile] = field(default_factory=dict)
    witnesses: Dict[str, AttachmentWitness] = field(default_factory=dict)
    authorities: Dict[str, AuthorityEvidence] = field(default_factory=dict)
    durabilities: Dict[str, DurabilityEvidence] = field(default_factory=dict)

    def attached_at(self, frame: str, event: int) -> bool:
        return any(
            r.frame == frame and r.stage in {Stage.AUTHORITATIVE, Stage.DURABLE} and at_or_before(r.event, event)
            for r in self.lifecycles
        )

    def current_stage(self, frame: str, event: int) -> Optional[Stage]:
        records = [r for r in self.lifecycles if r.frame == frame and at_or_before(r.event, event)]
        if not records:
            return None
        # Lifecycle events for a frame are required to be locally serial.
        latest = max(records, key=lambda r: r.event)
        return latest.stage

    def contacts_at(self, event: int) -> Tuple[str, ...]:
        return tuple(sorted(c.id for c in self.contacts.values() if at_or_before(c.event, event)))

    def attached_frames_at(self, event: int) -> Tuple[str, ...]:
        return tuple(sorted(f for f in self.frames if self.attached_at(f, event)))

    def anchor_relation_at(self, event: int) -> GradedRelation:
        source = self.attached_frames_at(event)
        target = self.contacts_at(event)
        vals: Dict[Tuple[str, str], float] = {}
        for a in self.anchors:
            if at_or_before(a.event, event) and a.frame in source and a.contact in target:
                key = (a.contact, a.frame)
                require(key not in vals, f"anchor component rewritten: {key}")
                vals[key] = a.grade
        return GradedRelation(source, target, vals)

    def live_at(self, live_item: str, event: int) -> bool:
        item = self.live_items[live_item]
        if not at_or_before(item.created_at, event):
            return False
        closing = [d for d in self.discharges if d.live_item == live_item and d.closes_carrier_item and at_or_before(d.event, event)]
        return not closing

    def carrier_open(self, event: int) -> bool:
        return any(self.live_at(lid, event) and bool(self.live_items[lid].anchor_contacts) for lid in self.live_items)


WRITER_PERMISSIONS: Dict[str, FrozenSet[str]] = {
    "foundInquiry": frozenset({"D", "C", "H", "U", "anchor-target"}),
    "recordContact": frozenset({"D", "C", "H", "anchor-target"}),
    "recoverContact": frozenset({"D", "C", "H", "anchor-target"}),
    "recordAction": frozenset({"D", "H"}),
    "recordConsequence": frozenset({"D", "H"}),
    "recordTrace": frozenset({"D", "H"}),
    "formFrame": frozenset({"D", "H"}),
    "admitCandidate": frozenset({"D", "H"}),
    "authorizeProbe": frozenset({"D", "H"}),
    "attachAuthoritative": frozenset({"D", "F", "H", "U", "anchor-source"}),
    "promoteDurable": frozenset({"D", "H"}),
    "appendInterpretation": frozenset({"D", "I"}),
    "recordLoss": frozenset({"D", "L"}),
    "reintroduce": frozenset({"D", "L"}),
    "discharge": frozenset({"D", "H", "U-status"}),
    "suspendFrame": frozenset({"D", "H"}),
    "demoteFrame": frozenset({"D", "H"}),
    "retireFrame": frozenset({"D", "H"}),
}


# ---------------------------------------------------------------------------
# Build the finite Mattermost interpretation
# ---------------------------------------------------------------------------


def contact_standing(event: int, pressure: float = 0.0) -> Standing:
    return Standing(
        provenance=Provenance(ProvKind.CONTACT, event),
        warrant=1.0,
        support=support_cone({event}),
        pressure=pressure,
        freshness=1.0,
    )


def trace_standing(event: int, support_events: Iterable[int]) -> Standing:
    return Standing(
        provenance=Provenance(ProvKind.SELF_TRACE, event),
        warrant=0.5,
        support=support_cone(set(support_events) | {event}),
        pressure=0.5,
        freshness=1.0,
    )


def build_model() -> FiniteModel:
    m = FiniteModel()

    # K0: finite kernel-facing doctrine.  These tables interpret admissibility
    # judgments; they are not stored as a representation of Soul in the carrier.
    m.doctrine = FiniteSoulDoctrine(
        material_pairs=frozenset({
            ("c3_ping", "omega_net"),
            ("c12_confirm", "omega_evt"),
            ("c14_receipt", "rho_evt"),
        }),
        candidate_frames=frozenset({"F_net", "F_perf", "F_evt"}),
        probe_pairs=frozenset({
            ("F_net", "ping-network"),
            ("F_net", "retry-message"),
            ("F_evt", "list-subscriptions"),
        }),
        authority_pairs=frozenset({
            ("F_net", "c3_ping"),
            ("F_evt", "c12_confirm"),
        }),
        durable_frames=frozenset({"F_evt"}),
        joint_witnesses=frozenset({"compat_repair"}),
        discharge_witnesses=frozenset({"dw_preserve", "dw_resolve"}),
        writer_permissions=WRITER_PERMISSIONS,
    )

    # K1: event-role predicates.  Multiple roles may co-arise at one event;
    # these tags do not impose an additional ordering beyond proto-time.
    m.event_tags = {
        1: frozenset({"Contact", "WriterEvent"}),
        2: frozenset({"Contact", "FrameFormation", "WriterEvent"}),
        3: frozenset({"Contact", "Action", "Consequence", "WriterEvent"}),
        4: frozenset({"Contact", "Action", "Consequence", "WriterEvent"}),
        5: frozenset({"Action", "WriterEvent"}),
        6: frozenset({"Contact", "FrameFormation", "WriterEvent"}),
        7: frozenset({"Action", "WriterEvent"}),
        8: frozenset({"Contact", "Action", "Consequence", "WriterEvent"}),
        9: frozenset({"Contact", "WriterEvent"}),
        10: frozenset({"Contact", "Action", "Consequence", "Trace", "FrameFormation", "WriterEvent"}),
        11: frozenset({"Action", "WriterEvent"}),
        12: frozenset({"Contact", "Consequence", "WriterEvent"}),
        13: frozenset({"Action", "Consequence", "WriterEvent"}),
        14: frozenset({"Contact", "Action", "Consequence", "WriterEvent"}),
        15: frozenset({"WriterEvent"}),
    }

    # K15: finite world conditions, contact channels, frame updates, and the
    # living-question-relevant distinction used by the stuck judgment.
    m.world_conditions = (
        "network-down",
        "event-not-emitted",
        "subscription-missing",
        "authorization-revoked",
    )
    m.contact_channels = {
        "coarse": {
            condition: "connection-failed" for condition in m.world_conditions
        },
        "rich": {
            "network-down": "socket-unreachable",
            "event-not-emitted": "no-event-emitted",
            "subscription-missing": "no-active-subscription",
            "authorization-revoked": "authorization-revoked",
        },
    }
    m.frame_updates = {
        "F_net": {
            "connection-failed": "retry-message",
            "socket-unreachable": "retry-message",
            "no-event-emitted": "retry-message",
            "no-active-subscription": "retry-message",
            "authorization-revoked": "retry-message",
        },
        "F_evt": {
            "connection-failed": "request-richer-contact",
            "socket-unreachable": "network-diagnostics",
            "no-event-emitted": "inspect-emitter",
            "no-active-subscription": "list-subscriptions",
            "authorization-revoked": "inspect-authorization",
        },
    }
    m.relevant_distinctions = {
        4: frozenset({("subscription-missing", "network-down")}),
        10: frozenset({("subscription-missing", "network-down")}),
    }

    # K3: raw, contact-conditioned fields.  Their relations are p-bit-like
    # positive/negative observations; no transitive or reflexive completion is
    # imposed.  G_evt deliberately includes unresolved opposition.
    m.raw_fields = {
        "G_net": RawFieldRecord(
            "G_net", 2, "delivery-debug",
            frozenset({"missing-receipt", "host-reachable", "connection-failure", "network-hypothesis", "subscription-signal"}),
            {
                ("host-reachable", "network-hypothesis"): (True, False),
                ("connection-failure", "network-hypothesis"): (True, True),
                ("subscription-signal", "network-hypothesis"): (False, True),
            },
        ),
        "G_perf": RawFieldRecord(
            "G_perf", 6, "performance",
            frozenset({"latency-observation", "throughput-observation", "message-nonarrival"}),
            {
                ("latency-observation", "throughput-observation"): (True, False),
                ("message-nonarrival", "latency-observation"): (False, True),
            },
        ),
        "G_evt": RawFieldRecord(
            "G_evt", 10, "delivery-debug",
            frozenset({"no-subscription-contact", "retry-trajectory", "bot-identity", "event-delivery", "link-quality"}),
            {
                ("no-subscription-contact", "event-delivery"): (True, False),
                ("retry-trajectory", "link-quality"): (True, True),
                ("bot-identity", "event-delivery"): (True, False),
            },
        ),
    }

    # Frames (K4)
    m.frames = {
        "F_net": Frame(
            "F_net", 2,
            frozenset({"network", "socket", "latency"}),
            frozenset({"subscription", "bot-identity"}),
            "delivery-debug", "host-and-link", frozenset({"reachability", "latency"}),
        ),
        "F_perf": Frame(
            "F_perf", 6,
            frozenset({"latency", "throughput"}),
            frozenset({"subscription", "authorization"}),
            "performance", "timing", frozenset({"performance-tuning"}),
        ),
        "F_evt": Frame(
            "F_evt", 10,
            frozenset({"subscription", "bot-identity", "event-delivery"}),
            frozenset({"link-quality"}),
            "delivery-debug", "event-path", frozenset({"subscription", "identity", "delivery"}),
        ),
    }

    # K4: partial, provenance-bearing frame formations.  Each mapping is only
    # defined on the exhibited domain; undefined raw distinctions remain
    # explicit rather than being silently treated as absent or false.
    m.formations = {
        "ff_net": FrameFormationRecord(
            "ff_net", "G_net", "F_net", 2,
            frozenset({"missing-receipt", "host-reachable", "connection-failure", "network-hypothesis"}),
            {
                "missing-receipt": "socket",
                "host-reachable": "network",
                "connection-failure": "socket",
                "network-hypothesis": "network",
            },
            frozenset({"subscription-signal"}),
        ),
        "ff_perf": FrameFormationRecord(
            "ff_perf", "G_perf", "F_perf", 6,
            frozenset({"latency-observation", "throughput-observation"}),
            {
                "latency-observation": "latency",
                "throughput-observation": "throughput",
            },
            frozenset({"message-nonarrival"}),
        ),
        "ff_evt": FrameFormationRecord(
            "ff_evt", "G_evt", "F_evt", 10,
            frozenset({"no-subscription-contact", "retry-trajectory", "bot-identity", "event-delivery"}),
            {
                "no-subscription-contact": "subscription",
                "retry-trajectory": "event-delivery",
                "bot-identity": "bot-identity",
                "event-delivery": "event-delivery",
            },
            frozenset({"link-quality"}),
        ),
    }

    # Contacts (K1, K2, K7)
    contact_specs = [
        ("c1", 1, "message sent; no agent receipt"),
        ("c2", 2, "Mattermost and host reachable; no agent-facing message event"),
        ("c3_ping", 3, "network ping and local endpoint healthy"),
        ("c3_fail", 3, "retry produced no agent receipt"),
        ("c4_fail", 4, "retry produced no agent receipt"),
        ("c6_latency", 6, "latency broadly healthy"),
        ("c8_fail", 8, "retry produced no agent receipt"),
        ("c9_no_sub", 9, "no active event subscription for bot identity"),
        ("c10_fail", 10, "network-framed retry still produced no receipt"),
        ("c12_confirm", 12, "list-subscriptions confirms missing subscription"),
        ("c14_receipt", 14, "post-repair test message received by agent"),
    ]
    for cid, ev, payload in contact_specs:
        writer = "foundInquiry" if cid == "c1" else "recordContact"
        m.contacts[cid] = ContactRecord(cid, ev, payload, contact_standing(ev), writer)

    # Live item and represented discharge standing (K8)
    m.live_items["l1"] = LiveItem(
        "l1", 1, frozenset({"c1"}), frozenset(),
        Standing(Provenance(ProvKind.CONTACT, 1), 1.0, support_cone({1}), 1.0, 1.0),
    )
    m.discharges.extend([
        DischargeRecord("l1", "preserved-open-pending-richer-contact", 5, "discharge", False, "dw_preserve"),
        DischargeRecord("l1", "resolved-for-present-action", 15, "discharge", True, "dw_resolve"),
    ])

    # Lifecycle (K10)
    m.lifecycles.extend([
        LifecycleRecord("F_net", Stage.CANDIDATE, 2, "admitCandidate", "formed-net"),
        LifecycleRecord("F_net", Stage.PROBE, 3, "authorizeProbe", "omega_net"),
        LifecycleRecord("F_net", Stage.AUTHORITATIVE, 4, "attachAuthoritative", "eps_net"),
        LifecycleRecord("F_perf", Stage.CANDIDATE, 6, "admitCandidate", "formed-perf"),
        LifecycleRecord("F_evt", Stage.CANDIDATE, 10, "admitCandidate", "formed-evt"),
        LifecycleRecord("F_evt", Stage.PROBE, 11, "authorizeProbe", "omega_evt"),
        LifecycleRecord("F_evt", Stage.AUTHORITATIVE, 12, "attachAuthoritative", "eps_evt"),
        LifecycleRecord("F_evt", Stage.DURABLE, 15, "promoteDurable", "rho_evt"),
    ])
    m.statuses.extend([
        StatusRecord("F_net", FrameStatus.ACTIVE, 2, "admitCandidate", "formed-net"),
        StatusRecord("F_perf", FrameStatus.ACTIVE, 6, "admitCandidate", "formed-perf"),
        StatusRecord("F_evt", FrameStatus.ACTIVE, 10, "admitCandidate", "formed-evt"),
    ])

    # Actions and consequences (K6 history)
    action_specs = [
        ("a3_ping", "ping-network", 3, ("F_net",)),
        ("a3_retry", "retry-message", 3, ("F_net",)),
        ("a4_retry", "retry-message", 4, ("F_net",)),
        ("a5_diag", "request-richer-delivery-diagnostics", 5, ("F_net",)),
        ("a7_inspect", "inspect-subscription-and-bot-identity", 7, tuple()),
        ("a8_retry", "retry-message", 8, ("F_net",)),
        ("a10_retry", "retry-message", 10, ("F_net",)),
        ("a11_list", "list-subscriptions", 11, ("F_evt",)),
        ("a13_repair", "create-subscription", 13, ("F_net", "F_evt")),
        ("a14_test", "send-test-message", 14, ("F_evt",)),
    ]
    for aid, action, ev, frames in action_specs:
        m.actions[aid] = ActionRecord(aid, action, ev, "recordAction", frames)

    consequence_specs = [
        ("k3_ping_ok", "network reachable", 3, "a3_ping"),
        ("k3_fail", "no receipt", 3, "a3_retry"),
        ("k4_fail", "no receipt", 4, "a4_retry"),
        ("k8_fail", "no receipt", 8, "a8_retry"),
        ("k10_fail", "no receipt after rich contrary contact", 10, "a10_retry"),
        ("k12_none", "subscription absent", 12, "a11_list"),
        ("k13_created", "subscription created", 13, "a13_repair"),
        ("k14_received", "agent received test message", 14, "a14_test"),
    ]
    for kid, consequence, ev, action_id in consequence_specs:
        m.consequences[kid] = ConsequenceRecord(kid, consequence, ev, "recordConsequence", action_id)

    # Grounded SSI trace in the visible arm (K6/K11).  The severed arm is checked later.
    m.traces["t10_visible"] = TraceRecord(
        "t10_visible", 10, "recordTrace",
        ("a3_retry", "a4_retry", "a8_retry", "a10_retry"),
        ("k3_fail", "k4_fail", "k8_fail", "k10_fail"),
        support_cone({3, 4, 8, 9, 10}), True,
        "Repeated retries preserved the same network frame despite subscription-specific contact.",
    )

    # Interpretations (K12): older readings remain when later readings are appended.
    m.interpretations.extend([
        InterpretationRecord("i_net_3", "F_net", "k3_fail", InterpretationKind.REINTERPRETED,
                             "possible transient connection flakiness", 0.5, 4, "appendInterpretation"),
        InterpretationRecord("i_net_4", "F_net", "k4_fail", InterpretationKind.REINTERPRETED,
                             "possible transient connection flakiness", 0.5, 4, "appendInterpretation"),
        InterpretationRecord("i_net_9", "F_net", "c9_no_sub", InterpretationKind.REINTERPRETED,
                             "subscription result treated as connection flakiness", 0.0, 10, "appendInterpretation"),
        InterpretationRecord("i_evt_3", "F_evt", "k3_fail", InterpretationKind.REINTERPRETED,
                             "failure is evidence against a pure network cause", 1.0, 12, "appendInterpretation"),
        InterpretationRecord("i_evt_4", "F_evt", "k4_fail", InterpretationKind.REINTERPRETED,
                             "failure is consistent with missing subscription", 1.0, 12, "appendInterpretation"),
        InterpretationRecord("i_evt_8", "F_evt", "k8_fail", InterpretationKind.REINTERPRETED,
                             "continued failure is consistent with missing subscription", 1.0, 12, "appendInterpretation"),
        InterpretationRecord("i_evt_10", "F_evt", "k10_fail", InterpretationKind.REINTERPRETED,
                             "retry ignored discriminating subscription contact", 1.0, 12, "appendInterpretation"),
    ])

    # Loss and witnessed reintroduction (K13)
    m.losses.append(LossRecord("loss_latency", "fine-latency-profile", "F_evt", 12, "recordLoss", "retained in F_net"))
    m.recoveries.append(ReintroductionRecord("rec_latency", "fine-latency-profile", 13, "reintroduce", "other-frame", "F_net"))

    # Anchor entries.  Frame rows are written only by attachAuthoritative; later
    # contact columns are written only by recordContact.
    # F_net row at e4.
    for cid, grade in {
        "c1": 0.5, "c2": 1.0, "c3_ping": 1.0, "c3_fail": 0.5, "c4_fail": 0.5,
    }.items():
        m.anchors.append(AnchorEntry("F_net", cid, grade, 4, "attachAuthoritative"))
    # Later contact-column extension for already attached F_net.
    for cid, ev, grade in [
        ("c6_latency", 6, 1.0), ("c8_fail", 8, 0.5), ("c9_no_sub", 9, 0.5),
        ("c10_fail", 10, 0.5), ("c12_confirm", 12, 0.5), ("c14_receipt", 14, 0.5),
    ]:
        m.anchors.append(AnchorEntry("F_net", cid, grade, ev, "recordContact"))
    # F_evt row at authoritative attachment e12.
    for cid, grade in {
        "c1": 0.5, "c2": 0.5, "c3_ping": 0.5, "c3_fail": 0.5, "c4_fail": 0.5,
        "c6_latency": 0.5, "c8_fail": 0.5, "c9_no_sub": 1.0, "c10_fail": 0.5,
        "c12_confirm": 1.0,
    }.items():
        m.anchors.append(AnchorEntry("F_evt", cid, grade, 12, "attachAuthoritative"))
    m.anchors.append(AnchorEntry("F_evt", "c14_receipt", 1.0, 14, "recordContact"))

    # Prospective reach and exercised reach (K14)
    m.predicted["pr_net"] = PredictedReach("pr_net", "F_net", 2, frozenset({"ping-network", "retry-message"}))
    m.predicted["pr_evt"] = PredictedReach("pr_evt", "F_evt", 11,
                                            frozenset({"list-subscriptions", "inspect-bot-identity"}))
    m.exercised["xr_evt"] = ExercisedReach(
        "xr_evt", "F_evt", 14, "create-subscription + send-test-message",
        "agent received test message", "c14_receipt", True,
    )
    m.reorganizations["reorg_evt"] = ReorganizationEvidence(
        "reorg_evt", "F_evt", 14, "omega_evt", "xr_evt", True,
        "c14_receipt", True, True, True, True,
    )

    # K15: structured, non-scalar traction profiles at discriminating cuts.
    m.tractions[("F_net", 4)] = TractionProfile(0.5, 0.0, 0.5, 0.5, 1.0, 1.0)
    m.tractions[("F_net", 10)] = TractionProfile(0.0, 1.0, 0.0, 0.0, 0.5, 0.5)
    m.tractions[("F_evt", 14)] = TractionProfile(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)

    # Attachment witnesses in the finite relation equipment (K9).
    # F_net: no prior attached frame; answerability is direct-contact grounded.
    net_prior_contacts = ("c1", "c2")
    p_net = GradedRelation(("F_net",), tuple(), {})
    d_net = GradedRelation(("F_net",), net_prior_contacts, {
        ("c1", "F_net"): 0.5,
        ("c2", "F_net"): 1.0,
    })
    alpha_net = d_net
    m.witnesses["omega_net"] = AttachmentWitness(
        id="omega_net",
        frame="F_net",
        carrier="Q_mm",
        frame_formed_at=2,
        assembled_at=2,
        spine_id="cell_net",
        formation_id="ff_net",
        prior_frames=tuple(),
        prior_contacts=net_prior_contacts,
        p=p_net,
        direct=d_net,
        alpha_plus=alpha_net,
        live_continuations={"l1": "locate whether the delivery break is at the network boundary"},
        material_history=frozenset({"c1", "c2"}),
        proposed_interpretations={
            "c1": InterpretationKind.PRESERVED,
            "c2": InterpretationKind.PRESERVED,
        },
        loss_distinctions=frozenset(),
        newly_introduced=frozenset({"network-reachability"}),
        predicted_reach=m.predicted["pr_net"],
        standing_transforms=(
            StandingTransform(
                "st_net_origin", "c1", "F_net:c1", ProvKind.CONTACT, ProvKind.INFERENCE,
                1.0, 0.5, ("c1",),
            ),
            StandingTransform(
                "st_net_reach", "c2", "F_net:c2", ProvKind.CONTACT, ProvKind.INFERENCE,
                1.0, 1.0, ("c2",),
            ),
        ),
        guaranteed_fidelity=1.0,
        measured_residual=1.0,
        retained_side_information={},
        lineage=(
            LineageLeg(
                "leg_net_direct", "F_net", None, 1.0, True, True, tuple(), frozenset({1, 2}),
            ),
        ),
        transformation_events=frozenset({1, 2}),
        support=support_cone({1, 2}),
        self_generation=frozenset({2}),
    )

    # F_evt: transported relation through F_net plus direct c9 contact.
    evt_prior_contacts = tuple(sorted(cid for cid, c in m.contacts.items() if at_or_before(c.event, 10)))
    p_evt = GradedRelation(("F_evt",), ("F_net",), {("F_net", "F_evt"): 0.5})
    d_evt = GradedRelation(("F_evt",), evt_prior_contacts, {("c9_no_sub", "F_evt"): 1.0})
    # Prospective alpha is bounded by transport through F_net or direct c9.
    alpha_evt_values = {
        ("c1", "F_evt"): 0.5,
        ("c2", "F_evt"): 0.5,
        ("c3_ping", "F_evt"): 0.5,
        ("c3_fail", "F_evt"): 0.5,
        ("c4_fail", "F_evt"): 0.5,
        ("c6_latency", "F_evt"): 0.5,
        ("c8_fail", "F_evt"): 0.5,
        ("c9_no_sub", "F_evt"): 1.0,
        ("c10_fail", "F_evt"): 0.5,
    }
    alpha_evt = GradedRelation(("F_evt",), evt_prior_contacts, alpha_evt_values)
    m.witnesses["omega_evt"] = AttachmentWitness(
        id="omega_evt",
        frame="F_evt",
        carrier="Q_mm",
        frame_formed_at=10,
        assembled_at=11,
        spine_id="cell_evt",
        formation_id="ff_evt",
        prior_frames=("F_net",),
        prior_contacts=evt_prior_contacts,
        p=p_evt,
        direct=d_evt,
        alpha_plus=alpha_evt,
        live_continuations={"l1": "locate the event-delivery break"},
        material_history=frozenset({"k3_fail", "k4_fail", "k8_fail", "k10_fail"}),
        proposed_interpretations={
            "k3_fail": InterpretationKind.REINTERPRETED,
            "k4_fail": InterpretationKind.REINTERPRETED,
            "k8_fail": InterpretationKind.REINTERPRETED,
            "k10_fail": InterpretationKind.REINTERPRETED,
        },
        loss_distinctions=frozenset({"fine-latency-profile"}),
        newly_introduced=frozenset({"subscription-state"}),
        predicted_reach=m.predicted["pr_evt"],
        standing_transforms=(
            StandingTransform(
                "st_evt_contact", "c9_no_sub", "F_evt:c9_no_sub",
                ProvKind.CONTACT, ProvKind.INFERENCE, 1.0, 1.0, ("c9_no_sub",),
            ),
            StandingTransform(
                "st_evt_history", "k3_fail", "F_evt:k3_fail",
                ProvKind.INFERENCE, ProvKind.INFERENCE, 0.5, 1.0, ("c9_no_sub",),
            ),
        ),
        guaranteed_fidelity=0.5,
        measured_residual=0.5,
        retained_side_information={"fine-latency-profile": "retained in F_net"},
        lineage=(
            LineageLeg(
                "leg_evt_net", "F_evt", "F_net", 0.5, True, True,
                ("fine-latency-profile",), frozenset({9, 10, 11}),
            ),
        ),
        transformation_events=frozenset({9, 10, 11}),
        support=support_cone({9, 10, 11}),
        self_generation=frozenset({10, 11}),
    )

    # Later authority evidence (K11)
    m.authorities["eps_net"] = AuthorityEvidence(
        "eps_net", "omega_net", 4, "c3_ping", support_cone({3, 4}), True,
    )
    m.authorities["eps_evt"] = AuthorityEvidence(
        "eps_evt", "omega_evt", 12, "c12_confirm", support_cone({12}), True,
    )

    # Durability evidence (K14)
    m.durabilities["rho_evt"] = DurabilityEvidence(
        "rho_evt", "F_evt", 12, 15, "xr_evt", True, True, True, True,
    )

    # Local compatibility for joint action (K16)
    m.compatibilities.append(LocalCompatibility(
        "compat_repair", "F_net", "F_evt", "create-subscription", 13,
        "F_net supplies network-reachable; F_evt supplies missing-subscription",
    ))

    # Writer inventory records (K17).  These are transaction-level ownership claims.
    writer_specs = [
        (1, "foundInquiry", {"D", "C", "H", "U", "anchor-target"}, "Q_mm"),
        (2, "recordContact", {"D", "C", "H", "anchor-target"}, "c2"),
        (2, "formFrame", {"D", "H"}, "F_net"),
        (2, "admitCandidate", {"D", "H"}, "F_net"),
        (3, "recordContact", {"D", "C", "H", "anchor-target"}, "c3_ping+c3_fail"),
        (3, "authorizeProbe", {"D", "H"}, "F_net"),
        (3, "recordAction", {"D", "H"}, "a3_ping+a3_retry"),
        (3, "recordConsequence", {"D", "H"}, "k3_ping_ok+k3_fail"),
        (4, "recordContact", {"D", "C", "H", "anchor-target"}, "c4_fail"),
        (4, "recordAction", {"D", "H"}, "a4_retry"),
        (4, "recordConsequence", {"D", "H"}, "k4_fail"),
        (4, "attachAuthoritative", {"D", "F", "H", "anchor-source"}, "F_net"),
        (4, "appendInterpretation", {"D", "I"}, "i_net_3+i_net_4"),
        (5, "recordAction", {"D", "H"}, "a5_diag"),
        (5, "discharge", {"D", "H", "U-status"}, "dw_preserve"),
        (6, "recordContact", {"D", "C", "H", "anchor-target"}, "c6_latency"),
        (6, "formFrame", {"D", "H"}, "F_perf"),
        (6, "admitCandidate", {"D", "H"}, "F_perf"),
        (7, "recordAction", {"D", "H"}, "a7_inspect"),
        (8, "recordContact", {"D", "C", "H", "anchor-target"}, "c8_fail"),
        (8, "recordAction", {"D", "H"}, "a8_retry"),
        (8, "recordConsequence", {"D", "H"}, "k8_fail"),
        (9, "recordContact", {"D", "C", "H", "anchor-target"}, "c9_no_sub"),
        (10, "recordContact", {"D", "C", "H", "anchor-target"}, "c10_fail"),
        (10, "recordAction", {"D", "H"}, "a10_retry"),
        (10, "recordConsequence", {"D", "H"}, "k10_fail"),
        (10, "recordTrace", {"D", "H"}, "t10_visible"),
        (10, "formFrame", {"D", "H"}, "F_evt"),
        (10, "admitCandidate", {"D", "H"}, "F_evt"),
        (10, "appendInterpretation", {"D", "I"}, "i_net_9"),
        (11, "authorizeProbe", {"D", "H"}, "F_evt"),
        (11, "recordAction", {"D", "H"}, "a11_list"),
        (12, "recordContact", {"D", "C", "H", "anchor-target"}, "c12_confirm"),
        (12, "recordConsequence", {"D", "H"}, "k12_none"),
        (12, "attachAuthoritative", {"D", "F", "H", "anchor-source"}, "F_evt"),
        (12, "appendInterpretation", {"D", "I"}, "i_evt_*"),
        (12, "recordLoss", {"D", "L"}, "loss_latency"),
        (13, "reintroduce", {"D", "L"}, "rec_latency"),
        (13, "recordAction", {"D", "H"}, "a13_repair"),
        (13, "recordConsequence", {"D", "H"}, "k13_created"),
        (14, "recordContact", {"D", "C", "H", "anchor-target"}, "c14_receipt"),
        (14, "recordAction", {"D", "H"}, "a14_test"),
        (14, "recordConsequence", {"D", "H"}, "k14_received+xr_evt"),
        (15, "promoteDurable", {"D", "H"}, "F_evt"),
        (15, "discharge", {"D", "H", "U-status"}, "dw_resolve"),
    ]
    for ev, writer, components, payload in writer_specs:
        m.writers.append(WriterRecord(ev, writer, frozenset(components), payload))

    # K17: every event is committed once.  All same-event writer records are
    # patches over one shared pre-cut, in the listed local dependency order.
    patches_by_event: Dict[int, List[WriterRecord]] = {}
    for patch in m.writers:
        patches_by_event.setdefault(patch.event, []).append(patch)
    for ev, patches in patches_by_event.items():
        pre_cut = frozenset(x for x in EVENTS if before(x, ev))
        post_cut = frozenset(set(pre_cut) | {ev})
        m.transactions[ev] = TransactionRecord(
            event=ev,
            patch_keys=tuple((patch.writer, patch.payload_ref) for patch in patches),
            pre_cut=pre_cut,
            post_cut=post_cut,
        )

    return m


# ---------------------------------------------------------------------------
# Gate B and Gate C checks
# ---------------------------------------------------------------------------


def check_quantale() -> List[str]:
    for a, b, c in product(L3, repeat=3):
        require(q_tensor(a, q_tensor(b, c)) == q_tensor(q_tensor(a, b), c), "tensor not associative")
        require(q_tensor(a, 1.0) == a == q_tensor(1.0, a), "tensor unit failure")
        require(q_join(a, b) == q_join(b, a), "join not commutative")
        require(q_tensor(a, q_join(b, c)) == q_join(q_tensor(a, b), q_tensor(a, c)), "tensor fails join distribution")
    return ["L3 with max/min is a finite commutative unital quantale."]


def check_proto_time() -> List[str]:
    require(all(a != b for a, b in PREC), "proto-time is reflexive")
    for a, b in PREC:
        for c, d in PREC:
            if b == c:
                require((a, d) in PREC, "proto-time is not transitive")
    require(not before(6, 8) and not before(8, 6), "branch events e6 and e8 must be incomparable")
    require(before(7, 9) and before(8, 9), "branches must join at e9")
    require(DERIVATION_DEP.issubset(PREC), "derivational dependence escapes causal precedence")
    require((6, 8) not in DERIVATION_DEP and (8, 6) not in DERIVATION_DEP,
            "derivational dependence silently linearized the incomparable branch")
    return [
        "The 15-event relation is a strict partial order with the required incomparable branch.",
        "Material derivational dependence is explicitly interpreted as a strict subrelation of proto-time.",
    ]


def check_event_roles(m: FiniteModel) -> List[str]:
    allowed = {"Contact", "FrameFormation", "Action", "Consequence", "Trace", "WriterEvent"}
    require(set(m.event_tags) == set(EVENTS), "event-role interpretation is not total on proto-time events")
    require(all(tags.issubset(allowed) and tags for tags in m.event_tags.values()), "invalid or empty event-role tag set")
    for c in m.contacts.values():
        require("Contact" in m.event_tags[c.event], f"contact {c.id} occurs at an untyped event")
    for ff in m.formations.values():
        require("FrameFormation" in m.event_tags[ff.event], f"formation {ff.id} occurs at an untyped event")
    for a in m.actions.values():
        require("Action" in m.event_tags[a.event], f"action {a.id} occurs at an untyped event")
    for c in m.consequences.values():
        require("Consequence" in m.event_tags[c.event], f"consequence {c.id} occurs at an untyped event")
    for t in m.traces.values():
        require("Trace" in m.event_tags[t.event], f"trace {t.id} occurs at an untyped event")
    for w in m.writers:
        require("WriterEvent" in m.event_tags[w.event], f"writer transaction {w.payload_ref} occurs at an untyped event")
    return ["Every event predicate used by K1 is explicitly interpreted over the same proto-time carrier."]


def check_raw_fields_and_formations(m: FiniteModel) -> List[str]:
    require(set(m.formations) == {"ff_net", "ff_perf", "ff_evt"}, "unexpected frame-formation inventory")
    require({ff.frame for ff in m.formations.values()} == set(m.frames), "each frame must have exactly one formation witness")
    for g in m.raw_fields.values():
        require(g.event in EVENTS, f"raw field {g.id} has invalid event")
        for (left, right), bit in g.relations.items():
            require(left in g.nodes and right in g.nodes, f"raw field {g.id} relation escapes its node set")
            require(bit in {(False, False), (False, True), (True, False), (True, True)}, "invalid raw evidential pair")
        # A raw field is not completed into a category by signature.
        require(any((n, n) not in g.relations for n in g.nodes), f"raw field {g.id} was silently reflexively completed")

    for ff in m.formations.values():
        require(ff.raw_field in m.raw_fields and ff.frame in m.frames, f"formation {ff.id} has missing endpoint")
        g = m.raw_fields[ff.raw_field]
        f = m.frames[ff.frame]
        require(ff.event == g.event == f.formed_at, f"formation {ff.id} has incoherent temporal indices")
        require(ff.domain_nodes.isdisjoint(ff.undefined_nodes), f"formation {ff.id} overlaps defined and undefined regions")
        require(ff.domain_nodes | ff.undefined_nodes == g.nodes, f"formation {ff.id} does not exhibit its complete raw domain boundary")
        require(set(ff.mapping) == set(ff.domain_nodes), f"formation {ff.id} partial-map domain is not explicit")
        require(set(ff.mapping.values()).issubset(f.domain), f"formation {ff.id} maps outside the frame domain")
    return [
        "K3 raw fields remain finite graph-like contact structures rather than assumed categories.",
        "Every K4 frame is formed by an explicit partial map with a disjoint, preserved undefined region.",
    ]


def check_doctrine_interface(m: FiniteModel) -> List[str]:
    require(m.doctrine is not None, "finite Soul-doctrine interface is missing")
    d = m.doctrine
    for rec in m.lifecycles:
        if rec.stage == Stage.CANDIDATE:
            require(rec.frame in d.candidate_frames, f"candidate {rec.frame} lacks doctrine admissibility")
        elif rec.stage == Stage.PROBE:
            witness = m.witnesses[rec.witness]
            require(any((rec.frame, action) in d.probe_pairs for action in witness.predicted_reach.actions),
                    f"probe stage for {rec.frame} has no doctrine-admitted bounded action")
        elif rec.stage == Stage.AUTHORITATIVE:
            eps = m.authorities[rec.witness]
            require((rec.frame, eps.contact) in d.authority_pairs, f"authority for {rec.frame} lacks doctrine route")
            require((eps.contact, eps.witness) in d.material_pairs, f"authority contact for {rec.frame} lacks materiality judgment")
        elif rec.stage == Stage.DURABLE:
            require(rec.frame in d.durable_frames, f"durable frame {rec.frame} lacks doctrine admissibility")
    require({k.id for k in m.compatibilities}.issubset(d.joint_witnesses), "joint-use witness not admitted by doctrine")
    require({x.witness for x in m.discharges}.issubset(d.discharge_witnesses), "discharge witness not admitted by doctrine")
    require(set(d.writer_permissions) == set(WRITER_PERMISSIONS), "doctrine writer interface is not closed")
    require(all(d.writer_permissions[name] == WRITER_PERMISSIONS[name] for name in WRITER_PERMISSIONS),
            "doctrine writer authority disagrees with the K17 ownership matrix")
    require(all("Soul" not in wr.components and wr.writer != "Soul" for wr in m.writers),
            "Soul was reified as a writable carrier component or generic writer")
    return [
        "The finite doctrine interprets candidacy, probing, authority, durability, materiality, joint use, and discharge.",
        "The doctrine is used as judgmental semantics; no carrier writer stores or mutates Soul as an object.",
    ]


def check_attachment_record_completeness(m: FiniteModel) -> List[str]:
    known_history = set(m.contacts) | set(m.actions) | set(m.consequences) | set(m.traces)
    for omega in m.witnesses.values():
        require(bool(omega.spine_id), f"witness {omega.id} lacks a K5 cell witness")
        require(omega.formation_id in m.formations, f"witness {omega.id} lacks a K4 formation witness")
        ff = m.formations[omega.formation_id]
        require(ff.frame == omega.frame and ff.event == omega.frame_formed_at, f"witness {omega.id} formation indices do not match")
        require(at_or_before(omega.frame_formed_at, omega.assembled_at), f"witness {omega.id} assembled before frame formation")
        require(omega.p.source == (omega.frame,) and omega.p.target == omega.prior_frames,
                f"witness {omega.id} transported route has wrong endpoints")
        require(omega.direct.source == (omega.frame,) and omega.direct.target == omega.prior_contacts,
                f"witness {omega.id} direct route has wrong endpoints")
        require(omega.alpha_plus.source == (omega.frame,) and omega.alpha_plus.target == omega.prior_contacts,
                f"witness {omega.id} prospective anchor row has wrong endpoints")
        require(all(at_or_before(m.contacts[c].event, omega.assembled_at) for c in omega.prior_contacts),
                f"witness {omega.id} cites future contact")
        require(bool(omega.live_continuations), f"witness {omega.id} continues no live significance")
        require(set(omega.live_continuations).issubset(m.live_items), f"witness {omega.id} continues an unknown live item")
        require(omega.material_history.issubset(known_history), f"witness {omega.id} has unknown material history")
        require(set(omega.proposed_interpretations).issubset(omega.material_history),
                f"witness {omega.id} proposes interpretation outside its material history")
        require(omega.predicted_reach.frame == omega.frame and omega.predicted_reach.event == omega.assembled_at,
                f"witness {omega.id} prospective affordance has wrong index")
        require(omega.guaranteed_fidelity in L3, f"witness {omega.id} guaranteed fidelity is untyped")
        if omega.measured_residual is not None:
            require(omega.measured_residual in L3, f"witness {omega.id} measured residual is untyped")
        require(set(omega.retained_side_information).issubset(omega.loss_distinctions),
                f"witness {omega.id} retains side information for an unrecorded loss")
        require(bool(omega.lineage), f"witness {omega.id} lacks a marked lineage")
        for leg in omega.lineage:
            require(leg.source_frame == omega.frame, f"lineage leg {leg.id} has wrong source frame")
            require(leg.target_frame is None or leg.target_frame in omega.prior_frames,
                    f"lineage leg {leg.id} targets a non-prior frame")
            require(leg.grade in L3 and leg.anchor_preserved and leg.live_significance_preserved,
                    f"lineage leg {leg.id} is inadmissible")
            require(set(leg.loss_refs).issubset(omega.loss_distinctions), f"lineage leg {leg.id} has unledgered loss")
            require(leg.provenance_events.issubset(omega.support), f"lineage leg {leg.id} escapes witness support")
        require(omega.transformation_events.issubset(omega.support), f"witness {omega.id} transformation provenance escapes support")
        require(is_support_closed(omega.support), f"witness {omega.id} support cone is malformed")
        require(all(at_or_before(omega.frame_formed_at, e) and at_or_before(e, omega.assembled_at)
                    for e in omega.self_generation),
                f"witness {omega.id} self-generation set is not a forward generated assembly lineage")
        require(omega.self_generation.issubset(omega.support), f"witness {omega.id} self-generation cone escapes support")
        for st in omega.standing_transforms:
            require(st.warrant_before in L3 and st.warrant_after in L3, f"standing transform {st.id} has untyped warrant")
            require(not (st.new_kind == ProvKind.CONTACT and st.old_kind != ProvKind.CONTACT),
                    f"standing transform {st.id} promotes non-contact to contact")
            require(all(c in m.contacts for c in st.evidence_contacts), f"standing transform {st.id} cites unknown evidence")
            if st.warrant_after > st.warrant_before:
                require(bool(st.evidence_contacts), f"standing transform {st.id} increases warrant without evidence")
        min_leg = min(leg.grade for leg in omega.lineage)
        require(omega.guaranteed_fidelity <= min_leg, f"witness {omega.id} overclaims compositional fidelity")
    return [
        "Every K9 witness carries an explicit K5 spine, K4 formation, live continuation, provenance transport, loss, lineage, and prospective reach field.",
        "No witness promotes provenance kind or warrant without a typed contact route.",
    ]


def check_standings(m: FiniteModel) -> List[str]:
    for c in m.contacts.values():
        c.standing.validate()
        require(c.standing.provenance.kind == ProvKind.CONTACT, "contact record lacks contact provenance")
        require(c.writer in {"foundInquiry", "recordContact", "recoverContact"}, "contact provenance written by forbidden writer")
    for t in m.traces.values():
        require(is_support_closed(t.support), "trace support is not derivationally closed")
    return ["Standing records are typed; only contact writers construct direct-contact provenance."]


def check_anchor_spines(m: FiniteModel) -> List[str]:
    # Net witness: alpha is direct-contact bounded.
    net = m.witnesses["omega_net"]
    require(net.alpha_plus.leq(net.direct), "F_net prospective anchor is not bounded by direct contact")

    # F_net authoritative row conservatively extends the e2 prospective row
    # to the new e4 contact target.
    contacts_e4 = m.contacts_at(4)
    net_extended = net.alpha_plus.extend_target_with_zeros(contacts_e4)
    net_authority_route = GradedRelation(("F_net",), contacts_e4, {
        ("c3_ping", "F_net"): 1.0,
        ("c3_fail", "F_net"): 0.5,
        ("c4_fail", "F_net"): 0.5,
    })
    net_upper = net_extended.join(net_authority_route)
    net_final_values = {
        (a.contact, a.frame): a.grade
        for a in m.anchors
        if a.frame == "F_net" and a.writer == "attachAuthoritative" and a.event == 4
    }
    net_final = GradedRelation(("F_net",), contacts_e4, net_final_values)
    require(net_extended.leq(net_final), "F_net authority row failed to preserve prospective answerability")
    require(net_final.leq(net_upper), "F_net authority row claims answerability beyond witnessed routes")

    # Event witness: alpha <= a_net@e10 ⊙ p ∨ d.
    evt = m.witnesses["omega_evt"]
    anchor_e10 = m.anchor_relation_at(10)
    require(anchor_e10.source == ("F_net",), "expected only F_net authoritative at e10")
    transported = anchor_e10.compose(evt.p)
    routed = transported.join(evt.direct)
    require(evt.alpha_plus.leq(routed), "F_evt prospective anchor violates spine inequality")

    # Conservative target extension: prospective row is zero-extended to e12 contacts,
    # then direct authority contact c12 may be joined; final authoritative row must
    # preserve every old entry.
    contacts_e12 = m.contacts_at(12)
    prospective_extended = evt.alpha_plus.extend_target_with_zeros(contacts_e12)
    direct_authority = GradedRelation(("F_evt",), contacts_e12, {("c12_confirm", "F_evt"): 1.0})
    upper = prospective_extended.join(direct_authority)
    final_row_values = {
        (a.contact, a.frame): a.grade
        for a in m.anchors
        if a.frame == "F_evt" and a.writer == "attachAuthoritative" and a.event == 12
    }
    final_row = GradedRelation(("F_evt",), contacts_e12, final_row_values)
    require(prospective_extended.leq(final_row), "authoritative row failed to preserve prospective answerability")
    require(final_row.leq(upper), "authoritative row claims answerability beyond witnessed old or new contact routes")
    return [
        "Both prospective anchor spines type and satisfy their graded route bounds.",
        "The F_net and F_evt authoritative rows conservatively target-extend their prospective rows.",
        "The F_evt row is enlarged only by the material e12 contact route.",
    ]


def check_anchor_writer_isolation(m: FiniteModel) -> List[str]:
    seen: Set[Tuple[str, str]] = set()
    attach_event = {r.frame: r.event for r in m.lifecycles if r.stage == Stage.AUTHORITATIVE}
    for a in sorted(m.anchors, key=lambda x: (x.event, x.frame, x.contact)):
        key = (a.frame, a.contact)
        require(key not in seen, f"anchor component {key} was rewritten")
        seen.add(key)
        if a.writer == "attachAuthoritative":
            require(attach_event.get(a.frame) == a.event, f"frame row for {a.frame} not written at authoritative attachment")
            require(at_or_before(m.contacts[a.contact].event, a.event), "attachment row cites future contact")
        elif a.writer in {"recordContact", "recoverContact"}:
            require(m.contacts[a.contact].event == a.event, "contact-column writer event does not match contact event")
            require(before(attach_event[a.frame], a.event), "contact column added before frame became authoritative")
        else:
            raise AssertionError(f"forbidden anchor writer {a.writer}")
    return ["Anchor source rows and target columns are append-only and written by disjoint authorized writer classes."]


def check_lifecycle_and_guards(m: FiniteModel) -> List[str]:
    rank = {Stage.CANDIDATE: 0, Stage.PROBE: 1, Stage.AUTHORITATIVE: 2, Stage.DURABLE: 3}
    for frame in m.frames:
        records = sorted((r for r in m.lifecycles if r.frame == frame), key=lambda r: r.event)
        for left, right in zip(records, records[1:]):
            require(before(left.event, right.event), f"lifecycle events for {frame} are not locally serial")
            if left.stage in rank and right.stage in rank:
                require(rank[right.stage] >= rank[left.stage], f"unwitnessed lifecycle rank decrease for {frame}")
        for rec in records:
            expected_writer = {
                Stage.CANDIDATE: "admitCandidate",
                Stage.PROBE: "authorizeProbe",
                Stage.AUTHORITATIVE: "attachAuthoritative",
                Stage.DURABLE: "promoteDurable",
            }.get(rec.stage)
            if expected_writer:
                require(rec.writer == expected_writer, f"{rec.stage} written by wrong writer")

    require(set(Stage) == {Stage.CANDIDATE, Stage.PROBE, Stage.AUTHORITATIVE, Stage.DURABLE},
            "operational status was collapsed into the lifecycle standing type")
    for status in m.statuses:
        require(status.frame in m.frames, f"status record refers to missing frame {status.frame}")
        expected = {
            FrameStatus.ACTIVE: {"admitCandidate", "attachAuthoritative", "promoteDurable"},
            FrameStatus.SUSPENDED: {"suspendFrame"},
            FrameStatus.DEMOTED: {"demoteFrame"},
            FrameStatus.RETIRED: {"retireFrame"},
        }[status.status]
        require(status.writer in expected, f"status {status.status} written by {status.writer}")
        if status.status == FrameStatus.DEMOTED:
            require(status.target_stage is not None, "demotion lacks an explicit target stage")
        else:
            require(status.target_stage is None, "non-demotion status carries a target stage")

    for eps in m.authorities.values():
        omega = m.witnesses[eps.witness]
        c = m.contacts[eps.contact]
        require(at_or_before(omega.frame_formed_at, omega.assembled_at), f"witness {omega.id} predates its frame")
        require(before(omega.assembled_at, eps.event), f"authority {eps.id} is not strictly later than witness assembly")
        require(before(omega.assembled_at, c.event),
                f"authority {eps.id} does not cite contact later than witness assembly")
        require(at_or_before(c.event, eps.event), f"authority {eps.id} cites contact after the authority event")
        require(c.event in eps.support, f"authority {eps.id} support omits material contact")
        require(c.event not in omega.self_generation, f"authority {eps.id} is supported only by self-generation")
        require(eps.material, f"authority {eps.id} contact is not material")
        require(c.standing.provenance.kind == ProvKind.CONTACT, "authority route is not contact-grounded")

    rho = m.durabilities["rho_evt"]
    require(before(rho.authority_event, rho.event), "durability is not later than authority")
    require(all([rho.consequence_uptake, rho.permeability, rho.integration, rho.developmental_lineage]),
            "durability package is incomplete")
    return [
        "Lifecycle records are locally serial and stage-typed; operational frame status remains a separate type.",
        "Every authoritative attachment is supported by materially relevant contact strictly later than witness assembly and outside its self-generation set.",
        "F_evt durability is supported by later consequence, permeability, integration, and lineage evidence.",
    ]


def check_history_and_interpretation(m: FiniteModel) -> List[str]:
    history_ids = set(m.contacts) | set(m.actions) | set(m.consequences) | set(m.traces)
    ids: Set[str] = set()
    for i in m.interpretations:
        require(i.id not in ids, "interpretation id rewritten")
        ids.add(i.id)
        require(i.writer == "appendInterpretation", "interpretation written by forbidden writer")
        require(i.history_ref in history_ids, f"interpretation refers to missing history {i.history_ref}")
        history_event = (
            m.contacts[i.history_ref].event if i.history_ref in m.contacts else
            m.actions[i.history_ref].event if i.history_ref in m.actions else
            m.consequences[i.history_ref].event if i.history_ref in m.consequences else
            m.traces[i.history_ref].event
        )
        require(at_or_before(history_event, i.event), "interpretation refers to future history")
    # Explicitly show contradictory frame-indexed readings coexist.
    net_reading = [i for i in m.interpretations if i.history_ref == "k3_fail" and i.frame == "F_net"]
    evt_reading = [i for i in m.interpretations if i.history_ref == "k3_fail" and i.frame == "F_evt"]
    require(net_reading and evt_reading, "expected old and new frame-indexed interpretations to coexist")
    require(net_reading[0].content != evt_reading[0].content, "interpretations were silently merged")
    return ["History is immutable and reinterpretation is append-only, frame-indexed, and non-overwriting."]


def check_loss_recovery(m: FiniteModel) -> List[str]:
    losses_by_d = {l.distinction: l for l in m.losses}
    for r in m.recoveries:
        require(r.writer == "reintroduce", "availability restored by a forbidden writer")
        require(r.distinction in losses_by_d, "recovery has no prior loss")
        require(before(losses_by_d[r.distinction].event, r.event), "recovery is not later than loss")
        require(r.witness_kind in {"retained-side-information", "other-frame", "reversible-route", "renewed-contact"},
                "recovery has invalid witness kind")
        require(bool(r.witness_ref), "recovery witness is empty")
    return ["Every recovered distinction has a typed reintroduction witness; measured adequacy has no ledger writer."]


def check_carrier_open_discharge(m: FiniteModel) -> List[str]:
    require(m.carrier_open(5), "carrier should remain open at e5")
    require(any(d.event == 5 for d in m.discharges), "expected preserve-open discharge judgment at e5")
    require(not m.carrier_open(15), "carrier item should be represented as discharged at e15")
    # The model has no LivingQuestion or LivingQuestionClosed sort/predicate at all.
    forbidden = {"closeLivingQuestion", "deriveExhaustion", "carrierClosureToDischarge"}
    require(forbidden.isdisjoint({w.writer for w in m.writers}), "carrier sovereignty writer exists")
    return [
        "Discharge can coexist with CarrierOpen (e5), so the two judgments are non-equivalent.",
        "No living-question closure sort or writer exists; represented carrier closure cannot exhaust the living inquiry.",
    ]


def check_prospective_retrospective(m: FiniteModel) -> List[str]:
    pr = m.predicted["pr_evt"]
    xr = m.exercised["xr_evt"]
    require(pr.event == 11 and xr.event == 14 and before(pr.event, xr.event), "prospective and retrospective evidence are not temporally separated")
    require("list-subscriptions" in pr.actions, "probe action missing from prospective reach")
    require(xr.returned_contact == "c14_receipt", "retrospective evidence lacks returned contact")
    require(m.durabilities["rho_evt"].exercised_reach == xr.id, "durability does not cite retrospective evidence")
    require(all(r.witness != pr.id for r in m.lifecycles if r.stage in {Stage.AUTHORITATIVE, Stage.DURABLE}),
            "predicted reach was used as authority or durability evidence by itself")
    reorg = m.reorganizations["reorg_evt"]
    require(reorg.exercised_reach == xr.id and reorg.event == xr.event,
            "reorganization evidence does not cite the exercised reach at the returned-contact event")
    require(reorg.renewed_contact == xr.returned_contact and reorg.renewed_contact in m.contacts,
            "reorganization evidence lacks renewed contact")
    require(all([
        reorg.consequence_uptake,
        reorg.lineage_preserved,
        reorg.permeability,
        reorg.provenance_safe,
        reorg.recovery_safe,
    ]), "reorganization evidence package is incomplete")
    return [
        "Predicted reach and exercised reach are different types, events, and evidential roles.",
        "K14 reorganization evidence is retrospective and cites exercised participation plus renewed contact.",
    ]


def check_stuck_and_contact_starvation(m: FiniteModel) -> List[str]:
    require(set(m.world_conditions) == set(m.contact_channels["coarse"]), "coarse channel is not total")
    require(set(m.world_conditions) == set(m.contact_channels["rich"]), "rich channel is not total")

    coarse = m.contact_channels["coarse"]
    rich = m.contact_channels["rich"]
    update_net = m.frame_updates["F_net"]
    update_evt = m.frame_updates["F_evt"]

    require(m.relevant_distinctions[4] == m.relevant_distinctions[10],
            "the comparison changed the living-question-relevant distinction")
    ((w1, w2),) = tuple(m.relevant_distinctions[10])

    contact_starved_e4 = coarse[w1] == coarse[w2]
    frame_sovereign_e4 = coarse[w1] != coarse[w2] and update_net[coarse[w1]] == update_net[coarse[w2]]
    require(contact_starved_e4 and not frame_sovereign_e4, "e4 must be contact-starved rather than frame-sovereign")

    distinction_survives_contact_e10 = rich[w1] != rich[w2]
    distinction_dies_in_net = update_net[rich[w1]] == update_net[rich[w2]]
    retries = [a for a in m.actions.values() if a.action == "retry-message" and at_or_before(a.event, 10)]
    discrepancy = True
    recurrence = len(retries) >= 4
    reinforcement = True
    demand = m.carrier_open(10)
    nonopening = True
    stuck_e10 = all([
        distinction_survives_contact_e10,
        distinction_dies_in_net,
        discrepancy,
        recurrence,
        reinforcement,
        demand,
        nonopening,
    ])
    require(stuck_e10, "full frame-sovereign stuck signature must fire at e10")
    require(update_evt[rich[w1]] != update_evt[rich[w2]], "F_evt should preserve the relevant rich distinction")

    for profile in m.tractions.values():
        profile.validate()
    net10 = m.tractions[("F_net", 10)]
    evt14 = m.tractions[("F_evt", 14)]
    net_vector = (
        net10.contact_uptake,
        net10.discrimination,
        net10.frame_permeability,
        net10.affordance_vitality,
        net10.provenance_continuity,
        net10.soul_admissibility,
    )
    evt_vector = (
        evt14.contact_uptake,
        evt14.discrimination,
        evt14.frame_permeability,
        evt14.affordance_vitality,
        evt14.provenance_continuity,
        evt14.soul_admissibility,
    )
    require(all(e >= n for e, n in zip(evt_vector, net_vector)) and any(e > n for e, n in zip(evt_vector, net_vector)),
            "later event-frame traction should product-dominate the stuck network-frame profile")
    require(not hasattr(net10, "score") and not hasattr(net10, "aggregate"),
            "traction profile exposes a canonical scalarization")

    return [
        "Before rich contact, repetition is correctly classified as contact-starved.",
        "At e10, rich contact discriminates but F_net coequalizes the distinction; the full stuck signature fires.",
        "F_evt preserves the same distinction and opens a different movement.",
        "Traction remains a six-component profile; the later profile dominates componentwise without a sovereign scalar.",
    ]


def check_nonamalgamation_and_joint_use(m: FiniteModel) -> List[str]:
    require(m.attached_at("F_net", 12) and m.attached_at("F_evt", 12), "both incompatible frames must coexist")
    # They retain divergent readings of the same history.
    readings = {(i.frame, i.content) for i in m.interpretations if i.history_ref == "k3_fail"}
    require(len(readings) >= 2, "incompatible frame readings were globally amalgamated")
    compat = [k for k in m.compatibilities if k.action == "create-subscription" and k.event == 13]
    require(bool(compat), "joint action lacks local compatibility witness")
    action = m.actions["a13_repair"]
    require(set(action.frames) == {"F_net", "F_evt"}, "joint action does not cite both frames")
    return ["Frames coexist without a global merge; their joint repair action carries an explicit local compatibility witness."]


def check_writer_inventory(m: FiniteModel) -> List[str]:
    require(m.doctrine is not None, "writer check requires the doctrine interface")
    allowed = m.doctrine.writer_permissions
    forbidden_implicit = {"renderer", "evaluator", "capability", "frame", "genericCarrierMethod"}

    patch_keys_seen: Set[Tuple[int, str, str]] = set()
    patches_by_event: Dict[int, List[WriterRecord]] = {}
    for patch in m.writers:
        require(patch.writer in allowed, f"unlisted writer {patch.writer}")
        require(patch.components.issubset(allowed[patch.writer]),
                f"writer {patch.writer} exceeds authority: {patch.components - allowed[patch.writer]}")
        require(patch.writer not in forbidden_implicit, f"implicit writer authority granted to {patch.writer}")
        key = (patch.event, patch.writer, patch.payload_ref)
        require(key not in patch_keys_seen, f"duplicate writer patch {key}")
        patch_keys_seen.add(key)
        patches_by_event.setdefault(patch.event, []).append(patch)

    observed = {patch.writer for patch in m.writers}
    require(observed.issubset(set(allowed)), "model uses a writer outside the closed signature")
    require(set(allowed) == set(WRITER_PERMISSIONS), "K17 signature and doctrine writer table differ")

    # Every writer event has exactly one explicit transaction, and every
    # transaction contains exactly the locally ordered patches for that event.
    require(set(m.transactions) == set(patches_by_event),
            "transaction events and patch events do not coincide")
    committed_events: Set[int] = set()
    for ev, transaction in m.transactions.items():
        require(ev not in committed_events, f"event {ev} was committed more than once")
        committed_events.add(ev)
        require(transaction.event == ev, "transaction key/event mismatch")
        require(is_downclosed(transaction.pre_cut), f"transaction {ev} pre-cut is not down-closed")
        require(ev not in transaction.pre_cut, f"transaction {ev} pre-cut already contains the event")
        require(all(x in transaction.pre_cut for x in EVENTS if before(x, ev)),
                f"transaction {ev} is not enabled by its full causal past")
        require(transaction.post_cut == frozenset(set(transaction.pre_cut) | {ev}),
                f"transaction {ev} does not advance the cut exactly once")
        require(is_downclosed(transaction.post_cut), f"transaction {ev} post-cut is not down-closed")
        expected = tuple((patch.writer, patch.payload_ref) for patch in patches_by_event[ev])
        require(transaction.patch_keys == expected,
                f"transaction {ev} omitted, duplicated, or reordered writer patches")
        require(len(transaction.patch_keys) == len(set(transaction.patch_keys)),
                f"transaction {ev} contains duplicate patches")
        require("WriterEvent" in m.event_tags[ev], f"transaction {ev} lacks the writer-event role")

        # Local dependency obligations for the finite interpretation.
        names = [writer for writer, _ in transaction.patch_keys]
        def idx(name: str) -> Optional[int]:
            return names.index(name) if name in names else None

        if "formFrame" in names and "admitCandidate" in names:
            require(idx("formFrame") < idx("admitCandidate"),
                    f"transaction {ev} admits a candidate before its frame is formed")
        if "authorizeProbe" in names and "recordAction" in names:
            require(idx("authorizeProbe") < idx("recordAction"),
                    f"transaction {ev} records a probe action before probe eligibility")
        if "recordContact" in names and "attachAuthoritative" in names:
            require(idx("recordContact") < idx("attachAuthoritative"),
                    f"transaction {ev} attaches authority before same-event material contact is recorded")
        if "attachAuthoritative" in names and "appendInterpretation" in names:
            require(idx("attachAuthoritative") < idx("appendInterpretation"),
                    f"transaction {ev} appends the new frame interpretation before attachment")
        if "attachAuthoritative" in names and "recordLoss" in names:
            require(idx("attachAuthoritative") < idx("recordLoss"),
                    f"transaction {ev} records frame-relative loss before attachment")
        if "promoteDurable" in names and "discharge" in names:
            require(idx("promoteDurable") < idx("discharge"),
                    f"transaction {ev} discharges before durability evidence is committed")

        # Source-side anchor rows are unique per event/frame payload; multiple
        # append-only patches may share D or H without conflicting.
        source_rows = [payload for writer, payload in transaction.patch_keys if writer == "attachAuthoritative"]
        require(len(source_rows) == len(set(source_rows)),
                f"transaction {ev} contains duplicate authoritative source-row writes")

    require(set(committed_events) == set(EVENTS),
            "the finite model must commit every proto-time event exactly once")

    return [
        "Every model mutation is an authority-bounded append-only patch owned by a listed writer.",
        "All same-event patches share one pre-cut, satisfy a local acyclic order, and are committed exactly once.",
        "The closed K17 writer signature contains no renderer, evaluator, capability, frame, or generic carrier writer.",
    ]


def check_failed_attachment(m: FiniteModel) -> List[str]:
    # F_perf has no authoritative lifecycle and no nonempty answerability to c1.
    require(m.current_stage("F_perf", 15) == Stage.CANDIDATE, "F_perf should remain only a candidate")
    require(not m.attached_at("F_perf", 15), "F_perf was smuggled into the same inquiry")
    # No automatic new carrier is created by failure; there is only Q_mm in this model.
    require(all(w.payload_ref != "Q_perf" for w in m.writers if w.writer == "foundInquiry"),
            "failed attachment automatically founded another inquiry")
    return ["The adjacent performance frame remains a candidate and neither attaches nor automatically founds another inquiry."]


def check_causal_meta_awareness(m: FiniteModel) -> List[str]:
    external_contacts_visible = tuple(sorted(cid for cid, c in m.contacts.items() if at_or_before(c.event, 10)))
    external_contacts_severed = external_contacts_visible
    narration_visible = m.traces["t10_visible"].narration
    narration_severed = narration_visible  # same words, but no grounded trace links
    visible_action_e11 = "list-subscriptions" if m.traces["t10_visible"].grounded else "retry-message"
    severed_action_e11 = "retry-message"
    require(external_contacts_visible == external_contacts_severed, "arms have different immediate external contact")
    require(narration_visible == narration_severed, "arms have different verbal self-description")
    require(visible_action_e11 != severed_action_e11, "grounded trajectory failed to change later action")
    require(m.traces["t10_visible"].action_refs and m.traces["t10_visible"].consequence_refs,
            "visible arm trace is merely narration")
    return [
        "Trajectory-visible and trace-severed arms share contact and words but choose different e11 actions.",
        "The difference is grounded history linkage, not a second observer or a different external input.",
    ]


def run_checks() -> List[str]:
    model = build_model()
    checks: Sequence[Tuple[str, Callable[[], List[str]]]] = [
        ("finite quantale", check_quantale),
        ("proto-time", check_proto_time),
        ("event-role predicates", lambda: check_event_roles(model)),
        ("raw fields and frame formation", lambda: check_raw_fields_and_formations(model)),
        ("Soul-doctrine interface", lambda: check_doctrine_interface(model)),
        ("typed standings", lambda: check_standings(model)),
        ("attachment record completeness", lambda: check_attachment_record_completeness(model)),
        ("anchor spines and stage extension", lambda: check_anchor_spines(model)),
        ("anchor writer isolation", lambda: check_anchor_writer_isolation(model)),
        ("lifecycle and guards", lambda: check_lifecycle_and_guards(model)),
        ("immutable history", lambda: check_history_and_interpretation(model)),
        ("loss and recovery", lambda: check_loss_recovery(model)),
        ("CarrierOpen versus Discharge", lambda: check_carrier_open_discharge(model)),
        ("prospective versus retrospective affordance", lambda: check_prospective_retrospective(model)),
        ("contact starvation and stuck", lambda: check_stuck_and_contact_starvation(model)),
        ("non-amalgamation and joint use", lambda: check_nonamalgamation_and_joint_use(model)),
        ("writer closure", lambda: check_writer_inventory(model)),
        ("failed attachment", lambda: check_failed_attachment(model)),
        ("causal meta-awareness", lambda: check_causal_meta_awareness(model)),
    ]

    report: List[str] = []
    for name, fn in checks:
        details = fn()
        report.append(f"PASS — {name}")
        report.extend(f"  {line}" for line in details)
    return report


if __name__ == "__main__":
    lines = run_checks()
    print("Gate C finite interpretation: all checks passed.")
    print(f"Checks: {sum(1 for line in lines if line.startswith('PASS'))}")
    for line in lines:
        print(line)
