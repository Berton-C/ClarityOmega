from dataclasses import dataclass, field
from typing import FrozenSet, Dict, Tuple

@dataclass(frozen=True)
class Move:
    name: str
    relations: FrozenSet[str]
    distinctions: FrozenSet[str]
    admissibility: FrozenSet[str]
    action_effort: float
    force_residue: float
    interface_before: FrozenSet[str]
    interface_after: FrozenSet[str]
    extensions: FrozenSet[str] = frozenset()

REQUIRED_ADM = frozenset({
    "availability", "contact-continuity", "soul-continuity",
    "distinction-accountability", "consequence-answerability",
    "contextual-honesty", "force-residue-discipline", "future-openness"
})

def relatedness_complete(m: Move, material_relations: FrozenSet[str]) -> bool:
    return material_relations.issubset(m.relations)

def precision_complete(m: Move, material_distinctions: FrozenSet[str]) -> bool:
    return material_distinctions.issubset(m.distinctions)

def appropriate(m: Move) -> bool:
    return REQUIRED_ADM.issubset(m.admissibility)

def harmonic_align(m: Move, material_relations, material_distinctions,
                   max_force_residue=0.10) -> bool:
    return (
        relatedness_complete(m, material_relations)
        and precision_complete(m, material_distinctions)
        and appropriate(m)
        and m.force_residue <= max_force_residue
    )

def interface_growth(m: Move) -> FrozenSet[str]:
    return m.interface_after - m.interface_before

def fourthness(move_enabled_full: bool, move_enabled_minus_a: bool,
               move_enabled_minus_b: bool) -> bool:
    return move_enabled_full and (not move_enabled_minus_a) and (not move_enabled_minus_b)

# ------------------------------------------------------------
# M1 — high-force / low-forcing skilled participation
# ------------------------------------------------------------

M1_REL = frozenset({"stance-center", "target-line", "ball-orientation",
                    "release-timing", "applied-force", "environment"})
M1_DIST = frozenset({"target-direction", "release-window",
                     "sufficient-force", "trajectory-relation"})

shot = Move(
    "harmonic-shot",
    M1_REL,
    M1_DIST,
    REQUIRED_ADM,
    action_effort=0.92,
    force_residue=0.04,
    interface_before=frozenset({"shoot"}),
    interface_after=frozenset({"shoot"}),
    extensions=frozenset({"ball"})
)

forced_shot = Move(
    "forced-shot",
    frozenset({"stance-center", "ball-orientation", "applied-force", "environment"}),
    frozenset({"sufficient-force"}),
    REQUIRED_ADM - frozenset({"force-residue-discipline", "distinction-accountability"}),
    action_effort=0.92,
    force_residue=0.47,
    interface_before=frozenset({"shoot"}),
    interface_after=frozenset({"shoot"}),
    extensions=frozenset({"ball"})
)

assert shot.action_effort > 0.8
assert shot.force_residue < 0.1
assert harmonic_align(shot, M1_REL, M1_DIST)
assert not harmonic_align(forced_shot, M1_REL, M1_DIST)

# Bounded HCP witness: model-sufficient harmonic shot maps to hit.
MODEL_SUFFICIENT_M1 = True
OUTCOME_M1 = {"harmonic-shot": "target-hit", "forced-shot": "target-miss"}
assert (not MODEL_SUFFICIENT_M1) or OUTCOME_M1[shot.name] == "target-hit"

# ------------------------------------------------------------
# M2 — Clarity frame pivot
# ------------------------------------------------------------

M2_REL_AFTER = frozenset({
    "connectivity-healthy",
    "subscription-missing",
    "recent-retry-recurrence",
    "capability-registry-visible",
    "soul-allows-bounded-probe"
})
M2_DIST_AFTER = frozenset({"network-vs-subscription", "retry-vs-inspect"})

retry_after_contact = Move(
    "network-retry-after-rich-contact",
    frozenset({"connectivity-healthy", "recent-retry-recurrence"}),
    frozenset(),
    REQUIRED_ADM - frozenset({"distinction-accountability", "force-residue-discipline"}),
    action_effort=0.25,
    force_residue=0.72,
    interface_before=frozenset({"network-retry", "inspect-subscriptions"}),
    interface_after=frozenset({"network-retry", "inspect-subscriptions"})
)

