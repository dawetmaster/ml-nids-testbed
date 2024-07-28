from fastapi import FastAPI
from argparse import ArgumentParser
from pathlib import Path
import psutil
import json
import os

app = FastAPI()

@app.get("/usage")
def get_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    return {"cpu_usage": cpu_usage, "memory_usage": memory_usage}

@app.get("/reports")
def get_reports():
    if report_file is None:
        return {"error": "No report file specified"}
    try:
        rf_path = Path(report_file).resolve()
        with open(rf_path) as f:
            report = json.load(f)
        return report
    except Exception as e:
        return {"error": f"Error reading report file: {str(e)}"}

def parse_cli_args():
    pass

def cli_parser():
    parser = ArgumentParser(description="IDS Testbed Agent for IDSes")
    parser.add_argument("--port", type=int, default=5758)
    parser.add_argument("--report_file", type=str, default=None)
    return parser

if __name__ == "__main__":
    import uvicorn
    parser = cli_parser()
    program_args = parser.parse_args()
    report_file = program_args.report_file
    uvicorn.run(app, host="0.0.0.0", port=program_args.port)