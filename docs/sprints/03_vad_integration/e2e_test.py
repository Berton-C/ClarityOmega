import re
import json

VAD_WORDS = {"frustrated": (-0.6,0.7,0.3), "stuck": (-0.5,0.4,0.2), "excited": (0.8,0.8,0.6), "love": (0.9,0.5,0.5), "anxious": (-0.5,0.7,0.2), "calm": (0.3,0.2,0.6), "angry": (-0.8,0.8,0.7), "happy": (0.8,0.6,0.6), "sad": (-0.6,0.3,0.3), "confused": (-0.3,0.5,0.2), "hopeful": (0.6,0.5,0.5), "tired": (-0.3,0.2,0.3), "curious": (0.5,0.6,0.5), "overwhelmed": (-0.5,0.8,0.2), "grateful": (0.8,0.4,0.5), "build": (0.4,0.6,0.7), "worried": (-0.5,0.6,0.2), "powerless": (-0.6,0.4,0.1), "clicking": (0.5,0.5,0.6), "strong": (0.6,0.6,0.8), "clear": (0.4,0.3,0.7), "afraid": (-0.7,0.7,0.2), "lost": (-0.5,0.4,0.2), "alive": (0.7,0.7,0.6), "proud": (0.7,0.5,0.8), "safe": (0.5,0.2,0.6), "scared": (-0.7,0.7,0.2), "good": (0.6,0.4,0.5), "bad": (-0.5,0.4,0.4), "feel": (0.0,0.3,0.4), "know": (0.1,0.3,0.6)}
TONE_MAP = {("pos","high","high"): "energized-confidence", ("pos","high","mid"): "enthusiastic-drive", ("pos","high","low"): "delighted-surrender", ("pos","mid","high"): "steady-resolve", ("pos","mid","mid"): "warm-engagement", ("pos","mid","low"): "receptive-warmth", ("pos","low","high"): "quiet-authority", ("pos","low","mid"): "gentle-warmth", ("pos","low","low"): "gentle-acceptance", ("neg","high","high"): "combative-defiance", ("neg","high","mid"): "agitated-resistance", ("neg","high","low"): "urgent-distress", ("neg","mid","high"): "guarded-tension", ("neg","mid","mid"): "steady-discomfort", ("neg","mid","low"): "vulnerable-frustration", ("neg","low","high"): "cold-withdrawal", ("neg","low","mid"): "quiet-resignation", ("neg","low","low"): "quiet-sadness", ("neutral","high","high"): "focused-flow", ("neutral","high","mid"): "alert-readiness", ("neutral","high","low"): "restless-searching", ("neutral","mid","high"): "grounded-awareness", ("neutral","mid","mid"): "balanced-presence", ("neutral","mid","low"): "uncertain-drift", ("neutral","low","high"): "settled-composure", ("neutral","low","mid"): "passive-observation", ("neutral","low","low"): "flat-numbness"}
STRATEGY_MAP = {"needs-support": "validate-then-assist", "needs-gentle-approach": "slow-pace-acknowledge-first", "high-engagement": "match-energy-collaborate", "default": "standard-responsive"}

def pipeline(text):
    words = re.findall(r"[a-z]+", text.lower())
    hits = [(w, VAD_WORDS[w]) for w in words if w in VAD_WORDS]
    if not hits: return {"tone": "balanced-presence", "vad": (0,0.3,0.5), "disc": ("neutral","mid","mid"), "matched": [], "nal": [], "strategy": "standard-responsive"}
    v=sum(h[1][0] for h in hits)/len(hits)
    a=sum(h[1][1] for h in hits)/len(hits)
    d=sum(h[1][2] for h in hits)/len(hits)
    vv="pos" if v>0.2 else ("neg" if v<-0.2 else "neutral")
    aa="high" if a>0.6 else ("low" if a<0.4 else "mid")
    dd="high" if d>0.6 else ("low" if d<0.4 else "mid")
    tone=TONE_MAP.get((vv,aa,dd),"balanced-presence")
    conf=min(0.99, 0.5+abs(v)*0.3+abs(a)*0.2)
    nal = ["(--> user-state %s) (stv 1.0 %.2f)" % (tone, conf)]
    strategy = "standard-responsive"
    if v < -0.2 and d < 0.4:
        strategy = "slow-pace-acknowledge-first"
        nal.append("INFERRED: needs-gentle-approach (conf=%.2f)" % (conf*0.85))
    elif v < -0.2:
        strategy = "validate-then-assist"
        nal.append("INFERRED: needs-support (conf=%.2f)" % (conf*0.8))
    elif v > 0.2 and a > 0.5:
        strategy = "match-energy-collaborate"
        nal.append("INFERRED: high-engagement (conf=%.2f)" % (conf*0.9))
    return {"tone": tone, "vad": (round(v,3),round(a,3),round(d,3)), "disc": (vv,aa,dd), "matched": [h[0] for h in hits], "nal": nal, "strategy": strategy}

print("=== END-TO-END INTEGRATION TEST ===")
print("Text -> VAD -> Tone -> NAL -> Strategy\n")
for t in ["I am worried this wont work and I feel powerless", "Everything is clicking into place and I feel strong and clear", "I dont know what I feel right now", "I am so angry and frustrated", "I feel calm and safe and grateful"]:
    r=pipeline(t)
    print("INPUT:", t)
    print("  TONE:", r["tone"])
    print("  VAD:", r["vad"])
    print("  STRATEGY:", r["strategy"])
    for n in r["nal"]: print("  NAL:", n)
    print()
