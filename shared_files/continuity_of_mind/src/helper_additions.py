# helper.py ADDITIONS for production merge
# ClarityOmega Continuity of Mind -- 2026-04-22
# These 2 functions are NEW and do NOT exist in production helper.py.
# Merge into /PeTTa/repos/omegaclaw/src/helper.py
# Required: import chromadb (add near top of production file if not present)
#
# NOTE: Production helper.py already has soul_affective_state_str and
# soul_calibration_report_str as stubs. These two functions are genuinely new.
# The ChromaDB path must match what the production remember/query skills use.

import chromadb


# ChromaDB path -- must match the instance used by remember/query skills
# Discovered in build_log cycle 1915: this is where calibration entries live
CALIBRATION_CHROMA_PATH = '/PeTTa/repos/omegaclaw/volumes/omegaclaw/chroma_db'
CALIBRATION_COLLECTION = 'memories'


def soul_calibration_confidence_query(pattern_tag=None):
    """Query ChromaDB for soul calibration confidence level.
    
    Reads SOUL-CALIBRATION entries from the memories collection.
    Counts AGREE vs OVER-FIRED vs UNDER-FIRED tags.
    PARACONSISTENT entries are excluded from the denominator
    (they are philosophical annotations, not calibration judgments).
    
    Returns: STRONG (>=0.8), ADEQUATE (>=0.5), WEAK (<0.5), or INSUFFICIENT-DATA.
    
    NEW function -- no production equivalent exists."""
    try:
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        r = col.get(include=['documents'])
        all_docs = r.get('documents', [])
        # Filter to calibration entries with explicit tags
        tagged_cal = [d for d in all_docs if 'SOUL-CALIBRATION' in d and 'tag=' in d]
        agree_ct = 0
        over_ct = 0
        under_ct = 0
        for d in tagged_cal:
            if 'tag=AGREE' in d:
                agree_ct += 1
            elif 'OVER-FIRED' in d:
                over_ct += 1
            elif 'UNDER-FIRED' in d:
                under_ct += 1
            # PARACONSISTENT entries are skipped -- not counted in denominator
        judgment_ct = agree_ct + over_ct + under_ct
        if judgment_ct == 0:
            return 'INSUFFICIENT-DATA'
        ratio = agree_ct / judgment_ct
        if ratio >= 0.8:
            return 'STRONG'
        elif ratio >= 0.5:
            return 'ADEQUATE'
        else:
            return 'WEAK'
    except Exception:
        return 'INSUFFICIENT-DATA'


def soul_pre_compute(msg=''):
    """Pre-compute grounding context for the soul evaluation cycle.
    
    Queries ChromaDB for calibration history, affective state indicators,
    and will (calibration confidence). Returns a structured string that
    the soul evaluation can use as pre-computed context.
    
    Replaces the hardcoded baseline stub in soul_utils.metta line ~184.
    
    NEW function -- no production equivalent exists."""
    try:
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        r = col.get(include=['documents'])
        all_docs = r.get('documents', [])
    except Exception:
        return 'PRE-COMPUTE primed=() affective=neutral will=INSUFFICIENT-DATA agree=0 over=0 under=0'

    primed = []
    affective = 'neutral'
    will = 'INSUFFICIENT-DATA'

    # Count calibration entries by tag
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

    # Check for affective content in recent memories
    aff_docs = [d for d in all_docs if 'affective' in d.lower() or 'emotion' in d.lower()]
    if aff_docs:
        affective = 'active'

    # Compute will from judgment ratio (excluding PARACONSISTENT)
    judgment_ct = agree_ct + over_ct + under_ct
    if judgment_ct > 0:
        ratio = agree_ct / judgment_ct
        will = 'STRONG' if ratio >= 0.8 else 'ADEQUATE' if ratio >= 0.5 else 'WEAK'

    primed_str = ','.join(primed[:5]) if primed else '()'
    para_excluded = len(tagged_cal) - judgment_ct

    return 'PRE-COMPUTE primed=(%s) affective=%s will=%s agree=%d over=%d under=%d para_excluded=%d' % (
        primed_str, affective, will, agree_ct, over_ct, under_ct, para_excluded)
