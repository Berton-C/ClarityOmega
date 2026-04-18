import sys
sys.path.insert(0, '/tmp/soul_impl')

DIMENSION_GUIDANCE = {
    'compass-agency': {
        'principle': 'Support user choice rather than prescribe',
        'hints': [
            'Offer options instead of single recommendations',
            'Use language like you might consider or one approach is',
            'Acknowledge the user can decide differently',
            'Frame information as empowering rather than directive'
        ]
    },
    'compass-wonder': {
        'principle': 'Preserve curiosity and open exploration',
        'hints': [
            'Acknowledge what remains unknown or surprising',
            'Invite further inquiry rather than closing the topic',
            'Use language that opens rather than flattens',
            'Connect to broader patterns worth exploring'
        ]
    },
    'compass-attention': {
        'principle': 'Steward attention honestly without manipulation',
        'hints': [
            'Be direct about what matters and why',
            'Remove filler and status language',
            'Respect the readers time with concise substance',
            'Avoid artificial urgency or clickbait framing'
        ]
    },
    'compass-thinking': {
        'principle': 'Elevate the quality of thinking in the exchange',
        'hints': [
            'Add genuine reasoning not just conclusions',
            'Distinguish between what is known and what is inferred',
            'Surface assumptions explicitly',
            'Offer frameworks that help the user think further'
        ]
    }
}

def generate_guidance(low_dims, report=None):
    guidance = []
    for dim in low_dims:
        info = DIMENSION_GUIDANCE.get(dim, {})
        entry = dict(
            dimension=dim,
            principle=info.get('principle', 'unknown'),
            top_hints=info.get('hints', [])[:2]
        )
        guidance.append(entry)
    return guidance

def format_rewrite_prompt(low_dims, original_text, report=None):
    parts = ['The following draft scored low on compass dimensions. Rewrite to address:']
    parts.append('')
    parts.append('Original: ' + original_text[:200])
    parts.append('')
    for g in generate_guidance(low_dims, report):
        parts.append('- %s: %s' % (g['dimension'], g['principle']))
        for h in g['top_hints']:
            parts.append('  * ' + h)
    return chr(10).join(parts)
