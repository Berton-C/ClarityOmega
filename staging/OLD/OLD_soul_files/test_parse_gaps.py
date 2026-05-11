import sys
sys.path.insert(0, '/PeTTa/repos/omegaclaw/soul')
try:
    import idle_goal_prompt as igp
    smap = igp.parse_self_map()
    gaps = smap.get('gaps', [])
    print('TOTAL GAPS:', len(gaps))
    for g in gaps:
        print('  NAME:', g.get('name'), 'SEVERITY:', g.get('severity'))
    high = [g for g in gaps if g.get('severity') == 'high']
    print('HIGH COUNT:', len(high))
    for h in high:
        print('  HIGH:', h.get('name'))
except Exception as e:
    print('ERROR:', type(e).__name__, e)
