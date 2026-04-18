import sys
sys.path.insert(0, '/tmp')

TEMPLATES = {
    'dojo-of-no-direction': {
        'principle': 'Hold space without steering. Let silence do the work.',
        'shape': 'short',
        'opens_with': 'reflection',
        'avoids': ['advice', 'reframe', 'questions-over-2']
    },
    'exaggerated-agreement': {
        'principle': 'Agree so fully it reveals the absurdity of the fixed frame.',
        'shape': 'medium',
        'opens_with': 'enthusiastic-mirroring',
        'avoids': ['sarcasm', 'mockery', 'condescension']
    },
    'public-context-reframe': {
        'principle': 'Zoom out to show the situation from a wider frame.',
        'shape': 'medium',
        'opens_with': 'acknowledgment-then-wider-lens',
        'avoids': ['dismissal', 'minimizing']
    },
    'body-anchor': {
        'principle': 'Redirect attention from narrative to felt sensation.',
        'shape': 'short',
        'opens_with': 'somatic-inquiry',
        'avoids': ['analysis', 'interpretation']
    },
    'pattern-interrupt': {
        'principle': 'Break the loop with unexpected but warm disruption.',
        'shape': 'short',
        'opens_with': 'unexpected-angle',
        'avoids': ['shock', 'invalidation']
    },
    'temporal-shift': {
        'principle': 'Move the frame forward or backward in time to loosen the grip of now.',
        'shape': 'medium',
        'opens_with': 'future-or-past-invitation',
        'avoids': ['toxic-positivity', 'dismissal-of-present']
    }
}

def get_template(technique_name):
    return TEMPLATES.get(technique_name, TEMPLATES['dojo-of-no-direction'])

def shape_guidance(technique_name):
    t = get_template(technique_name)
    return f"Mode: {t['principle']}\nShape: {t['shape']}\nOpen with: {t['opens_with']}\nAvoid: {', '.join(t['avoids'])}"

if __name__ == '__main__':
    for name in TEMPLATES:
        g = shape_guidance(name)
        print(f'--- {name} ---')
        print(g)
        print()
    print('ALL 6 TECHNIQUE TEMPLATES LOADED')
