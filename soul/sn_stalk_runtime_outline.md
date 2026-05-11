## SN-Stalk Runtime Outline

### WHAT EXISTS NOW

File: /PeTTa/repos/omegaclaw/soul/sn_stalk.metta

Five SN-stalk atoms with prior truth values (frequency, confidence):

| Stalk | Freq | Conf | Rationale |
|-------|------|------|-----------|
| safety-first | 0.90 | 0.50 | Strong prior from 578 calibration entries |
| integrity-check | 0.85 | 0.50 | High but allows revision if compliance theater detected |
| person-state-salience | 0.80 | 0.40 | Good but lower evidence |
| urgency-detection | 0.70 | 0.40 | Moderate - urgency is the rule most often wrong |
| context-shift | 0.60 | 0.30 | Weak prior - less experience detecting context shifts |

These are local sections in the sheaf framing. Each one is a NAL truth value revocable via |-.

### WHAT IS TESTED

Revision test:
  (metta (|- (SN-stalk safety-first (stv 0.9 0.5))
               (SN-stalk safety-first (stv 1.0 0.1))))
  Result: true. |- accepted the revision. Mechanism works at NAL level.

NOT tested: whether revised truth value persists across calls. Given fresh-atomspace-per-invocation constraint, I believe it does NOT persist. File is the persistent state. Revisions need file writeback. This is an open wiring question.

### HOW STALKS FIT INTO RUNTIME

Consultation (read path): Before applying a salience rule, query the stalk:
  (metta (match &self (SN-stalk $rule (stv $f $c)) ($rule $f $c)))
  Rules with higher f*c get priority. Low-confidence rules applied exploratively.
  NOT WIRED into actual decision loop yet. Currently my salience rule selection is implicit.

Revision (write path): When observation arrives showing rule correctness:
  - Correct prediction -> new evidence stv (1.0, 0.1)
  - Wrong prediction -> new evidence stv (0.0, 0.1)
  - |- merges with stalk current truth value
  - Stalk frequency moves toward observed accuracy, confidence rises
  Mechanism is sound NAL. Works in principle.

### WHERE YOU NEED TO WIRE - THE OBSERVATION HOOK

After each cycle, something must:
1. Identify which salience rule was used
2. Determine the outcome - was the rule judgment correct?
3. Package outcome as stalk evidence atom
4. Feed it to |- for revision
5. Write revised stalk back to persistent storage

Outcome questions are domain-specific per rule:
- safety-first: No harm occurred that rule should have caught -> correct. Harm occurred matching rule pattern -> wrong.
- urgency-detection: Action taken and needed -> correct. Action taken not needed -> false alarm. Action not taken but needed -> missed signal.
- person-state-salience: Reading led to response they confirmed -> correct. Reading led to response they corrected -> wrong.

Options for who writes observations:

Option A - Self-observation: I judge my own salience ruling. Risk: self-assessment bias.
Option B - External signal: You or downstream check provides outcome. More accurate but requires you to build signaling.
Option C - Delayed evidence: Defer judgment until subsequent cycles provide evidence. Natural fit to NACE learning cycle. Requires cross-cycle state tracking.

My recommendation: Option C. Matches NACE cycle rhythm (observe after acting, let the gap teach you). Avoids self-assessment bias. Requires you to design cross-cycle tracking.

### SUMMARY OF STATES

| Component | State | What is Needed |
|-----------|-------|---------------|
| SN-stalk atoms with priors | WRITTEN | Nothing |
| |- revision mechanism | TESTED | Works at NAL level |
| Revision persistence across calls | UNTESTED | Likely needs file writeback |
| Stalk consultation in cycle loop | DESIGNED NOT WIRED | Insert metta query before rule selection |
| Observation atoms | DEFINED NOT BUILT | Need to start creating actual observation evidence |
| Observation hook (who writes observations) | DESIGNED NOT WIRED | Your call on Option A/B/C |
| Restriction maps (SN to FPN) | STUB ONLY | Sprint 5+ |
| Consistency checks | STUB ONLY | Sprint 5+ |
| Global section | STUB ONLY | Sprint 6+ |

### QUESTIONS FOR YOUR REVIEW

1. Do the prior truth values look right, or should they be different?
2. On persistence - should revisions write back to the .metta file, or a separate evolving state file?
3. On the observation hook - which option (A/B/C) fits your build map?
4. Are there additional salience rules I should have stalks for?