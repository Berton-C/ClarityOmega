import py_compile
try:
    py_compile.compile('/PeTTa/repos/omegaclaw/src/helper.py.deduped', doraise=True)
    print('DEDUPED_SYNTAX_OK')
except py_compile.PyCompileError as e:
    print(f'SYNTAX_ERROR: {e}')
