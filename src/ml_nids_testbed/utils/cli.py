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
    subprograms = parser.add_subparsers(dest="subprogram")
    boil_the_frog_parser = subprograms.add_subparsers("boil_the_frog")
    boil_the_frog_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
    )
    mix_pcap_parser = subprograms.add_subparsers("mix_pcap")
    mix_pcap_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
    )
    mix_pcap_parser.add_argument(
        "-p",
        "--packet",
        action="append",
        dest="packet",
        help="Packet type to mix",
        choices=["TCP", "UDP", "ICMP"],
    )
    mix_pcap_parser.add_argument(
        "--pcap-file",
        action="append",
        dest="pcap_file",
        help="Pcap file to mix",
    )
    return parser
