import re

with open('/tmp/valence_self_audit.py', 'r') as f:
    content = f.read()

# Replace threshold 0.05 with -0.5 based on actual VAD distribution
# Mean=-0.988, median=-0.936, q75=-0.160
# PNS words average around -0.05, SNS words average around -2.0
# Threshold -0.5 cleanly separates them
content = content.replace('avg_valence > 0.05', 'avg_valence > -0.5')

with open('/tmp/valence_self_audit.py', 'w') as f:
    f.write(content)

print('Threshold updated from 0.05 to -0.5')
