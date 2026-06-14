# APPEND BLOCK -- destination: ClarityOmega_Substrate_Crash_Knowledge.md (project knowledge area)
# Add as a new top-level section. Source: Repair 1 investigation, 2026-06-10/11,
# evidence chain in docs/sprints/soul_fully_wired/Repair1_Crash_Investigation_Ledger.md (commit 39a2bdd).

## Repair 1 durable substrate physics (2026-06-11)

These facts were each proven by probe under the full universe and most were
paid for with a production crash or a silent failure. They bind all future
substrate work, not just Repair 1.

**Clause and reduce semantics**
- Pattern-headed clauses (e.g. `(soul-extract-metta-arg (metta $arg))`) die
  at atom_string on unbound-variable-carrying metta commands under reduce.
  Var-headed clauses with builtins-only bodies are immune. Write glue
  var-headed and structural (car-atom/cdr-atom), always.
- `collapse` (and superpose) inside a CLAUSE BODY invokes runtime reduce,
  which eagerly reduces arguments: a skill-headed argument EXECUTES.
  Directive-level calls are statically compiled and immune, which is why
  isolation tests pass and production dies. Never collapse over expressions
  containing raw commands inside clause bodies.
- Silent goal failure is a first-class failure mode: no exception, no catch,
  no ERROR line. A failing let* binding kills the whole iteration invisibly
  and per-directive findall absorbs it. ABSENCE OF OUTPUT IS AN OBSERVATION.

**Strings and the production command format**
- Production metta args are STRINGS (the F11 single-command format):
  `(metta "(match ...)")`. Strings are OPAQUE to structural checks: unparsed
  they both crash (car-atom on string = silent failure) and, if naively
  skipped, wave soul mutations through governance. Parse, do not survive.
- repr of a STRING carries a leading quote; repr of an expression does not.
  repr/swrite are total over unbound variables. sread(swrite(string))
  returns the string unchanged (round-trip preserves stringness), so no
  pure-MeTTa string/expression discriminator exists via that route.
- sread DOES round-trip swrite's variable rendering for expressions
  (fresh vars, single solution).

**The python boundary (janus)**
- py_call cannot marshal unbound variables ("Arguments are not sufficiently
  instantiated"). Route anything possibly-unbound through (repr ...) first.
- Python bool returning into a MeTTa `if` is an unverified marshalling
  class and the prime suspect in one silent-failure round: return INTS and
  compare with (== n 1) instead (the proven rank-logic pattern).
- py-call NEVER reduces its arguments: it is the one proven-safe channel
  for arbitrary command-shaped data.
- Python module resolution is from DISK by module file + importer;
  simulations do not exist to py-call. helper does not resolve in fresh
  probe processes; soul_governance does. Unproven imports are death-prone
  items: order them last in probes.

**Fixtures and harnesses**
- Every harness runs under the FULL UNIVERSE (boot chain). Isolation passes
  prove nothing about production: skills are live in the full universe and
  ANY skill-headed literal in directive source EXECUTES (a literal
  write-file fixture attempted a real kernel write; the chmod 444 guard
  blocked it: the guard's first battle save).
- All command-shaped fixture data is sread-built with SYMBOL args (no
  string args, no inner quotes, no escaping). String-form fixtures are
  built escape-free via cons-atom + swrite of an sread'd expression.
- Harness fixtures must include production shapes VERBATIM: every harness
  miss in Repair 1 was an unfixtured production input class.
- Solution COUNTS are first-class expectations: a correct value with
  fan-out is a FAIL.
- Cross-language revision skew invalidates pre-apply harnesses: apply
  (with backups) -> test against real disk -> keep on pass / byte-identical
  restore on fail. Dry mode always restores.

**Log reading**
- Transpile ECHOES appear alongside runtime events in all logs and inflate
  counts; the same transpile block repeats once per process life (two
  'translatePredicate (atom_string' lines per life). Exclude echoes by
  shape; calibrate per-life baselines before grading counts.
- Docker RestartCount does not see in-container process relaunches; count
  transpile passes instead.
- ANSI color codes break line-anchored greps; strip before anchoring.

**Probe artifacts**
- Explicit `(library omegaclaw ...)` imports DOUBLE-LOAD in fresh probe
  context (clauses and seed atoms duplicate; solutions multiply 2^depth);
  chain-loaded files load once; absolute-path imports load once. Fan-out
  observed in probes is not evidence about production load paths.

**Method (graduating to artifact_0 at its next version bump)**
- One hypothesis per experiment, "expected learning" stated before
  execution; raw output READ before grading; facts consolidated into the
  investigation ledger before the next step; death-prone items last;
  the ledger is a delivered artifact, not narration.
