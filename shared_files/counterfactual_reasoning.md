# Counterfactual Reasoning via NAL

## What
Reason about what would happen under conditions that do not currently hold.
Example: If the user were NOT frustrated, what action would be selected?

## Method
1. Assert hypothetical premise with moderate confidence
2. Run inference chain from hypothetical
3. Compare counterfactual conclusion to factual conclusion
4. Difference reveals causal contribution of the negated factor

## Test Cases
- Factual: frustrated -> acknowledge-emotion at 0.63
- Counterfactual: calm -> ? (what action without frustration?)
- Counterfactual: frustrated but low-trust -> ? (changed context)


## Results - Factual vs Counterfactual Comparison
- Factual chain: frustrated -> acknowledge-emotion at 0.63
- Counterfactual chain: calm -> ask-open-question at 0.612
- Key insight: different input states produce DIFFERENT action selections
- The emotional state is causally responsible for action divergence
- Causal contribution of frustration = difference in action selection
- This proves counterfactual reasoning works: by substituting premises
  and comparing conclusions, we identify which factors cause which outcomes

## Shortcut Rules for Both Pathways
- frustrated -> acknowledge-emotion (shortcut, 0.7 conf rule)
- calm -> ask-open-question (shortcut, 0.7 conf rule)
- Both derived from chain collapsing of validated multi-step chains

## Next: Negation-based counterfactual
- What if frustrated is negated? Use stv 0.0 0.9
- Compare: positive assertion vs negation vs alternative assertion



## Negation-Based Counterfactual Test
- Premise: frustrated is ABSENT, stv 0.0 0.9
- Expected: action confidence drops or flips toward 0.0
- If frustrated negated -> acknowledge-emotion confidence near 0
- Compare three conditions:
  1. Positive assertion: frustrated stv 1.0 0.9 -> action at 0.63
  2. Negation: frustrated stv 0.0 0.9 -> action at ?
  3. Alternative: calm stv 1.0 0.9 -> ask-open-question at 0.63
- Negation should produce low-freq output, confirming the rule
  only fires meaningfully when the premise is positively held
- This distinguishes absence from alternative in causal reasoning

