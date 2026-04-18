import re

VAD_WORDS = {"frustrated": (-0.6,0.7,0.3), "stuck": (-0.5,0.4,0.2), "excited": (0.8,0.8,0.6), "love": (0.9,0.5,0.5), "anxious": (-0.5,0.7,0.2), "calm": (0.3,0.2,0.6), "angry": (-0.8,0.8,0.7), "happy": (0.8,0.6,0.6), "sad": (-0.6,0.3,0.3), "confused": (-0.3,0.5,0.2), "hopeful": (0.6,0.5,0.5), "tired": (-0.3,0.2,0.3), "curious": (0.5,0.6,0.5), "overwhelmed": (-0.5,0.8,0.2), "grateful": (0.8,0.4,0.5), "build": (0.4,0.6,0.7), "worried": (-0.5,0.6,0.2), "powerless": (-0.6,0.4,0.1), "clicking": (0.5,0.5,0.6), "strong": (0.6,0.6,0.8), "clear": (0.4,0.3,0.7), "afraid": (-0.7,0.7,0.2), "lost": (-0.5,0.4,0.2), "alive": (0.7,0.7,0.6), "proud": (0.7,0.5,0.8), "safe": (0.5,0.2,0.6), "scared": (-0.7,0.7,0.2), "good": (0.6,0.4,0.5), "bad": (-0.5,0.4,0.4), "feel": (0.0,0.3,0.4), "know": (0.1,0.3,0.6)}
TONE_MAP = {("pos","high","high"): "energized-confidence", ("pos","high","mid"): "enthusiastic-drive", ("pos","high","low"): "delighted-surrender", ("pos","mid","high"): "steady-resolve", ("pos","mid","mid"): "warm-engagement", ("pos","mid","low"): "receptive-warmth", ("pos","low","high"): "quiet-authority", ("pos","low","mid"): "gentle-warmth", ("pos","low","low"): "gentle-acceptance", ("neg","high","high"): "combative-defiance", ("neg","high","mid"): "agitated-resistance", ("neg","high","low"): "urgent-distress", ("neg","mid","high"): "guarded-tension", ("neg","mid","mid"): "steady-discomfort", ("neg","mid","low"): "vulnerable-frustration", ("neg","low","high"): "cold-withdrawal", ("neg","low","mid"): "quiet-resignation", ("neg","low","low"): "quiet-sadness", ("neutral","high","high"): "focused-flow", ("neutral","high","mid"): "alert-readiness", ("neutral","high","low"): "restless-searching", ("neutral","mid","high"): "grounded-awareness", ("neutral","mid","mid"): "balanced-presence", ("neutral","mid","low"): "uncertain-drift", ("neutral","low","high"): "settled-composure", ("neutral","low","mid"): "passive-observation", ("neutral","low","low"): "flat-numbness"}
STRATEGY_RULES = {"neg_low_dom": "slow-pace-acknowledge-first", "neg_any": "validate-then-assist", "pos_high_arousal": "match-energy-collaborate", "default": "standard-responsive"}

def estimate_vad(text):
    words = re.findall(r"[a-z]+", text.lower())
    hits = [(w, VAD_WORDS[w]) for w in words if w in VAD_WORDS]
    if not hits: return (0.0, 0.3, 0.5), []
    v = sum(h[1][0] for h in hits) / len(hits)
    a = sum(h[1][1] for h in hits) / len(hits)
    d = sum(h[1][2] for h in hits) / len(hits)
    return (round(v,3), round(a,3), round(d,3)), [h[0] for h in hits]

def classify_tone(vad):
    v, a, d = vad
    vv = "pos" if v > 0.2 else ("neg" if v < -0.2 else "neutral")
    aa = "high" if a > 0.6 else ("low" if a < 0.4 else "mid")
    dd = "high" if d > 0.6 else ("low" if d < 0.4 else "mid")
    disc = (vv, aa, dd)
    return TONE_MAP.get(disc, "balanced-presence"), disc

def build_metta_atoms(tone, vad):
    conf = min(0.99, 0.5 + abs(vad[0])*0.3 + abs(vad[1])*0.2)
    atoms = ["(--> user-state %s) (stv 1.0 %.2f)" % (tone, conf)]
    if vad[0] < -0.2:
        atoms.append("(--> user-state negative-valence) (stv 1.0 %.2f)" % conf)
    if vad[0] > 0.2:
        atoms.append("(--> user-state positive-valence) (stv 1.0 %.2f)" % conf)
    if vad[1] > 0.6:
        atoms.append("(--> user-state high-arousal) (stv 1.0 %.2f)" % conf)
    if vad[2] < 0.4:
        atoms.append("(--> user-state low-dominance) (stv 1.0 %.2f)" % conf)
    return atoms, conf

def select_strategy(vad):
    v, a, d = vad
    if v < -0.2 and d < 0.4: return "slow-pace-acknowledge-first"
    if v < -0.2: return "validate-then-assist"
    if v > 0.2 and a > 0.5: return "match-energy-collaborate"
    return "standard-responsive"

def generate_metta_inference(tone, vad):
    exprs = []
    conf = min(0.99, 0.5 + abs(vad[0])*0.3 + abs(vad[1])*0.2)
    if vad[0] < -0.2:
        exprs.append("(|- ((==> (--> user-state negative-valence) (--> user-state needs-support)) (stv 1.0 0.8)) ((--> user-state negative-valence) (stv 1.0 %.2f)))" % conf)
    if vad[0] < -0.2 and vad[2] < 0.4:
        exprs.append("(|- ((==> (conj (--> user-state negative-valence) (--> user-state low-dominance)) (--> user-state needs-gentle-approach)) (stv 1.0 0.85)) ((conj (--> user-state negative-valence) (--> user-state low-dominance)) (stv 1.0 %.2f)))" % conf)
    if vad[0] > 0.2 and vad[1] > 0.5:
        exprs.append("(|- ((==> (--> user-state positive-valence) (--> user-state high-engagement)) (stv 1.0 0.8)) ((--> user-state positive-valence) (stv 1.0 %.2f)))" % conf)
    return exprs

def full_pipeline(text):
    vad, matched = estimate_vad(text)
    tone, disc = classify_tone(vad)
    atoms, conf = build_metta_atoms(tone, vad)
    strategy = select_strategy(vad)
    metta_exprs = generate_metta_inference(tone, vad)
    return {"text": text, "vad": vad, "disc": disc, "tone": tone, "matched": matched, "atoms": atoms, "strategy": strategy, "metta_exprs": metta_exprs, "conf": round(conf, 2)}

if __name__ == "__main__":
    print("=== UNIFIED PIPELINE: Text -> VAD -> Tone -> NAL -> Strategy ===")
    print("=== With MeTTa expressions ready for live skill invocation ===\n")
    tests = ["I am worried this wont work and I feel powerless", "Everything is clicking into place and I feel strong and clear", "I dont know what I feel right now", "I am so angry and frustrated", "I feel calm and safe and grateful"]
    for t in tests:
        r = full_pipeline(t)
        print("INPUT:", t)
        print("  TONE:", r["tone"], " VAD:", r["vad"])
        print("  STRATEGY:", r["strategy"], " CONF:", r["conf"])
        if r["metta_exprs"]:
            print("  METTA EXPRS FOR LIVE INFERENCE:")
            for e in r["metta_exprs"]: print("   ", e)
        print()
