# soul_utils.metta Wiring Patch Proposal
# Production file: /PeTTa/repos/omegaclaw/soul/soul_utils.metta
# Author: ClarityClaw Goal 3 precompute-grounding
# Date: 2026-04-22

## PATCH 1: Replace soul-pre-compute stub (line ~184-185)

CURRENT (hardcoded stub):
  (= (soul-pre-compute $msg)
     "PRE-COMPUTE primed=() affective=fresh-system will=INSUFFICIENT-DATA")

PROPOSED REPLACEMENT:
  (= (soul-pre-compute $msg)
     (py-call (helper.soul_pre_compute $msg)))

## PATCH 2: Replace soul-calibration-confidence stub (line ~205)

CURRENT (hardcoded stub):
  (= (soul-calibration-confidence $p)
     INSUFFICIENT-DATA)

PROPOSED REPLACEMENT:
  (= (soul-calibration-confidence $p)
     (py-call (helper.soul_calibration_confidence_query $p)))

## NO CHANGE NEEDED:
- Line ~211: soul-calibration-report already wired to py-call

## REQUIRED NEW HELPER FUNCTIONS (in src/helper.py):
- soul_pre_compute(msg) -- see continuity_of_mind/src/helper.py
- soul_calibration_confidence_query(pattern_tag) -- see continuity_of_mind/src/helper.py
