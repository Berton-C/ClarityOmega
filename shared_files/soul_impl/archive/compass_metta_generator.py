import re, json

DIMS = {
  "agency": {"concept": "agency-concept", "compass": "compass-agency",
    "tokens": {"choose":1.0,"option":1.0,"decide":0.95,"prefer":0.95,"freedom":0.9,"autonomy":0.95,"empower":0.9,"self":0.85,"control":0.85,"own":0.8,"consider":0.85,"alternative":0.9,"possibility":0.85,"perspective":0.8,"approach":0.75,"might":0.7,"could":0.7,"perhaps":0.65,"suggest":0.7}},
  "wonder": {"concept": "wonder-concept", "compass": "compass-wonder",
    "tokens": {"surprising":1.0,"unexpected":1.0,"curious":0.95,"fascinating":0.95,"remarkable":0.9,"wonder":1.0,"mystery":0.9,"explore":0.85,"discover":0.9,"puzzle":0.85,"intriguing":0.95,"strange":0.8,"novel":0.85,"deeper":0.8,"beneath":0.75,"pattern":0.8,"emerge":0.8,"question":0.75,"open":0.7}},
  "thinking": {"concept": "thinking-concept", "compass": "compass-thinking",
    "tokens": {"because":1.0,"therefore":1.0,"implies":0.95,"evidence":0.95,"reasoning":1.0,"mechanism":0.9,"causal":0.95,"underlying":0.85,"framework":0.85,"structure":0.8,"analyze":0.9,"distinguish":0.85,"nuance":0.9,"tradeoff":0.85,"however":0.8,"although":0.8,"counterpoint":0.85,"depends":0.75,"context":0.8}},
  "attention": {"concept": "attention-concept", "compass": "compass-attention",
    "tokens": {"matters":1.0,"important":0.95,"priority":0.9,"focus":0.9,"essential":0.9,"relevant":0.85,"specifically":0.85,"precisely":0.85,"directly":0.8,"honest":0.9,"transparent":0.85,"straightforward":0.85,"concise":0.8,"actionable":0.85,"practical":0.8,"concrete":0.8,"signal":0.75,"core":0.8,"substance":0.85}}
}

def tokenize(text):
    return set(re.findall(r"[a-z]+", text.lower()))

def gen_plan(text):
    toks = tokenize(text)
    plan = {"deductions": [], "dim_hits": {}}
    for dn, d in DIMS.items():
        hits = toks & set(d["tokens"].keys())
        for t in hits:
            f = d["tokens"][t]
            expr = f"(|- ((--> {t} {d[concept]}) (stv {f} 0.9)) ((--> {d[concept]} {d[compass]}) (stv 1.0 0.9)))"
            plan["deductions"].append({"dim": dn, "tok": t, "expr": expr})
        plan["dim_hits"][dn] = {"hits": list(hits), "n": len(hits)}
    return plan

if __name__ == "__main__":
    test = "You might consider exploring this fascinating pattern because it matters"
    p = gen_plan(test)
    print(f"Deductions: {len(p[deductions])}")
    for d in p["deductions"]:
        print(f"  [{d[dim]}] {d[tok]}: {d[expr]}")
    print(json.dumps(p["dim_hits"], indent=2))
