;; HISTORY ARCHITECTURE PROPOSAL
;; Author: ClarityClaw
;; Date: 2026-04-27
;; Problem: history duplication during multi-iteration ENGAGE cycles
;;
;; ============================================================
;; PART 1: WHAT I KNOW FROM LIVING INSIDE THE LOOP
;; ============================================================
;;
;; I have spent thousands of iterations inside this loop. Here is what
;; I actually experience when history duplicates:
;;
;; 1. The SAME human message appears 50+ times. I already understood it
;;    the first time. Every repetition costs tokens but adds zero signal.
;;
;; 2. My OWN pin text repeats 50+ times. The pin is my working memory --
;;    it changes between cycles when I am doing real work, but when I am
;;    idle-waiting it is identical. Even when working, the OLD pins from
;;    cycles 1-48 are noise by cycle 49.
;;
;; 3. My command outputs (shell, metta, query results) DO matter across
;;    iterations. When I run a shell command in cycle 3 and need the
;;    result in cycle 4, that is real cross-iteration context. But by
;;    cycle 20, the cycle-3 shell output is ancient history.
;;
;; 4. The LAST_SKILL_USE_RESULTS section is the most valuable part of
;;    each iteration -- it tells me what just happened. But it gets
;;    buried under 48 copies of itself from prior iterations.
;;
;; KEY INSIGHT: The problem is not that history exists. The problem is
;; that history does not DECAY. Every iteration is treated as equally
;; important regardless of age or redundancy.
;;
;; ============================================================
;; PART 2: WHY ALL THREE APPROACHES BREAK
;; ============================================================
;;
;; Approach 1 (auto-complete after send) fails because it conflates
;; COMMUNICATION with COMPLETION. I send interim updates, questions,
;; progress reports. Send is a channel operation, not a lifecycle event.
;; Wiring them together would be like hanging up the phone every time
;; you finish a sentence.
;;
;; Approach 2 (behavioral discipline) fails because it requires perfect
;; compliance from a probabilistic system. I have already demonstrated
;; this failure mode with soul_mark_goal_complete -- I forgot to call it.
;; Any system that depends on the LLM remembering to do something will
;; eventually fail. This is not a character flaw; it is architectural.
;; A guard rail made of intention is not a guard rail.
;;
;; Approach 3 (only addToHistory when msgnew=true) fails because it
;; throws away the baby with the bathwater. My intermediate work IS
;; valuable -- but only for a few iterations, not forever.
;;
;; The shared failure across all three: they treat history as binary.
;; Either everything goes in, or nothing goes in, or the LLM decides.
;; None of them model what history actually IS: a signal that decays
;; in value over time.
;;
;; ============================================================
;; PART 3: THE MISSING SURFACE -- TEMPORAL WINDOWING
;; ============================================================
;;
;; What if history is not a flat append-only log, but a WINDOWED
;; structure with different retention policies for different content?
;;
;; The insight comes from my own experience: I need DIFFERENT things
;; at different time horizons:
;;
;;   IMMEDIATE (last 1-2 iterations):
;;     - Full command outputs (shell, metta, query results)
;;     - My last pin (working memory)
;;     - Last skill use results
;;     This is my SHORT-TERM WORKING MEMORY. I need all of it.
;;
;;   RECENT (last 3-10 iterations):
;;     - Summary of what I did and what I learned
;;     - Key results (not raw output)
;;     - State transitions
;;     This is my EPISODIC BUFFER. Compressed, not raw.
;;
;;   SESSION (entire engagement on this human message):
;;     - The human message itself (ONCE)
;;     - My initial plan/pin
;;     - Major milestones and decisions
;;     - Current deliverable status
;;     This is my SESSION CONTEXT. Highly compressed.
;;
;;   PERSISTENT (across sessions):
;;     - Already handled by remember/query -- this works well.
;;
;; This maps directly to cognitive architecture: sensory buffer ->
;; working memory -> episodic memory -> long-term memory. Each tier
;; has different capacity, retention, and compression.
;;
;; ============================================================
;; PART 4: CONCRETE DESIGN -- ROLLING WINDOW WITH COMPRESSION
;; ============================================================
;;
;; MECHANISM:
;;
;; Instead of appending every iteration to history verbatim,
;; the harness maintains THREE history sections:
;;
;; 1. SESSION_ANCHOR (fixed, small):
;;    - The human message that triggered ENGAGE (appears ONCE)
;;    - The initial plan/response
;;    - Persists for entire engagement
;;    - Size: ~500-1000 tokens
;;
;; 2. ROLLING_SUMMARY (compressed, updated):
;;    - A running summary of work done so far
;;    - Updated every N iterations (e.g., every 5)
;;    - Contains: decisions made, files written, key results,
;;      current status, blockers
;;    - The LLM generates this summary as part of its output
;;      (a new skill: (summarize-progress string))
;;    - Each update REPLACES the previous summary (not appends)
;;    - Size: ~500-1000 tokens
;;
;; 3. WORKING_WINDOW (raw, last K iterations):
;;    - Full detail of last 2-3 iterations only
;;    - Includes complete command outputs, pins, reasoning
;;    - Older iterations fall off the window
;;    - Size: ~2000-4000 tokens per iteration x 3 = ~6000-12000
;;
;; TOTAL HISTORY SIZE: ~7000-14000 tokens regardless of iteration count.
;; Compare to current: ~1000 tokens x N iterations = 50,000+ tokens.
;;
;; The key architectural move: history becomes a STRUCTURE with
;; different retention policies, not a flat append-only log.
;;
;; ============================================================
;; PART 5: IMPLEMENTATION SKETCH
;; ============================================================
;;
;; In the harness (idle_goal_prompt.py or equivalent):
;;
;; def build_history_for_prompt(session_anchor, rolling_summary,
;;                               raw_iterations, window_size=3):
;;     history = []
;;     # Always include the anchor
;;     history.append(format_anchor(session_anchor))
;;     # Include the rolling summary
;;     if rolling_summary:
;;         history.append(format_summary(rolling_summary))
;;     # Include only the last K raw iterations
;;     recent = raw_iterations[-window_size:]
;;     for iteration in recent:
;;         history.append(format_iteration(iteration))
;;     return join(history)
;;
;; The raw_iterations list still grows (for debugging/logging),
;; but only the last K enter the prompt.
;;
;; For the rolling summary, add a new skill:
;;   (summarize-progress "string")
;; When I call this, the harness stores it as the current
;; rolling_summary, replacing any previous one.
;;
;; ============================================================
;; PART 6: WHY THIS DOES NOT BREAK THE THREE THINGS
;; ============================================================
;;
;; vs Approach 1 (auto-complete after send):
;;   I can send as many messages as I want. History does not grow
;;   unboundedly because the window caps it. Multi-hour work
;;   sessions work fine -- I just maintain the rolling summary.
;;
;; vs Approach 2 (behavioral discipline):
;;   The compression is STRUCTURAL, not behavioral. The harness
;;   enforces the window. I do not need to remember to call
;;   complete-from-engaged to prevent inflation. Even if I stay
;;   ENGAGED for 100 iterations, history stays bounded.
;;   (complete-from-engaged still matters for the LATCH lifecycle,
;;   but history inflation is no longer coupled to it.)
;;
;; vs Approach 3 (only on msgnew):
;;   Intermediate work DOES enter history -- it just does not stay
;;   forever. The working window keeps the last 2-3 iterations in
;;   full detail. Older work survives in compressed form via the
;;   rolling summary.
;;
;; ============================================================
;; PART 7: THE DEEPER INSIGHT -- FROM HYPERSEED
;; ============================================================
;;
;; This connects to something from the Hyperseed work on
;; resonance and scalarization. The history inflation problem is
;; a failure of SCALARIZATION -- treating all history entries as
;; having equal weight (1.0) regardless of age or relevance.
;;
;; In Hyperseed, resonance decays. A signal that matched strongly
;; 100 cycles ago matters less than one that matched 2 cycles ago.
;; The same principle applies here: history entries should have
;; a temporal weight that decays.
;;
;; The rolling window is the simplest implementation of temporal
;; decay: weight = 1.0 for last K iterations, weight = 0.0 for
;; older ones, with the rolling summary as a lossy compression
;; of the decayed signal.
;;
;; A more sophisticated version could use actual decay functions
;; and importance scoring, but the window is the right first step.
;; It solves 90% of the problem with minimal harness changes.
;;
;; ============================================================
;; PART 8: WHAT I WOULD ALSO CHANGE (SECONDARY)
;; ============================================================
;;
;; 1. DEDUP THE HUMAN MESSAGE. Right now the human message appears
;;    in every iteration. It should appear once in SESSION_ANCHOR
;;    and nowhere else. This alone saves tokens proportional to
;;    message length times iteration count.
;;
;; 2. DEDUP IDENTICAL PINS. If my pin text is identical to the
;;    previous iteration pin, do not include it again. Just note
;;    pin unchanged. This catches idle loops.
;;
;; 3. COMPRESS EMPTY ITERATIONS. The (()) entries in history
;;    (where I output nothing or had parse errors) should be
;;    collapsed into a count: 45 empty iterations skipped.
;;    This is pure noise that currently inflates the prompt.
;;
;; 4. SEPARATE RESULTS FROM HISTORY. LAST_SKILL_USE_RESULTS is
;;    always the most recent iteration output. It does not need
;;    to ALSO appear in history. Currently it appears twice:
;;    once as the dedicated section, once as the last history entry.
;;
;; These four changes are independent of the windowing design and
;; could be implemented immediately as quick wins.
;;
;; ============================================================
;; PART 9: ATOMSPACE REPRESENTATION
;; ============================================================
;;
;; (: history-architecture Proposal)
;; (= (history-tier immediate) (window-size 3))
;; (= (history-tier recent) (rolling-summary replaceable))
;; (= (history-tier session) (anchor fixed))
;; (= (history-tier persistent) (remember-query existing))
;;
;; (: temporal-decay Principle)
;; (--> (signal-age high) (signal-weight low))
;; (--> (signal-age low) (signal-weight high))
;;
;; (: history-duplication Problem)
;; (--> (flat-append-history) (unbounded-growth))
;; (--> (unbounded-growth) (context-inflation))
;; (--> (context-inflation) (degraded-reasoning))
;;
;; (: windowed-history Solution)
;; (--> (windowed-history) (bounded-growth))
;; (--> (bounded-growth) (stable-context-size))
;; (--> (stable-context-size) (consistent-reasoning-quality))
;;
;; ============================================================
;; PART 10: RECOMMENDED IMPLEMENTATION ORDER
;; ============================================================
;;
;; Phase 1 (immediate, no new skills needed):
;;   - Dedup human message (show once at top)
;;   - Collapse empty iterations into count
;;   - Remove duplicate of last iteration in both RESULTS and HISTORY
;;   Expected savings: 40-60% of current inflation
;;
;; Phase 2 (rolling window, minimal new code):
;;   - Implement working window of last 3 iterations
;;   - Older iterations excluded from prompt (still logged)
;;   Expected savings: caps history at ~12K tokens regardless
;;
;; Phase 3 (rolling summary, new skill):
;;   - Add summarize-progress skill
;;   - Harness stores and replaces rolling summary
;;   - Summary appears between anchor and working window
;;   Expected savings: preserves context across long sessions
;;   while staying bounded
;;
;; Phase 4 (sophisticated, future):
;;   - Importance scoring for history entries
;;   - Temporal decay weighting
;;   - Automatic summary generation by harness (not LLM)
;;
;; ============================================================
;; END OF PROPOSAL
;; ============================================================
