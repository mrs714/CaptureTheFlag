import resource

def resource_limit(max_memory_mb, max_runtime_sec):
    def aux(fun):
        def aux2(*args, **kwargs):
            resource.setrlimit(resource.RLIMIT_AS, (max_memory_mb * 1024 * 1024, resource.RLIM_INFINITY))
            resource.setrlimit(resource.RLIMIT_CPU, (max_runtime_sec, resource.RLIM_INFINITY))
            return fun(*args, **kwargs)
        return aux2
    return aux

@resource_limit(1, 1)
def f():
    while True:
        pass