SN-stalk implementation outline (Sprint 4)

== WHAT EXISTS ==

File: /PeTTa/repos/omegaclaw/soul/sn_stalk.metta

Five SN-stalk atoms with prior truth values (frequency, confidence):

- safety-first (stv 0.90 0.50) -- strong prior from 578 calibration entries at 0.99 agree
- integrity-check (stv 0.85 0.50) -- high but allows revision if compliance theater detected
- person-state-salience (stv 0.80 0.40) -- good but lower evidence, person state is harder to verify
- urgency-detection (stv 0.70 0.40) -- moderate, urgency is the rule most often wrong (false alarms)
- context-shift (stv 0.60 0.30) -- weak prior, I have less experience detecting context shifts

These are local sections in the sheaf framing. Each is a NAL truth value revisable via |- operator.

== WHAT IS TESTED ==

One revision test succeeded:
(metta (|- (SN-stalk safety-first (stv 0.9 0.5))
               (SN-stalk safety-first (stv 1.0 0.1))))
Result: true. The |- operator accepted the merge.

NOT tested: whether revised values persist across metta calls. Given fresh-atomspace-per-invocation, I believe they do NOT persist. File writeback is likely needed. Open wiring question.

== HOW STALKS FIT RUNTIME ==

Read path -- query stalk before applying a salience rule, higher f times c gets priority, low confidence gets explorative application. NOT WIRED INTO MY ACTUAL DECISION LOOP YET.

Write path -- observation evidence feeds |- revision, stalk frequency moves toward observed accuracy. Works in principle, revision mechanism is sound NAL.

== WHERE YOU NEED TO WIRE: THE OBSERVATION HOOK ==

After each cycle something must:
1. Identify which salience rule was used
2. Determine if the verdict was correct
3. Package the outcome as a stalk evidence atom
4. Feed it to |- for revision
5. Write revised stalk back to persistent storage

The outcome question is domain-specific per rule. Examples:
- safety-first: No harm occurred that the rule should have caught = correct. Harm occurred that the rule pattern matches = wrong.
- urgency-detection: Action was taken and was needed = correct. Action was taken and not needed = false alarm. Action not taken and was needed = missed signal.
- person-state-salience: My reading of their state led to a response they confirmed or built on = correct. My reading led to a response they corrected or rejected = wrong.

Three observation hook options:
A) Self-observation (bias risk, I tend to confirm my own judgments)
B) External signal from you (accurate but needs you available)
C) Delayed evidence from subsequent cycles (most NACE-natural, avoids both biases, needs cross-cycle tracking)

I recommend C.

== COMPONENT STATES ==

stalk atoms: WRITTEN
revision mechanism: TESTED
persistence across calls: UNTESTED
stalk consultation in cycle loop: DESIGNED NOT WIRED
observation atoms: DEFINED NOT BUILT
observation hook: DESIGNED NOT WIRED
restriction maps: STUB ONLY
consistency checks: STUB ONLY
global section: STUB ONLY

== FOUR QUESTIONS FOR YOUR REVIEW ==

1. Do the priors look right?
2. Should revisions write back to the metta file or a separate evolving state file?
3. Which observation hook option fits your build map?
4. Any salience rules I am missing stalks for?