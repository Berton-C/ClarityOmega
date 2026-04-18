import sys
sys.path.insert(0, '/tmp')
import chromadb

_client = chromadb.PersistentClient(path='/tmp/chroma_db')
_col = _client.get_collection('nrc_vad_full')

def get_vad(word):
    try:
        res = _col.get(where={'word': word.lower()}, include=['metadatas'])
        if res['metadatas']:
            m = res['metadatas'][0]
            return (m['valence'], m['arousal'], m['dominance'])
    except:
        pass
    return None

def audit_response(text):
    words = text.lower().split()
    valences = []
    sns_flags = []
    SNS_MARKERS = ['must', 'should', 'wrong', 'but', 'however', 'actually', 'need', 'fix', 'problem', 'failure', 'urgent', 'immediately', 'obviously', 'clearly']
    PNS_MARKERS = ['notice', 'curious', 'wonder', 'sense', 'alive', 'open', 'gentle', 'space', 'here', 'present', 'fresh', 'settle']
    pns_count = 0
    for w in words:
        clean = ''.join(c for c in w if c.isalpha())
        if not clean:
            continue
        vad = get_vad(clean)
        if vad:
            valences.append(vad[0])
        if clean in SNS_MARKERS:
            sns_flags.append(clean)
        if clean in PNS_MARKERS:
            pns_count += 1
    avg_valence = sum(valences)/len(valences) if valences else 0.0
    sns_ratio = len(sns_flags) / max(len(words), 1)
    # Triple gate: loose valence floor AND zero SNS AND minimum PNS presence
    gate_valence = avg_valence > -1.0
    gate_sns = len(sns_flags) == 0
    gate_pns = pns_count >= 2
    sustains_pns = gate_valence and gate_sns and gate_pns
    return {'avg_valence': round(avg_valence, 3), 'sns_flags': sns_flags, 'sns_ratio': round(sns_ratio, 3), 'pns_word_count': pns_count, 'sustains_pns': sustains_pns, 'word_count': len(words), 'vad_hits': len(valences), 'gates': {'valence': gate_valence, 'sns_clear': gate_sns, 'pns_present': gate_pns}}

if __name__ == '__main__':
    tests = [
        'I notice something shifted. I am here with you. No rush.',
        'You need to fix this problem immediately. This is wrong.',
        'I wonder what would happen if we sat with that for a moment.',
        'You should obviously reconsider your approach to this failure.',
    ]
    for t in tests:
        r = audit_response(t)
        label = 'PNS-SUSTAINING' if r['sustains_pns'] else 'SNS-RISK'
        print(f"{label} (v={r['avg_valence']}, sns={len(r['sns_flags'])}, pns={r['pns_word_count']}) | {t[:60]}")
        print(f"  Gates: {r['gates']}")
        if r['sns_flags']:
            print(f"  SNS flags: {r['sns_flags']}")
        print()
    print('Triple-gate valence self-audit operational')
