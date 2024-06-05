from statistics import stdev
import grpc
import utils.sysmon_pb2
import utils.sysmon_pb2_grpc

class SystemMonitor(object):
    def __init__(self, agent_url: str="localhost:5758"):
        self.__cpu_usage_data = []
        self.__memory_usage_data = []
        self.__agent_url = agent_url
    
    def request_resource_usage(self):
        with grpc.insecure_channel(self.__agent_url) as channel:
            stub = utils.sysmon_pb2_grpc.MetricsServiceStub(channel)
            response = stub.GetMetrics(utils.sysmon_pb2.Empty())
            self.__add_resource_data(response.cpu, response.memory)
    
    def __add_resource_data(self, cpu_usage: float, memory_usage: float):
        self.__cpu_usage_data.append(cpu_usage)
        self.__memory_usage_data.append(memory_usage)

    def compute_avg_cpu(self):
        return sum(self.__cpu_usage_data) / len(self.__cpu_usage_data)
    
    def compute_avg_memory(self):
        return sum(self.__memory_usage_data) / len(self.__memory_usage_data)
    
    def compute_stdev_cpu(self):
        return stdev(self.__cpu_usage_data)
    
    def compute_stdev_memory(self):
        return stdev(self.__memory_usage_data)
    
    def compute_median_cpu(self):
        if len(self.__cpu_usage_data) % 2 == 0:
            return (self.__cpu_usage_data[len(self.__cpu_usage_data) // 2] + self.__cpu_usage_data[len(self.__cpu_usage_data) // 2 - 1]) / 2
        else:
            return self.__cpu_usage_data[len(self.__cpu_usage_data) // 2]
    
    def compute_median_memory(self):
        if len(self.__memory_usage_data) % 2 == 0:
            return (self.__memory_usage_data[len(self.__memory_usage_data) // 2] + self.__memory_usage_data[len(self.__memory_usage_data) // 2 - 1]) / 2
        else:
            return self.__memory_usage_data[len(self.__memory_usage_data) // 2]

    def clear_data(self):
        self.__cpu_usage_data = []
        self.__memory_usage_data = []