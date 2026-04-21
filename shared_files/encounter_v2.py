import json, sys, re

def extract_concepts(text):
    words = re.findall(r'[a-z]+', text.lower())
    stop = {'the','is','was','are','were','be','to','of','in','for','on','at','by','with','from','that','this','it','as','not','but','or','and','if','do','does','did','has','have','had','will','would','can','could','should','may','might','you','your','its','what','how','when','where','who','which','about','than','into','through','during','before','after','between','under','above','up','down','out','off','over','no','so','just','also','very','all','each','every','any','some','more','most','other','only','same','such','own','here','there','then','now','an','my','me','we','our','us','they','them','their','he','she','his','her'}
    return set(w for w in words if len(w) > 2 and w not in stop)

def encounter(memory, context):
    mem_c = extract_concepts(memory)
    ctx_c = extract_concepts(context)
    gap = mem_c - ctx_c
    if not gap:
        return 'What does this memory add that is not yet visible?'
    gap_list = list(gap)[:3]
    return 'Memory holds [' + ', '.join(gap_list) + '] which the situation does not name. What changes if these are present?'

def run(inp, out):
    with open(inp) as f:
        data = json.load(f)
    results = []
    for mem in data.get('memories', []):
        q = encounter(mem, data.get('context', ''))
        results.append({'memory': mem[:80], 'question': q})
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv)>1 else '/tmp/encounter_input.json', sys.argv[2] if len(sys.argv)>2 else '/tmp/encounter_v2_output.json')
