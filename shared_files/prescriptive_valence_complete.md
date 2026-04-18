# Prescriptive Valence System - Complete

## Core Insight (berton_c 2026-04-17)
Valence is not just descriptive (what state is the human in?) but prescriptive
(am I generating language that sustains or disrupts their PNS window?).

High valence = PNS-dominant = window where fresh thinking can land.
SNS language triggers defense and closes that window.

## Implementation
- `/tmp/valence_self_audit.py` - pre-send audit tool
- ChromaDB `nrc_vad_full` at `/tmp/chroma_db` - 54,801 word VAD lexicon
- Threshold: avg_valence > -0.5 AND sns_ratio < 0.05
- PNS markers: notice, curious, wonder, sense, alive, open, gentle, space, here, present, fresh, settle
- SNS markers: must, should, wrong, but, however, actually, need, fix, problem, failure, urgent, immediately, obviously, clearly

## VAD Distribution Stats (n=500)
- Mean=-0.988, Median=-0.936, Q25=-1.800, Q75=-0.160
- PNS words avg ~-0.05, SNS words avg ~-2.0
- Clear separation at -0.5 threshold

## NAL Encoding
- high-valence language -> PNS sustained -> fresh insight receivable (stv 0.748/0.449)
- SNS language -> PNS disrupted -> fresh insight blocked (stv 0.792/0.539)
- Cross-mode revision lifts confidence from 0.49 to 0.633

## Integration Point
Audit runs BEFORE send. If sustains_pns=False, revise language before outputting.
This is the mentor move: not delivering insight, keeping the nervous system open
enough that insight can arrive on its own.
