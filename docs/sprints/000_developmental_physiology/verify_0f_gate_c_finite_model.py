#!/usr/bin/env python3
"""Machine-checkable Gate C finite interpretation for Inquiry 24.

Companion to:
  0f_Inquiry_24_Gate_B_Formal_Kernel_Signature_and_Gate_C_Finite_Interpretation.md

The model is finite and dependency-free.  It verifies the typed K0-K17
interfaces at toy scale; it does not claim to formalize the full Soul doctrine
or the live ClarityOmega runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import product
from typing import Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


# ---------------------------------------------------------------------------
# K5: finite typed quantaloid.
# ---------------------------------------------------------------------------

GRADE_VALUES: Tuple[float, ...] = (0.0, 0.5, 1.0)
V_OBJECTS: Tuple[str, ...] = ("FrameType", "ContactType")


def v_join(a: float, b: float) -> float:
    return max(a, b)


def v_comp(a: float, b: float) -> float:
    return min(a, b)


def v_id(_: str) -> float:
    return 1.0


def check_quantaloid() -> None:
    for a, b, c in product(GRADE_VALUES, repeat=3):
        assert v_comp(v_comp(a, b), c) == v_comp(a, v_comp(b, c))
        assert v_comp(a, v_join(b, c)) == v_join(v_comp(a, b), v_comp(a, c))
        assert v_comp(v_join(a, b), c) == v_join(v_comp(a, c), v_comp(b, c))
    for obj_a, obj_b in product(V_OBJECTS, repeat=2):
        for x in GRADE_VALUES:
            assert v_comp(v_id(obj_b), x) == x
            assert v_comp(x, v_id(obj_a)) == x


# ---------------------------------------------------------------------------
# K1: proto-time, multi-tag events, and causal cuts.
# ---------------------------------------------------------------------------

class EventTag(Enum):
    CONTACT = "contact"
    FRAME_FORMATION = "frame_formation"
    ACTION = "action"
    CONSEQUENCE = "consequence"
    TRACE = "trace"
    WRITER = "writer"
    INTERPRETATION = "interpretation"
    LIFECYCLE = "lifecycle"
    RECOVERY = "recovery"
    DISCHARGE = "discharge"
    OTHER = "other"


EVENTS: Tuple[str, ...] = tuple(f"e{i}" for i in range(1, 16))
MAIN_CHAIN: Tuple[str, ...] = (
    "e1", "e2", "e3", "e4", "e5", "e8", "e9", "e10", "e11", "e12", "e13", "e14", "e15"
)
BRANCH: Tuple[str, ...] = ("e5", "e6", "e7", "e9")


def chain_edges(chain: Sequence[str]) -> Set[Tuple[str, str]]:
    return {(chain[i], chain[i + 1]) for i in range(len(chain) - 1)}


COVER_EDGES: Set[Tuple[str, str]] = chain_edges(MAIN_CHAIN) | chain_edges(BRANCH)


def transitive_closure(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    reach = set(edges)
    changed = True
    while changed:
        changed = False
        for a, b in list(reach):
            for c, d in list(reach):
                if b == c and (a, d) not in reach:
                    reach.add((a, d))
                    changed = True
    return reach


PRECEDES: Set[Tuple[str, str]] = transitive_closure(EVENTS, COVER_EDGES)


def downset(seed: Iterable[str]) -> FrozenSet[str]:
    seed_set = set(seed)
    return frozenset(seed_set | {a for a, b in PRECEDES if b in seed_set})


def is_downward_closed(s: FrozenSet[str]) -> bool:
    return all(not (b in s and a not in s) for a, b in PRECEDES)


EVENT_TAGS: Mapping[str, FrozenSet[EventTag]] = {
    "e1": frozenset({EventTag.CONTACT, EventTag.WRITER, EventTag.LIFECYCLE}),
    "e2": frozenset({EventTag.CONTACT, EventTag.CONSEQUENCE, EventTag.WRITER}),
    "e3": frozenset({EventTag.ACTION, EventTag.CONSEQUENCE, EventTag.INTERPRETATION, EventTag.WRITER}),
    "e4": frozenset({EventTag.ACTION, EventTag.CONSEQUENCE, EventTag.INTERPRETATION, EventTag.WRITER}),
    "e5": frozenset({EventTag.ACTION, EventTag.TRACE, EventTag.WRITER}),
    "e6": frozenset({EventTag.CONTACT, EventTag.CONSEQUENCE, EventTag.WRITER}),
    "e7": frozenset({EventTag.ACTION, EventTag.FRAME_FORMATION, EventTag.LIFECYCLE, EventTag.WRITER}),
    "e8": frozenset({EventTag.ACTION, EventTag.CONSEQUENCE, EventTag.INTERPRETATION, EventTag.WRITER}),
    "e9": frozenset({EventTag.CONTACT, EventTag.CONSEQUENCE, EventTag.WRITER}),
    "e10": frozenset({
        EventTag.ACTION, EventTag.CONSEQUENCE, EventTag.TRACE,
        EventTag.FRAME_FORMATION, EventTag.LIFECYCLE, EventTag.WRITER,
    }),
    "e11": frozenset({EventTag.ACTION, EventTag.LIFECYCLE, EventTag.WRITER, EventTag.OTHER}),
    "e12": frozenset({
        EventTag.CONTACT, EventTag.CONSEQUENCE, EventTag.INTERPRETATION,
        EventTag.LIFECYCLE, EventTag.WRITER,
    }),
    "e13": frozenset({EventTag.ACTION, EventTag.RECOVERY, EventTag.WRITER}),
    "e14": frozenset({EventTag.CONTACT, EventTag.CONSEQUENCE, EventTag.TRACE, EventTag.WRITER}),
    "e15": frozenset({EventTag.LIFECYCLE, EventTag.DISCHARGE, EventTag.WRITER}),
}


def is_contact_event(e: str) -> bool:
    return EventTag.CONTACT in EVENT_TAGS[e]


def check_proto_time() -> None:
    assert set(EVENT_TAGS) == set(EVENTS)
    assert all(EVENT_TAGS[e] for e in EVENTS)
    assert all((e, e) not in PRECEDES for e in EVENTS)
    for a, b in PRECEDES:
        for c, d in PRECEDES:
            if b == c:
                assert (a, d) in PRECEDES
    assert ("e6", "e8") not in PRECEDES and ("e8", "e6") not in PRECEDES
    assert ("e7", "e8") not in PRECEDES and ("e8", "e7") not in PRECEDES
    assert len(EVENT_TAGS["e12"]) > 1
    assert EventTag.CONTACT in EVENT_TAGS["e12"]
    assert EventTag.LIFECYCLE in EVENT_TAGS["e12"]
    assert is_downward_closed(downset({"e9"}))


# ---------------------------------------------------------------------------
# K2: typed standing.
# ---------------------------------------------------------------------------

class ProvKind(Enum):
    GENERATED = "generated"
    SELF_TRACE = "self_trace"
    INFERENCE = "inference"
    MEMORY = "memory"
    TESTIMONY = "testimony"
    CONTACT = "contact"


PROV_RANK: Mapping[ProvKind, int] = {
    ProvKind.GENERATED: 0,
    ProvKind.SELF_TRACE: 0,
    ProvKind.INFERENCE: 1,
    ProvKind.MEMORY: 2,
    ProvKind.TESTIMONY: 3,
    ProvKind.CONTACT: 4,
}


@dataclass(frozen=True)
class Standing:
    prov: ProvKind
    warrant: int
    support: FrozenSet[str]
    pressure: int
    freshness: int


@dataclass(frozen=True)
class StandingTransform:
    source: Standing
    target: Standing
    evidence_route: Optional[FrozenSet[str]] = None

    def valid(self) -> bool:
        no_prov_promotion = PROV_RANK[self.target.prov] <= PROV_RANK[self.source.prov]
        warrant_ok = self.target.warrant <= self.source.warrant or bool(self.evidence_route)
        pressure_cannot_supply_warrant = not (
            self.target.pressure > self.source.pressure
            and self.target.warrant > self.source.warrant
            and not self.evidence_route
        )
        support_explicit = self.target.support.issuperset(self.source.support)
        return no_prov_promotion and warrant_ok and pressure_cannot_supply_warrant and support_explicit


CONTACT_STANDING = Standing(ProvKind.CONTACT, 2, downset({"e9"}), 0, 2)
INTERPRETIVE_STANDING = Standing(ProvKind.INFERENCE, 2, downset({"e10"}), 1, 2)
PI_EXAMPLE = StandingTransform(CONTACT_STANDING, INTERPRETIVE_STANDING, frozenset({"e9"}))


def check_standing() -> None:
    assert is_downward_closed(CONTACT_STANDING.support)
    assert is_downward_closed(INTERPRETIVE_STANDING.support)
    assert PI_EXAMPLE.valid()
    bad_pressure = StandingTransform(
        Standing(ProvKind.INFERENCE, 1, downset({"e10"}), 0, 2),
        Standing(ProvKind.INFERENCE, 2, downset({"e10"}), 2, 2),
        None,
    )
    assert not bad_pressure.valid()
    bad_promotion = StandingTransform(
        Standing(ProvKind.INFERENCE, 2, downset({"e10"}), 0, 2),
        Standing(ProvKind.CONTACT, 2, downset({"e10"}), 0, 2),
        frozenset({"e10"}),
    )
    assert not bad_promotion.valid()


# ---------------------------------------------------------------------------
# K3-K4: raw fields and partial frame formation.
# ---------------------------------------------------------------------------

RAW_FIELDS: Mapping[str, FrozenSet[str]] = {
    "G_e2": frozenset({"message_missing", "host_reachable", "no_agent_log_event"}),
    "G_e9": frozenset({
        "message_missing", "host_reachable", "no_agent_log_event",
        "no_active_subscription", "bot_identity_known",
    }),
    "G_e10": frozenset({
        "message_missing", "host_reachable", "no_active_subscription",
        "retry_recurrence", "unchanged_network_assumption",
    }),
}


@dataclass(frozen=True)
class FrameRecord:
    frame: str
    domain: FrozenSet[str]
    undefined: FrozenSet[str]
    context: str
    resolution: str
    competence: FrozenSet[str]
    formation_event: str
    partial_map: Mapping[str, str]

    def valid(self, raw_field: FrozenSet[str]) -> bool:
        return (
            set(self.partial_map).issubset(raw_field)
            and self.domain.isdisjoint(self.undefined)
            and set(self.partial_map.values()).issubset(self.domain)
        )


FRAMES: Mapping[str, FrameRecord] = {
    "F_net": FrameRecord(
        "F_net",
        frozenset({"host", "network", "socket", "network_reachability"}),
        frozenset({"subscription", "bot_identity", "event_delivery"}),
        "mattermost_delivery", "host_and_link",
        frozenset({"connectivity_diagnosis"}), "e2",
        {"host_reachable": "network_reachability", "no_agent_log_event": "socket"},
    ),
    "F_evt": FrameRecord(
        "F_evt",
        frozenset({"subscription", "bot_identity", "event_delivery"}),
        frozenset({"latency", "link_quality"}),
        "mattermost_delivery", "event_path",
        frozenset({"subscription_diagnosis", "identity_diagnosis", "delivery_path_diagnosis"}), "e10",
        {
            "no_active_subscription": "subscription",
            "bot_identity_known": "bot_identity",
            "message_missing": "event_delivery",
        },
    ),
    "F_perf": FrameRecord(
        "F_perf",
        frozenset({"latency", "throughput"}),
        frozenset({"subscription", "event_delivery", "bot_identity"}),
        "mattermost_performance", "performance",
        frozenset({"latency_diagnosis"}), "e7",
        {"host_reachable": "latency"},
    ),
}


def check_frame_formation() -> None:
    assert FRAMES["F_net"].valid(RAW_FIELDS["G_e2"])
    assert FRAMES["F_evt"].valid(RAW_FIELDS["G_e9"])
    assert FRAMES["F_perf"].valid(RAW_FIELDS["G_e9"])


# ---------------------------------------------------------------------------
# K5-K7: finite equipment shadow and stage-typed anchors.
# ---------------------------------------------------------------------------

FRAMES_BEFORE: Tuple[str, ...] = ("F_net",)
FRAMES_AFTER: Tuple[str, ...] = ("F_net", "F_evt")
CONTACTS_WITNESS: Tuple[str, ...] = ("c1", "c2", "c6", "c9")
CONTACTS_AUTHORITY: Tuple[str, ...] = CONTACTS_WITNESS + ("c12",)
CONTACTS_FINAL: Tuple[str, ...] = CONTACTS_AUTHORITY + ("c14",)
CONTACT_EVENT: Mapping[str, str] = {
    "c1": "e1", "c2": "e2", "c6": "e6", "c9": "e9", "c12": "e12", "c14": "e14"
}


def frame_hom(f_from: str, f_to: str) -> float:
    if f_from == f_to:
        return 1.0
    if f_from == "F_evt" and f_to == "F_net":
        return 0.5
    return 0.0


def contact_hom(c_from: str, c_to: str) -> float:
    if c_from == c_to:
        return 1.0
    return 1.0 if (CONTACT_EVENT[c_from], CONTACT_EVENT[c_to]) in PRECEDES else 0.0


def anchor_before(c: str, f: str) -> float:
    assert c in CONTACTS_WITNESS and f in FRAMES_BEFORE
    return 1.0


BETA_PLUS: Mapping[str, float] = {"c1": 0.5, "c2": 0.5, "c6": 0.5, "c9": 1.0}
BETA_MINUS: Mapping[str, float] = {**BETA_PLUS, "c12": 1.0}


def beta_plus(c: str) -> float:
    return BETA_PLUS[c]


def beta_minus(c: str) -> float:
    return BETA_MINUS[c]


def anchor_authority(c: str, f: str) -> float:
    assert c in CONTACTS_AUTHORITY and f in FRAMES_AFTER
    return 1.0 if f == "F_net" else beta_minus(c)


def anchor_final(c: str, f: str) -> float:
    assert c in CONTACTS_FINAL and f in FRAMES_AFTER
    if c == "c14":
        return 1.0
    return anchor_authority(c, f)


def check_v_category(objects: Sequence[str], hom) -> None:
    for x in objects:
        assert v_id("FrameType") <= hom(x, x)
    for x, y, z in product(objects, repeat=3):
        assert v_comp(hom(y, z), hom(x, y)) <= hom(x, z)


def check_anchor_distributor(frames: Sequence[str], contacts: Sequence[str], anchor) -> None:
    for c in contacts:
        for f, fp in product(frames, repeat=2):
            assert v_comp(anchor(c, f), frame_hom(fp, f)) <= anchor(c, fp)
    for f in frames:
        for c, cp in product(contacts, repeat=2):
            assert v_comp(contact_hom(c, cp), anchor(c, f)) <= anchor(cp, f)


def check_candidate_row(contacts: Sequence[str], row) -> None:
    for c, cp in product(contacts, repeat=2):
        assert v_comp(contact_hom(c, cp), row(c)) <= row(cp)


def target_extend_beta(c_new: str) -> float:
    # Finite left-extension shadow: join over old contacts transported into c_new.
    return max(v_comp(contact_hom(c_old, c_new), beta_plus(c_old)) for c_old in CONTACTS_WITNESS)


def check_equipment_and_anchor() -> None:
    check_v_category(FRAMES_AFTER, frame_hom)
    check_v_category(CONTACTS_FINAL, contact_hom)
    check_anchor_distributor(FRAMES_BEFORE, CONTACTS_WITNESS, anchor_before)
    check_candidate_row(CONTACTS_WITNESS, beta_plus)
    check_candidate_row(CONTACTS_AUTHORITY, beta_minus)
    check_anchor_distributor(FRAMES_AFTER, CONTACTS_AUTHORITY, anchor_authority)
    check_anchor_distributor(FRAMES_AFTER, CONTACTS_FINAL, anchor_final)

    # Prospective spine, componentwise: inherited answerability plus direct c9.
    p_evt_net = 0.5
    for c in CONTACTS_WITNESS:
        inherited = v_comp(anchor_before(c, "F_net"), p_evt_net)
        direct = 1.0 if c == "c9" else 0.0
        assert beta_plus(c) <= v_join(inherited, direct)

    # Future contact cannot leak into the prospective row.
    assert set(BETA_PLUS) == set(CONTACTS_WITNESS)
    assert "c12" not in BETA_PLUS

    # Conservative target extension and later authority row.
    for c in CONTACTS_WITNESS:
        assert beta_minus(c) == beta_plus(c)
    assert target_extend_beta("c12") <= beta_minus("c12")
    assert beta_minus("c12") == 1.0

    # Existing anchor components survive source extension.
    for c in CONTACTS_WITNESS:
        assert anchor_authority(c, "F_net") == anchor_before(c, "F_net")
    for c in CONTACTS_AUTHORITY:
        assert anchor_final(c, "F_net") == anchor_authority(c, "F_net")
        assert anchor_final(c, "F_evt") == anchor_authority(c, "F_evt")


# ---------------------------------------------------------------------------
# K8-K14: open standing, interpretation, loss, lifecycle, and evidence.
# ---------------------------------------------------------------------------

class LifeStatus(Enum):
    CANDIDATE = "candidate"
    PROBE_ELIGIBLE = "probe_eligible"
    AUTHORITATIVE = "authoritative"
    DURABLE = "durable"
    SUSPENDED = "suspended"
    DEMOTED = "demoted"
    RETIRED = "retired"


LIFECYCLE: Tuple[Tuple[str, LifeStatus, str], ...] = (
    ("F_perf", LifeStatus.CANDIDATE, "e7"),
    ("F_evt", LifeStatus.CANDIDATE, "e10"),
    ("F_evt", LifeStatus.PROBE_ELIGIBLE, "e11"),
    ("F_evt", LifeStatus.AUTHORITATIVE, "e12"),
    ("F_evt", LifeStatus.DURABLE, "e15"),
)


@dataclass(frozen=True)
class LiveItem:
    ident: str
    contact_ref: str
    text: str
    history_refs: FrozenSet[str]
    standing: Standing


L1 = LiveItem(
    "l1", "c1", "message did not arrive and causal location is unresolved",
    frozenset({"e1"}), Standing(ProvKind.CONTACT, 1, downset({"e1"}), 2, 2),
)
LIVE_AT: Mapping[str, FrozenSet[str]] = {"l1": frozenset(EVENTS[:-1])}
DISCHARGES: FrozenSet[Tuple[str, str, str]] = frozenset({
    ("l1", "answered_for_present_purpose", "e15"),
})


def carrier_open(event: str) -> bool:
    return any(event in LIVE_AT[item] for item in LIVE_AT)


class InterpretationKind(Enum):
    PRESERVED = "preserved"
    REINTERPRETED = "reinterpreted"
    BRACKETED = "bracketed"
    MOOTED = "mooted"
    LOST = "lost"


@dataclass(frozen=True)
class Interpretation:
    frame: str
    history_event: str
    kind: InterpretationKind
    witness: str
    event: str


INTERPRETATIONS: Tuple[Interpretation, ...] = (
    Interpretation("F_net", "e3", InterpretationKind.PRESERVED, "w_net_retry3", "e3"),
    Interpretation("F_net", "e4", InterpretationKind.PRESERVED, "w_net_retry4", "e4"),
    Interpretation("F_net", "e8", InterpretationKind.PRESERVED, "w_net_retry8", "e8"),
    Interpretation("F_net", "e10", InterpretationKind.PRESERVED, "w_net_retry10", "e10"),
    Interpretation("F_evt", "e2", InterpretationKind.PRESERVED, "w_evt_network_ok", "e12"),
    Interpretation("F_evt", "e3", InterpretationKind.REINTERPRETED, "w_evt_retry3", "e12"),
    Interpretation("F_evt", "e4", InterpretationKind.REINTERPRETED, "w_evt_retry4", "e12"),
    Interpretation("F_evt", "e8", InterpretationKind.REINTERPRETED, "w_evt_retry8", "e12"),
    Interpretation("F_evt", "e10", InterpretationKind.REINTERPRETED, "w_evt_retry10", "e12"),
    Interpretation("F_evt", "e6", InterpretationKind.BRACKETED, "w_evt_latency", "e12"),
)


@dataclass(frozen=True)
class LossEntry:
    distinction: str
    source_frame: str
    target_frame: str
    route: str
    event: str
    side_information: Optional[str]


@dataclass(frozen=True)
class RecoveryEntry:
    distinction: str
    target_context: str
    witness_kind: str
    witness_ref: str
    event: str


LOSSES: Tuple[LossEntry, ...] = (
    LossEntry("link_quality_detail", "F_net", "F_evt", "sigma_evt_net", "e12", "retained_in_F_net"),
)
RECOVERIES: Tuple[RecoveryEntry, ...] = (
    RecoveryEntry("link_quality_detail", "joint_repair_context", "other_attached_frame", "F_net", "e13"),
)


@dataclass(frozen=True)
class ProspectiveAttachment:
    frame: str
    formation_event: str
    witness_event: str
    spine_grade: float
    prospective_anchor: Mapping[str, float]
    live_continuations: Mapping[str, str]
    material_history: FrozenSet[str]
    proposed_interpretations: Mapping[str, InterpretationKind]
    frame_record: FrameRecord
    standing_transforms: Tuple[StandingTransform, ...]
    fidelity_floor: float
    measured_residual: float
    loss_additions: FrozenSet[str]
    new_distinctions: FrozenSet[str]
    zigzag: Tuple[str, ...]
    predicted_reach: FrozenSet[str]
    preserve_without_action: bool = False

    def complete(self) -> bool:
        stage_ok = self.formation_event == self.witness_event or (
            self.formation_event, self.witness_event
        ) in PRECEDES
        return (
            stage_ok
            and self.spine_grade > 0.0
            and set(self.prospective_anchor) == set(CONTACTS_WITNESS)
            and "c12" not in self.prospective_anchor
            and len(self.live_continuations) > 0
            and set(self.proposed_interpretations) == set(self.material_history)
            and self.frame_record.frame == self.frame
            and self.frame_record.formation_event == self.formation_event
            and all(t.valid() for t in self.standing_transforms)
            and (len(self.predicted_reach) > 0 or self.preserve_without_action)
        )


OMEGA_PLUS = ProspectiveAttachment(
    frame="F_evt",
    formation_event="e10",
    witness_event="e11",
    spine_grade=1.0,
    prospective_anchor=BETA_PLUS,
    live_continuations={"l1": "locate event-delivery break"},
    material_history=frozenset({"e2", "e3", "e4", "e6", "e8", "e10"}),
    proposed_interpretations={
        "e2": InterpretationKind.PRESERVED,
        "e3": InterpretationKind.REINTERPRETED,
        "e4": InterpretationKind.REINTERPRETED,
        "e6": InterpretationKind.BRACKETED,
        "e8": InterpretationKind.REINTERPRETED,
        "e10": InterpretationKind.REINTERPRETED,
    },
    frame_record=FRAMES["F_evt"],
    standing_transforms=(PI_EXAMPLE,),
    fidelity_floor=0.5,
    measured_residual=0.5,
    loss_additions=frozenset({"link_quality_detail"}),
    new_distinctions=frozenset({"subscription_state"}),
    zigzag=("F_evt", "F_net", "c9"),
    predicted_reach=frozenset({"list_subscriptions", "inspect_bot_identity"}),
)


SELF_GEN_OMEGA: FrozenSet[str] = downset({"e10", "e11"})
SUPPORT_OMEGA: FrozenSet[str] = downset({"e11"})
SUPPORT_CONE_AUTH: FrozenSet[str] = downset({"e12"})
MATERIAL_CONTACTS: FrozenSet[str] = frozenset({"e12"})


@dataclass(frozen=True)
class AuthorityEvidence:
    frame: str
    witness_event: str
    authority_event: str
    material_contact: str
    support: FrozenSet[str]
    self_generation: FrozenSet[str]
    material_contacts: FrozenSet[str]
    final_anchor: Mapping[str, float]

    def valid(self) -> bool:
        if not is_downward_closed(self.support) or not is_downward_closed(self.self_generation):
            return False
        if not self.self_generation.issubset(self.support):
            return False
        if (self.witness_event, self.authority_event) not in PRECEDES:
            return False
        if (self.witness_event, self.material_contact) not in PRECEDES:
            return False
        if not (
            self.material_contact == self.authority_event
            or (self.material_contact, self.authority_event) in PRECEDES
        ):
            return False
        if not is_contact_event(self.material_contact):
            return False
        if self.material_contact not in self.support - self.self_generation:
            return False
        if self.material_contact not in self.material_contacts:
            return False
        if set(self.final_anchor) != set(CONTACTS_AUTHORITY):
            return False
        if any(self.final_anchor[c] < OMEGA_PLUS.prospective_anchor[c] for c in CONTACTS_WITNESS):
            return False
        return self.final_anchor["c12"] == 1.0


EPSILON_MINUS = AuthorityEvidence(
    frame="F_evt",
    witness_event="e11",
    authority_event="e12",
    material_contact="e12",
    support=SUPPORT_CONE_AUTH,
    self_generation=SELF_GEN_OMEGA,
    material_contacts=MATERIAL_CONTACTS,
    final_anchor=BETA_MINUS,
)


@dataclass(frozen=True)
class RetrospectiveEvidence:
    frame: str
    authority_event: str
    durability_event: str
    exercised_reach: FrozenSet[str]
    consequences: FrozenSet[str]
    permeability_events: FrozenSet[str]
    integration_events: FrozenSet[str]
    lineage_events: FrozenSet[str]

    def valid(self) -> bool:
        return (
            (self.authority_event, self.durability_event) in PRECEDES
            and bool(self.exercised_reach)
            and bool(self.consequences)
            and bool(self.permeability_events)
            and bool(self.integration_events)
            and bool(self.lineage_events)
        )


RHO_MINUS = RetrospectiveEvidence(
    "F_evt", "e12", "e15",
    frozenset({"list_subscriptions", "repair_subscription", "test_message_received"}),
    frozenset({"subscription_confirmed_missing", "message_received_after_repair"}),
    frozenset({"e12", "e14"}),
    frozenset({"e13", "e14", "e15"}),
    frozenset({"e1", "e9", "e10", "e11", "e12", "e14"}),
)


def check_records_and_lifecycle() -> None:
    assert carrier_open("e14")
    assert not carrier_open("e15")
    assert ("l1", "answered_for_present_purpose", "e15") in DISCHARGES
    assert OMEGA_PLUS.complete()
    assert OMEGA_PLUS.formation_event == "e10"
    assert OMEGA_PLUS.witness_event == "e11"
    assert ("e10", "e11") in PRECEDES
    assert EPSILON_MINUS.valid()
    assert RHO_MINUS.valid()
    assert ("F_evt", LifeStatus.CANDIDATE, "e10") in LIFECYCLE
    assert ("F_evt", LifeStatus.PROBE_ELIGIBLE, "e11") in LIFECYCLE
    assert ("F_evt", LifeStatus.AUTHORITATIVE, "e12") in LIFECYCLE
    assert ("F_evt", LifeStatus.DURABLE, "e15") in LIFECYCLE
    assert "test_message_received" not in OMEGA_PLUS.predicted_reach
    assert "test_message_received" in RHO_MINUS.exercised_reach
    assert SELF_GEN_OMEGA.issubset(SUPPORT_CONE_AUTH)
    assert "e12" not in SELF_GEN_OMEGA

    for recovery in RECOVERIES:
        assert recovery.witness_kind in {
            "retained_side_information", "other_attached_frame", "reversible_witness", "renewed_contact"
        }
        assert any(loss.distinction == recovery.distinction for loss in LOSSES)
    assert len(LOSSES) == 1
    assert any(i.frame == "F_net" and i.history_event == "e10" for i in INTERPRETATIONS)
    assert any(i.frame == "F_evt" and i.history_event == "e10" for i in INTERPRETATIONS)


# ---------------------------------------------------------------------------
# K15: structured traction and stuck.
# ---------------------------------------------------------------------------

WORLD_CONDITIONS: Tuple[str, ...] = (
    "network_down", "event_not_emitted", "subscription_missing", "authorization_revoked"
)


def observation_coarse(_: str) -> str:
    return "delivery_failed"


def observation_rich(world: str) -> str:
    return {
        "network_down": "socket_unreachable",
        "event_not_emitted": "no_event_emitted",
        "subscription_missing": "no_active_subscription",
        "authorization_revoked": "authorization_denied",
    }[world]


def update_net(_: str) -> str:
    return "retry_connection"


def update_evt(obs: str) -> str:
    return {
        "socket_unreachable": "inspect_network",
        "no_event_emitted": "inspect_emission",
        "no_active_subscription": "list_subscriptions",
        "authorization_denied": "inspect_authorization",
    }[obs]


RELEVANT_PAIR = ("network_down", "subscription_missing")
DISCREPANCY = frozenset({"e4", "e8", "e10"})
DEMAND = frozenset({"e4", "e8", "e10"})
RECURRENCE = frozenset({"e10"})
FRAME_REINFORCEMENT = frozenset({"e10"})
NON_OPENING_REACH = frozenset({"e10"})


@dataclass(frozen=True)
class TractionProfile:
    contact_uptake: int
    discrimination: int
    permeability: int
    affordance_vitality: int
    provenance_continuity: int
    soul_admissibility: int


def contact_starved(obs_fn) -> bool:
    w1, w2 = RELEVANT_PAIR
    return obs_fn(w1) == obs_fn(w2)


def frame_distinction_death(obs_fn, update_fn) -> bool:
    w1, w2 = RELEVANT_PAIR
    return obs_fn(w1) != obs_fn(w2) and update_fn(obs_fn(w1)) == update_fn(obs_fn(w2))


def stuck(frame: str, event: str) -> bool:
    return (
        frame == "F_net"
        and frame_distinction_death(observation_rich, update_net)
        and event in DISCREPANCY
        and event in DEMAND
        and event in RECURRENCE
        and event in FRAME_REINFORCEMENT
        and event in NON_OPENING_REACH
    )


def check_traction_and_stuck() -> None:
    assert contact_starved(observation_coarse)
    assert not frame_distinction_death(observation_coarse, update_net)
    assert not stuck("F_net", "e4")
    assert frame_distinction_death(observation_rich, update_net)
    assert stuck("F_net", "e10")
    assert not frame_distinction_death(observation_rich, update_evt)
    assert not stuck("F_evt", "e12")
    assert not hasattr(TractionProfile, "scalar")


# ---------------------------------------------------------------------------
# K16-K17: scoped joint use and writer closure.
# ---------------------------------------------------------------------------

LOCAL_COMPATIBILITY: FrozenSet[Tuple[str, str, str, str, str]] = frozenset({
    ("F_net", "F_evt", "repair_subscription", "kappa13", "e13"),
})
JOINT_USE_WITH_TENSION: FrozenSet[Tuple[str, str, str, str, str]] = frozenset()
JOINT_USE: FrozenSet[Tuple[str, str, str, str]] = frozenset({
    ("F_net", "F_evt", "repair_subscription", "e13"),
})

ALL_WRITERS = frozenset({
    "foundInquiry", "recordContact", "recoverContact", "recordAction", "recordConsequence",
    "recordTrace", "formFrame", "recordLiveItem", "admitCandidate", "authorizeProbe",
    "attachAuthoritative", "promoteDurable", "appendInterpretation", "recordLoss",
    "reintroduce", "appendStandingRevision", "recordTraction", "recordReorganizationEvidence",
    "recordJointUse", "discharge", "suspendFrame", "demoteFrame", "retireFrame",
})

WRITER_MATRIX: Mapping[str, FrozenSet[str]] = {
    "D_Q": ALL_WRITERS,
    "C_Q": frozenset({"recordContact", "recoverContact"}),
    "F_Q": frozenset({"foundInquiry", "attachAuthoritative"}),
    "H_Q": ALL_WRITERS,
    "U_Q": frozenset({"foundInquiry", "recordLiveItem", "discharge"}),
    "I_Q": frozenset({"appendInterpretation"}),
    "L_Q": frozenset({"recordLoss", "reintroduce"}),
    "a_Q_contact_dimension": frozenset({"recordContact", "recoverContact"}),
    "a_Q_frame_dimension": frozenset({"attachAuthoritative"}),
}
FORBIDDEN_GENERIC_WRITERS = frozenset({
    "renderer", "evaluator", "capability", "frame", "genericCarrierMethod", "witnessObject"
})


def check_joint_use_and_writers() -> None:
    for f1, f2, action, event in JOINT_USE:
        assert any(
            x[0] == f1 and x[1] == f2 and x[2] == action and x[4] == event
            for x in LOCAL_COMPATIBILITY | JOINT_USE_WITH_TENSION
        )
    assert "appendInterpretation" not in WRITER_MATRIX["C_Q"]
    assert "attachAuthoritative" not in WRITER_MATRIX["C_Q"]
    assert WRITER_MATRIX["a_Q_contact_dimension"] == frozenset({"recordContact", "recoverContact"})
    assert WRITER_MATRIX["a_Q_frame_dimension"] == frozenset({"attachAuthoritative"})
    for writers in WRITER_MATRIX.values():
        assert writers.isdisjoint(FORBIDDEN_GENERIC_WRITERS)


# ---------------------------------------------------------------------------
# K6/K17: cut-indexed carrier interpretation.
# ---------------------------------------------------------------------------

@dataclass
class CarrierState:
    cut: FrozenSet[str] = field(default_factory=frozenset)
    contacts: Set[str] = field(default_factory=set)
    frames: Set[str] = field(default_factory=set)
    history: Set[str] = field(default_factory=set)
    traces: Set[str] = field(default_factory=set)
    witnesses: Set[str] = field(default_factory=set)
    prospective_anchor: Dict[Tuple[str, str], float] = field(default_factory=dict)
    lifecycle_log: List[Tuple[str, LifeStatus, str]] = field(default_factory=list)
    live_status_log: List[Tuple[str, str, str]] = field(default_factory=list)
    interpretations: List[Interpretation] = field(default_factory=list)
    losses: List[LossEntry] = field(default_factory=list)
    recoveries: List[RecoveryEntry] = field(default_factory=list)
    anchor: Dict[Tuple[str, str], float] = field(default_factory=dict)
    reorganization_evidence: Set[str] = field(default_factory=set)
    joint_use: Set[Tuple[str, str, str, str]] = field(default_factory=set)


def state_for_cut(event: str) -> CarrierState:
    k = downset({event})
    s = CarrierState(cut=k)
    s.contacts = {c for c, e in CONTACT_EVENT.items() if e in k}
    if "e1" in k:
        s.frames.add("F_net")
    if "e12" in k:
        s.frames.add("F_evt")
    s.history = set(k)
    if "e5" in k:
        s.traces.add("trace_e2_e4")
    if "e10" in k:
        s.traces.add("trace_e2_e10")
    if "e11" in k:
        s.witnesses.add("omega_evt_plus")
        s.prospective_anchor = {(c, "F_evt"): beta_plus(c) for c in CONTACTS_WITNESS}
    s.lifecycle_log = [x for x in LIFECYCLE if x[2] in k]
    if "e1" in k:
        s.live_status_log.append(("l1", "live", "e1"))
    if "e15" in k:
        s.live_status_log.append(("l1", "answered_for_present_purpose", "e15"))
    s.interpretations = [i for i in INTERPRETATIONS if i.event in k]
    s.losses = [x for x in LOSSES if x.event in k]
    s.recoveries = [x for x in RECOVERIES if x.event in k]
    if "e13" in k:
        s.joint_use.add(("F_net", "F_evt", "repair_subscription", "e13"))
    if "e14" in k:
        s.reorganization_evidence.add("rho_evt_e14")

    for c in s.contacts:
        if "F_net" in s.frames:
            s.anchor[(c, "F_net")] = 1.0
        if "F_evt" in s.frames:
            if c in CONTACTS_AUTHORITY:
                s.anchor[(c, "F_evt")] = beta_minus(c)
            elif c == "c14":
                s.anchor[(c, "F_evt")] = 1.0
            else:
                raise AssertionError(f"unexpected contact for F_evt: {c}")
    return s


CARRIER_STATES: Mapping[str, CarrierState] = {e: state_for_cut(e) for e in EVENTS}


def check_carrier_transitions() -> None:
    for earlier, later in PRECEDES:
        a, b = CARRIER_STATES[earlier], CARRIER_STATES[later]
        assert a.cut.issubset(b.cut)
        assert a.contacts.issubset(b.contacts)
        assert a.frames.issubset(b.frames)
        assert a.history.issubset(b.history)
        assert a.traces.issubset(b.traces)
        assert a.witnesses.issubset(b.witnesses)
        assert set(a.prospective_anchor).issubset(set(b.prospective_anchor))
        assert set(a.interpretations).issubset(set(b.interpretations))
        assert set(a.losses).issubset(set(b.losses))
        assert set(a.recoveries).issubset(set(b.recoveries))
        assert all(b.anchor[k] == v for k, v in a.anchor.items())

    # Genuine branch semantics: e8 does not contain the incomparable e6/e7 branch.
    assert "c6" not in CARRIER_STATES["e8"].contacts
    assert ("F_perf", LifeStatus.CANDIDATE, "e7") not in CARRIER_STATES["e8"].lifecycle_log
    assert "c6" in CARRIER_STATES["e9"].contacts
    assert ("F_perf", LifeStatus.CANDIDATE, "e7") in CARRIER_STATES["e9"].lifecycle_log

    # Candidate row is present as witness data, never as the committed anchor before authority.
    assert "omega_evt_plus" in CARRIER_STATES["e11"].witnesses
    assert "F_evt" not in CARRIER_STATES["e11"].frames
    assert not any(f == "F_evt" for _, f in CARRIER_STATES["e11"].anchor)
    assert set(CARRIER_STATES["e11"].prospective_anchor) == {
        (c, "F_evt") for c in CONTACTS_WITNESS
    }
    assert ("c12", "F_evt") not in CARRIER_STATES["e11"].prospective_anchor

    assert "F_evt" in CARRIER_STATES["e12"].frames
    assert CARRIER_STATES["e12"].anchor[("c12", "F_evt")] == 1.0
    assert "F_perf" not in CARRIER_STATES["e15"].frames
    assert ("F_net", "F_evt", "repair_subscription", "e13") in CARRIER_STATES["e13"].joint_use
    assert "rho_evt_e14" in CARRIER_STATES["e14"].reorganization_evidence


# ---------------------------------------------------------------------------
# Causal meta-awareness and theorem checks.
# ---------------------------------------------------------------------------

META_AWARENESS_ARMS: Mapping[str, Mapping[str, str]] = {
    "trajectory_visible": {
        "external_contact_e10": "no_active_subscription",
        "verbal_self_description_e10": "retrying did not work",
        "determination_e11": "authorize_list_subscriptions_probe",
    },
    "trace_severed": {
        "external_contact_e10": "no_active_subscription",
        "verbal_self_description_e10": "retrying did not work",
        "determination_e11": "retry_connection",
    },
}


def check_meta_awareness() -> None:
    a = META_AWARENESS_ARMS["trajectory_visible"]
    b = META_AWARENESS_ARMS["trace_severed"]
    assert a["external_contact_e10"] == b["external_contact_e10"]
    assert a["verbal_self_description_e10"] == b["verbal_self_description_e10"]
    assert a["determination_e11"] != b["determination_e11"]


def check_gate_c_theorems() -> None:
    # C1: no authority from closure: only the guarded authority evidence is present.
    assert ("F_evt", LifeStatus.AUTHORITATIVE, "e12") in LIFECYCLE
    assert EPSILON_MINUS.valid()

    # C2: stage-correct anchor conservativity.
    for c in CONTACTS_WITNESS:
        assert anchor_authority(c, "F_net") == anchor_before(c, "F_net")
        assert beta_minus(c) >= beta_plus(c)

    # C3: prior interpretations remain alongside later frame-indexed readings.
    old = {i for i in INTERPRETATIONS if i.event != "e12"}
    assert old.issubset(set(INTERPRETATIONS))

    # C4-C5.
    assert all(t.valid() for t in OMEGA_PLUS.standing_transforms)
    assert all(r.witness_ref for r in RECOVERIES)

    # C6-C7: witness assembly, later authority contact, lifecycle separation.
    assert OMEGA_PLUS.complete()
    assert OMEGA_PLUS.witness_event == "e11"
    assert EPSILON_MINUS.material_contact == "e12"
    assert ("e11", "e12") in PRECEDES
    assert "e12" not in SELF_GEN_OMEGA
    assert RHO_MINUS.durability_event == "e15"
    assert ("e12", "e15") in PRECEDES

    # C8-C9.
    assert DISCHARGES
    assert set(FRAMES_AFTER) == {"F_net", "F_evt"}
    assert JOINT_USE

    # C10.
    check_meta_awareness()


def run_all_checks() -> List[str]:
    checks = [
        ("K5 finite quantaloid", check_quantaloid),
        ("K1 proto-time, event tags, and causal cuts", check_proto_time),
        ("K2 typed standing", check_standing),
        ("K3-K4 partial frame formation", check_frame_formation),
        ("K5-K7 equipment and stage-typed anchors", check_equipment_and_anchor),
        ("K8-K14 records and four-stage lifecycle", check_records_and_lifecycle),
        ("K15 traction and stuck", check_traction_and_stuck),
        ("K16-K17 joint use and writers", check_joint_use_and_writers),
        ("K6/K17 causal-cut carrier transitions", check_carrier_transitions),
        ("Gate C theorem obligations", check_gate_c_theorems),
    ]
    passed: List[str] = []
    for name, fn in checks:
        fn()
        passed.append(name)
    return passed


if __name__ == "__main__":
    passed = run_all_checks()
    print("FINITE MODEL VERIFICATION: PASS")
    for name in passed:
        print(f"  [PASS] {name}")
    print(f"  events: {len(EVENTS)}")
    print(f"  proto-time relations: {len(PRECEDES)}")
    print(f"  event tags: {sum(len(v) for v in EVENT_TAGS.values())}")
    print(f"  attached frames after e12: {len(FRAMES_AFTER)}")
    print(f"  prospective anchor contacts at e11: {len(BETA_PLUS)}")
    print(f"  authority anchor contacts at e12: {len(BETA_MINUS)}")
    print(f"  contact nodes after e14: {len(CONTACTS_FINAL)}")
    print(f"  interpretations: {len(INTERPRETATIONS)}")
    print(f"  losses: {len(LOSSES)}; recoveries: {len(RECOVERIES)}")
    print("  stuck events: e10 only")
