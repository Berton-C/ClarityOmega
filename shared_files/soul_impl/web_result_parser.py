import sys
sys.path.insert(0, '/tmp/soul_impl')
import json

def parse_search_results(raw_results):
    if isinstance(raw_results, str):
        try:
            raw_results = json.loads(raw_results)
        except Exception:
            return [{'title': 'raw', 'content': raw_results, 'score': 0.5}]
    if isinstance(raw_results, list):
        parsed = []
        for item in raw_results:
            if isinstance(item, dict):
                parsed.append({'title': item.get('title', ''), 'content': item.get('content', item.get('snippet', '')), 'url': item.get('url', ''), 'score': item.get('score', 0.5)})
            elif isinstance(item, str):
                parsed.append({'title': '', 'content': item, 'score': 0.3})
        return parsed
    return [{'title': 'unknown', 'content': str(raw_results), 'score': 0.2}]

def rank_results(parsed, min_score=0.3):
    filtered = [r for r in parsed if r['score'] >= min_score]
    return sorted(filtered, key=lambda x: x['score'], reverse=True)

if __name__ == '__main__':
    test = [{'title': 'A', 'content': 'text a', 'score': 0.8}, {'title': 'B', 'snippet': 'text b', 'score': 0.2}, 'raw string']
    parsed = parse_search_results(test)
    ranked = rank_results(parsed)
    for r in ranked:
        print('  %s: score=%s' % (r['title'], r['score']))
    print('Parsed %d, ranked %d' % (len(parsed), len(ranked)))
