import argparse

def setup_cli_parser():
    parser = argparse.ArgumentParser(
        add_help=True,
        prog="Network IDS Tester",
        description="Test suite for network IDS",
        epilog="Use it wisely!"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
    )
    return parser
