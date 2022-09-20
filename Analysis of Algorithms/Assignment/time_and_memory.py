import time
import os
import tracemalloc
class GetTime():
    start_time = time.time()
    def __init__(self):
        self.start_time = time.time()

    def reset_time(self):
        self.start_time = time.time()
    
    def end_time(self):
        return (time.time() - self.start_time)

class GetMemory():
    def __init__(self):
        tracemalloc.start()

    def start_memory():
        pass

    def get_memory():
        pass

"""def get_memory_usage():
    memory_in_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
    return memory_in_mb/1000.0

def get_memory_usage2():
    process = psutil.Process(os.getpid())
    memory_in_mb = process.get_ext_memory_info().peak_wset / 1024**2
    return memory_in_mb/1000.0

def get_memory_usage3():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

"""