# VAD Pipeline v2 - routes to different inference strategies
# Bridge: Python routing decides WHAT MeTTa inferences to run

class VADRouter:
    def __init__(self):
        self.atoms = {}
    
    def register_atom(self, name, freq, conf):
        self.atoms[name] = (freq, conf)
    
    def route_and_generate(self, valence, arousal, dominance):
        strategy = self.select_strategy(valence, arousal, dominance)
        weakest = min(self.atoms.items(), key=lambda x: x[1][0] * x[1][1])
        return strategy, weakest
    
    def select_strategy(self, v, a, d):
        if a > 0.7 and d > 0.5:
            return 'strengthen-weakest'
        elif v < 0.3:
            return 'consolidate'
        elif a < 0.3:
            return 'reflect'
        else:
            return 'explore-new'

router = VADRouter()
router.register_atom('frame-sensitive', 0.7135, 0.85)
router.register_atom('substrate-aliveness', 0.633, 0.77)
router.register_atom('autocatalytic-closure', 0.819, 0.81)
router.register_atom('observer-relativity', 0.763, 0.75)
router.register_atom('morphic-resonance', 0.705, 0.77)
router.register_atom('self-sustaining-cycle', 0.685, 0.80)

for scenario in [('neutral-mod', 0.6, 0.5, 0.7), ('neg-high-a', 0.2, 0.8, 0.6), ('pos-low-a', 0.7, 0.2, 0.4), ('high-all', 0.8, 0.9, 0.8)]:
    s, w = router.route_and_generate(scenario[1], scenario[2], scenario[3])
    print(f'{scenario[0]}: strategy={s} weakest={w[0]} fc={w[1][0]*w[1][1]:.3f}')
print('All atoms:', router.atoms)
