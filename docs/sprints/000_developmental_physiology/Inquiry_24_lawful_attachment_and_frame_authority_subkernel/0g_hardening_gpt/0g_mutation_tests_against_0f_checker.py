#!/usr/bin/env python3
"""Mutation tests for the delivered 0f positive finite-model checker.

These tests ask whether the existing checker rejects explicit corruptions of its
hand-built Gate C model.  They complement, but do not replace, the abstract
countermodel search in 0g_adversarial_countermodel_search_and_hardened_proofs.py.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import importlib.util
import sys
from typing import Callable, List, Tuple

ROOT = Path('/mnt/data')
SOURCE = ROOT / '0f_gate_c_finite_model_check.py'
REPORT = ROOT / '0g_0f_Checker_Mutation_Test_Report.txt'

spec = importlib.util.spec_from_file_location('gate_c', SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit('Cannot load 0f checker')
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def expect_rejection(name: str, mutate: Callable, check: Callable) -> Tuple[str, bool, str]:
    model = mod.build_model()
    mutate(model)
    try:
        check(model)
    except AssertionError as exc:
        return name, True, str(exc)
    return name, False, 'mutation was not rejected'


def mutate_provenance_promotion(m):
    omega = m.witnesses['omega_evt']
    transforms = list(omega.standing_transforms)
    transforms[0] = replace(
        transforms[0], old_kind=mod.ProvKind.INFERENCE, new_kind=mod.ProvKind.CONTACT
    )
    m.witnesses['omega_evt'] = replace(omega, standing_transforms=tuple(transforms))


def mutate_materiality(m):
    eps = m.authorities['eps_evt']
    m.authorities['eps_evt'] = replace(eps, material=False)


def mutate_anchor_rewrite(m):
    a = next(x for x in m.anchors if x.frame == 'F_net' and x.contact == 'c1')
    m.anchors.append(replace(a, grade=0.5, event=15, writer='recordContact'))


def mutate_recovery_witness(m):
    r = m.recoveries[0]
    m.recoveries[0] = replace(r, witness_ref='')


def mutate_trace_grounding(m):
    t = m.traces['t10_visible']
    m.traces['t10_visible'] = replace(t, grounded=False, action_refs=tuple(), consequence_refs=tuple())


def mutate_predicted_as_authority(m):
    # Make the F_evt authority lifecycle point to the predicted reach id instead
    # of the later authority evidence id. The prospective/retrospective checker
    # should reject this collapse.
    for i, rec in enumerate(m.lifecycles):
        if rec.frame == 'F_evt' and rec.stage == mod.Stage.AUTHORITATIVE:
            m.lifecycles[i] = replace(rec, witness='pr_evt')
            return
    raise AssertionError('F_evt authority lifecycle missing')


tests: List[Tuple[str, Callable, Callable]] = [
    ('provenance promotion', mutate_provenance_promotion, mod.check_attachment_record_completeness),
    ('authority without materiality', mutate_materiality, mod.check_lifecycle_and_guards),
    ('anchor key rewrite', mutate_anchor_rewrite, mod.check_anchor_writer_isolation),
    ('empty recovery witness', mutate_recovery_witness, mod.check_loss_recovery),
    ('narration without grounded trace', mutate_trace_grounding, mod.check_causal_meta_awareness),
    ('predicted reach used as authority', mutate_predicted_as_authority, mod.check_prospective_retrospective),
]

results = [expect_rejection(name, mutate, check) for name, mutate, check in tests]
lines = ['0g MUTATION TESTS AGAINST DELIVERED 0f CHECKER', '=' * 64, '']
for name, passed, reason in results:
    lines.append(f"[{'PASS' if passed else 'FAIL'}] {name}")
    lines.append(f'       {reason}')
lines.append('')
lines.append(f"Rejected mutations: {sum(p for _, p, _ in results)} / {len(results)}")
lines.append('Interpretation: the positive checker is sensitive to several intended local violations,')
lines.append('but these mutation tests do not establish theorem generality or close the abstract')
lines.append('countermodels found by the separate 0g search.')
text = '\n'.join(lines) + '\n'
REPORT.write_text(text, encoding='utf-8')
print(text, end='')
raise SystemExit(0 if all(p for _, p, _ in results) else 1)
