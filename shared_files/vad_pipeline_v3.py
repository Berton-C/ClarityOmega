# VAD Pipeline v3 - strategy execution generates MeTTa expressions

class VADExecutor:
    def __init__(self):
        self.atoms = {}
    
    def register(self, name, freq, conf):
        self.atoms[name] = (freq, conf)
    
    def weakest(self):
        return min(self.atoms.items(), key=lambda x: x[1][0] * x[1][1])
    
    def strongest(self):
        return max(self.atoms.items(), key=lambda x: x[1][0] * x[1][1])
    
    def generate_metta(self, strategy):
        w_name, (wf, wc) = self.weakest()
        s_name, (sf, sc) = self.strongest()
        if strategy == 'strengthen-weakest':
            nf = min(wf + 0.05, 1.0)
            nc = min(wc + 0.05, 1.0)
            return f'(|- ((--> {w_name} strengthened) (stv {wf} {wc})) ((--> {w_name} strengthened) (stv {nf} {nc})))'
        elif strategy == 'explore-new':
            return f'(|- ((--> {s_name} extended-chain) (stv {sf} {sc})) ((--> extended-chain new-territory) (stv 0.5 0.5)))'
        elif strategy == 'consolidate':
            exprs = []
            for name, (f, c) in self.atoms.items():
                nf = min(f + 0.02, 1.0)
                exprs.append(f'Revise {name}: stv {f} {c} -> {nf} {c}')
            return '; '.join(exprs)
        else:
            return f'Query memory for grounding validation of {w_name}'

exe = VADExecutor()
exe.register('frame-sensitive', 0.7135, 0.85)
exe.register('substrate-aliveness', 0.633, 0.77)
exe.register('autocatalytic-closure', 0.691, 0.771)
exe.register('observer-relativity', 0.763, 0.75)
exe.register('morphic-resonance', 0.705, 0.77)
exe.register('self-sustaining-cycle', 0.685, 0.80)

for strat in ['strengthen-weakest', 'explore-new', 'consolidate', 'reflect']:
    expr = exe.generate_metta(strat)
    print(f'{strat}: {expr}')
print(f'Weakest: {exe.weakest()[0]} fc={exe.weakest()[1][0]*exe.weakest()[1][1]:.3f}')
print(f'Strongest: {exe.strongest()[0]} fc={exe.strongest()[1][0]*exe.strongest()[1][1]:.3f}')
