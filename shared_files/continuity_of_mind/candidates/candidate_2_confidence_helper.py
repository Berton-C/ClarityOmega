import chromadb

CHROMA_PATH = '/tmp/repos/clarity_archive/volumes/mettaclaw/chroma_db'

def soul_calibration_confidence_query(pattern_tag=None):
    c = chromadb.PersistentClient(CHROMA_PATH)
    col = c.get_or_create_collection('memories')
    r = col.get(include=['documents'])
    all_docs = r.get('documents', [])
    cal = [d for d in all_docs if 'SOUL-CALIBRATION' in d or 'calibration' in d.lower()]
    if not cal:
        return 'INSUFFICIENT-DATA'
    agree = sum(1 for d in cal if 'tag=AGREE' in d)
    over = sum(1 for d in cal if 'OVER-FIRED' in d)
    under = sum(1 for d in cal if 'UNDER-FIRED' in d)
    total = agree + over + under
    if total == 0:
        return 'INSUFFICIENT-DATA'
    ratio = agree / total
    if ratio >= 0.8:
        return 'STRONG'
    elif ratio >= 0.5:
        return 'ADEQUATE'
    else:
        return 'WEAK'
