import sys
sys.path.insert(0, '/tmp/soul_impl')
from rewrite_guidance import generate_guidance, format_rewrite_prompt

g = generate_guidance(['compass-attention', 'compass-thinking'])
print('Guidance entries:', len(g))
for entry in g:
    print(' ', entry['dimension'], '-', entry['principle'])

p = format_rewrite_prompt(['compass-attention'], 'Here is a test draft')
print(p[:300])
print('REWRITE GUIDANCE TEST PASSED')
