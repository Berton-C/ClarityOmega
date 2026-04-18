import sys
sys.path.insert(0, '/tmp/soul_impl')
from web_result_parser import parse_search_results, rank_results
from coherence_check import check_coherence
from source_validation import validate_sources

def score_web_component():
    test_data = [{'title': 'Test Result', 'content': 'A substantial piece of content for testing the web pipeline end to end', 'url': 'https://example.com/test', 'score': 0.75}]
    parsed = parse_search_results(test_data)
    ranked = rank_results(parsed)
    coherence = check_coherence(ranked)
    validated = validate_sources(ranked)
    pipeline_works = len(parsed) > 0 and len(ranked) > 0 and len(validated) > 0
    freq = 0.8 if pipeline_works else 0.4
    if coherence['coherent']:
        freq += 0.1
    freq = min(freq, 0.95)
    conf = 0.3 + (0.5 * freq)
    fc = round(freq * conf, 4)
    print('Web scored: f=%.3f c=%.3f fc=%.4f' % (freq, conf, fc))
    print('Pipeline: %s' % ('PASS' if pipeline_works else 'FAIL'))
    return {'f': freq, 'c': conf, 'fc': fc}

if __name__ == '__main__':
    score_web_component()
