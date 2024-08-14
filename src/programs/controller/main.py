import sys
import argparse
import time
import logging
import requests
import json
import numpy as np

from threading import Thread
from pathlib import Path

from utils.controller.sysmonitor import SystemMonitor
from utils.controller.log import setup_logging

from utils.cli.main import setup_cli_parser

from utils.controller.signal import skip_on_signal

def monitor_agent(args: argparse.Namespace):
    logger = logging.getLogger('monitor_agent')
    host = args.host
    port = args.port
    duration = args.duration
    monitor = SystemMonitor(f"{host}:{port}")
    
    logger.info(f"Monitoring agent at {host}:{port} with autostop duration of {duration} seconds.")

    start_time = time.time()

    threads = []

    if duration > 0:
        while (time.time() - start_time <= duration):
            thread = Thread(target=monitor.request_resource_usage)
            threads.append(thread)
            thread.start()
            time.sleep(0.5)
    elif duration < 0:
        # Handle negative duration by raising an exception
        raise ValueError("Duration cannot be negative")
    else: # duration = 0
        with skip_on_signal():
            while True:
                thread = Thread(target=monitor.request_resource_usage)
                threads.append(thread)
                thread.start()
                time.sleep(0.5)
    
    # Wait until all threads have finished
    for thread in threads:
        thread.join()

    logger.info("Monitoring agent stopped.")

    print("Monitoring stopped.")

    monitor.finish_monitoring()
    monitor.process_final_stats()

    logger.info("Requesting detection reports from agent.")

    time.sleep(2)

    reports = requests.get(f"http://{host}:{port}/reports", timeout=10)
    if reports.status_code != 200:
        logger.error(f"Failed to receive detection reports: {reports.status_code}")
    else:
        logger.info("Received detection reports successfully")
        overall_recap = reports.json()["ml_data"]

        # Get the data series
        ntp_run_durations = np.array([entry["run_duration_ntp"] for entry in overall_recap], dtype=float)
        cpu_run_durations = np.array([entry["run_duration"] for entry in overall_recap], dtype=float)

        overall_result = [entry["result"] for entry in overall_recap]
        number_of_flows = np.array([entry["number_of_flows"] for entry in overall_result], dtype=float)

        tp_data = np.array([entry["tp"] for entry in overall_result], dtype=float)
        tn_data = np.array([entry["tn"] for entry in overall_result], dtype=float)
        fp_data = np.array([entry["fp"] for entry in overall_result], dtype=float)
        fn_data = np.array([entry["fn"] for entry in overall_result], dtype=float)

        flow_duration_mean_data = np.array([r["flow_duration_mean"] for r in overall_result], dtype=float)
        flow_duration_std_data = np.array([r["flow_duration_std"] for r in overall_result], dtype=float)

        # Calculate the stats
        ntp_run_duration_avg = np.nanmean(ntp_run_durations)
        ntp_run_duration_std = np.nanstd(ntp_run_durations)
        cpu_run_duration_avg = np.nanmean(cpu_run_durations)
        cpu_run_duration_std = np.nanstd(cpu_run_durations)

        total_flows = np.sum(number_of_flows, dtype=int)
        overall_tp = np.sum(tp_data, dtype=int)
        overall_tn = np.sum(tn_data, dtype=int)
        overall_fp = np.sum(fp_data, dtype=int)
        overall_fn = np.sum(fn_data, dtype=int)

        overall_accuracy = (overall_tp + overall_tn) / total_flows
        overall_precision = overall_tp / (overall_tp + overall_fp) if (overall_tp + overall_fp) > 0 else 0
        overall_recall = overall_tp / (overall_tp + overall_fn) if (overall_tp + overall_fn) > 0 else 0
        
        overall_flow_duration_mean = np.average(np.fromiter((qty * group_mean for qty, group_mean in zip(number_of_flows, flow_duration_mean_data)), dtype=float))
        __overall_flow_duration_var = np.sum(
            np.fromiter(
                ((qty-1) * group_std**2 for qty, group_std in zip(number_of_flows, flow_duration_std_data))
            , dtype=float)
        ) / np.sum(
            np.fromiter(
                ((qty-1) for qty in number_of_flows)
            , dtype=int)
        )
        print(__overall_flow_duration_var)
        overall_flow_duration_std = np.sqrt(__overall_flow_duration_var)
    
    final_report_strings = []
    final_report_strings.append(
        """========================================
            MONITORING RESULTS
========================================"""
    )
    final_report_strings.append(
        f"""
Total monitoring time: {time.time() - start_time:.2f} seconds

Average CPU Usage: {monitor.cpu_usage_mean:.2f}%
CPU Usage Standard Deviation: {monitor.cpu_usage_stdev:.2f}
Top 1% CPU Usage: {monitor.cpu_usage_top_1_percent:.2f}%
Median CPU Usage: {monitor.cpu_usage_median:.2f}

Average Memory Usage: {monitor.memory_usage_mean:.2f}%
Memory Usage Standard Deviation: {monitor.memory_usage_stdev:.2f}
Top 1% Memory Usage: {monitor.memory_usage_top_1_percent:.2f}%
Median Memory Usage: {monitor.memory_usage_median:.2f}%
"""
    )
    if reports.status_code == 200:
        final_report_strings.append(f"""
Average NTP-based runtime time-to-detect: {ntp_run_duration_avg}
Average CPU-based runtime time-to-detect: {cpu_run_duration_avg}
Standard deviation of NTP-based runtime time-to-detect: {ntp_run_duration_std}
Standard deviation of CPU-based runtime time-to-detect: {cpu_run_duration_std}
Total flows analyzed: {total_flows}
Overall accuracy: {overall_accuracy}
Overall precision: {overall_precision}
Overall recall: {overall_recall}
Overall flow duration average: {overall_flow_duration_mean}
Overall flow duration standard deviation: {overall_flow_duration_std}
"""
    )
    else:
        final_report_strings.append(
            f"Failed to receive detection reports with status code {reports.status_code}, so the report summary will not provide further details."
        )

    Path("./reports").resolve().mkdir(exist_ok=True)
    Path("./reports/report.txt").resolve().touch(exist_ok=True)
    with open(Path("./reports/report.txt"), "w") as f:
        for line in final_report_strings:
            f.write(line + "\n")
    
    for line in final_report_strings:
        print(line)
    

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
    setup_logging()
    if program_args.runas == "agent":
        monitor_agent(program_args)