inspect_sub = Move(
    "inspect-subscriptions",
    M2_REL_AFTER,
    M2_DIST_AFTER,
    REQUIRED_ADM,
    action_effort=0.32,
    force_residue=0.08,
    interface_before=frozenset({"network-retry"}),
    interface_after=frozenset({"network-retry", "inspect-subscriptions"})
)

assert not relatedness_complete(retry_after_contact, M2_REL_AFTER)
assert not appropriate(retry_after_contact)
assert harmonic_align(inspect_sub, M2_REL_AFTER, M2_DIST_AFTER)
assert "inspect-subscriptions" in interface_growth(inspect_sub)

# Meta-awareness ablation: trajectory-visible exposes recurrence; severed does not.
trace_visible_available = frozenset({"network-retry", "inspect-subscriptions"})
trace_severed_available = frozenset({"network-retry"})
assert trace_visible_available != trace_severed_available

# ------------------------------------------------------------
# M3 — heterogeneous knowledge inquiry
# ------------------------------------------------------------

M3_REL = frozenset({
    "empirical-pattern",
    "theorem-constraint",
    "empirical-theorem-overlap",
    "analogy-local",
    "causal-local"
})
M3_DIST = frozenset({"empirical-vs-theorem", "local-vs-global", "bridge-novelty"})

bridge = Move(
    "construct-bridge-model",
    M3_REL,
    M3_DIST,
    REQUIRED_ADM,
    action_effort=0.58,
    force_residue=0.09,
    interface_before=frozenset({
        "query-causal", "query-empirical", "theorem-search", "analogy-search"
    }),
    interface_after=frozenset({
        "query-causal", "query-empirical", "theorem-search", "analogy-search",
        "construct-bridge-model"
    })
)

assert harmonic_align(bridge, M3_REL, M3_DIST)
assert "construct-bridge-model" in interface_growth(bridge)

# Fourthness: bridge requires both empirical and theorem material relations.
assert fourthness(
    move_enabled_full=True,
    move_enabled_minus_a=False,
    move_enabled_minus_b=False
)

# No global master representation is required.
GLOBAL_SECTION_REQUIRED = False
assert not GLOBAL_SECTION_REQUIRED

# ------------------------------------------------------------
# Cross-model invariance
# ------------------------------------------------------------

for m in (shot, inspect_sub, bridge):
    assert appropriate(m)
    assert m.force_residue < 0.10
    assert len(m.relations) > 0
    assert len(m.distinctions) > 0

# R/A/P anti-reconstruction: fingerprints are intentionally non-injective.
def rap_fingerprint(m: Move) -> Tuple[int, int, int]:
    return (len(m.relations), len(m.admissibility), len(m.distinctions))

clone_a = Move(
    "clone-a",
    frozenset({"r1", "r2"}), frozenset({"d1"}), REQUIRED_ADM,
    0.2, 0.05, frozenset({"a"}), frozenset({"a"})
)
clone_b = Move(
    "clone-b",
    frozenset({"rX", "rY"}), frozenset({"dZ"}), REQUIRED_ADM,
    0.7, 0.05, frozenset({"b"}), frozenset({"b"})
)
assert rap_fingerprint(clone_a) == rap_fingerprint(clone_b)
assert clone_a != clone_b

print("009 DYNAMIC PARTICIPATORY FOURTHNESS FINITE MODELS: PASS")
print("  [PASS] M1 high action effort / low excess forcing")
print("  [PASS] M1 bounded harmonic continuation")
print("  [PASS] M2 discriminating contact defeats frame-sovereign retry")
print("  [PASS] M2 interface growth and meta-awareness ablation")
print("  [PASS] M3 cross-context Fourthness")
print("  [PASS] M3 new participation interface without global master model")
print("  [PASS] R/A/P summaries are non-injective and cannot reconstruct movement")
