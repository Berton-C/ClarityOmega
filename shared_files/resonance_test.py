import numpy as np
bundle=np.array([0.294,0.659,0.591])
k1=np.array([0.3,0.8,0.5])
k2=np.array([0.7,0.2,0.9])
k3=np.array([0.5,0.6,0.15])
joy=np.array([0.98,0.824,0.794])
anger=np.array([0.167,0.865,0.657])
fear=np.array([0.073,0.84,0.293])
def cos_sim(a,b): return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
for name,key in [('k1',k1),('k2',k2),('k3',k3)]:
    for ename,evec in [('joy',joy),('anger',anger),('fear',fear)]:
        probe=key*evec
        print(f'Resonance {name}->{ename}: {cos_sim(probe,bundle):.4f}')
