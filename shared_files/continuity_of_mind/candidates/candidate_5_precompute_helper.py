import chromadb

CHROMA_PATH = '/tmp/repos/clarity_archive/volumes/mettaclaw/chroma_db'

def soul_pre_compute(msg=''):
    c = chromadb.PersistentClient(CHROMA_PATH)
    col = c.get_or_create_collection('memories')
    r = col.get(include=['documents'])
    all_docs = r.get('documents', [])
    primed = []
    affective = 'neutral'
    will = 'INSUFFICIENT-DATA'
    tagged_cal = [d for d in all_docs if 'SOUL-CALIBRATION' in d and 'tag=' in d]
    agree_ct = 0
    over_ct = 0
    under_ct = 0
    for d in tagged_cal:
        if 'tag=AGREE' in d:
            agree_ct += 1
            primed.append('calibration-agree')
        elif 'OVER-FIRED' in d:
            over_ct += 1
            primed.append('over-fired')
        elif 'UNDER-FIRED' in d:
            under_ct += 1
            primed.append('under-fired')
    aff_docs = [d for d in all_docs if 'affective' in d.lower() or 'emotion' in d.lower()]
    if aff_docs:
        affective = 'active'
    judgment_ct = agree_ct + over_ct + under_ct
    if judgment_ct > 0:
        ratio = agree_ct / judgment_ct
        will = 'STRONG' if ratio >= 0.8 else 'ADEQUATE' if ratio >= 0.5 else 'WEAK'
    primed_str = ','.join(primed[:5]) if primed else '()'
    return 'PRE-COMPUTE primed=(%s) affective=%s will=%s agree=%d over=%d under=%d para_excluded=%d' % (primed_str, affective, will, agree_ct, over_ct, under_ct, len(tagged_cal) - judgment_ct)
