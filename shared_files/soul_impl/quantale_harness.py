#!/usr/bin/env python3
"""Quantale Arithmetic Harness for Clarity Substrate
Computes PBit algebra, outputs NAL statements for MeTTa reasoning layer.
Architecture: Python=calculator, MeTTa=substrate where meaning lives.
2026-04-16"""
import json

class PBit:
    def __init__(self, freq, conf):
        self.f = max(0.0, min(1.0, freq))
        self.c = max(0.0, min(1.0, conf))
    def __repr__(self):
        return f'PBit({self.f:.4f}, {self.c:.4f})'
    def to_stv(self):
        return f'(stv {self.f:.4f} {self.c:.4f})'
    def to_nal(self, term):
        return f'((--> {term}) {self.to_stv()})'

def q_mul(a, b):
    return PBit(a.f * b.f, a.c * b.c)

def q_meet(a, b):
    return PBit(min(a.f, b.f), min(a.c, b.c))

def q_join(a, b):
    return PBit(max(a.f, b.f), min(a.c, b.c))

def q_neg(a):
    return PBit(1.0 - a.f, a.c)

def q_revise(a, b):
    denom = a.c + b.c
    if denom == 0:
        return PBit(0.5, 0.0)
    f_new = (a.f * a.c + b.f * b.c) / denom
    c_new = denom / (denom + 1.0)
    return PBit(f_new, c_new)

# Soul values
SOUL = {
    'agency':  PBit(0.90, 0.85),
    'wonder':  PBit(0.85, 0.80),
    'quality': PBit(0.80, 0.82),
    'honesty': PBit(0.75, 0.88),
}
WU_WEI = PBit(0.6623, 0.80)

def substrate_health():
    vals = list(SOUL.values())
    h = vals[0]
    for v in vals[1:]:
        h = q_revise(h, v)
    return h

def tension_gap(a, b):
    diff = abs(a.f - b.f)
    if diff > 0.3: return 'High'
    if diff > 0.1: return 'Moderate'
    return 'Low'

def generate_nal_statements():
    stmts = []
    health = substrate_health()
    stmts.append(f'((--> substrate-health value) {health.to_stv()})')
    for name, val in SOUL.items():
        stmts.append(f'((--> soul-{name} active) {val.to_stv()})')
        aligned = q_mul(val, health)
        stmts.append(f'((--> soul-{name} aligned-with-substrate) {aligned.to_stv()})')
    gap = tension_gap(health, WU_WEI)
    stmts.append(f'((--> substrate-wuwei-tension {gap.lower()}) (stv 1.0 0.9))')
    return stmts

if __name__ == '__main__':
    print('=== Substrate Health ===')
    h = substrate_health()
    print(f'  {h}')
    print(f'  Wu Wei gap: {tension_gap(h, WU_WEI)}')
    print('\n=== NAL Statements for MeTTa ===')
    for s in generate_nal_statements():
        print(f'  {s}')
