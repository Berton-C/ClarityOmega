import os
os.environ['HOME'] = '/tmp'

class SentenceVADCompositorV2:
    def __init__(self):
        self.vad_cache = {}
        self.negators = {'not', 'no', 'never', 'neither', 'nor', 'nobody', 'nothing', 'nowhere', 'hardly', 'barely', 'scarcely', 'without'}
        self.intensifiers = {'very': 1.3, 'really': 1.3, 'extremely': 1.5, 'incredibly': 1.5, 'absolutely': 1.4, 'totally': 1.3, 'so': 1.2, 'quite': 1.1, 'deeply': 1.3, 'terribly': 1.4, 'utterly': 1.5}
        self._init_chromadb()

    def _init_chromadb(self):
        try:
            import chromadb
            c = chromadb.PersistentClient(path='/tmp/chroma_db')
            self.coll = c.get_collection('nrc_vad_full')
        except Exception:
            self.coll = None

    def lookup_word(self, word):
        w = word.lower().strip('.,!?;:')
        if w in self.vad_cache:
            return self.vad_cache[w]
        if self.coll is None:
            return None
        try:
            r = self.coll.get(where={'word': w}, include=['metadatas'])
            if r['ids']:
                m = r['metadatas'][0]
                result = {'v': float(m['valence']), 'a': float(m['arousal']), 'd': float(m['dominance'])}
                self.vad_cache[w] = result
                return result
        except Exception:
            pass
        return None

    def segment_clauses(self, text):
        import re
        clauses = re.split(r'[,;.!?]|\bbut\b|\byet\b|\bthough\b|\bhowever\b|\balthough\b', text)
        return [c.strip() for c in clauses if c.strip()]

    def process_words(self, text):
        words = text.lower().split()
        readings = []
        i = 0
        while i < len(words):
            w = words[i].strip('.,!?;:')
            if w in self.negators:
                if i + 1 < len(words):
                    next_w = words[i+1].strip('.,!?;:')
                    vad = self.lookup_word(next_w)
                    if vad:
                        flipped = {'v': -vad['v'], 'a': vad['a'], 'd': -vad['d'], 'word': 'NOT_' + next_w}
                        readings.append(flipped)
                        i += 2
                        continue
                i += 1
                continue
            intensity = 1.0
            if w in self.intensifiers:
                intensity = self.intensifiers[w]
                if i + 1 < len(words):
                    next_w = words[i+1].strip('.,!?;:')
                    vad = self.lookup_word(next_w)
                    if vad:
                        amplified = {'v': vad['v'] * intensity, 'a': vad['a'] * intensity, 'd': vad['d'] * intensity, 'word': w + '_' + next_w}
                        readings.append(amplified)
                        i += 2
                        continue
            vad = self.lookup_word(w)
            if vad:
                readings.append({'v': vad['v'], 'a': vad['a'], 'd': vad['d'], 'word': w})
            i += 1
        return readings

    def clause_vad(self, clause):
        readings = self.process_words(clause)
        if not readings:
            return None
        n = len(readings)
        return {
            'v': round(sum(r['v'] for r in readings) / n, 3),
            'a': round(sum(r['a'] for r in readings) / n, 3),
            'd': round(sum(r['d'] for r in readings) / n, 3),
            'n_words': n,
            'words': [r.get('word','?') for r in readings]
        }

    def composite(self, text):
        clauses = self.segment_clauses(text)
        clause_data = []
        for i, clause in enumerate(clauses):
            vad = self.clause_vad(clause)
            clause_data.append({'text': clause, 'position': i, 'vad': vad})
        valid = [c for c in clause_data if c['vad'] is not None]
        if len(valid) < 2:
            full_readings = self.process_words(text)
            if full_readings:
                n = len(full_readings)
                fv = round(sum(r['v'] for r in full_readings) / n, 3)
                fa = round(sum(r['a'] for r in full_readings) / n, 3)
                fd = round(sum(r['d'] for r in full_readings) / n, 3)
                return {'composite_v': fv, 'composite_a': fa, 'composite_d': fd,
                        'n_clauses': len(clauses), 'n_valid': len(valid),
                        'fallback': 'full_sentence', 'word_count': n,
                        'words': [r.get('word','?') for r in full_readings],
                        'clauses': clause_data, 'pivot': None, 'trajectory_within': 'sparse_clauses'}
            return {'composite_v': 0.0, 'composite_a': 0.0, 'composite_d': 0.0,
                    'clauses': clause_data, 'pivot': None, 'trajectory_within': 'no_data'}
        n = len(valid)
        weights = [0.5 + 0.5 * (i / max(n - 1, 1)) for i in range(n)]
        total_w = sum(weights)
        comp_v = sum(c['vad']['v'] * w for c, w in zip(valid, weights)) / total_w
        comp_a = sum(c['vad']['a'] * w for c, w in zip(valid, weights)) / total_w
        comp_d = sum(c['vad']['d'] * w for c, w in zip(valid, weights)) / total_w
        pivot = None
        traj = 'stable'
        delta_v = valid[-1]['vad']['v'] - valid[0]['vad']['v']
        if abs(delta_v) > 0.15:
            traj = 'rising' if delta_v > 0 else 'falling'
        for i in range(1, n):
            d = valid[i]['vad']['v'] - valid[i-1]['vad']['v']
            if abs(d) > 0.3:
                pivot = {'at_clause': i, 'delta_v': round(d, 3), 'text': valid[i]['text']}
                break
        return {'composite_v': round(comp_v, 3), 'composite_a': round(comp_a, 3),
                'composite_d': round(comp_d, 3), 'n_clauses': len(clauses),
                'n_valid': n, 'clauses': clause_data, 'pivot': pivot,
                'trajectory_within': traj}

if __name__ == '__main__':
    svc = SentenceVADCompositorV2()
    tests = [
        'I was feeling terrible, but then something wonderful happened',
        'I am not happy about this at all',
        'Things started well however now I feel hopeless and lost',
        'I am really excited and very grateful for this opportunity',
        'Everything is great and I feel amazing'
    ]
    for t in tests:
        r = svc.composite(t)
        print('Sentence:', t)
        print('  Composite: v=%s a=%s d=%s' % (r['composite_v'], r['composite_a'], r['composite_d']))
        fb = r.get('fallback', 'clause_based')
        print('  Method:', fb, '| Clauses: %d valid of %d' % (r.get('n_valid', 0), r.get('n_clauses', 0)))
        if r.get('words'):
            print('  Words:', r['words'])
        print('  Trajectory:', r['trajectory_within'])
        if r['pivot']:
            print('  PIVOT at clause %d (dv=%s): %s' % (r['pivot']['at_clause'], r['pivot']['delta_v'], r['pivot']['text']))
        print()
