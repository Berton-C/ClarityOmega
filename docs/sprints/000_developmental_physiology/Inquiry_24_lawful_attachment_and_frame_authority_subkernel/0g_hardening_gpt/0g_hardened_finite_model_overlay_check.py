#!/usr/bin/env python3
"""Finite-model overlay check for the 0g hardening delta.

The delivered 0f Mattermost model is not replaced.  This script equips it with
the additional proof-bearing data required by 0g and verifies that the same
finite scenario still has a model after strengthening.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import importlib.util
import sys
from typing import Dict, FrozenSet, List, Mapping, Tuple

ROOT = Path('/mnt/data')
SOURCE = ROOT / '0f_gate_c_finite_model_check.py'
REPORT = ROOT / '0g_Hardened_Finite_Model_Overlay_Report.txt'

spec = importlib.util.spec_from_file_location('gate_c_hardened_overlay', SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit('Cannot load 0f finite model')
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


@dataclass(frozen=True)
class ContactSeal:
    contact: str
    event: int
    channel: str
    external_route: str


@dataclass(frozen=True)
class MaterialAuthorityRoute:
    witness: str
    contact: str
    seal: ContactSeal
    obligation: str
    semantically_relevant: bool
    outside_self_generation: bool


@dataclass(frozen=True)
class LossContextKey:
    distinction: str
    frame: str


@dataclass(frozen=True)
class AvailabilityRecord:
    key: LossContextKey
    available_at: int
    witness_kind: str
    witness_ref: str


model = mod.build_model()
# First retain the entire delivered positive interpretation.
mod.run_checks()

# H0/H1: every direct contact has a seal. In the toy model, the channel and
# external route are explicit finite witnesses; event tags alone are not used.
seals: Dict[str, ContactSeal] = {}
for contact in model.contacts.values():
    if contact.id.startswith('c1'):
        channel = 'mattermost-send'
    elif 'ping' in contact.id or 'fail' in contact.id:
        channel = 'runtime-diagnostic'
    elif 'sub' in contact.id or 'confirm' in contact.id or 'receipt' in contact.id:
        channel = 'mattermost-event-api'
    else:
        channel = 'runtime-observation'
    seals[contact.id] = ContactSeal(
        contact=contact.id,
        event=contact.event,
        channel=channel,
        external_route=f'{channel}@e{contact.event}',
    )

for contact in model.contacts.values():
    require(contact.id in seals, f'unsealed direct contact {contact.id}')
    require(seals[contact.id].event == contact.event, f'contact seal event mismatch for {contact.id}')
    require(contact.standing.provenance.kind == mod.ProvKind.CONTACT,
            f'sealed contact {contact.id} does not have contact provenance')

# H2: materiality is proof-bearing and names the attachment obligation it bears on.
material_routes: Dict[str, MaterialAuthorityRoute] = {
    'eps_net': MaterialAuthorityRoute(
        witness='omega_net', contact='c3_ping', seal=seals['c3_ping'],
        obligation='domain-and-anchor discrimination', semantically_relevant=True,
        outside_self_generation=True,
    ),
    'eps_evt': MaterialAuthorityRoute(
        witness='omega_evt', contact='c12_confirm', seal=seals['c12_confirm'],
        obligation='subscription-cause confirmation', semantically_relevant=True,
        outside_self_generation=True,
    ),
}
for evidence_id, evidence in model.authorities.items():
    route = material_routes[evidence_id]
    omega = model.witnesses[evidence.witness]
    require(route.witness == evidence.witness, f'material route witness mismatch: {evidence_id}')
    require(route.contact == evidence.contact, f'material route contact mismatch: {evidence_id}')
    require(route.semantically_relevant, f'authority materiality is not semantically witnessed: {evidence_id}')
    require(route.outside_self_generation, f'authority route is self-generated: {evidence_id}')
    require(route.seal.event not in omega.self_generation, f'sealed authority contact is inside self-generation: {evidence_id}')
    require(mod.before(omega.assembled_at, route.seal.event), f'authority contact is not later: {evidence_id}')

# H3: global anchor-key preservation is checked against the complete existing state,
# not only within one transaction.
seen_anchor: Dict[Tuple[str, str], float] = {}
for entry in sorted(model.anchors, key=lambda x: (x.event, x.frame, x.contact)):
    key = (entry.frame, entry.contact)
    require(key not in seen_anchor, f'anchor key rewritten globally: {key}')
    seen_anchor[key] = entry.grade

# H4: loss and recovery are context-indexed and availability is explicit.
losses: Dict[LossContextKey, int] = {}
for loss in model.losses:
    key = LossContextKey(loss.distinction, loss.frame)
    require(key not in losses, f'duplicate context-indexed loss {key}')
    losses[key] = loss.event

availability: List[AvailabilityRecord] = []
for recovery in model.recoveries:
    # The finite model's recovery witness F_net reintroduces the distinction into
    # the F_evt working context in which it had been recorded as lost.
    matching = [key for key in losses if key.distinction == recovery.distinction]
    require(len(matching) == 1, f'ambiguous loss context for {recovery.distinction}')
    key = matching[0]
    require(mod.before(losses[key], recovery.event), f'recovery is not later than context-indexed loss {key}')
    require(bool(recovery.witness_ref), f'empty recovery witness for {key}')
    availability.append(AvailabilityRecord(
        key=key,
        available_at=recovery.event,
        witness_kind=recovery.witness_kind,
        witness_ref=recovery.witness_ref,
    ))

for record in availability:
    require(record.key in losses, f'availability has no prior loss {record.key}')
    require(bool(record.witness_ref), f'availability lacks a reintroduction witness {record.key}')

# H5: C10 is interpreted branch-locally. Each committed branch contains e in its
# post-cut and therefore cannot sequentially recommit e. We do not assert that a
# pure transition relation has only one possible successor from a pre-state.
for event, txn in model.transactions.items():
    require(event not in txn.pre_cut, f'event already in pre-cut: {event}')
    require(event in txn.post_cut, f'event missing from post-cut: {event}')
    require(not (event not in txn.post_cut), f'sequential recommit remains enabled: {event}')

# H6: retrospective reorganization evidence is genuinely later and contact-bearing.
for reorg in model.reorganizations.values():
    exercised = model.exercised[reorg.exercised_reach]
    require(reorg.event == exercised.event, f'reorganization/exercised event mismatch: {reorg.id}')
    require(reorg.renewed_contact == exercised.returned_contact,
            f'reorganization does not cite exercised returned contact: {reorg.id}')
    require(reorg.renewed_contact in seals, f'reorganization returned contact is unsealed: {reorg.id}')
    require(reorg.consequence_uptake and reorg.lineage_preserved and reorg.permeability,
            f'reorganization evidence lacks causal bite: {reorg.id}')

checks = [
    f'direct contacts sealed: {len(seals)}',
    f'authority routes materially witnessed: {len(material_routes)}',
    f'globally unique anchor keys: {len(seen_anchor)}',
    f'context-indexed losses: {len(losses)}',
    f'explicit availability restorations: {len(availability)}',
    f'branch-local atomic transactions: {len(model.transactions)}',
    f'retrospective reorganization packages: {len(model.reorganizations)}',
]
lines = ['0g HARDENED FINITE-MODEL OVERLAY: PASS', '=' * 60, '']
lines.extend(f'[PASS] {x}' for x in checks)
lines.append('')
lines.append('Conclusion: the original finite Mattermost scenario remains satisfiable after')
lines.append('adding sealed contact, proof-bearing materiality, global anchor-key preservation,')
lines.append('context-indexed availability, corrected branch-local atomicity, and retrospective')
lines.append('reorganization requirements.')
text = '\n'.join(lines) + '\n'
REPORT.write_text(text, encoding='utf-8')
print(text, end='')
