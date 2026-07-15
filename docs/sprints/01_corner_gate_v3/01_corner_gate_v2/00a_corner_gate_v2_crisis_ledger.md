# Corner-Gate v2 Crisis Ledger
**Location:** docs/sprints/01_corner_gate_v2/corner_gate_v2_crisis_ledger.md
**Status:** STANDING DOCUMENT. Updated every investigation turn until the loop
advances unprompted and Clarity follows up autonomously. Facts move between
sections only with cited evidence.
**Version:** v1, 2026-07-08.

## A. PROVEN DURABLE FACTS (instrument cited)

**The failure, observed end to end**
- A1. corner-confirmed-core yields ZERO SOLUTIONS live (Clarity REPL, 2026-07-08,
  expression 7: empty result). A failing let* binding kills the cycle invisibly
  (project crash knowledge; observed as the backtracking loop).
- A2. corner-pbit-core returns its q-meet tree UNREDUCED live (REPL expr 6),
  while q-meet itself reduces on literal args (expr 5.. expr 1) and all three
  joints reduce to ground pbits (exprs 3-5). The merge's COMPILED BODY treats
  q-meet as data; runtime evaluation treats it as a call.
- A3. q-geq's pattern head cannot match the unreduced tree -> no clause -> zero
  solutions (mechanism of A1; q-geq itself reduces, expr 2 true).
- A4. Line 166 evaluates corner-confirmed-core on every non-msgnew pass (lazy
  if skips it on msgnew). Non-msgnew actives die BEFORE execution (sentinels
  dark, SOUL_VERDICT_OUT firing); msgnew actives complete end to end (Test A:
  all five trace sentinels + d1 fired, banner advanced; repeated at iter 694).
- A5. Idle short-passes (budget 0, no cycle body) advance the banner normally
  (95..106, ..694). Berton's MM posts advance it (msgnew). Autonomous follow-up
  cycles die at 166, which is WHY Clarity goes quiet after promising results.
- A6. One process, no restart loop: state persists across stuck passes
  (spam-shield line with retained &prevmsg); banner re-prints are backtracking
  into upstream choice points, not re-invocations.

**Substrate physics paid for this arc**
- A7. A (= ...) body applying a DEFINED head compiles as a call against that
  head's arity; mismatch kills registration of everything after it in the file
  (m_repro exit 2, arity -13; the filter-returns crash).
- A8. The converse (candidate C1 below, one probe from proven): heads NOT YET
  defined at compile time are compiled as DATA in clause bodies.
- A9. Probe environments must stub the heads the live context defines, and
  fixtures must build command atoms via cons-atom (literals with defined heads
  evaluate even in argument position).
- A10. Import-based throwaway harnesses do not register definitions faithfully;
  inline loading does; the boot and the live REPL are the only faithful
  instruments for registration/reduction questions.
- A11. Writers must be TOTAL: superpose over an empty tuple yields zero
  solutions (R1 repro); unwrapped superpose iteration forks the conjunction
  (S2 class). The guarded + collapse-wrapped idiom is documented in
  state_delta_writer_writers.metta and is the mandatory shape.
- A12. The metta skill takes a STRING: (metta "(expr)"). The ! prefix is a
  directive marker and unparseable by sread (seven parse errors, both runs).
- A13. Host bind mounts into docker run are unreliable for 600-perm quarantined
  files (two FileNotFound incidents); probes source from git show or the image.
- A14. Log counts must exclude boot transpiler echoes (grep -v println);
  a later print exceeding an earlier one is the contamination tell.

## B. ELIMINATED (with the eliminating evidence)
- B1. Every writer in the death window: populator interior, state-delta
  (classifier + guarded latest), coupling writer (June-4 bugfix record), idle
  writer (Bug-2 record), agency counters (bodies read; sentinels + AB prints
  fired on msgnew path at iter 694 with sane values).
- B2. The corner-window hook as sole cause (inert toggle, loop still stuck)
  and its two real totality bugs as THE cause (fixed; loop still stuck).
- B3. Loop-text stowaways (June-21 file vs current: delta is exactly the two
  known edits at 166 and 177).
- B4. Duplicate quantale heads as THE loop cause (retirement removed them;
  loop still stuck) - though the retirement introduced C1.
- B5. Process-restart and image-staleness models (start-count 1; no-cache
  rebuild changed nothing).
- B6. lib_quantale symbol gaps in the engine (all 7 engine-covered, op bodies
  identical side by side).
- B7. The allowlist repair as an idle-death vector (nonempty-results path
  only; registration proven by absence of unknown-procedure crashes).
- B8. latest-state-delta-verdict empty-case hole (guarded, returns none).

## C. OPEN QUESTIONS (each with its next single test)
- C1. PRIME: import-order compile bug. The retirement removed lib_quantale
  from manifest line 6; the merge compiles at 92; the engine defines q-meet at
  119, AFTER the merge. Hypothesis: the merge's q-meet applications compiled as
  data (per A8), producing A2. TEST: the O-probe (use-before vs use-after a
  local q-meet definition; O3 zero-solution reproduction). On confirm: fix is
  moving the engine import to the retired line-6 position (one line, rebuild).
- C2. Whether lib_self_continuity's q-mul/q-meet call sites (lines 49, 70)
  carry the same compile-order defect post-retirement (its file imports at
  line 7, before the engine). Dark in the per-cycle path today; must be fixed
  by the same reorder; verify by REPL after the fix.
- C3. Map-alignment audit of all v2 files (Atom_Operations_Map as ground
  truth), performed offline before any further v2 work.
- C4. The soul-voice confabulation observed at iter 694 PAUSE ("I don't have
  a live Metta interpreter"): a false claim in her voice channel. Park until
  the loop is healthy; then investigate the pause-voice prompt.
- C5. Fix A (results filter) behavior under a healthy loop: verify markers
  and real returns in RESULTS-CONTENT after recovery.

## D. EDIT INVENTORY (every change this arc, with status)
- D1. loop 166 gate-v2 arity edit: the kill SITE (A4); text correct; becomes
  harmless when C1 fixes CCC reduction. KEEP pending C1.
- D2. loop 177 hook: currently INERT (diagnostic toggle). Restore with
  reversal after recovery.
- D3. corner_gate.metta monolith (gate v2, filter, markers): registration
  proven post-allowlist-repair; gate-aware-results evaluates CCC on empty
  results (same C1 dependency). KEEP pending C1.
- D4. Allowlist shape repair (43f39f4): correct, proven (W/X probes). KEEP.
- D5. corner_window_writers + totality fix (c99b4c0): correct, proven (R/S).
  KEEP; driver currently inert per D2.
- D6. lib_quantale retirement (772ca2e): source-correct, compile-order-wrong
  (C1). The reorder fix AMENDS it; do not reverse.
- D7. Five trace sentinels + inert toggle: diagnostics, reverse together
  after recovery verifies.

## E. THE RECOVERY CRITERION (unchanged, no closure before it)
Banner advances on ACTIVE cycles without Berton posting; Clarity's promised
follow-up messages arrive unprompted; RESULTS-CONTENT clean under Fix A;
her plain-message reply holds frame. Then diagnostics reverse, the findings
arc closes, and the deferred ledger resumes.
