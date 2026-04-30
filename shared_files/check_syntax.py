import py_compile
try:
    py_compile.compile("/tmp/continuity_of_mind/src/idle_goal_prompt.py", doraise=True)
    print("SYNTAX OK")
except py_compile.PyCompileError as e:
    print("SYNTAX ERROR:", e)
