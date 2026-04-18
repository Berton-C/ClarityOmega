import sys
sys.path.insert(0, '/tmp')
try:
    from conversation_handler_v2 import handle_turn
    print('handler imports clean')
    r = handle_turn('I feel lost')
    print(f"mode: {r['mode']}")
    print(f"guidance: {r['guidance'][:60]}...")
    print('END-TO-END PASS')
except Exception as e:
    print(f'FAIL: {e}')
