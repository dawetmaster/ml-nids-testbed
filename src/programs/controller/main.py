import sys
import argparse
import time
import logging
import asyncio

from utils.controller.sysmonitor import SystemMonitor
from utils.controller.log import setup_logging

from utils.cli.main import setup_cli_parser

def monitor_agent(args: argparse.Namespace):
    host = args.host
    port = args.port
    monitor = SystemMonitor(f"{host}:{port}")
    start_time = time.time()
    while (time.time() - start_time <= 60):
        asyncio.run(monitor.request_resource_usage())
        time.sleep(0.5)
    print(f'Average CPU Usage: {monitor.cpu_usage_mean:.2f}%')
    print(f'Standard Deviation: {monitor.cpu_usage_stdev:.2f}')


def get_parsed_args(parser: argparse.ArgumentParser):
    return parser.parse_args()

def get_subparser_by_name(parser, name):
    for action in parser._subparsers._actions:
        if isinstance(action, argparse._SubParsersAction):
            for choice, subparser in action.choices.items():
                if choice == name:
                    return subparser
    return None

def determine_program(args: argparse.Namespace, parser: argparse.ArgumentParser):
    if len(sys.argv) == 1:
        display_help_and_exit(parser)

def display_help_and_exit(parser: argparse.ArgumentParser):
    parser.print_help(sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    parser = setup_cli_parser()
    if len(sys.argv) == 1:
        display_help_and_exit(parser)
    program_args = get_parsed_args(parser)
    if program_args.test:
        print("Arguments: %s" % program_args)
        sys.exit(0)
    if program_args.runas == "agent":
        monitor_agent(program_args)
