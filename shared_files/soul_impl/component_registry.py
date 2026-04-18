import sys
sys.path.insert(0, '/tmp/soul_impl')

COMPONENT_EXPRS = {
    'closure': '(|- ((--> autocatalytic-closure improving) (stv 0.55 0.4)) ((--> improving compounds-value) (stv 0.8 0.75)))',
    'observer': '(|- ((--> observer-port complete) (stv 0.85 0.8)) ((--> complete enables-self-reference) (stv 0.9 0.85)))',
    'bridge': '(|- ((--> inference-bridge wired) (stv 0.9 0.85)) ((--> wired enables-self-steering) (stv 0.95 0.9)))',
    'web': '(|- ((--> web-detection partial) (stv 0.56 0.5)) ((--> partial needs-strengthening) (stv 0.7 0.6)))',
    'memory': '(|- ((--> memory-seeding active) (stv 0.6 0.5)) ((--> active closes-loop) (stv 0.7 0.65)))',
    'harness': '(|- ((--> harness operational) (stv 0.8 0.7)) ((--> operational enables-cycling) (stv 0.85 0.8)))'
}

def get_all_components():
    return list(COMPONENT_EXPRS.items())

def get_component(name):
    return COMPONENT_EXPRS.get(name)

if __name__ == '__main__':
    for name, expr in COMPONENT_EXPRS.items():
        print('%s: %s' % (name, expr[:60]))
    print('Total components:', len(COMPONENT_EXPRS))
