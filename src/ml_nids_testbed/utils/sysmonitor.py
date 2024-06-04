import psutil
import time
import threading
import logging

logger = logging.getLogger(__name__)

class SystemMonitor(object):
    def __init__(self, interval: float=1.0):
        self.__cpu_usage_data = []
        self.__memory_usage_data = []
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._monitor_system)
        self.interval = interval

    def start(self):
        if not self._thread.is_alive():
            self._thread.start()
            print("Monitoring started.")
    
    def stop(self):
        self._thread.join()

    def _monitor_system(self):
        while not self._stop_event.is_set():
            # Get CPU usage percentage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Get virtual memory usage
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent

            time.sleep(self.interval)
