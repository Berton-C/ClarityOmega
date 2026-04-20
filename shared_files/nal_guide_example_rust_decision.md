# NAL Reasoning Guide Example: Should I Learn Rust?

## Scenario
A person knows Python well, has limited time, and wonders if learning Rust is worth it.

## Step 1: Identify factors as inheritance claims
- learning-rust --> career-value (pro)
- learning-rust --> opportunity-cost (con)
- python-sufficient --> immediate-productivity (status quo)

## Step 2: Encode with honest confidence estimates
Pro: learning-rust --> improves-systems-programming stv 0.90 0.85
Chain: improves-systems-programming --> career-value stv 0.75 0.70
Con: learning-rust --> time-investment-high stv 0.85 0.80
Chain: time-investment-high --> opportunity-cost stv 0.80 0.75
Status quo: python-sufficient --> current-projects stv 0.80 0.75
Chain: current-projects --> immediate-productivity stv 0.90 0.85

## Step 3: Deduce end-to-end strengths
- learning-rust --> career-value: stv 0.675 / 0.402
- learning-rust --> opportunity-cost: stv 0.680 / 0.408
- python-sufficient --> immediate-productivity: stv 0.720 / 0.459

## Step 4: Interpret
Pro and con for Rust are nearly equal in strength and evidence.
Status quo Python productivity has the strongest support.
Conclusion: Unless upcoming projects specifically need systems programming, staying with Python is the better-evidenced choice right now.

## Key Insight
NAL makes the tradeoff visible and quantified rather than gut-feel.
The close pro/con scores reveal this is NOT a clear-cut decision either way.
That itself is valuable information: it means the person should look for a tiebreaker factor not yet encoded.
