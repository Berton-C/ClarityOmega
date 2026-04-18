import re
from unified_pipeline import estimate_vad, classify_tone, select_strategy
import math

class ConversationTracker:
    def __init__(self):
        self.turns = []
    
    def add_turn(self, text):
        vad, matched = estimate_vad(text)
        tone, disc = classify_tone(vad)
        strategy = select_strategy(vad)
        turn = {"text": text, "vad": vad, "tone": tone, "strategy": strategy, "turn_num": len(self.turns)+1}
        if self.turns:
            prev = self.turns[-1]["vad"]
            delta = math.sqrt(sum((a-b)**2 for a,b in zip(vad, prev)))
            turn["delta"] = round(delta, 3)
            turn["shift"] = delta > 0.25
            turn["valence_trend"] = "rising" if vad[0] - prev[0] > 0.15 else ("falling" if prev[0] - vad[0] > 0.15 else "stable")
        else:
            turn["delta"] = 0.0
            turn["shift"] = False
            turn["valence_trend"] = "initial"
        self.turns.append(turn)
        return turn
    
    def trajectory_summary(self):
        if len(self.turns) < 2: return "insufficient-data"
        vals = [t["vad"][0] for t in self.turns]
        if vals[-1] - vals[0] > 0.3: return "lifting"
        if vals[0] - vals[-1] > 0.3: return "dropping"
        if max(vals) - min(vals) > 0.4: return "oscillating"
        return "stable"
    
    def adjust_strategy(self, base_strategy):
        traj = self.trajectory_summary()
        if traj == "lifting" and base_strategy == "validate-then-assist":
            return "match-energy-collaborate"
        if traj == "dropping" and base_strategy == "standard-responsive":
            return "validate-then-assist"
        return base_strategy

if __name__ == "__main__":
    ct = ConversationTracker()
    convos = ["I am frustrated and stuck and feel powerless", "I guess there might be hope but I am still worried", "Actually this is starting to click and I feel hopeful", "I feel strong and clear and excited about what is next"]
    print("=== TEMPORAL TRAJECTORY TEST ===")
    for c in convos:
        r = ct.add_turn(c)
        adj = ct.adjust_strategy(r["strategy"])
        print("Turn %d: %s" % (r["turn_num"], c[:50]))
        print("  tone=%s vad=%s delta=%.3f shift=%s trend=%s" % (r["tone"], r["vad"], r["delta"], r["shift"], r["valence_trend"]))
        print("  base_strategy=%s adjusted=%s" % (r["strategy"], adj))
        print()
    print("TRAJECTORY:", ct.trajectory_summary())
