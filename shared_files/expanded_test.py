import re
VAD = {
    'frustrated': (-0.6,0.7,0.3), 'stuck': (-0.5,0.4,0.2),
    'excited': (0.8,0.8,0.6), 'love': (0.9,0.5,0.5),
    'anxious': (-0.5,0.7,0.2), 'calm': (0.3,0.2,0.6),
    'angry': (-0.8,0.8,0.7), 'happy': (0.8,0.6,0.6),
    'sad': (-0.6,0.3,0.3), 'confused': (-0.3,0.5,0.2),
    'hopeful': (0.6,0.5,0.5), 'tired': (-0.3,0.2,0.3),
    'curious': (0.5,0.6,0.5), 'overwhelmed': (-0.5,0.8,0.2),
    'grateful': (0.8,0.4,0.5), 'build': (0.4,0.6,0.7),
    'worried': (-0.5,0.6,0.2), 'powerless': (-0.6,0.4,0.1),
    'clicking': (0.5,0.5,0.6), 'strong': (0.6,0.6,0.8),
    'clear': (0.4,0.3,0.7), 'afraid': (-0.7,0.7,0.2),
    'lost': (-0.5,0.4,0.2), 'alive': (0.7,0.7,0.6),
    'proud': (0.7,0.5,0.8), 'safe': (0.5,0.2,0.6),
    'scared': (-0.7,0.7,0.2), 'good': (0.6,0.4,0.5),
    'bad': (-0.5,0.4,0.4), 'feel': (0.0,0.3,0.4),
    'know': (0.1,0.3,0.6),
}
TM = {('pos','high','high'):'energized-confidence',('pos','mid','mid'):'warm-engagement',('neg','high','low'):'urgent-distress',('neg','low','low'):'quiet-sadness',('neg','mid','low'):'vulnerable-frustration',('neg','mid','mid'):'steady-discomfort',('pos','mid','low'):'receptive-warmth',('pos','low','mid'):'gentle-warmth',('neutral','mid','mid'):'balanced-presence',('neg','low','mid'):'quiet-resignation'}
def run(t):
    import re
    w=[x for x in re.findall(r'[a-z]+',t.lower()) if x in VAD]
    if not w: return 'no match'
    v=sum(VAD[x][0] for x in w)/len(w)
    a=sum(VAD[x][1] for x in w)/len(w)
    d=sum(VAD[x][2] for x in w)/len(w)
    vv='pos' if v>0.2 else ('neg' if v<-0.2 else 'neutral')
    aa='high' if a>0.6 else ('low' if a<0.4 else 'mid')
    dd='high' if d>0.6 else ('low' if d<0.4 else 'mid')
    tone=TM.get((vv,aa,dd),'balanced-presence')
    return f'{round(v,2)},{round(a,2)},{round(d,2)} -> {vv}/{aa}/{dd} -> {tone} | {w}'
print('T1:', run('I am worried this wont work and I feel powerless'))
print('T2:', run('Everything is clicking into place and I feel strong and clear'))
print('T3:', run('I dont know what I feel right now things are just happening'))
