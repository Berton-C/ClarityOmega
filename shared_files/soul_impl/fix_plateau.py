#!/usr/bin/env python3
with open('/tmp/soul_impl/cycle_loop.py', 'r') as f:
    content = f.read()
content = content.replace('if len(history) >= 2 and abs(new_conf - history[-1]) < threshold:', 'if len(history) >= 1 and abs(new_conf - history[-1]) < threshold:')
with open('/tmp/soul_impl/cycle_loop.py', 'w') as f:
    f.write(content)
print('Fixed: changed >= 2 to >= 1 in detect_plateau')