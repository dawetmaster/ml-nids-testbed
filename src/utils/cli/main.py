import argparse
from utils.cli.runas import setup_runas

def setup_cli_parser():
    parser = argparse.ArgumentParser(
        add_help=True,
        prog="main.py",
        description="Test suite for network IDS",
        epilog="Use it wisely!"
    )
    parser.add_argument(
        "-t",
        "--test_args",
        action="store_true",
        dest="test",
    )
    setup_runas(parser)

    return parser