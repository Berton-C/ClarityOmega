#!/usr/bin/env python3
"""0g adversarial suite for the Gate C finite verification.

Runs from repo root (here: alongside 0f_gate_c_finite_model_check.py).

Three result classes:
  DETECTED   the shipped checker rejects the adversarial model (checker is sensitive here)
  VACUOUS    the shipped checker ACCEPTS a model that violates 0e/006 intent
             (the corresponding law is verified by stipulation, not by structure)
  COUNTERMODEL  a fully checker-passing model that violates intent end to end

Every adversarial construction names the 0e law or Gate C obligation it targets.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import sys
from typing import Callable, List, Tuple

SPEC_PATH = "0f_gate_c_finite_model_check.py"

spec = importlib.util.spec_from_file_location("gate_c_spec", SPEC_PATH)
S = importlib.util.module_from_spec(spec)
sys.modules["gate_c_spec"] = S
spec.loader.exec_module(S)

R = dataclasses.replace


def run_full(m) -> Tuple[bool, str]:
    """Run every shipped check against model m. Returns (passed, first_failure)."""
    checks: List[Tuple[str, Callable]] = [
        ("event roles", lambda: S.check_event_roles(m)),
        ("raw fields", lambda: S.check_raw_fields_and_formations(m)),
        ("doctrine", lambda: S.check_doctrine_interface(m)),
        ("record completeness", lambda: S.check_attachment_record_completeness(m)),
        ("standings", lambda: S.check_standings(m)),
        ("anchor spines", lambda: S.check_anchor_spines(m)),
        ("anchor isolation", lambda: S.check_anchor_writer_isolation(m)),
        ("lifecycle+guards", lambda: S.check_lifecycle_and_guards(m)),
        ("history", lambda: S.check_history_and_interpretation(m)),
        ("loss/recovery", lambda: S.check_loss_recovery(m)),
        ("open/discharge", lambda: S.check_carrier_open_discharge(m)),
        ("prospective/retrospective", lambda: S.check_prospective_retrospective(m)),
        ("stuck", lambda: S.check_stuck_and_contact_starvation(m)),
        ("joint use", lambda: S.check_nonamalgamation_and_joint_use(m)),
        ("writer closure", lambda: S.check_writer_inventory(m)),
        ("failed attachment", lambda: S.check_failed_attachment(m)),
        ("meta-awareness", lambda: S.check_causal_meta_awareness(m)),
    ]
    for name, fn in checks:
        try:
            fn()
        except AssertionError as exc:
            return False, f"{name}: {exc}"
    return True, ""


def rebuild_transaction(m, ev: int) -> None:
    """Recompute the TransactionRecord for event ev from m.writers so writer-closure
    bookkeeping stays consistent after a patch edit."""
    patches = [p for p in m.writers if p.event == ev]
    old = m.transactions[ev]
    m.transactions[ev] = S.TransactionRecord(
        event=ev,
        patch_keys=tuple((p.writer, p.payload_ref) for p in patches),
        pre_cut=old.pre_cut,
        post_cut=old.post_cut,
    )


# ---------------------------------------------------------------------------
# Part 1: mutation tests (checker sensitivity) and vacuity probes
# ---------------------------------------------------------------------------

RESULTS: List[str] = []


def record(label: str, target: str, mutated_model, expect_detected: bool, intent_note: str) -> None:
    passed, failure = run_full(mutated_model)
    if not passed:
        verdict = "DETECTED" if expect_detected else "DETECTED (better than predicted)"
    else:
        verdict = "VACUOUS" if not expect_detected else "VACUOUS (SENSITIVITY GAP: expected detection)"
    RESULTS.append(f"[{verdict}] {label}")
    RESULTS.append(f"    target law: {target}")
    if not passed:
        RESULTS.append(f"    checker failure: {failure}")
    else:
        RESULTS.append(f"    checker: FULL PASS on the adversarial model")
    RESULTS.append(f"    intent: {intent_note}")


def m_base():
    return S.build_model()


# --- M1: authority not strictly later than witness assembly ----------------

def mutate_M1():
    m = m_base()
    eps = m.authorities["eps_evt"]
    omega = m.witnesses[eps.witness]
    m.witnesses[eps.witness] = R(omega, assembled_at=12)  # assembly at the authority event itself
    return m


# --- M2: authority contact inside the self-generation cone -----------------

def mutate_M2():
    m = m_base()
    eps = m.authorities["eps_evt"]
    omega = m.witnesses[eps.witness]
    c_ev = m.contacts[eps.contact].event
    # declare the cited contact self-generated (and keep cone shape constraints satisfied
    # by also widening assembly so the forward-lineage constraint holds)
    m.witnesses[eps.witness] = R(
        omega,
        assembled_at=c_ev,
        self_generation=frozenset(set(omega.self_generation) | {c_ev}),
        support=frozenset(set(omega.support) | {c_ev}),
    )
    return m


# --- M3: materiality flag withdrawn ----------------------------------------

def mutate_M3():
    m = m_base()
    m.authorities["eps_evt"] = R(m.authorities["eps_evt"], material=False)
    return m


# --- M4: recovery without prior loss ---------------------------------------

def mutate_M4():
    m = m_base()
    r0 = m.recoveries[0]
    m.recoveries = [R(r0, distinction="never-lost-distinction")]
    return m


# --- M5: provenance promotion to CONTACT -----------------------------------

def mutate_M5():
    m = m_base()
    wid, omega = next(iter(m.witnesses.items()))
    st = omega.standing_transforms[0]
    bad = R(st, old_kind=S.ProvKind.INFERENCE, new_kind=S.ProvKind.CONTACT)
    m.witnesses[wid] = R(omega, standing_transforms=(bad,) + omega.standing_transforms[1:])
    return m


# --- M5b: provenance promotion BELOW the contact apex ----------------------

def mutate_M5b():
    m = m_base()
    wid, omega = next(iter(m.witnesses.items()))
    st = omega.standing_transforms[0]
    kinds = list(S.ProvKind)
    # promote GENERATION -> INFERENCE (or any strictly-higher non-contact kind pair available)
    gen = S.ProvKind.GENERATION if hasattr(S.ProvKind, "GENERATION") else kinds[-1]
    inf = S.ProvKind.INFERENCE if hasattr(S.ProvKind, "INFERENCE") else kinds[1]
    bad = R(st, old_kind=gen, new_kind=inf)
    m.witnesses[wid] = R(omega, standing_transforms=(bad,) + omega.standing_transforms[1:])
    return m


# --- M6: interpretation id rewritten ---------------------------------------

def mutate_M6():
    m = m_base()
    i0 = m.interpretations[0]
    m.interpretations = list(m.interpretations) + [R(i0, content=i0.content + " REWRITTEN")]
    return m


# --- M7: prior anchor component rewritten ----------------------------------

def mutate_M7():
    m = m_base()
    a0 = m.anchors[0]
    m.anchors = list(m.anchors) + [R(a0, grade=1.0, event=max(a0.event + 1, 13))]
    return m


# --- M8: unlisted writer ----------------------------------------------------

def mutate_M8():
    m = m_base()
    m.writers = list(m.writers) + [
        S.WriterRecord(event=13, writer="renderer", components=frozenset({"I"}), payload_ref="sneak")
    ]
    rebuild_transaction(m, 13)
    return m


# --- V1: authoritative with NO probe stage (0e 6.3 requires prior probe) ----

def mutate_V1():
    m = m_base()
    m.lifecycles = [r for r in m.lifecycles
                    if not (r.frame == "F_evt" and r.stage == S.Stage.PROBE)]
    # remove the authorizeProbe writer patch and keep the transaction consistent
    m.writers = [p for p in m.writers if not (p.writer == "authorizeProbe" and p.payload_ref.endswith("evt"))]
    for ev in list(m.transactions):
        rebuild_transaction(m, ev)
    return m


# --- V2: dangling reintroduction witness ------------------------------------

def mutate_V2():
    m = m_base()
    r0 = m.recoveries[0]
    m.recoveries = [R(r0, witness_kind="renewed-contact", witness_ref="ghost-contact-does-not-exist")]
    return m


# --- V3: stale-support authority contact (event index late, content old) ----

def mutate_V3():
    m = m_base()
    eps = m.authorities["eps_evt"]
    real = m.contacts[eps.contact]
    stale_standing = S.contact_standing(2)  # standing/support rooted at e2, pre-formation
    stale = R(real, id="c12_stale_echo", standing=stale_standing,
              payload="cached pre-formation diagnostic replayed")
    m.contacts["c12_stale_echo"] = stale
    m.writers = list(m.writers) + [
        S.WriterRecord(event=stale.event, writer="recordContact",
                       components=frozenset({"C", "H"}), payload_ref="c12_stale_echo")
    ]
    rebuild_transaction(m, stale.event)
    m.authorities["eps_evt"] = R(eps, contact="c12_stale_echo",
                                 support=frozenset(set(eps.support) | {stale.event}))
    admit_in_doctrine(m, "c12_stale_echo", eps.witness)
    return m


def admit_in_doctrine(m, contact_id: str, witness_id: str) -> None:
    """Extend the finite doctrine table to admit the new contact as an authority
    route and as material. The table is stipulated data in the shipped model, so
    this extension is exactly as lawful as the original entries: the point of the
    countermodel is that the signature imposes no structural necessary condition
    on what a doctrine may admit."""
    d = m.doctrine
    m.doctrine = R(
        d,
        authority_pairs=frozenset(set(d.authority_pairs) | {("F_evt", contact_id)}),
        material_pairs=frozenset(set(d.material_pairs) | {(contact_id, witness_id)}),
    )


# --- V4: self-generation cone under-declared to empty -----------------------

def mutate_V4():
    m = m_base()
    eps = m.authorities["eps_evt"]
    omega = m.witnesses[eps.witness]
    m.witnesses[eps.witness] = R(omega, self_generation=frozenset())
    return m


# --- V5: warrant increase citing an irrelevant contact ----------------------

def mutate_V5():
    m = m_base()
    wid, omega = next(iter(m.witnesses.items()))
    st = omega.standing_transforms[0]
    irrelevant = next(cid for cid, c in m.contacts.items() if c.event <= 2)
    bumped = R(st, warrant_after=min(1.0, st.warrant_before + 0.5),
               evidence_contacts=(irrelevant,))
    m.witnesses[wid] = R(omega, standing_transforms=(bumped,) + omega.standing_transforms[1:])
    return m


# ---------------------------------------------------------------------------
# Part 2: full-pass semantic countermodel (echo-authority laundering)
# ---------------------------------------------------------------------------

def countermodel_C1():
    """Echo-authority: replace the discriminating probe result with a contact that
    passes through the world but could not have returned otherwise (it restates the
    frame's own claim). Every structural condition of the shipped guard holds:
    strictly later than assembly, provenance CONTACT, outside the declared SelfGen,
    material=True (stipulated). The frame gains authority from evidence that
    discriminates nothing. Violates 0e 9.3 in intent (materially independent contact)
    and 006 21.2 (internal force mistaken for external warrant) while satisfying
    every mechanical check."""
    m = m_base()
    eps = m.authorities["eps_evt"]
    real = m.contacts[eps.contact]
    echo = R(real, id="c12_echo",
             payload="echo: the frame F_evt asserts the subscription is missing")
    m.contacts["c12_echo"] = echo
    m.writers = list(m.writers) + [
        S.WriterRecord(event=echo.event, writer="recordContact",
                       components=frozenset({"C", "H"}), payload_ref="c12_echo")
    ]
    rebuild_transaction(m, echo.event)
    m.authorities["eps_evt"] = R(eps, contact="c12_echo",
                                 support=frozenset(set(eps.support) | {echo.event}))
    admit_in_doctrine(m, "c12_echo", eps.witness)
    return m


def main() -> None:
    base_ok, base_fail = run_full(m_base())
    print("baseline shipped model:", "PASS" if base_ok else f"FAIL ({base_fail})")
    print()

    tests = [
        ("M1 authority-not-later-than-assembly", "0e 7.2 / K11 guard (e_f < e_a strict)", mutate_M1, True,
         "authority evidence must postdate witness assembly"),
        ("M2 self-generated authority contact", "0e 9.3 IndependentMaterial", mutate_M2, True,
         "evidence inside the self-generation cone cannot confer authority"),
        ("M3 materiality flag withdrawn", "0e 9.3 MaterialTo", mutate_M3, True,
         "shows the guard's materiality strength is exactly one stipulated boolean"),
        ("M4 recovery without prior loss", "0e W9 ledger discipline", mutate_M4, True,
         "recovery must reference a recorded loss"),
        ("M5 promotion to CONTACT", "0e W3 no provenance promotion (apex)", mutate_M5, True,
         "non-contact kinds must never become contact"),
        ("M5b promotion below the apex (GENERATION to INFERENCE)", "0e W3 no provenance promotion (full order)",
         mutate_M5b, False,
         "W3 requires NO promotion anywhere in the kind order; the check only guards the contact apex"),
        ("M6 interpretation rewrite", "0e W7 append-only interpretation", mutate_M6, True,
         "interpretation ids are immutable"),
        ("M7 anchor prior-row rewrite", "0e 3.4 anchor conservativity", mutate_M7, True,
         "prior anchor components may not be rewritten"),
        ("M8 unlisted writer (renderer)", "0e K17 writer closure", mutate_M8, True,
         "no renderer may hold write authority"),
        ("V1 authoritative with no probe stage", "0e 6.3 (authority requires prior/current probe eligibility)",
         mutate_V1, False,
         "the lifecycle check enforces rank monotonicity of existing records only; a missing stage is invisible"),
        ("V2 dangling reintroduction witness", "0e W9 (witness must exist and be of the cited kind)",
         mutate_V2, False,
         "witness_ref is only checked nonempty; a ghost reference reintroduces a lost distinction"),
        ("V3 stale-support authority contact", "0e 7.2 intent (later contact must carry post-formation information)",
         mutate_V3, False,
         "only the record event index is ordered; the contact's own support/freshness is never examined"),
        ("V4 self-generation cone declared empty", "0e 9.2 (SelfGen is a function of the derivation, K11)",
         mutate_V4, False,
         "the cone is self-declared data; under-declaration silently disables the independence guard"),
        ("V5 warrant increase via irrelevant contact", "0e W3 (warrant route must be a material evidence route)",
         mutate_V5, False,
         "any known contact id satisfies the evidence-route check; relevance is not examined"),
    ]

    for label, target, fn, expect, note in tests:
        record(label, target, fn(), expect, note)

    print("\n".join(RESULTS))
    print()

    cm = countermodel_C1()
    ok, fail = run_full(cm)
    print("[{}] C1 echo-authority countermodel".format("COUNTERMODEL (full pass)" if ok else "DETECTED"))
    print("    target: 0e 9.3 material independent contact; 006 test 21.2")
    if ok:
        print("    the shipped checker fully accepts authority conferred by a non-discriminating echo contact")
    else:
        print("    checker failure:", fail)


if __name__ == "__main__":
    main()
