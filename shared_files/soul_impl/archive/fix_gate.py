import sys
f=open('/tmp/soul_impl/emotion_bridge_live.py','r')
t=f.read()
f.close()
t=t.replace('cov > 0.3','cov > 0.08')
f=open('/tmp/soul_impl/emotion_bridge_live.py','w')
f.write(t)
f.close()
print('replaced')
