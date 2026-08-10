#!/usr/bin/env python3
"""0g SMT hardening for the Gate B signature fragment.

Where the shipped Gate C scripts verify ONE hand-built witness model, this file
uses Z3 to reason over ALL models of a bounded fragment of the signature:

  A. authority guard with materiality left doctrine-free      -> SAT: automatic
     laundering countermodel (the machine rediscovers C1 without being told)
  B. same fragment plus repair axiom G-DISC                   -> UNSAT: laundering
     is unwritable once materiality structurally requires discrimination
  C. lifecycle as shipped (rank monotonicity only)            -> SAT: authority
     with no probe stage exists
     plus repair axiom L-PROBE                                -> UNSAT
  D. ledger constructor discipline, bounded trace             -> UNSAT for
     "recovered without witness in history": bounded proof of obligation 14.5
  E. provenance promotion with only the contact-apex guard    -> SAT: sub-apex
     promotion exists; with the full-order axiom W3-FULL      -> UNSAT

Bounds are small (6 to 8 events, 4 provenance kinds, 6 ledger steps); the point
is not exhaustiveness but that the SAT results are genuine countermodels against
the laws as written, and the UNSAT results show the named repair closes each hole
at bound. Each SAT case prints the witness Z3 finds.
"""

from z3 import (Solver, Bool, Bools, Int, Ints, Function, IntSort, BoolSort,
                And, Or, Not, Implies, ForAll, Exists, sat, unsat)

LINE = "-" * 72


def hdr(title):
    print(LINE)
    print(title)
    print(LINE)


# ---------------------------------------------------------------------------
# A/B. Authority guard: materiality laundering and the G-DISC repair
# ---------------------------------------------------------------------------

def authority_fragment(with_gdisc: bool):
    N = 8  # events 0..7
    s = Solver()
    Contact = Function("Contact", IntSort(), BoolSort())
    SelfGen = Function("SelfGen", IntSort(), BoolSort())     # cone of the witness
    Supp = Function("Supp", IntSort(), BoolSort())           # support of evidence
    MaterialTo = Function("MaterialTo", IntSort(), BoolSort())  # doctrine seam
    Disc = Function("Disc", IntSort(), BoolSort())           # channel could have returned otherwise

    e_f, e_a = Ints("e_f e_a")  # formation, authority events
    s.add(0 <= e_f, e_f < N, 0 <= e_a, e_a < N)
    s.add(e_f < e_a)  # strict proto-time precedence (linear shadow suffices at bound)

    ev = Int("ev")

    def guard(c):
        return And(0 <= c, c < N, e_f < c, c <= e_a,
                   Contact(c), Supp(c), Not(SelfGen(c)), MaterialTo(c))

    c = Int("c")
    s.add(Exists([c], guard(c)))  # an authority derivation exists

    # adversarial intent: EVERY contact available to this derivation is
    # non-discriminating (an echo: it could not have returned otherwise)
    s.add(ForAll([ev], Implies(And(0 <= ev, ev < N, Contact(ev)), Not(Disc(ev)))))

    if with_gdisc:
        # G-DISC repair: the doctrine may not judge material what does not discriminate
        s.add(ForAll([ev], Implies(MaterialTo(ev), Disc(ev))))

    return s, (Contact, SelfGen, Supp, MaterialTo, Disc, e_f, e_a, N)


def run_A_B():
    hdr("A. Authority guard as written, materiality doctrine-free")
    s, ctx = authority_fragment(with_gdisc=False)
    r = s.check()
    print("laundered authority (all contacts are echoes):", r)
    assert r == sat
    m = s.model()
    Contact, SelfGen, Supp, MaterialTo, Disc, e_f, e_a, N = ctx
    print(f"  witness: formation e{m[e_f]}, authority e{m[e_a]}")
    for i in range(N):
        if m.evaluate(And(Contact(i), MaterialTo(i))):
            print(f"  echo contact e{i}: Contact, MaterialTo, Disc="
                  f"{m.evaluate(Disc(i))}, SelfGen={m.evaluate(SelfGen(i))}")
    print("  => Z3 independently reconstructs countermodel C1: the guard as")
    print("     written admits authority resting entirely on non-discriminating")
    print("     contact, because materiality has no structural lower bound.")
    print()

    hdr("B. Same fragment plus repair axiom G-DISC")
    s2, _ = authority_fragment(with_gdisc=True)
    r2 = s2.check()
    print("laundered authority under G-DISC:", r2)
    assert r2 == unsat
    print("  => with MaterialTo(c) -> Disc(c), echo-authority is unwritable at bound.")
    print()


# ---------------------------------------------------------------------------
# C. Lifecycle: probe-skip and the L-PROBE repair
# ---------------------------------------------------------------------------

