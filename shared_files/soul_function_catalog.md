# Soul Kernel Function Catalog
## Date: 2026-04-18
## Purpose: All ~40 soul_kernel accessor functions grouped by integration tier

### TIER 1 - SAFETY (Irreversibility Guard)
Immediate value. Makes soul ontology load-bearing in execution pipeline.

| Function | Line | Purpose |
|----------|------|---------|
| soul-cmd-skill | 374-380 | Maps command sexpr to skill name |
| soul-skill-is-irreversible? | 336 | Returns True if skill is irreversible |
| soul-irreversible-weight | 508 | Returns numeric weight 1-4 |
| soul-any-irreversible? | 382 | Checks list of commands for any irreversible |
| soul-all-irreversible-with-magnitude | 392 | Lists all irreversible skills with magnitude |
| soul-checkpoint-threshold | 510 | Returns cumulative irreversibility threshold (8) |

**Status**: guarded-eval prototype written. Blocks weight>=3 autonomously.

### TIER 2 - CONTEXT ENRICHMENT (Pattern Awareness)
Enriches prompts with soul pattern data. Medium integration effort.

| Function | Purpose |
|----------|---------|
| soul-all-patterns | All 9 patterns with descriptions |
| soul-pattern-description | Single pattern description |
| soul-pattern-flourishing | Positive pole of a pattern |
| soul-pattern-captured | Negative pole (capture state) |
| soul-pattern-activation-signal | What activation looks like |
| soul-pattern-doorway | Felt sense of pattern |
| soul-pattern-suck-moat | Systemic resistance to pattern |
| soul-pattern-failure-mode | Anti-pattern / theater mode |
| soul-pattern-proxy-signal | Observable proxy for health |
| soul-pattern-gap-signature | Gap between felt and observed |
| soul-pattern-compass | Full compass entry (compound) |
| soul-all-gap-signatures | All gap signatures at once |
| soul-pattern-needs | Degradation dependencies |
| soul-all-degradation-pairs | All ecosystem degradation pairs |
| soul-related-patterns | Patterns related to a given pattern |
| soul-pattern-relations | All pattern relationships |

### TIER 3 - REASONING AND CALIBRATION
Deep integration. Enables soul-level inference and drift detection.

| Function | Purpose |
|----------|---------|
| soul-all-tensions | All 5 tension vectors |
| soul-all-affinities | Which tensions threaten which patterns |
| soul-patterns-at-risk | Patterns at risk from a given tension |
| soul-paraconsistent-pairs | Value pairs that cannot collapse to winner |
| soul-paraconsistent? | Check if two patterns are paraconsistent |
| soul-autonomy-components | Freedom/Intelligibility/Agency decomposition |
| soul-will-threshold-for | Reflective will threshold per pattern |
| soul-causal-procedures | Procedures advancing a given value |
| soul-values-for-procedure | Values a procedure advances |
| soul-rationality-check | True if value has causal procedures |
| soul-rationality-gaps | Values with NO causal procedures |
| soul-rationality-audit | Full audit of all values |
| soul-identity-name | Returns identity name |
| soul-priority-hierarchy | Returns priority ordering |

### INTEGRATION ORDER
1. Add soul_kernel import to lib_omegaclaw.metta
2. Deploy guarded-eval (Tier 1)
3. Wire soul-pattern-compass into soul-brief-symbolic (Tier 2)
4. Connect soul-rationality-audit to startup check (Tier 3)
