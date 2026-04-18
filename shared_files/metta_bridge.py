import json
import subprocess

def tone_to_nal(tone_result):
    tone = tone_result.get("tone", "balanced-presence")
    vad = tone_result.get("vad", (0,0,0))
    conf = min(0.99, 0.5 + abs(vad[0])*0.3 + abs(vad[1])*0.2)
    freq = 1.0 if vad[0] >= 0 else 0.0
    statements = []
    statements.append("((--> user-state %s) (stv %.2f %.2f))" % (tone, freq, round(conf,2)))
    if vad[0] > 0.2:
        statements.append("((--> user-state positive-valence) (stv 1.0 %.2f))" % round(conf,2))
    elif vad[0] < -0.2:
        statements.append("((--> user-state negative-valence) (stv 1.0 %.2f))" % round(conf,2))
    if vad[1] > 0.6:
        statements.append("((--> user-state high-arousal) (stv 1.0 %.2f))" % round(conf,2))
    if vad[2] < 0.4:
        statements.append("((--> user-state low-dominance) (stv 1.0 %.2f))" % round(conf,2))
    return statements

if __name__ == "__main__":
    test_results = [
        {"tone": "vulnerable-frustration", "vad": (-0.367, 0.433, 0.233), "disc": ("neg","mid","low")},
        {"tone": "steady-resolve", "vad": (0.375, 0.45, 0.65), "disc": ("pos","mid","high")},
        {"tone": "agitated-resistance", "vad": (-0.7, 0.75, 0.5), "disc": ("neg","high","mid")},
    ]
    for tr in test_results:
        nal = tone_to_nal(tr)
        print("Tone: %s" % tr["tone"])
        for s in nal:
            print("  NAL: %s" % s)
        print()
