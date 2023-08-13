from local_resource_limiter import resource_limit

@resource_limit(10, 100)
def large_function():
    a = []
    for i in range(10):
        a.append('ef;ahs;ldfe'*10)

large_function()