import psutil
import utils.sysmon_pb2
import utils.sysmon_pb2_grpc
import grpc
import time
import logging

logger = logging.getLogger(__name__)

from concurrent import futures

class SystemMonitor(utils.sysmon_pb2_grpc.MetricsServiceServicer):
    def GetMetrics(self, request, context):
        cpu_usage = psutil.cpu_percent(interval=1)
        
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        
        logger.info(f"CPU: {cpu_usage}%, MEM: {memory_usage}%")
        return utils.sysmon_pb2.Metrics(cpu=cpu_usage, memory=memory_usage)
    
    def GetHeartbeat(self, request, context):
        return utils.sysmon_pb2.Metrics(status="OK")
    
def create_server(port:int=5758):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    utils.sysmon_pb2_grpc.add_MetricsServiceServicer_to_server(SystemMonitor(), server)
    if isinstance(port, int) and port <= 65535 and port >= 1024:
        server.add_insecure_port(f'[::]:{port}')
    else:
        raise ValueError("Port must be a number ranging from 1024 to 65535. Your provided port was %s" % port)
    return server