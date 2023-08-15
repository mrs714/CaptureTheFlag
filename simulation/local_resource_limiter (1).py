import pynisher

def resource_limit(max_memory_mb, max_runtime_sec):
    def aux(fun):
        return pynisher.limit(
            fun,
            memory = (max_memory_mb, "MB"),
            wall_time = (max_runtime_sec, "s")
        )
    return aux