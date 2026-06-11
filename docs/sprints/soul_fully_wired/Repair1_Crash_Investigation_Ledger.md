# Repair 1 Crash Investigation Ledger

**Destination:** docs/sprints/soul_fully_wired/Repair1_Crash_Investigation_Ledger.md
**Status:** CLOSED 2026-06-11 (pending live confirmation). Mechanism, artifact, and fix all named and validated; see F19-F21. Every
experiment cites facts from here; every result lands here before the next
experiment is designed.
**Discipline:** one hypothesis per experiment, stated with "what we expect
to learn" before execution; results recorded as facts (F), falsified
theories (X), or open unknowns (U) before the next step.

## Durable facts (evidence-pointed)

- **F1.** Production crash signature: `atom_string/2: insufficiently
  instantiated` at first wired cycle carrying `(metta (match ... $x $y))`
  commands (unbound vars from her unquoted emissions). Evidence: crash log
  2026-06-10 ~22:37.
- **F2.** sread-parsed batches carry genuine unbound Prolog variables; sread
  + println on them is safe. Evidence: U0/U1/U2 echoes, all probes.
- **F3.** The verdict chain on production-shaped data is CLEAN in isolation
  (kernel+gate+seed+module only). Evidence: u_probe 6/6.
- **F4.** Boot loads via run.metta -> git-import! (registers library name)
  -> lib_omegaclaw -> L23 lib_clarity_reasoning -> soul files. import!
  silently swallows ALL failures (metta.pl catch). Proven cost four times
  (staging not mounted; missing git-import; wrong path; placement).
- **F5.** Directive-level calls are STATICALLY COMPILED by the transpiler
  (compiled goal chains visible in every raw log). Clause-BODY collapse
  invokes runtime reduce. Evidence: B0b compiled goal vs probe4 T2 survival.
- **F6.** `(collapse (soul-cmd-skill $cmd))` in a clause body died at
  split_string with metta-headed cmds under full universe, both before AND
  after the soul_utils retirement. Evidence: env_probe2 runs 204916, 211307.
- **F7.** soul_utils.metta L135-160 contained a complete legacy string-based
  gate (six names colliding with the committed gate; string-contains
  bodies). Retired 2026-06-10 (apply_soul_utils_gate_retirement.py,
  applied, uncommitted). Census: namespace_census.py output.
- **F8.** The legacy collision was REAL but NOT the split_string killer:
  the same death survived the retirement. Evidence: env_probe2 211307.
- **F9.** Structural primitives validated under full universe on
  production-shaped data: car-atom head extraction ("metta"), structural
  arg extraction (unbound vars intact), resolve-operation-risk(metta)=2,
  unknown floor=3. Evidence: probe4 T3-T6, zero errors.
- **F10.** With structural dispatch replacing the collapse site, the chain
  passes B0b and computes B8 = correct PROCEED verdict under full universe
  -- BUT with a ~16-fold solution fan-out (16 identical B8 prints), and a
  NEW atom_string death later in the same run (site unlocated, after B8).
  Evidence: env_probe2 082419. THE FAN-OUT IS A NEW PRIMARY FACT: the
  module's "deterministic single-clause" design still multiplies solutions
  under the full universe; multiplication sources unidentified.
