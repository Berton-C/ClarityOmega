# Observer-Relativity: Frame-dependent truth values
from quantale_tensor import PBit, q_mul, q_revise

class ObserverFrame:
    def __init__(self, name, biases):
        self.name = name
        self.biases = biases
    def transform(self, statement, base_tv):
        if statement in self.biases:
            bias = self.biases[statement]
            shifted_f = base_tv.f * bias.f + (1 - base_tv.f) * (1 - bias.f)
            combined_c = base_tv.c * bias.c
            return PBit(shifted_f, combined_c)
        return base_tv
    def __repr__(self):
        return f'Observer({self.name})'

def multi_observer_revision(observers, statement, base_tv):
    transformed = []
    for obs in observers:
        tv = obs.transform(statement, base_tv)
        transformed.append((obs.name, tv))
    if len(transformed) >= 2:
        merged = transformed[0][1]
        for _, tv in transformed[1:]:
            merged = q_revise(merged, tv)
        transformed.append(('consensus', merged))
    return transformed

if __name__ == '__main__':
    clarity = ObserverFrame('clarity', {
        'growth-is-good': PBit(0.9, 0.85),
        'speed-over-depth': PBit(0.2, 0.80),
        'autonomy-matters': PBit(0.95, 0.90),
    })
    external = ObserverFrame('external-eval', {
        'growth-is-good': PBit(0.7, 0.70),
        'speed-over-depth': PBit(0.8, 0.75),
        'autonomy-matters': PBit(0.4, 0.60),
    })
    base = PBit(0.6, 0.5)
    for stmt in ['growth-is-good', 'speed-over-depth', 'autonomy-matters']:
        print(f'Statement: {stmt} base: {base}')
        results = multi_observer_revision([clarity, external], stmt, base)
        for name, tv in results:
            print(f'  {name}: f={tv.f:.4f} c={tv.c:.4f}')
        print()
