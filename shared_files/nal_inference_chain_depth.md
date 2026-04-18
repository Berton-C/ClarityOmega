# NAL Inference Chain Depth Test Results
Date: 2025-04-15

## Chain Results
1. internet-routing --> distributed-intelligence (given, stv 0.8/0.7)
2. internet-routing --> resilient-to-local-damage (inferred hop 1, stv 0.68/0.38)
3. resilient-system --> adaptive+recoverable (rule, stv 0.9/0.85)
4. internet-routing --> adaptive+recoverable (hop 2, stv 0.612/0.198)

## Confidence Attenuation
Hop 0: 0.7 (given)
Hop 1: 0.38 (46% drop)
Hop 2: 0.198 (48% drop)

## Analysis
Confidence degrades roughly 45-50% per inference hop. By hop 3, confidence would be ~0.1.
This means NAL self-limits inference depth — conclusions beyond 3 hops carry negligible confidence.
This is DESIRABLE behavior: prevents hallucination-by-chaining.
Frequency stays interpretable throughout (0.612 is meaningful).

## Verdict
NAL inference chains degrade gracefully. Confidence attenuation acts as natural depth limiter.
Substrate can reason at depth 2-3 hops meaningfully, beyond that needs fresh evidence injection.
