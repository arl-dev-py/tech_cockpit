import psutil
import subprocess


def get_cpu_info():
    cpu_temp = get_cpu_temperature()
    return {
        'cores': psutil.cpu_count(logical=True),
        'usage': psutil.cpu_percent(interval=None),
        'per_core': psutil.cpu_percent(interval=None, percpu=True),
        'temp': f"{cpu_temp}°C (max 95°)",
        'cpu_model': "Unknown"
    }


def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                if 'cpu' in name.lower() or 'core' in name.lower():
                    for entry in entries:
                        if entry.current:
                            return f"{entry.current:.1f}"
        return "42.5"
    except:
        return "42.5"


def get_gpu_info():
    try:
        result = subprocess.run(['nvidia-smi',
                                 '--query-gpu=utilization.gpu,temperature.gpu,memory.used,memory.total',
                                 '--format=csv,noheader,nounits'],
                                capture_output=True, text=True, timeout=3)

        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            gpu_list = []
            for line in lines:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 4:
                    load, temp, mem_used, mem_total = parts
                    gpu_list.append({
                        'load': f"{load}%",
                        'temp': f"{temp}°C (max 83°)",
                        'mem_used': f"{mem_used}MB",
                        'mem_total': f"{mem_total}MB"
                    })
            return gpu_list
    except:
        pass
    return [{'load': '0%', 'temp': '35°C (max 83°)', 'mem_used': '0MB', 'mem_total': '8GB'}]


def get_top_processes():
    processes = []
    EXCLUDE = ['System Idle Process', 'System', 'smss.exe', 'csrss.exe', 'wininit.exe']

    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
        try:
            cpu = float(proc.info['cpu_percent'])
            if cpu > 0 and proc.info['name'] not in EXCLUDE:
                processes.append(
                    (proc.info['cpu_percent'], proc.info['name'], proc.info['memory_info'].rss)
                )
        except:
            continue

    processes.sort(key=lambda x: x[0], reverse=True)
    result = processes[:5]

    result_dicts = []
    for elem in result:
        process_dict = {}
        process_dict["name"] = elem[1][:12]
        process_dict["cpu"] = f"{elem[0]:.1f}%"
        process_dict["ram"] = f"{elem[2] / 1024 ** 3:.1f}GB"
        result_dicts.append(process_dict)

    return result_dicts

