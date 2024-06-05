import grpc
import utils.sysmon_pb2
import utils.sysmon_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:5758') as channel:
        stub = utils.sysmon_pb2_grpc.MetricsServiceStub(channel)
        response = stub.GetMetrics(utils.sysmon_pb2.Empty())
        print(f"CPU Usage: {response.cpu}%")
        print(f"Memory Usage: {response.memory}%")

if __name__ == '__main__':
    run()