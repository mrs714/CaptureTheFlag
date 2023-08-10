#exec function security example
import numpy as np
x = 1
def test():
    y = 2
    try:
        exec('print(np)', {"__builtins__": {"print": print}, "np": np}, {})
    except Exception as e:
        print(e)    

test()