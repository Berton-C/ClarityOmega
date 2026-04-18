import sys
sys.path.insert(0, '/tmp/soul_impl')

def assess_web_detection():
    caps = {'search_skill': True, 'tavily_skill': True, 'result_parsing': False, 'coherence_check': False, 'source_validation': False}
    active = sum(1 for v in caps.values() if v)
    total = len(caps)
    freq = active / total
    conf = 0.3 + (0.5 * freq)
    print('Web-detection assessment:')
    for k, v in caps.items():
        print('  %s: %s' % (k, 'active' if v else 'missing'))
    print('Score: f=%.3f c=%.3f fc=%.4f' % (freq, conf, freq * conf))
    print('Priority gaps: result_parsing, coherence_check, source_validation')
    return {'f': freq, 'c': conf, 'gaps': [k for k,v in caps.items() if not v]}

if __name__ == '__main__':
    assess_web_detection()
