import math

class Mem:
    def __init__(s,mid,txt,emb,w=1.0):
        s.mid=mid;s.txt=txt;s.emb=emb;s.w=w

def cos(a,b):
    d=sum(x*y for x,y in zip(a,b))
    na=math.sqrt(sum(x*x for x in a))
    nb=math.sqrt(sum(x*x for x in b))
    return d/(na*nb) if na*nb>0 else 0

def flat(q,ms,k=5):
    s=[(m,cos(q,m.emb)*m.w) for m in ms]
    s.sort(key=lambda x:-x[1])
    return s[:k]

def spread(q,ms,edges,k=5,decay=0.5,steps=2):
    act={m.mid:cos(q,m.emb)*m.w for m in ms}
    mm={m.mid:m for m in ms}
    for st in range(steps):
        na=dict(act)
        for a,b,w in edges:
            na[b]=na.get(b,0)+act.get(a,0)*w*(decay**(st+1))
            na[a]=na.get(a,0)+act.get(b,0)*w*(decay**(st+1))
        act=na
    s=[(mm[i],act[i]) for i in act if i in mm]
    s.sort(key=lambda x:-x[1])
    return s[:k]

ms=[Mem('g1','resource allocation',[.9,.8,.7,.1,.1,.1,.1,.1,.1]),
    Mem('g2','distributed governance',[.8,.9,.6,.1,.1,.1,.2,.1,.1]),
    Mem('b1','nutrient transport',[.1,.1,.1,.9,.8,.7,.1,.1,.1]),
    Mem('b2','mycelial topology',[.1,.2,.1,.8,.9,.6,.1,.1,.1]),
    Mem('i1','pattern continuity',[.1,.1,.1,.1,.1,.1,.9,.8,.7]),
    Mem('i2','substrate independence',[.2,.1,.1,.1,.1,.2,.8,.9,.6]),
    Mem('br1','governance-biology bridge',[.5,.4,.3,.5,.4,.3,.1,.1,.1],.8),
    Mem('n1','emergent coordination',[.3,.2,.1,.3,.2,.1,.3,.2,.1],.3)]
edges=[('g1','g2',.8),('b1','b2',.8),('i1','i2',.8),('g2','br1',.7),('br1','b1',.7),('br1','n1',.5),('i1','n1',.4)]
q=[.85,.75,.65,.1,.1,.1,.1,.1,.1]
print('FLAT:');[print(f'  {m.mid:8s} {m.txt:30s} {s:.4f}') for m,s in flat(q,ms)]
print('SPREAD:');[print(f'  {m.mid:8s} {m.txt:30s} {s:.4f}') for m,s in spread(q,ms,edges)]
fi=[m.mid for m,s in flat(q,ms,3)];si=[m.mid for m,s in spread(q,ms,edges,3)]
print(f'Flat top3: {fi}');print(f'Spread top3: {si}')
print(f'Only in spread: {[x for x in si if x not in fi]}')
