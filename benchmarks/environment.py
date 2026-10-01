import platform
import sys

import psutil


def collect_environment():

    memory = psutil.virtual_memory()

    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(
            interval=0.5
        ),
        "memory_total_mb": round(
            memory.total / 1024 / 1024,
            2
        ),
        "memory_available_mb": round(
            memory.available / 1024 / 1024,
            2
        ),
    }