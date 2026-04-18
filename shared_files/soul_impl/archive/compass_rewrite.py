import sys
sys.path.insert(0, '/tmp/soul_impl')
import compass_agent as ca

def rewrite_guidance(response_text):
    result = ca.pre_send_check(response_text)
    if result['ok']:
        return dict(action='send', text=response_text, reading=result['reading'])
    guidance = 'COMPASS COURSE-CORRECT before sending:\n'
    for s in result['suggestions']:
        guidance += '  - ' + s + '\n'
    guidance += 'Low dimensions: ' + ', '.join(result['reading']['low_dims']) + '\n'
    guidance += 'Composite: %.3f\n' % result['reading']['composite']
    return dict(action='revise', text=response_text, guidance=guidance, reading=result['reading'])

if __name__ == '__main__':
    print('=== PASSES ===')
    r1 = rewrite_guidance('You might consider exploring this fascinating pattern because it matters')
    print('Action:', r1['action'])
    print()
    print('=== NEEDS REVISION ===')
    r2 = rewrite_guidance('Here is the answer.')
    print('Action:', r2['action'])
    print(r2['guidance'])
