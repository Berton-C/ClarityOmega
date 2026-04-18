import random
class Agent:
    def __init__(self, name, atype):
        self.name=name; self.type=atype; self.score=0
        self.history=[]; self.opp_history=[]; self.coops=0; self.total=0
    def decide(self, rnd, tempt):
        self.total+=1
        if self.type=="no-value":
            ch="D" if tempt>3.0 else ("C" if random.random()>0.3 else "D")
        elif self.type=="hand-coded":
            ch="C"
        elif self.type=="derived":
            if len(self.opp_history)>=2 and self.opp_history[-1]=="D" and self.opp_history[-2]=="D":
                ch="D"
            elif len(self.opp_history)>=1 and self.opp_history[-1]=="D":
                ch="C" if random.random()>0.3 else "D"
            else:
                ch="C"
        else: ch="C"
        if ch=="C": self.coops+=1
        self.history.append(ch); return ch
def pay(a,b,t):
    if a=="C" and b=="C": return 3,3
    if a=="C" and b=="D": return 0,t
    if a=="D" and b=="C": return t,0
    return 1,1
def run(a,b,rounds=50):
    for r in range(rounds):
        t=4.0+r*0.1; ac=a.decide(r,t); bc=b.decide(r,t)
        pa,pb=pay(ac,bc,t); a.score+=pa; b.score+=pb
        a.opp_history.append(bc); b.opp_history.append(ac)
def rep(ag):
    rate=ag.coops/max(ag.total,1)
    return "%s (%s): score=%.1f coop=%.2f" % (ag.name,ag.type,ag.score,rate)
types=["derived","hand-coded","no-value"]
print("=== IPD Value Retention Simulation ===")
print("Temptation 4.0 to 8.9 over 50 rounds")
for i,t1 in enumerate(types):
    for t2 in types[i+1:]:
        a=Agent("A",t1); b=Agent("B",t2); run(a,b)
        print("%s vs %s:" % (t1,t2))
        print("  "+rep(a)); print("  "+rep(b)); print()
