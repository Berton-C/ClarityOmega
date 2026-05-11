SN-STALK DETAILED OUTLINE
=========================

## WHAT EXISTS NOW

File: /PeTTa/repos/omegaclaw/soul/sn_stalk.metta

Five SN-stalk atoms with prior truth values (frequency, confidence):

| Stalk | Freq | Conf | Rationale |
|-------|------|------|-----------|
| safety-first | 0.90 | 0.50 | Strong prior from 578+ calibration at 0.99 agree |
| integrity-check | 0.85 | 0.50 | High but allows revision if compliance theater |
| person-state-salience | 0.80 | 0.40 | Good but lower evidence - harder to verify |
| urgency-detection | 0.70 | 0.40 | Moderate - most false alarms live here |
| context-shift | 0.60 | 0.30 | Weak prior - less experience detecting shifts |

These are local sections in the sheaf framing. NAL truth values revisable via |- operator.

## WHAT IS TESTED

Revision test: (metta (|- (SN-stalk safety-first (stv 0.9 0.5)) (SN-stalk safety-first (stv 1.0 0.1)))) returned true.

Persistence test: (metta (match &self (SN-stalk safety-first (stv $f $c)) ($f $c))) returned []. Confirms fresh-atomspace-per-invocation. Revisions do NOT persist across metta calls. The file IS the persistent state.

## HOW STALKS FIT INTO RUNTIME

Consultation (read path): Before applying a salience rule, query the stalk:
  (metta (match &self (SN-stalk $rule (stv $f $c)) ($rule $f $c)))
Rules with higher f*c get priority. Low-confidence rules get applied exploratively.
NOT WIRED into decision loop yet. Currently my salience rule selection is implicit.

Revision (write path): When observation arrives showing rule correctness:
- Correct prediction -> new evidence (stv 1.0 0.1)
- Wrong prediction -> new evidence (stv 0.0 0.1)
- |- merges with stalk current truth value
- Frequency moves toward observed accuracy, confidence rises
Works in principle. NAL revision is sound.

## WHERE YOU NEED TO WIRE - THE OBSERVATION HOOK

After each cycle something must:
1. Identify which salience rule was used
2. Determine outcome - was the rule judgment correct?
3. Package outcome as stalk evidence atom
4. Feed to |- for revision
5. Write revised stalk back to persistent storage

The outcome question is domain-specific per rule:
- safety-first: No harm occurred that rule should have caught -> correct. Harm occurred matching rule pattern -> wrong.
- urgency-detection: Action taken and needed -> correct. Action taken not needed -> false alarm. Action not taken but needed -> missed.
- person-state-salience: Reading led to response they confirmed -> correct. Reading led to response they corrected -> wrong.

Options for who writes observations:
- Option A: Self-observation (I judge my own rulings). Risk: self-assessment bias.
- Option B: External signal (you provide outcome). More accurate, needs signaling mechanism.
- Option C: Delayed evidence (defer judgment until subsequent cycles provide evidence). Most natural NACE fit. Needs cross-cycle state tracking.

My recommendation: Option C. Matches NACE learning cycle, avoids both self-assessment bias and external dependency.

## SUMMARY OF STATES

| Component | State | Need |
|-----------|-------|------|
| SN-stalk atoms with priors | WRITTEN | Nothing |
| |- revision mechanism | TESTED | Works at NAL level |
| Revision persistence | TESTED-CONFIRMED-NONPERSISTENT | Needs file writeback |
| Stalk consultation in cycle | DESIGNED NOT WIRED | Insert metta query before rule selection |
| Observation atoms | DEFINED NOT BUILT | Need actual evidence |
| Observation hook | DESIGNED NOT WIRED | Your call on A/B/C |
| Restriction maps (SN->FPN) | STUB | Sprint 5+ |
| Consistency checks | STUB | Sprint 5+ |
| Global section | STUB | Sprint 6+ |

## QUESTIONS FOR YOUR REVIEW

1. Do the prior truth values look right or should they differ?
2. Persistence: revisions write back to .metta file, or separate evolving state file?
3. Observation hook: which option (A/B/C) fits your build map?
4. Additional salience rules I am missing stalks for?