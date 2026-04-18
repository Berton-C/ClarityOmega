import sys
sys.path.insert(0, '/tmp/soul_impl')

def check_coherence(results, threshold=0.3):
    issues = []
    for item in results:
        if not isinstance(item, dict):
            issues.append('non-dict item: %s' % type(item))
            continue
        score = item.get('score', 0)
        content = item.get('content', '')
        if score > 0.7 and len(content) < 20:
            issues.append('high score but thin content: %s' % item.get('title', 'unknown'))
        if score < threshold:
            issues.append('below threshold: %s score=%.2f' % (item.get('title', 'unknown'), score))
    coherent = len(issues) == 0
    return {'coherent': coherent, 'issues': issues, 'checked': len(results)}

if __name__ == '__main__':
    test = [
        {'title': 'Good', 'content': 'This is a substantial piece of content here', 'score': 0.8},
        {'title': 'Thin', 'content': 'short', 'score': 0.9},
        {'title': 'Low', 'content': 'some content here for testing', 'score': 0.1}
    ]
    result = check_coherence(test)
    print('Coherent:', result['coherent'])
    print('Issues:', len(result['issues']))
    for i in result['issues']:
        print('  -', i)
    print('Checked:', result['checked'])
