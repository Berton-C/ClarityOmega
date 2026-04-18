import os
for f in sorted(os.listdir('/tmp')):
  if f.endswith('.extracted.txt'):
    path = '/tmp/' + f
    size = os.path.getsize(path)
    with open(path) as fh:
      content = fh.read()[:1500]
    print('=== ' + f[:55] + ' === ' + str(size) + ' chars')
    print(content)
    print()
