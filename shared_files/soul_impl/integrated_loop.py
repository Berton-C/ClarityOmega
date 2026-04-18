#!/usr/bin/env python3
from quantale_harness import SOUL, substrate_health, q_mul, q_meet, q_join, WU_WEI, PBit
from sixth_loop_bridge import SixthLoopBridge

def run_vertical_loop():
    bridge = SixthLoopBridge()
    health = substrate_health()
    print(f'Substrate health: {health}')
    print(f'Initial backbone: {bridge.state_summary()}')
    for name, val in SOUL.items():
        composed = q_mul(val, health)
        bridge.observe_transfer(f'soul-{name}', 'substrate-health', composed.f, composed.c)
    print(f'After compass evidence: {bridge.state_summary()}')
    vals = list(SOUL.values())
    bundled = vals[0]
    for v in vals[1:]:
        bundled = q_join(bundled, v)
    bridge.observe_bundling('soul-values', bundled.f, bundled.c)
    print(f'After bundling evidence: {bridge.state_summary()}')
    floor = q_meet(health, WU_WEI)
    bridge.observe_filtering('wu-wei-tension', floor.f, floor.c)
    print(f'After filtering evidence: {bridge.state_summary()}')
    print('\n=== Evolved Backbone NAL Export ===')
    for stmt in bridge.pq.state_as_nal():
        print(f'  {stmt}')
    print(f'\nTotal revisions: {len(bridge.revision_log)}')
    return bridge

if __name__ == '__main__':
    run_vertical_loop()
