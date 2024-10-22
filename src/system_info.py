import platform
import psutil

def get_system_info():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "disk_total": psutil.disk_usage('/').total
    }
