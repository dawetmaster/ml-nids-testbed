import argparse

def setup_runas(parser: argparse.ArgumentParser):
    subcommands = parser.add_subparsers(dest="runas")
    _setup_agent(subcommands)

def _setup_agent(subcommands: argparse._SubParsersAction):
    agent = subcommands.add_parser("agent")
    agent.add_argument("-p", "--port", type=int, default=5758)
    agent.add_argument("-H", "--host", type=str, default="127.0.0.1")
    agent.add_argument("--duration", type=int, default=0, help="Set 0 for disable autostopping")
