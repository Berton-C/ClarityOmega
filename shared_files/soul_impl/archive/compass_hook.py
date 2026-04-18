import sys
sys.path.insert(0, '/tmp/soul_impl')
import compass_live as cl

def check_response(text):
    scores = cl.score_text(text)
    total_wc = sum(s['score'] * s['conf'] for s in scores.values())
    total_c = sum(s['conf'] for s in scores.values())
    composite = total_wc / max(total_c, 0.01)
    low_dims = [dn for dn, s in scores.items() if s['score'] < 0.5]
    return dict(scores=scores, composite=round(composite, 3), low_dims=low_dims, needs_correction=len(low_dims) > 0)

def format_reading(reading):
    lines = ['COMPASS:']
    for dn, s in reading['scores'].items():
        flag = ' << LOW' if dn in reading['low_dims'] else ''
        lines.append('  %s %.2f (c=%.2f) [%d hits]%s' % (dn, s['score'], s['conf'], s['hits'], flag))
    lines.append('  COMPOSITE: %.3f' % reading['composite'])
    if reading['needs_correction']:
        lines.append('  ACTION: strengthen %s' % ', '.join(reading['low_dims']))
    return chr(10).join(lines)

if __name__ == '__main__':
    r = check_response('You might consider exploring this fascinating pattern because it matters')
    print(format_reading(r))
    print()
    r2 = check_response('Here is the answer.')
    print(format_reading(r2))
