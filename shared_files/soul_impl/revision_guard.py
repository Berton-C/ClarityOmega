# Revision Guard: Application-layer filter for NAL revision
# Prevents same-origin confidence pumping while allowing cross-source accumulation

def extract_stamp(premise_str):
    """Extract origin stamp from a stamped NAL premise.
    Stamps are embedded as term prefixes like (stampedA ...)"""
    import re
    match = re.search(r'stamped([A-Za-z0-9_]+)', premise_str)
    return match.group(1) if match else None

def stamps_overlap(p1_str, p2_str):
    """Check if two premises share any origin stamps."""
    s1 = set(re.findall(r'stamped([A-Za-z0-9_]+)', p1_str))
    s2 = set(re.findall(r'stamped([A-Za-z0-9_]+)', p2_str))
    import re
    s1 = set(re.findall(r'stamped([A-Za-z0-9_]+)', p1_str))
    s2 = set(re.findall(r'stamped([A-Za-z0-9_]+)', p2_str))
    return len(s1 & s2) > 0

def guarded_revision(p1, p2, metta_fn):
    """Only invoke NAL revision if premises have non-overlapping stamps.
    metta_fn: callable that executes (|- p1 p2) and returns result."""
    if stamps_overlap(p1, p2):
        return {'blocked': True, 'reason': 'same-origin stamps overlap', 'stamps': extract_stamp(p1)}
    result = metta_fn(p1, p2)
    return {'blocked': False, 'result': result}

def guarded_deduction(p1, p2, metta_fn):
    """Deduction always proceeds — stamps propagate as provenance tags."""
    result = metta_fn(p1, p2)
    return {'blocked': False, 'result': result}

# Usage pattern in orchestration loop:
# for each revision candidate pair (p1, p2):
#     outcome = guarded_revision(p1, p2, lambda a,b: metta_exec(f'(|- {a} {b})'))
#     if outcome['blocked']: log('Revision blocked: same origin')
#     else: update_knowledge_base(outcome['result'])
