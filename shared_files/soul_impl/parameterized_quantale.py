# Parameterized Quantale: Layer 0 of Transfer Backbone
# Tensor product governed by NAL-revisable parameters
# Sixth loop strengthens these via cross-domain evidence

class ParameterizedQuantale:
    def __init__(self):
        self.tensor_strength = (0.7, 0.5)
        self.join_breadth = (0.8, 0.5)
        self.meet_floor = (0.6, 0.5)
        self.alignment_coupling = (0.5, 0.3)

    def q_mul(self, a, b):
        af, ac = a
        bf, bc = b
        tf, tc = self.tensor_strength
        return (af * bf * tf, ac * bc * tc)

    def q_join(self, a, b):
        jf, jc = self.join_breadth
        return (max(a[0], b[0]) * jf, max(a[1], b[1]) * jc)

    def q_meet(self, a, b):
        mf, mc = self.meet_floor
        return (min(a[0], b[0]) * mf, min(a[1], b[1]) * mc)

    def revise_param(self, name, new_ev):
        old = getattr(self, name)
        w1 = old[1] / (1 - old[1])
        w2 = new_ev[1] / (1 - new_ev[1])
        rf = (w1 * old[0] + w2 * new_ev[0]) / (w1 + w2)
        rc = (w1 + w2) / (w1 + w2 + 1)
        setattr(self, name, (round(rf, 4), round(rc, 4)))
        return getattr(self, name)

    def state_as_nal(self):
        params = [
            ('tensor-strength', self.tensor_strength),
            ('join-breadth', self.join_breadth),
            ('meet-floor', self.meet_floor),
            ('alignment-coupling', self.alignment_coupling)
        ]
        return [f'(--> {n} (stv {v[0]} {v[1]}))' for n, v in params]
