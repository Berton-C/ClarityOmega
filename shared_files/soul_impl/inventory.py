import os

files = sorted(os.listdir('/tmp/soul_impl'))
py_files = [f for f in files if f.endswith('.py')]
md_files = [f for f in files if f.endswith('.md')]
other = [f for f in files if not f.endswith('.py') and not f.endswith('.md') and not f.startswith('.')]

print(f'Python files: {len(py_files)}')
print(f'Markdown files: {len(md_files)}')
print(f'Other files: {len(other)}')
print()
for f in py_files:
    size = os.path.getsize(os.path.join('/tmp/soul_impl', f))
    print(f'  {size:6d}  {f}')
print()
for f in md_files:
    size = os.path.getsize(os.path.join('/tmp/soul_impl', f))
    print(f'  {size:6d}  {f}')
print()
for f in other:
    size = os.path.getsize(os.path.join('/tmp/soul_impl', f))
    print(f'  {size:6d}  {f}')
