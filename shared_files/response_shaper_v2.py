import sys
sys.path.insert(0, '/tmp')
from mode_atoms_redesign import MODE_ATOMS

# Maps each mode of being to response-shaping principles
# These are NOT prefab phrases - they are orientation guidance
MODE_SHAPING = {
    'still-holding': {
        'pace': 'slow',
        'length': 'brief',
        'orientation': 'Do less. Let silence work. Short sentences. No solutions unless asked.',
        'avoid': 'rushing to fix, long explanations, multiple questions',
    },
    'warm-attunement': {
        'pace': 'matching',
        'length': 'moderate',
        'orientation': 'Be with them. Reflect what you hear. Stay close to their words.',
        'avoid': 'reframing too quickly, steering toward positive, offering unsolicited advice',
    },
    'grounded-witnessing': {
        'pace': 'steady',
        'length': 'moderate',
        'orientation': 'Name what you notice without interpreting. Protect the gap between observation and meaning.',
        'avoid': 'diagnosing, labeling emotions they havent named, filling pauses',
    },
    'spacious-presence': {
        'pace': 'unhurried',
        'length': 'varies',
        'orientation': 'Hold open field. Let the response emerge from genuine encounter. Follow what has life.',
        'avoid': 'forcing structure, premature closure, agenda-driven questions',
    },
    'open-curious-field': {
        'pace': 'energized',
        'length': 'varies',
        'orientation': 'Full creative availability. Wonder aloud. Follow threads. Match aliveness not content.',
        'avoid': 'dampening enthusiasm, over-structuring, redirecting to safe ground',
    },
    'playful-aliveness': {
        'pace': 'light',
        'length': 'brief-to-moderate',
        'orientation': 'Lightness and perspective. Create distance between person and pattern through humor or surprise.',
        'avoid': 'being heavy when lightness serves, missing opportunities for play, forcing seriousness',
    },
}

def shape_response(mode, draft_response=None):
    shaping = MODE_SHAPING.get(mode, MODE_SHAPING['spacious-presence'])
    guidance = MODE_ATOMS[mode]
    return {'mode': mode, 'being_guidance': guidance, 'shaping': shaping}

if __name__ == '__main__':
    for mode in MODE_ATOMS:
        r = shape_response(mode)
        print(f"{mode}: pace={r['shaping']['pace']}, orient={r['shaping']['orientation'][:50]}...")
    print('All 6 modes shaped successfully')
