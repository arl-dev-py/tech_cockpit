import psutil


def get_cpu_info():
    cpu_temp = "N/A"

    try:
        import wmi
        w = wmi.WMI(namespace="root\\wmi")
        temp_info = w.MSAcpi_ThermalZoneTemperature()
        if temp_info:
            temp_kelvin = temp_info[0].CurrentTemperature / 10.0
            cpu_temp = f"{temp_kelvin - 273.15:.1f}°C"
    except:
        cpu_temp = "N/A (WMI недоступно)"

    return {
        'cores': psutil.cpu_count(),
        'usage': psutil.cpu_percent(interval=None),
        'per_core': psutil.cpu_percent(interval=None, percpu=True),
        'temp': cpu_temp,
        'max_temp': "95°C",
        'cpu_model': "Неизвестно"
    }
