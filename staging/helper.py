# helper.py ADDITIONS for production merge
# Goal 3 precompute-grounding -- ClarityClaw 2026-04-22
# These 2 functions are NEW and do NOT exist in production helper.py.
# Merge into /PeTTa/repos/omegaclaw/src/helper.py after line ~439.
# Required import (add near top of production file if not present):
#   import chromadb

def soul_calibration_confidence_query(pattern_tag=None):
    """Query ChromaDB calibration collection for confidence level.
    Returns STRONG/ADEQUATE/WEAK/INSUFFICIENT-DATA based on record count.
    NEW function -- no production equivalent exists."""
    try:
        client = chromadb.Client()
        collection = client.get_or_create_collection(name="soul_calibration")
        if pattern_tag and str(pattern_tag).strip():
            results = collection.get(where={"tag": str(pattern_tag)}, limit=100)
        else:
            results = collection.get(limit=100)
        count = len(results.get("ids", []))
        if count >= 20:
            return "STRONG"
        elif count >= 10:
            return "ADEQUATE"
        elif count >= 3:
            return "WEAK"
        else:
            return "INSUFFICIENT-DATA"
    except Exception:
        return "INSUFFICIENT-DATA"


def soul_pre_compute(msg=None):
    """Pre-compute grounding context for soul cycle.
    Queries calibration confidence and returns primed/affective/will string.
    NEW function -- replaces hardcoded stub in soul_utils.metta line ~184."""
    confidence = soul_calibration_confidence_query()
    affective = "fresh-system"
    try:
        from helper import soul_affective_state_str
        affective = soul_affective_state_str()
    except Exception:
        pass
    return (
        "PRE-COMPUTE primed=(calibration-confidence=" + confidence + ")"
        " affective=" + str(affective) +
        " will=" + confidence
    )
