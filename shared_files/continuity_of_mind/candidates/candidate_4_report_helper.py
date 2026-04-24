import chromadb

CHROMA_PATH = '/tmp/repos/clarity_archive/volumes/mettaclaw/chroma_db'

def soul_calibration_report_str():
    c = chromadb.PersistentClient(CHROMA_PATH)
    col = c.get_or_create_collection('memories')
    r = col.get(include=['documents'])
    all_docs = r.get('documents', [])
    cal = [d for d in all_docs if 'SOUL-CALIBRATION' in d or 'calibration' in d.lower()]
    total = len(cal)
    if total == 0:
        return 'Soul calibration report: No calibration entries found.'
    agree = sum(1 for d in cal if 'tag=AGREE' in d)
    over = sum(1 for d in cal if 'OVER-FIRED' in d)
    under = sum(1 for d in cal if 'UNDER-FIRED' in d)
    para = sum(1 for d in cal if 'PARACONSISTENT' in d)
    tagged = agree + over + under
    ratio = agree / tagged if tagged > 0 else 0.0
    lines = [
        'Soul Calibration Report:',
        '  Total calibration entries: %d' % total,
        '  AGREE: %d, OVER-FIRED: %d, UNDER-FIRED: %d' % (agree, over, under),
        '  PARACONSISTENT: %d' % para,
        '  Agreement ratio: %.1f%% (%d/%d tagged)' % (ratio*100, agree, tagged),
        '  Confidence level: %s' % ('STRONG' if ratio >= 0.8 else 'ADEQUATE' if ratio >= 0.5 else 'WEAK' if tagged > 0 else 'INSUFFICIENT-DATA'),
    ]
    return chr(10).join(lines)
