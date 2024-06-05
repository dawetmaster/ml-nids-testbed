import psutil

class SystemMonitor:
    def get_metrics(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        
        return {'cpu': cpu_usage, 'memory': memory_usage}