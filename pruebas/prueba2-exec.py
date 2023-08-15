from RestrictedPython import compile_restricted_exec, safe_builtins
import sys
import traceback

code = """patat = 3
def test():
    patat.hola()
test()
"""

compiled = compile_restricted_exec(code)
if compiled.errors:
    print("Errors:")
    for error in compiled.errors:
        print(error)
else:

    bytecode= compiled.code
    try:
        exec(bytecode, {"__builtins__": safe_builtins}, {})
    except:
        cl, exc, tb = sys.exc_info()
        tb2 = traceback.extract_tb(tb)
        print(f"Line {tb2[-1].lineno}: {cl.__name__}: {exc}")