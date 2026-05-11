import sys
sys.path.insert(0, '/PeTTa/repos/omegaclaw/soul')
import idle_goal_prompt as igp
smap = igp.parse_self_map()
gaps = smap.get('gaps', [])
print('GAP COUNT:', len(gaps))
for g in gaps:
    print('  ', g.get('name'), '|', g.get('severity'))
high = [g['name'] for g in gaps if g.get('severity') == 'high']
print('HIGH GAPS:', high)
print('HIGH COUNT:', len(high))
print('SELF_MAP PATH:', igp.SELF_MAP)
with open(igp.SELF_MAP) as f:
    txt = f.read()
for line in txt.splitlines():
    if 'self-map-gap' in line and 'high' in line:
        print('RAW HIGH LINE:', line.strip())