- **F11.** P3 (gate's soul-is-metta-cmd? pre-retirement) returned THREE
  solutions (false/true/true). Two are explained (utils stub False + gate
  clause True). The THIRD is UNEXPLAINED and was never resolved. Evidence:
  env_probe3 205456. Likely related to F10's multiplication class.
- **F12.** Kernel soul-cmd-skill = 12 clauses, all constant bodies, kernel
  only (full-tree census). The skill mapping is identity (head = skill).
- **F13.** janus resolution (read from metta.pl L219-237): ".method" ->
  object method; "mod.fun" -> py_call(M:...) requiring an IMPORTED module;
  bare names and builtins-planted attrs -> janus builtin registry,
  unreachable. The only route to custom Python: a module file via the
  importer (sys.path + __import__) -- the helper.py mechanism.
- **F14.** Literal metta-headed expressions in ANY directive are live
  ammunition under the full universe (B0a type-error). sread is the only
  safe carrier for command-shaped data in source text.
- **F15.** Seeding gate = flag file ./memory/soul_seeded.flag; "already
  loaded" during the outage was crash-loop container reuse, not a break.
- **F16.** soul_utils is loaded in production but NOT via
  lib_clarity_reasoning (empty grep). Importer unknown (U2).

## Falsified theories (and what killed each)

- **X1.** "Eager reduction executes metta elements at function-call
  boundaries" (general form). Killed by probe3 P1/P2/P4.
- **X2.** "A == / quote / car-atom overlay makes one-clause functions
  nondet." Killed by the empty overlay census.
- **X3.** "The soul_utils legacy gate collision is the split_string
  killer." Killed by env_probe2 211307 (death survived retirement).
  (The collision was real and retiring it was correct regardless.)
- **X4.** "Clause-body collapse-over-command is THE killer" (complete
  form). Half-true: removing it cleared B0b (F10), but fan-out and a
  later atom_string death persist, so it was A killer, not THE mechanism.

## Open unknowns (each is a checkable item, not a guess)

- **U1.** F10's fan-out source: which link(s) in the compiled chain yield
  multiple solutions under the full universe, and with what multiplicity.
- **U2.** soul_utils's actual importer (non-blocking; parked).
- **U3.** F11's third P3 solution (probably same class as U1).
- **U4.** The post-B8 atom_string death site in run 082419 (unlocated;
  the log exists and must be READ, not theorized about).
- **U5.** Whether the G-series (glue) shares U1's multiplication.

## Design constraints extracted (binding on the rewrite and re-apply)

- **C1.** No collapse/superpose over expressions containing raw commands
  inside clause bodies (F5/F6).
- **C2.** No literal metta-headed expressions anywhere in source
  directives; sread-built fixtures only (F14).
- **C3.** Custom Python only via module files + importer; absolute paths;
  verify the file exists at the imported path BEFORE trusting import!
  (F4, F13).
- **C4.** Every harness/probe runs under the FULL universe (boot chain),
  not isolation; isolation passes prove nothing about production (F3+F6).
- **C5.** Solution COUNTS are first-class harness expectations, not just
  values: a correct value with fan-out is a FAIL (F10, F11).

## Closing facts

- **F-table (probe5 D-series, run 083923):** chain-loaded files
  deterministic (kernel atoms 1, resolver 1); probe-explicitly-imported
  files exactly doubled (membership 2, gate predicate 2, module fns 2);
  explosion = 2 compounding through call depth (grounding 16 = 2^4).
- **F19 (U1/U6/U7 closed):** absolute-path import loads once (E0=1); the
  library spec IN PROBE CONTEXT was the doubler; the fan-out was a PROBE
  ARTIFACT; production (single-load via lib_clarity_reasoning chain)
  never had it. Evidence: env_probe6 084550.
- **F20 (U4/U3/F11 closed; THE PRODUCTION KILLER):** pattern-headed
  clauses (e.g. (soul-extract-metta-arg (metta $arg))) die at
  atom_string on unbound-variable-carrying metta commands under reduce;
  var-headed builtins-only forms are immune (T4/D5/D9/Q-series).
  Production path: glue -> gate's pattern-headed extract -> death.
- **F21 (the fix, validated):** complete structural replacement glue
  (var-headed throughout, gate's pattern-headed extract and quote-bodied
  target-head bypassed) passes 13/13 under the full universe on
  production shapes INCLUDING the killer input, deterministic (counts 1).
  Evidence: env_probe7 084825. Cut into apply_repair1_wiring.py MA_BLOCK
  rev 2; wiring harness upgraded to full-universe (C4) with count
  expectations (C5) and the previously-missing production-shape fixture.

## Handoffs out of this investigation

- Gate-file hardening (Clarity's lead): soul-extract-metta-arg's pattern
  head and soul-target-head's quote-on-var body are F20-vulnerable; the
  gate's own structural fallback (documented in its comments) is the
  validated cure. The wiring no longer calls either, so this is
  non-blocking hardening, not a blocker.
- Durable constraints C1-C5 graduate to the project knowledge dump.
