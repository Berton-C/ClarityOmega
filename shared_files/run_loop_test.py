from hyperon import MeTTa
import os
os.chdir('/PeTTa/repos/omegaclaw')
m = MeTTa()
try:
    print('=== Loading context.metta ===')
    r1 = m.run(open('src/context.metta').read())
    print('context result:', r1)
except Exception as e:
    print('context error:', e)
try:
    print('=== Loading loop.metta ===')
    r2 = m.run(open('src/loop.metta').read())
    print('loop result:', r2)
except Exception as e:
    print('loop error:', e)
print('=== TEST COMPLETE ===')
