import time
import psutil
import os

def measure_encryption(func, *args, **kwargs):
    """
    Measures time, CPU %, and memory usage of an encryption/decryption function.
    Returns result + metrics.
    """
    process = psutil.Process(os.getpid())

    # Measure start time and resources
    start_time = time.perf_counter()
    cpu_start = process.cpu_times()
    mem_start = process.memory_info().rss

    # Run the actual function (encrypt or decrypt)
    result = func(*args, **kwargs)

    # Measure end time and resources
    end_time = time.perf_counter()
    cpu_end = process.cpu_times()
    mem_end = process.memory_info().rss

    # Compute metrics
    elapsed_time = (end_time - start_time) * 1000  # ms
    cpu_used = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)
    mem_used = mem_end - mem_start

    metrics = {
        "time_ms": elapsed_time,
        "cpu_time": cpu_used,
        "mem_bytes": mem_used
    }

    return result, metrics
