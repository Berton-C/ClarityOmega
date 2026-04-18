# Goal 12 Step 6: Embedding Memory Bridge Design

## Problem
The felt-sense field currently seeds from fallback constants or prior accumulation.
It should also incorporate signals from real embedding memory queries.

## Architecture
1. On each exchange, query embedding memory with key phrases from user message
2. Extract emotional/relational patterns from retrieved memories
3. Use those patterns to modulate the felt-sense field before resonance computation
4. This creates a feedback loop: past conversations shape present felt-sense

## Data Flow
user_message -> extract_query_phrases(msg) -> query(phrases) -> parse_memory_signals(results) -> modulate_field(signals, current_field) -> resonance_computation

## Implementation Steps
- Step 6a: Write query phrase extractor from user messages
- Step 6b: Write memory signal parser that extracts VAD/relational signals from query results
- Step 6c: Write field modulation function that blends memory signals into current field
- Step 6d: Wire into felt_sense_pipeline_v2.py
- Step 6e: Test with real queries against actual embedding memory

## Key Constraint
Query results are text strings with timestamps. Parser must extract signal from natural language memory entries. This is the interpretive bridge between symbolic memory and distributed felt-sense.
