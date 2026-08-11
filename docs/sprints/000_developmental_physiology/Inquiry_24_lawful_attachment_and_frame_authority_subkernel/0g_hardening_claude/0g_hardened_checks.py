#!/usr/bin/env python3
"""0g hardened checks.

Adds the six checks whose absence the adversarial suite demonstrated, then
re-runs every previously VACUOUS mutant and the full-pass countermodel C1 to
show each is now DETECTED, while the shipped base model still passes.

The checks are the finite shadows of the signature repairs proposed in 0g:
  HG1  route provenance on authority evidence      (repair G-ROUTE, toward G-DISC)
  HG2  post-formation freshness of authority support (repair G-FRESH)
  HG3  probe-before-authority                       (repair L-PROBE)
  HG4  resolvable reintroduction witnesses          (repair R-RES)
  HG5  full-order provenance non-promotion          (repair W3-FULL)
  HG6  self-generation lower bound recomputed       (repair SG-DERIVED, partial)
"""

from __future__ import annotations

import importlib.util
import sys

for name in ("gate_c_spec", "adv"):
    sys.modules.pop(name, None)

spec = importlib.util.spec_from_file_location("gate_c_spec", "0f_gate_c_finite_model_check.py")
S = importlib.util.module_from_spec(spec)
sys.modules["gate_c_spec"] = S
spec.loader.exec_module(S)

aspec = importlib.util.spec_from_file_location("adv", "0g_adversarial_suite.py")
A = importlib.util.module_from_spec(aspec)
sys.modules["adv"] = A
aspec.loader.exec_module(A)

require = S.require

# Hardening data: generating-route provenance for authority-eligible contacts.
# This table is the field the ContactRecord type is missing; in a repaired
# signature it lives ON the contact, written by recordContact from the
# consequence linkage, never stipulated separately.
AUTHORITY_CONTACT_SOURCE = {
    "c12_confirm": "a11_list",   # returned by the authorized probe
    "c3_ping": "a3_ping",        # returned by the network diagnostic
}

PROV_RANK = {
    S.ProvKind.CONTACT: 5,
    S.ProvKind.TESTIMONY: 4,
    S.ProvKind.MEMORY: 3,
    S.ProvKind.INFERENCE: 2,
    S.ProvKind.GENERATION: 1,
    S.ProvKind.SELF_TRACE: 0,
}


def hg1_route_provenance(m):
    for eps in m.authorities.values():
        require(eps.contact in AUTHORITY_CONTACT_SOURCE,
                f"authority {eps.id} cites a contact with no generating-route provenance")
        aid = AUTHORITY_CONTACT_SOURCE[eps.contact]
        require(aid in m.actions, f"authority {eps.id} route action {aid} does not exist")
        act = m.actions[aid]
        c = m.contacts[eps.contact]
        require(act.event <= c.event <= act.event + 1,
                f"authority {eps.id} route action and contact are temporally unlinked")


def hg2_freshness(m):
    for eps in m.authorities.values():
        omega = m.witnesses[eps.witness]
        c = m.contacts[eps.contact]
        require(any(e > omega.frame_formed_at for e in c.standing.support),
                f"authority {eps.id} evidence support is entirely pre-formation (stale)")


def hg3_probe_before_authority(m):
    probes = {(r.frame) : r.event for r in m.lifecycles if r.stage == S.Stage.PROBE}
    for r in m.lifecycles:
        if r.stage == S.Stage.AUTHORITATIVE:
            require(r.frame in probes and probes[r.frame] <= r.event,
                    f"authoritative {r.frame} has no prior or current probe-eligibility record")


def hg4_recovery_resolves(m):
    side_info = set()
    for w in m.witnesses.values():
        side_info |= set(w.retained_side_information.values()) | set(w.retained_side_information.keys())
    for r in m.recoveries:
        if r.witness_kind == "renewed-contact":
            require(r.witness_ref in m.contacts, f"recovery {r.id} cites a nonexistent contact")
        elif r.witness_kind == "other-frame":
            require(r.witness_ref in m.frames, f"recovery {r.id} cites a nonexistent frame")
        elif r.witness_kind == "retained-side-information":
            require(r.witness_ref in side_info, f"recovery {r.id} cites unretained side information")
        elif r.witness_kind == "reversible-route":
            require(r.witness_ref in m.actions, f"recovery {r.id} cites a nonexistent route")


def hg5_full_order_provenance(m):
    for w in m.witnesses.values():
        for st in w.standing_transforms:
            require(PROV_RANK[st.new_kind] <= PROV_RANK[st.old_kind],
                    f"standing transform {st.id} promotes provenance below the apex "
                    f"({st.old_kind.value} -> {st.new_kind.value})")


def hg6_selfgen_lower_bound(m):
    for w in m.witnesses.values():
        require(w.frame_formed_at in w.self_generation,
                f"witness {w.id} under-declares its self-generation cone "
                f"(formation event missing): the cone must be recomputed, not stipulated")


HARDENED = [hg1_route_provenance, hg2_freshness, hg3_probe_before_authority,
            hg4_recovery_resolves, hg5_full_order_provenance, hg6_selfgen_lower_bound]


def run_hardened(m):
    for fn in HARDENED:
        try:
            fn(m)
        except AssertionError as exc:
            return False, f"{fn.__name__}: {exc}"
    return True, ""


def full(m):
    ok, why = A.run_full(m)
    if not ok:
        return False, why
    return run_hardened(m)


def main():
    ok, why = full(A.m_base())
    print("base model under shipped + hardened checks:", "PASS" if ok else f"FAIL ({why})")
    print()
    cases = [
        ("M5b sub-apex provenance promotion", A.mutate_M5b),
        ("V1 authority with no probe stage", A.mutate_V1),
        ("V2 dangling reintroduction witness", A.mutate_V2),
        ("V3 stale-support authority contact", A.mutate_V3),
        ("V4 self-generation cone declared empty", A.mutate_V4),
        ("C1 echo-authority countermodel", A.countermodel_C1),
    ]
    all_closed = True
    for label, fn in cases:
        ok, why = full(fn())
        status = "STILL VACUOUS" if ok else "DETECTED"
        all_closed = all_closed and not ok
        print(f"[{status}] {label}")
        if not ok:
            print(f"    hardened failure: {why}")
    print()
    print("hardening result:", "all previously vacuous adversarial models are now detected"
          if all_closed else "GAPS REMAIN")


if __name__ == "__main__":
    main()
