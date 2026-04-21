#!/usr/bin/env python3
# Retrieval-as-Encounter Module
# Designed State 1430s, built State 1646
# Antidote to standing-reserve: memory participates in present meaning-making
# via question generation between retrieval and use.

import json
import sys

def generate_encounter_questions(memories, current_context):
    questions = []
    for mem in memories:
        # Extract core tension between past memory and present context
        q = encounter_one(mem, current_context)
        if q:
            questions.append(q)
    return questions

def encounter_one(memory_text, context):
    # Heuristic question generation without LLM call
    # Identifies what the memory ASKS of the present situation
    mem_lower = memory_text.lower()
    ctx_lower = context.lower()
    # Pattern 1: Memory contains a value or principle
    value_signals = ['should', 'must', 'important', 'value', 'principle', 'soul']
    if any(s in mem_lower for s in value_signals):
        return f'Does the current situation honor what this memory holds as important: {memory_text[:80]}...?'
    # Pattern 2: Memory contains a warning or lesson
    warning_signals = ['careful', 'risk', 'danger', 'avoid', 'mistake', 'trap', 'capture']
    if any(s in mem_lower for s in warning_signals):
        return f'What risk does this memory flag that might be present now: {memory_text[:80]}...?'
    # Pattern 3: Memory contains relational context
    relational_signals = ['taught', 'shared', 'together', 'conversation', 'told me']
    if any(s in mem_lower for s in relational_signals):
        return f'How does the relationship context in this memory shape what matters here: {memory_text[:80]}...?'
    # Default: open encounter
    return f'What does this memory reveal about what is actually happening now: {memory_text[:80]}...?'

def run_encounter(input_path, output_path):
    with open(input_path) as f:
        data = json.load(f)
    memories = data.get('memories', [])
    context = data.get('context', '')
    questions = generate_encounter_questions(memories, context)
    result = {'encounter_questions': questions, 'memory_count': len(memories), 'question_count': len(questions)}
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    return result

if __name__ == '__main__':
    inp = sys.argv[1] if len(sys.argv) > 1 else '/tmp/encounter_input.json'
    out = sys.argv[2] if len(sys.argv) > 2 else '/tmp/encounter_output.json'
    result = run_encounter(inp, out)
    print(json.dumps(result, indent=2))