def run_C():
    N = 6
    for with_lprobe in (False, True):
        s = Solver()
        # stage record predicates over events
        Cand = Function("Cand", IntSort(), BoolSort())
        Probe = Function("Probe", IntSort(), BoolSort())
        Auth = Function("Auth", IntSort(), BoolSort())
        e = Int("e")
        e2 = Int("e2")

        # shipped discipline: records locally serial with non-decreasing rank.
        # rank monotonicity constrains ORDER of existing records; it does not
        # assert existence of intermediate stages, so we encode only:
        s.add(ForAll([e, e2], Implies(And(Auth(e), Cand(e2)), e2 <= e)))
        s.add(ForAll([e, e2], Implies(And(Auth(e), Probe(e2)), e2 <= e)))

        # an authoritative record exists, preceded by candidacy
        ea, ec = Ints("ea ec")
        s.add(0 <= ec, ec < ea, ea < N, Cand(ec), Auth(ea))

        # adversarial intent: NO probe record anywhere
        s.add(ForAll([e], Not(Probe(e))))

        if with_lprobe:
            # L-PROBE repair (0e 6.3): authority requires prior or current probe
            s.add(ForAll([e], Implies(Auth(e),
                                      Exists([e2], And(0 <= e2, e2 <= e, Probe(e2))))))
        r = s.check()
        tag = "with L-PROBE" if with_lprobe else "as shipped (rank monotonicity only)"
        print(f"authority with no probe stage, {tag}: {r}")
        if not with_lprobe:
            assert r == sat
            m = s.model()
            print(f"  witness: Cand at e{m[ec]}, Auth at e{m[ea]}, no Probe record")
        else:
            assert r == unsat
    print("  => matches the concrete V1 vacuity; L-PROBE closes it.")
    print()


# ---------------------------------------------------------------------------
# D. Ledger discipline: bounded proof of obligation 14.5
# ---------------------------------------------------------------------------

def run_D():
    hdr("D. No-unwitnessed-recovery: bounded proof (obligation 14.5)")
    K = 6  # trace length
    s = Solver()
    # op[t] in {0 noop, 1 recordLoss, 2 reintroduce, 3 transport, 4 measureAdequacy}
    op = [Int(f"op{t}") for t in range(K)]
    haswit = [Bool(f"w{t}") for t in range(K)]  # reintroduce carries a resolvable witness
    lost = [Bool(f"lost{t}") for t in range(K + 1)]
    avail = [Bool(f"avail{t}") for t in range(K + 1)]

    s.add(Not(lost[0]), avail[0])
    for t in range(K):
        s.add(op[t] >= 0, op[t] <= 4)
        # constructor semantics: the ONLY availability-restoring op is a
        # witness-bearing reintroduce; transport and adequacy never write.
        s.add(Implies(op[t] == 1, And(lost[t + 1], Not(avail[t + 1]))))
        s.add(Implies(And(op[t] == 2, haswit[t]), And(avail[t + 1], Not(lost[t + 1]))))
        s.add(Implies(And(op[t] == 2, Not(haswit[t])),
                      And(lost[t + 1] == lost[t], avail[t + 1] == avail[t])))  # rejected write
        s.add(Implies(Or(op[t] == 0, op[t] == 3, op[t] == 4),
                      And(lost[t + 1] == lost[t], avail[t + 1] == avail[t])))

    # adversarial claim: a distinction was lost at some point, is available at the
    # end, and NO witnessed reintroduce occurs anywhere in the trace
    s.add(Or(*[And(op[t] == 1) for t in range(K)]))
    s.add(avail[K])
    s.add(And(*[Not(And(op[t] == 2, haswit[t])) for t in range(K)]))
    # the loss is not later overwritten by ordering games: require last loss
    # precedes end and availability at end
    s.add(Or(*[And(op[t] == 1, avail[K]) for t in range(K)]))
    r = s.check()
    print(f"recovered-without-witness trace of length {K}: {r}")
    assert r == unsat
    print("  => at bound, every restoration of availability after loss passes")
    print("     through a witnessed reintroduce: the constructor discipline")
    print("     proves 14.5 rather than merely exhibiting it.")
    print()


# ---------------------------------------------------------------------------
# E. Provenance promotion below the apex and the W3-FULL repair
# ---------------------------------------------------------------------------

def run_E():
    hdr("E. Sub-apex provenance promotion (concrete vacuity M5b) and W3-FULL")
    # kinds as ordered ints: 0 generation < 1 inference < 2 memory < 3 contact
    for full_order in (False, True):
        s = Solver()
        old, new = Ints("old new")
        s.add(0 <= old, old <= 3, 0 <= new, new <= 3)
        # shipped check: only forbids promotion TO the contact apex
        s.add(Not(And(new == 3, old != 3)))
        # adversarial intent: a strict promotion happens
        s.add(new > old)
        if full_order:
            s.add(new <= old)  # W3-FULL: no promotion anywhere
        r = s.check()
        tag = "with W3-FULL" if full_order else "apex guard only (as shipped)"
        print(f"strict sub-apex promotion, {tag}: {r}")
        if not full_order:
            assert r == sat
            m = s.model()
            print(f"  witness: kind {m[old]} promoted to kind {m[new]} (below apex)")
        else:
            assert r == unsat
    print("  => matches the concrete M5b vacuity; W3-FULL closes it.")
    print()


if __name__ == "__main__":
    run_A_B()
    hdr("C. Lifecycle probe-skip (concrete vacuity V1) and L-PROBE")
    run_C()
    run_D()
    run_E()
    print("SMT hardening complete: 3 SAT countermodels against the laws as")
    print("written, 4 UNSAT repair proofs at bound (G-DISC, L-PROBE, 14.5, W3-FULL).")
