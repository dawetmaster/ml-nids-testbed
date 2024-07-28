from statistics import stdev
from utils.controller.stats import Statistics
import tempfile
import logging
import numpy as np
import requests

class SystemMonitor(object):
    def __init__(self, agent_url: str="localhost:5758", batch_size: int=1000):
        self.__cpu_usage_current_batch = []
        self.__memory_usage_current_batch = []
        self.__cpu_usage_data_batch_files = []
        self.__memory_usage_data_batch_files = []
        self.__agent_url = agent_url
        self.__cpustats = Statistics()
        self.__memstats = Statistics()
        self.__batch_size = batch_size
        self.__logger = logging.getLogger("sysmonitor")

    @property
    def cpu_usage_mean(self):
        return self.__cpustats.avg
    @property
    def memory_usage_mean(self):
        return self.__memstats.avg
    @property
    def cpu_usage_stdev(self):
        return self.__cpustats.stddev
    @property
    def memory_usage_stdev(self):
        return self.__memstats.stddev
    @property
    def cpu_usage_top_1_percent(self):
        return self.__cpu_top_1_percent
    @property
    def memory_usage_top_1_percent(self):
        return self.__memory_top_1_percent
    @property
    def cpu_usage_median(self):
        return np.median(self.__cpu_median)
    @property
    def memory_usage_median(self):
        return np.median(self.__memory_median)

    async def request_resource_usage(self):
        result = requests.get("http://" + self.__agent_url + "/usage", timeout=3)
        if result.status_code == 200:
            cpu_usage = float(result.json()["cpu_usage"])
            memory_usage = float(result.json()["memory_usage"])
            self.__logger.info(f"CPU: {cpu_usage:.2f}% MEM: {memory_usage:.2f}%")
            self.__add_resource_data(cpu_usage, memory_usage)
        else:
            self.__logger.error(f"Failed to retrieve resource usage from agent: {result.status_code}")

    def __process_batch(self, temporary_file, current_batch):
        np.save(temporary_file, np.array(current_batch))

    def __add_resource_data(self, cpu_usage: float, memory_usage: float):
        # Update statistics dynamically to further calculate mean and variance
        self.__cpustats.update(cpu_usage)
        self.__memstats.update(memory_usage)
        # This process is needed to complete the current batch
        self.__cpu_usage_current_batch.append(cpu_usage)
        self.__memory_usage_current_batch.append(memory_usage)
        if len(self.__cpu_usage_current_batch) > self.__batch_size:
            # Save current batch to temporary file
            cpu_temporary_file = tempfile.TemporaryFile()
            memory_temporary_file = tempfile.TemporaryFile()
            self.__process_batch(cpu_temporary_file, self.__cpu_usage_current_batch)
            self.__process_batch(memory_temporary_file, self.__memory_usage_current_batch)
            # Reset current batch
            self.__cpu_usage_current_batch = []
            self.__memory_usage_current_batch = []
            # Append temporary file to data batches
            self.__cpu_usage_data_batch_files.append(cpu_temporary_file)
            self.__memory_usage_data_batch_files.append(memory_temporary_file)

    def finish_monitoring(self):
        cpu_temporary_file = tempfile.TemporaryFile()
        memory_temporary_file = tempfile.TemporaryFile()
        self.__process_batch(cpu_temporary_file, self.__cpu_usage_current_batch)
        self.__process_batch(memory_temporary_file, self.__memory_usage_current_batch)

    def process_final_stats(self):
        cpu_data = self.__final_processing_batch(self.__cpu_usage_data_batch_files)
        memory_data = self.__final_processing_batch(self.__memory_usage_data_batch_files)
        self.__cpu_median = np.median(cpu_data)
        self.__memory_median = np.median(memory_data)
        self.__cpu_top_1_percent = np.percentile(cpu_data, 99)
        self.__memory_top_1_percent = np.percentile(memory_data, 99)

    def __final_processing_batch(self, data_batch_files):
        all_data = []
        for file in data_batch_files:
            file.seek(0)  # Reset file pointer to the beginning
            batch = np.load(file)
            all_data.append(batch)
            file.close()
        return all_data
