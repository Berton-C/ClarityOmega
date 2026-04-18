import os
import subprocess
result = subprocess.run(['grep', '-rl', 'metta', '/PeTTa/repos/omegaclaw/'], capture_output=True, text=True, timeout=10)
for line in result.stdout.strip().split('\n'):
    if line.endswith('.py'):
        with open(line) as f:
            content = f.read()
        if 'MeTTa' in content or 'runner' in content.lower() or 'atomspace' in content.lower() or 'load' in content.lower():
            hits = []
            for i, l in enumerate(content.splitlines()):
                low = l.lower()
                if 'metta' in low or 'runner' in low or 'atomspace' in low:
                    hits.append(f'  {i+1}: {l.rstrip()}')
            if hits:
                print(f'\n=== {line} ===')
                for h in hits[:10]:
                    print(h)
