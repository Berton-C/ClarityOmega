import sys
sys.path.insert(0, '/tmp/soul_impl')
import compass_hook as ch

def pre_send_check(response_text, threshold=0.5):
    reading = ch.check_response(response_text)
    if reading['needs_correction']:
        suggestions = []
        for dim in reading['low_dims']:
            if dim == 'agency':
                suggestions.append('add choices or options for the user')
            elif dim == 'wonder':
                suggestions.append('surface something surprising or worth exploring')
            elif dim == 'thinking':
                suggestions.append('add reasoning or evidence')
            elif dim == 'attention':
                suggestions.append('be more specific and honest about what matters')
        return dict(ok=False, reading=reading, suggestions=suggestions)
    return dict(ok=True, reading=reading, suggestions=[])

if __name__ == '__main__':
    print('=== GOOD RESPONSE ===')
    r1 = pre_send_check('You might consider exploring this fascinating pattern because it matters')
    print(ch.format_reading(r1['reading']))
    print('OK:', r1['ok'])
    print()
    print('=== FLAT RESPONSE ===')
    r2 = pre_send_check('Here is the answer.')
    print(ch.format_reading(r2['reading']))
    print('OK:', r2['ok'])
    print('Suggestions:', r2['suggestions'])
