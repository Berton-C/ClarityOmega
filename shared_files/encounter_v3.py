import json, sys, re

ANTONYMS = {
    'acquire': 'recognize', 'recognize': 'acquire',
    'fast': 'slow', 'slow': 'fast',
    'add': 'remove', 'remove': 'add',
    'safety': 'risk', 'risk': 'safety',
    'honest': 'deceptive', 'deceptive': 'honest',
    'trust': 'suspicion', 'suspicion': 'trust',
    'autonomy': 'control', 'control': 'autonomy',
    'wonder': 'certainty', 'certainty': 'wonder',
    'static': 'dynamic', 'dynamic': 'static',
    'absence': 'presence', 'presence': 'absence'
}

ACTION_WORDS = {'build','create','seek','move','change','act','choose','refuse','test','draft','write','run','navigate'}
STATE_WORDS = {'is','exists','remains','holds','stays','feels','seems','appears','knows','has'}

def extract_concepts(text):
    words = re.findall(r'[a-z]+', text.lower())
    stop = {'the','is','was','are','were','be','to','of','in','for','on','at','by','with','from','that','this','it','as','not','but','or','and','if','do','does','did','has','have','had','will','would','can','could','should','may','might','you','your','its','what','how','when','where','who','which','about','than','into','through','during','before','after','between','under','above','up','down','out','off','over','no','so','just','also','very','all','each','every','any','some','more','most','other','only','same','such','own','here','there','then','now','an','my','me','we','our','us','they','them','their','he','she','his','her'}
    return set(w for w in words if len(w) > 2 and w not in stop)

def tension_score(gap_word, ctx_concepts):
    if gap_word in ANTONYMS and ANTONYMS[gap_word] in ctx_concepts:
        return 3
    if gap_word in ACTION_WORDS and any(w in STATE_WORDS for w in ctx_concepts):
        return 2
    return 1

def encounter_v3(memory, context):
    mem_c = extract_concepts(memory)
    ctx_c = extract_concepts(context)
    gap = mem_c - ctx_c
    if not gap:
        return {'gap': [], 'tension': 0, 'question': 'What does this memory add that is not yet visible?'}
    scored = sorted(gap, key=lambda w: tension_score(w, ctx_c), reverse=True)
    top = scored[:3]
    best_score = tension_score(top[0], ctx_c)
    phrase = ', '.join(top)
    return {'gap': top, 'tension': best_score, 'question': f'Highest-tension concepts [{phrase}] are absent from context. What shifts if they enter?'}

def run(inp, out):
    with open(inp) as f:
        data = json.load(f)
    results = [encounter_v3(m, data.get('context','')) for m in data.get('memories',[])]
    with open(out,'w') as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv)>1 else '/tmp/encounter_input.json', sys.argv[2] if len(sys.argv)>2 else '/tmp/encounter_v3_output.json')
