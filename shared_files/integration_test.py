import sys
sys.path.insert(0, '/tmp')
try:
    from agent_loop_mode_protocol import full_turn_pipeline, format_context_block
    tests = [
        'I feel lost and I do not know what to do',
        'This is incredible I feel so alive right now',
        'Just checking in nothing special',
    ]
    for t in tests:
        result = full_turn_pipeline(t)
        block = format_context_block(result)
        print(f'INPUT: {t}')
        print(f'MODE: {result.get("mode", "NONE")}')
        print(f'BLOCK: {block[:120]}')
        print()
    print('Integration test PASSED')
except Exception as e:
    print(f'Integration test FAILED: {e}')
    import traceback
    traceback.print_exc()
