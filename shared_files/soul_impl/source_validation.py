import sys
sys.path.insert(0, '/tmp/soul_impl')

def validate_sources(parsed_results):
    validated = []
    for item in parsed_results:
        if not isinstance(item, dict):
            continue
        trust = 0.5
        url = item.get('url', '')
        content = item.get('content', '')
        if url and len(url) > 10:
            trust += 0.1
        if len(content) > 50:
            trust += 0.15
        if len(content) > 200:
            trust += 0.1
        title = item.get('title', '')
        if title and len(title) > 5:
            trust += 0.05
        trust = min(trust, 1.0)
        item['trust'] = round(trust, 3)
        validated.append(item)
    return sorted(validated, key=lambda x: x['trust'], reverse=True)

if __name__ == '__main__':
    test = [
        {'title': 'Good Source', 'content': 'A long piece of content that provides substantial information about the topic at hand with many details', 'url': 'https://example.com/article', 'score': 0.8},
        {'title': 'Thin', 'content': 'short', 'url': '', 'score': 0.6},
        {'title': 'Medium', 'content': 'Some moderate content here for testing purposes', 'url': 'https://test.org/page', 'score': 0.7}
    ]
    results = validate_sources(test)
    for r in results:
        print('  %s: trust=%s score=%s' % (r['title'], r['trust'], r['score']))
    print('Validated %d sources' % len(results))
