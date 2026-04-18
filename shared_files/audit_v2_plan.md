# Audit V2 - Fix False Negatives

## Problem
PNS-sustaining sentences fail because neutral function words drag avg valence below -0.5.
Example: I notice you said that. I am here with you. No rush. v=-0.886 REVISE (should PASS)

## Solution: Triple Gate
1. avg_valence > -1.0 (loose floor filters truly harsh language)
2. sns_ratio < 0.05 (no SNS trigger words)
3. pns_count >= 2 (actively PNS-sustaining)

All three must pass. This fixes false negatives while preserving true SNS detection.
