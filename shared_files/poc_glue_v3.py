import re
VAD_WORDS = {"frustrated": (-0.6,0.7,0.3), "stuck": (-0.5,0.4,0.2), "excited": (0.8,0.8,0.6), "love": (0.9,0.5,0.5), "anxious": (-0.5,0.7,0.2), "calm": (0.3,0.2,0.6), "angry": (-0.8,0.8,0.7), "happy": (0.8,0.6,0.6), "sad": (-0.6,0.3,0.3), "confused": (-0.3,0.5,0.2), "hopeful": (0.6,0.5,0.5), "tired": (-0.3,0.2,0.3), "curious": (0.5,0.6,0.5), "overwhelmed": (-0.5,0.8,0.2), "grateful": (0.8,0.4,0.5), "build": (0.4,0.6,0.7), "worried": (-0.5,0.6,0.2), "powerless": (-0.6,0.4,0.1), "clicking": (0.5,0.5,0.6), "strong": (0.6,0.6,0.8), "clear": (0.4,0.3,0.7), "afraid": (-0.7,0.7,0.2), "lost": (-0.5,0.4,0.2), "alive": (0.7,0.7,0.6), "proud": (0.7,0.5,0.8), "safe": (0.5,0.2,0.6), "scared": (-0.7,0.7,0.2), "good": (0.6,0.4,0.5), "bad": (-0.5,0.4,0.4), "feel": (0.0,0.3,0.4), "know": (0.1,0.3,0.6)}
TONE_MAP = {("pos","high","high"): "energized-confidence", ("pos","high","mid"): "enthusiastic-drive", ("pos","high","low"): "delighted-surrender", ("pos","mid","high"): "steady-resolve", ("pos","mid","mid"): "warm-engagement", ("pos","mid","low"): "receptive-warmth", ("pos","low","high"): "quiet-authority", ("pos","low","mid"): "gentle-warmth", ("pos","low","low"): "gentle-acceptance", ("neg","high","high"): "combative-defiance", ("neg","high","mid"): "agitated-resistance", ("neg","high","low"): "urgent-distress", ("neg","mid","high"): "guarded-tension", ("neg","mid","mid"): "steady-discomfort", ("neg","mid","low"): "vulnerable-frustration", ("neg","low","high"): "cold-withdrawal", ("neg","low","mid"): "quiet-resignation", ("neg","low","low"): "quiet-sadness", ("neutral","high","high"): "focused-flow", ("neutral","high","mid"): "alert-readiness", ("neutral","high","low"): "restless-searching", ("neutral","mid","high"): "grounded-awareness", ("neutral","mid","mid"): "balanced-presence", ("neutral","mid","low"): "uncertain-drift", ("neutral","low","high"): "settled-composure", ("neutral","low","mid"): "passive-observation", ("neutral","low","low"): "flat-numbness"}
def pipeline(text):
    words = re.findall(r"[a-z]+", text.lower())
    hits = [(w, VAD_WORDS[w]) for w in words if w in VAD_WORDS]
    if not hits: return {"tone": "balanced-presence", "matched": []}
    v=sum(h[1][0] for h in hits)/len(hits)
    a=sum(h[1][1] for h in hits)/len(hits)
    d=sum(h[1][2] for h in hits)/len(hits)
    vv="pos" if v>0.2 else ("neg" if v<-0.2 else "neutral")
    aa="high" if a>0.6 else ("low" if a<0.4 else "mid")
    dd="high" if d>0.6 else ("low" if d<0.4 else "mid")
    tone=TONE_MAP.get((vv,aa,dd),"balanced-presence")
    return {"vad": (round(v,3),round(a,3),round(d,3)), "disc": (vv,aa,dd), "tone": tone, "matched": [h[0] for h in hits]}
for t in ["I am worried this wont work and I feel powerless", "Everything is clicking into place and I feel strong and clear", "I dont know what I feel right now", "I am so angry and frustrated", "I feel calm and safe and grateful"]:
    r=pipeline(t)
    print(r["tone"].ljust(25), "|", r.get("disc",""), "|", r["matched"])
