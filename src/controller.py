import grpc
import lib.sysmon_pb2 as sysmon__pb2
import lib.sysmon_pb2_grpc as sysmon__pb2_grpc
import sys
import argparse
import time
import logging

from utils.controller.sysmonitor import SystemMonitor
from utils.controller.log import setup_logging
from utils.cli.main import setup_cli_parser

def run():
    # setup_logging()
    # logger = logging.getLogger("controller")
    host = 'localhost'
    port = 5758
    parser = setup_cli_parser()
    args = parser.parse_args()
    print(args)
    # monitor = SystemMonitor(f"{host}:{port}")
    # start_time = time.time()
    # while (time.time() - start_time <= 60):
    #     monitor.request_resource_usage()
    #     time.sleep(0.5)
    # print(f'Average CPU Usage: {monitor.cpu_usage_mean:.2f}%')
    # print(f'Standard Deviation: {monitor.cpu_usage_stdev:.2f}')


def get_parsed_args(parser: argparse.ArgumentParser):
    return parser.parse_args()

def determine_program(args: argparse.Namespace, parser: argparse.ArgumentParser):
    if len(sys.argv) == 1:
        display_help_and_exit(parser)

def display_help_and_exit(parser: argparse.ArgumentParser):
    parser.print_help(sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    run()
