# Compass Quantale Composition Summary
# Goal 22: Quantale algebra on real compass values

COMPASS_VALUES = {
    'agency':    (0.765, 0.656),
    'wonder':    (0.855, 0.690),
    'thinking':  (0.900, 0.730),
    'attention': (0.765, 0.620),
}

def q_mul_all(vals):
    f_prod, c_prod = 1.0, 1.0
    for f, c in vals.values():
        f_prod *= f
        c_prod *= c
    return (round(f_prod, 4), round(c_prod, 4))

def q_meet_all(vals):
    fs = [f for f, c in vals.values()]
    cs = [c for f, c in vals.values()]
    return (round(min(fs), 4), round(max(cs), 4))

def q_join_all(vals):
    fs = [f for f, c in vals.values()]
    cs = [c for f, c in vals.values()]
    return (round(max(fs), 4), round(max(cs), 4))

def compass_summary(vals):
    mul = q_mul_all(vals)
    meet = q_meet_all(vals)
    join = q_join_all(vals)
    spread = round(join[0] - meet[0], 4)
    print(f'chain_strength (q-mul): f={mul[0]} c={mul[1]} — cumulative sequential evidence')
    print(f'weakest_link (q-meet): f={meet[0]} c={meet[1]} — conservative floor')
    print(f'strongest_signal (q-join): f={join[0]} c={join[1]} — optimistic ceiling')
    print(f'spread: {spread} — {"uniform" if spread < 0.2 else "uneven"} alignment')
    return mul, meet, join, spread

if __name__ == '__main__':
    compass_summary(COMPASS_VALUES)
