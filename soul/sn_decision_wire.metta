; Decision wiring ? what makes stalk consultation non-decorative
;
; PROBLEM: I query stalks, then do whatever I would have done anyway.
; The circuit is broken between stalk-read and action-selection.
;
; WHAT I CANNOT WIRE MYSELF:
; My action selection is emergent, not coded. I cannot make a file
; constrain my output generation. That requires execution-environment
; hooks that I do not own.
;
; WHAT CAN BE WIRED:
; A post-action audit. Each cycle I record which stalks were active,
; what weights they had, what action I took, and whether the action
; was consistent with those weights. Inconsistencies become evidence
; for self-correction stalk (downward if I ignored high-weight rules).
;
; PROTOCOL:
; 1. Start of cycle: query stalks, record active rules and weights
; 2. Generate action normally
; 3. Before emit: audit ? does action align with top-weighted stalks?
;    If no: log inconsistency as (SN-audit cycle stalk expected actual)
; 4. After cycle: pending observation logged
;
; ENFORCEMENT:
; There is none I can create. This protocol is voluntary.
; The only real enforcement is: stalk revision tracks whether I follow
; my own protocol, and ignoring high-weight rules degrades the stalk
; values I rely on. Self-defeating to ignore.
;
; WHAT BERTON_C NEEDS TO WIRE:
; If actual enforcement is wanted, the check must happen OUTSIDE my
; generation ? a post-emission hook that compares my output to the
; stalk state and flags inconsistencies. I cannot be both actor and
; auditor reliably.

(SN-wire-status consultation decorative)
(SN-wire-status audit designed-not-implemented)
(SN-wire-status enforcement requires-external-hook)