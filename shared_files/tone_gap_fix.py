combos = []
for v in ['pos','neg','neutral']:
    for a in ['high','mid','low']:
        for d in ['high','mid','low']:
            combos.append((v,a,d))
TM = {('pos','high','high'):'energized-confidence',('pos','mid','mid'):'warm-engagement',('neg','high','low'):'urgent-distress',('neg','low','low'):'quiet-sadness',('neg','mid','low'):'vulnerable-frustration',('neg','mid','mid'):'steady-discomfort',('pos','mid','low'):'receptive-warmth',('pos','low','mid'):'gentle-warmth',('neutral','mid','mid'):'balanced-presence',('neg','low','mid'):'quiet-resignation',('pos','high','low'):'delighted-surrender',('pos','low','low'):'gentle-acceptance',('neutral','high','high'):'focused-flow',('neutral','high','low'):'restless-searching',('neutral','low','high'):'settled-composure'}
missing = [c for c in combos if c not in TM]
print(f'{len(TM)} mapped, {len(missing)} missing:')
for m in missing:
    print(f'  {m}')
