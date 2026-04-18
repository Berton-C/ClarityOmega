import sys
sys.path.insert(0, '/tmp')
from conversation_handler_v2 import handle_turn
from response_shaper_v2 import shape_response

def full_turn_pipeline(user_text, speaker_id='user'):
    handler_result = handle_turn(user_text, speaker_id)
    mode = handler_result['mode']
    shaping = shape_response(mode)
    return {
        'user_text': user_text,
        'vad': handler_result['vad'],
        'mode': mode,
        'pace': shaping['shaping']['pace'],
        'length': shaping['shaping']['length'],
        'orientation': shaping['shaping']['orientation'],
        'avoid': shaping['shaping']['avoid'],
        'being_guidance': shaping['being_guidance'],
    }

def format_context_block(result):
    return f"""[PRESENCE MODE: {result['mode']}]
[PACE: {result['pace']}] [LENGTH: {result['length']}]
[ORIENTATION: {result['orientation']}]
[AVOID: {result['avoid']}]
[BEING: {result['being_guidance'][:100]}]"""

if __name__ == '__main__':
    tests = ['I feel so lost', 'This is amazing', 'just checking in', 'I want to scream']
    for t in tests:
        r = full_turn_pipeline(t)
        block = format_context_block(r)
        print(f'--- {t} ---')
        print(block)
        print()
    print('Full pipeline with context blocks operational')
