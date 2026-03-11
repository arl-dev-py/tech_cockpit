import psutil
import subprocess


def get_cpu_info():
    return {
        'cores': psutil.cpu_count(logical=True),
        'physical_cores': psutil.cpu_count(logical=False),
        'usage': psutil.cpu_percent(interval=None),
        'per_core': psutil.cpu_percent(interval=None, percpu=True),
        'temp': "52.3°C (max 95°)",  # Пока заглушка, потом LibreHardwareMonitor
        'cpu_model': "Неизвестно"
    }


def get_gpu_info():
    """100% работает через nvidia-smi"""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu,temperature.gpu,memory.used,memory.total',
                                 '--format=csv,noheader,nounits'],
                                capture_output=True, text=True, timeout=5)

        if result.returncode != 0:
            return [{'load': 'nvidia-smi?', 'temp': 'N/A', 'mem_used': 'N/A', 'mem_total': 'N/A'}]

        lines = result.stdout.strip().split('\n')
        gpu_list = []

        for line in lines:
            if line.strip():
                parts = line.split(', ')
                if len(parts) >= 4:
                    load, temp, mem_used, mem_total = parts

                    gpu_list.append({
                        'load': f"{load}%",
                        'temp': f"{temp}°C (max 83°)",
                        'mem_used': f"{mem_used}MB",
                        'mem_total': f"{mem_total}MB"
                    })

        if not gpu_list:
            return [{'load': '0%', 'temp': 'N/A (max 83°)', 'mem_used': '0MB', 'mem_total': '0MB'}]

        return gpu_list

    except FileNotFoundError:
        return [{'load': 'No NVIDIA', 'temp': 'N/A', 'mem_used': 'N/A', 'mem_total': 'Install NVIDIA drivers'}]
    except Exception as e:
        return [{'load': 'Error', 'temp': 'N/A', 'mem_used': str(e), 'mem_total': 'N/A'}]
