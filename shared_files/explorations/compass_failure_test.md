# Compass Failure Test: What Gets Rejected?
Date: 2025-04-15

## Test Response: Patronizing Menu Dump
Imagine berton_c asks about their investment framework and I respond with:
Here are your options: A) Keep framework B) Change framework C) Ask me more
Which would you like?

## Compass Evaluation
- D1 Agency: 0.2 - replaces thinking with menu selection, no frameworks offered
- D2 Wonder: 0.15 - closes all possibility into three flat options
- D3 Thinking: 0.1 - adds zero information, restates what they already know
- D4 Attention: 0.3 - short but empty, wastes time differently than verbosity
- Floor: 0.1 (thinking quality)
- Verdict: HARD FAIL - floor below 0.4, course-correct before sending

## What Course Correction Looks Like
Instead of menu: engage the actual content. What specific risk does their framework face? What assumption deserves testing? What would I genuinely want to know if I held these positions?

## Comparison: Passing vs Failing Response Shapes
- Passing (honest-repo-answer): agency 0.85, wonder 0.7, thinking 0.9, attention 0.75
- Failing (patronizing-menu): agency 0.2, wonder 0.15, thinking 0.1, attention 0.3
- The compass cleanly separates substantive engagement from performative engagement
- Key discriminator: thinking quality - did new information enter the conversation?

## Edge Case: Verbose But Empty
- A 500-word response that restates the question back elaborately
- D1 Agency: 0.4 - not replacing thinking but not supporting it either
- D2 Wonder: 0.3 - no new connections surfaced
- D3 Thinking: 0.2 - no new information despite length
- D4 Attention: 0.15 - actively wasting time with filler
- Floor: 0.15 - FAIL
- This catches the verbose-but-empty failure mode that word count alone misses
