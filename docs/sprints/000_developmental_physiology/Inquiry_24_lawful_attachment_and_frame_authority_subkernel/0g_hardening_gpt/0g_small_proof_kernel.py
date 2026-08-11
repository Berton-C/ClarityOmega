#!/usr/bin/env python3
"""Tiny proof-term checker used as an independent hardening cross-check.

The kernel checks explicit intuitionistic propositional proof terms.  It is not
an encoding of the full dependent K0-K17 signature; it checks the corrected
logical skeleton of the theorem obligations attacked in 0g.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Tuple

REPORT = Path('/mnt/data/0g_Small_Proof_Kernel_Report.txt')


class Formula:
    pass


@dataclass(frozen=True)
class Atom(Formula):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Bottom(Formula):
    def __str__(self) -> str:
        return '⊥'


BOT = Bottom()


@dataclass(frozen=True)
class Imp(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f'({self.left} → {self.right})'


@dataclass(frozen=True)
class And(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f'({self.left} ∧ {self.right})'


@dataclass(frozen=True)
class Or(Formula):
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f'({self.left} ∨ {self.right})'


def Not(a: Formula) -> Formula:
    return Imp(a, BOT)


class Proof:
    pass


@dataclass(frozen=True)
class Hyp(Proof):
    name: str


@dataclass(frozen=True)
class ImpIntro(Proof):
    name: str
    assumption: Formula
    body: Proof


@dataclass(frozen=True)
class ImpElim(Proof):
    fn: Proof
    arg: Proof


@dataclass(frozen=True)
class AndIntro(Proof):
    left: Proof
    right: Proof


@dataclass(frozen=True)
class AndElimLeft(Proof):
    pair: Proof


@dataclass(frozen=True)
class AndElimRight(Proof):
    pair: Proof


@dataclass(frozen=True)
class OrIntroLeft(Proof):
    proof: Proof
    right: Formula


@dataclass(frozen=True)
class OrIntroRight(Proof):
    left: Formula
    proof: Proof


@dataclass(frozen=True)
class FalseElim(Proof):
    false_proof: Proof
    target: Formula


class ProofError(Exception):
    pass


def check(proof: Proof, context: Mapping[str, Formula]) -> Formula:
    if isinstance(proof, Hyp):
        try:
            return context[proof.name]
        except KeyError as exc:
            raise ProofError(f'unknown hypothesis {proof.name}') from exc
    if isinstance(proof, ImpIntro):
        extended = dict(context)
        if proof.name in extended:
            raise ProofError(f'duplicate local hypothesis {proof.name}')
        extended[proof.name] = proof.assumption
        return Imp(proof.assumption, check(proof.body, extended))
    if isinstance(proof, ImpElim):
        fn_type = check(proof.fn, context)
        arg_type = check(proof.arg, context)
        if not isinstance(fn_type, Imp):
            raise ProofError(f'implication elimination on non-implication {fn_type}')
        if fn_type.left != arg_type:
            raise ProofError(f'implication argument mismatch: expected {fn_type.left}, got {arg_type}')
        return fn_type.right
    if isinstance(proof, AndIntro):
        return And(check(proof.left, context), check(proof.right, context))
    if isinstance(proof, AndElimLeft):
        pair_type = check(proof.pair, context)
        if not isinstance(pair_type, And):
            raise ProofError(f'left projection on non-conjunction {pair_type}')
        return pair_type.left
    if isinstance(proof, AndElimRight):
        pair_type = check(proof.pair, context)
        if not isinstance(pair_type, And):
            raise ProofError(f'right projection on non-conjunction {pair_type}')
        return pair_type.right
    if isinstance(proof, OrIntroLeft):
        return Or(check(proof.proof, context), proof.right)
    if isinstance(proof, OrIntroRight):
        return Or(proof.left, check(proof.proof, context))
    if isinstance(proof, FalseElim):
        got = check(proof.false_proof, context)
        if got != BOT:
            raise ProofError(f'false elimination requires ⊥, got {got}')
        return proof.target
    raise ProofError(f'unknown proof term {type(proof).__name__}')


def expect(name: str, context: Mapping[str, Formula], proof: Proof, goal: Formula) -> Tuple[str, bool, str]:
    try:
        inferred = check(proof, context)
        if inferred != goal:
            return name, False, f'goal mismatch: inferred {inferred}; expected {goal}'
        return name, True, str(goal)
    except ProofError as exc:
        return name, False, str(exc)


# Atoms
Authority = Atom('Authority')
ClosureOnly = Atom('ClosureOnly')
Later = Atom('Later')
Material = Atom('Material')
Outside = Atom('OutsideSelfGen')
GuardBasis = And(Later, And(Material, Outside))

DirectProv = Atom('DirectProv')
Seal = Atom('Seal')
Generated = Atom('Generated')

Commit = Atom('Commit')
PostHasE = Atom('PostHasE')
EnabledPost = Atom('EnabledPost')
SecondCommit = Atom('SecondSequentialCommit')

PatchWF = Atom('PatchWF')
PreserveAnchor = Atom('PreserveAnchor')
HistoryPatchWF = Atom('HistoryPatchWF')
PreserveHistory = Atom('PreserveHistory')

Available = Atom('AvailableAfterLoss')
ReintroTransition = Atom('ReintroTransition')
Recovery = Atom('RecoveryRecord')
Witness = Atom('ReintroWitness')

Durable = Atom('Durable')
Authoritative = Atom('Authoritative')
CandidateOrProbe = Atom('CandidateOrProbe')

JointUse = Atom('JointUse')
LocalCompat = Atom('LocalCompatibility')
RetainedTension = Atom('RetainedTension')

Reorg = Atom('ReorganizationEvidence')
Exercised = Atom('ExercisedReach')
Returned = Atom('ReturnedContact')
Consequence = Atom('ConsequenceUptake')
ReorgBasis = And(Exercised, And(Returned, Consequence))

proofs: List[Tuple[str, Mapping[str, Formula], Proof, Formula]] = []

# H-C1
ctx = {
    'ab': Imp(Authority, GuardBasis),
    'cn': Imp(ClosureOnly, Not(GuardBasis)),
}
p = ImpIntro('hc', ClosureOnly,
        ImpIntro('ha', Authority,
            ImpElim(
                ImpElim(Hyp('cn'), Hyp('hc')),
                ImpElim(Hyp('ab'), Hyp('ha')))))
proofs.append(('H-C1 no authority from closure-only basis', ctx, p, Imp(ClosureOnly, Not(Authority))))

# H-C4
ctx = {'ds': Imp(DirectProv, Seal), 'gn': Imp(Generated, Not(Seal))}
p = ImpIntro('hg', Generated,
        ImpIntro('hd', DirectProv,
            ImpElim(
                ImpElim(Hyp('gn'), Hyp('hg')),
                ImpElim(Hyp('ds'), Hyp('hd')))))
proofs.append(('H-C4 sealed direct provenance', ctx, p, Imp(Generated, Not(DirectProv))))

# H-C10*
ctx = {
    'cp': Imp(Commit, PostHasE),
    'pd': Imp(PostHasE, Not(EnabledPost)),
    'se': Imp(SecondCommit, EnabledPost),
}
p = ImpIntro('hc', Commit,
        ImpIntro('hs', SecondCommit,
            ImpElim(
                ImpElim(Hyp('pd'), ImpElim(Hyp('cp'), Hyp('hc'))),
                ImpElim(Hyp('se'), Hyp('hs')))))
proofs.append(('H-C10* branch-local no sequential recommit', ctx, p, Imp(Commit, Not(SecondCommit))))

# H-C2
ctx = {'cw': Imp(Commit, PatchWF), 'wp': Imp(PatchWF, PreserveAnchor)}
p = ImpIntro('hc', Commit, ImpElim(Hyp('wp'), ImpElim(Hyp('cw'), Hyp('hc'))))
proofs.append(('H-C2 anchor conservativity', ctx, p, Imp(Commit, PreserveAnchor)))

# H-C3
ctx = {'cw': Imp(Commit, HistoryPatchWF), 'wp': Imp(HistoryPatchWF, PreserveHistory)}
p = ImpIntro('hc', Commit, ImpElim(Hyp('wp'), ImpElim(Hyp('cw'), Hyp('hc'))))
proofs.append(('H-C3 history conservativity', ctx, p, Imp(Commit, PreserveHistory)))

# H-C5
ctx = {
    'at': Imp(Available, ReintroTransition),
    'tr': Imp(ReintroTransition, Recovery),
    'rw': Imp(Recovery, Witness),
}
p = ImpIntro('ha', Available,
        ImpElim(Hyp('rw'), ImpElim(Hyp('tr'), ImpElim(Hyp('at'), Hyp('ha')))))
proofs.append(('H-C5 availability implies witnessed recovery', ctx, p, Imp(Available, Witness)))

# H-C7
ctx = {'da': Imp(Durable, Authoritative), 'ac': Imp(Authoritative, CandidateOrProbe)}
p = ImpIntro('hd', Durable, ImpElim(Hyp('ac'), ImpElim(Hyp('da'), Hyp('hd'))))
proofs.append(('H-C7 lifecycle non-collapse', ctx, p, Imp(Durable, CandidateOrProbe)))

# H-C9 (the premise itself is the sealed introduction-rule inversion)
ctx = {'jw': Imp(JointUse, Or(LocalCompat, RetainedTension))}
p = ImpIntro('hj', JointUse, ImpElim(Hyp('jw'), Hyp('hj')))
proofs.append(('H-C9 joint use exposes scoped witness', ctx, p, Imp(JointUse, Or(LocalCompat, RetainedTension))))

# H-K14
ctx = {'rb': Imp(Reorg, ReorgBasis)}
p = ImpIntro('hr', Reorg,
        AndElimLeft(AndElimRight(ImpElim(Hyp('rb'), Hyp('hr')))))
proofs.append(('H-K14 reorganization contains returned contact', ctx, p, Imp(Reorg, Returned)))

results = [expect(*item) for item in proofs]
lines = ['0g SMALL PROOF KERNEL REPORT', '=' * 56, '']
for name, passed, detail in results:
    lines.append(f"[{'PASS' if passed else 'FAIL'}] {name}")
    lines.append(f'       {detail}')
lines.append('')
lines.append(f'Explicit proof terms accepted: {sum(p for _, p, _ in results)} / {len(results)}')
text = '\n'.join(lines) + '\n'
REPORT.write_text(text, encoding='utf-8')
print(text, end='')
raise SystemExit(0 if all(p for _, p, _ in results) else 1)
