path = '/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_clarity_reasoning.metta'
with open(path) as f:
    content = f.read()
if 'lib_meta_inference' not in content:
    content = content.replace('lib_inference_router))', 'lib_inference_router))\n!(import! &self (library omegaclaw lib_meta_inference))')
    with open(path, 'w') as f:
        f.write(content)
    print('added')
else:
    print('already present')
