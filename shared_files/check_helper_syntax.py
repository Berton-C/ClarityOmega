import py_compile
try:
    py_compile.compile('/PeTTa/repos/omegaclaw/src/helper.py', doraise=True)
    print('HELPER_PY_SYNTAX_OK')
except py_compile.PyCompileError as e:
    print('SYNTAX_ERROR: ' + str(e))
