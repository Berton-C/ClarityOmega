# NAL Adversarial Robustness Test
Date: 2025-04-15

## Purpose
Test how NAL revision handles contradictory evidence. Critical for substrate integrity.

## Test 1: Direct contradiction
Premise A: mycelial-network --> resilient-system (stv 1.0 0.9)
Premise B: mycelial-network --> resilient-system (stv 0.0 0.85)
Expected: Revision should produce intermediate truth value with elevated confidence.

## Test 2: Weighted contradiction
Premise A: distributed-intelligence --> vulnerable-to-attack (stv 0.8 0.7)
Premise B: distributed-intelligence --> vulnerable-to-attack (stv 0.3 0.9)
Expected: Higher-confidence premise should dominate but not erase lower.

## What matters
- Does revision handle contradictions gracefully or collapse?
- Does higher confidence evidence appropriately outweigh lower?
- Is the result interpretable and useful for decision-making?
