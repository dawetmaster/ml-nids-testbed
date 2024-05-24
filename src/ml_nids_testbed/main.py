from methods import boil_the_frog, smuggler
from enums.protocol_type import ProtocolType
from utils.log import setup_logging
from utils.cli import setup_cli_parser
import logging
import sys

setup_logging()

logger = logging.getLogger(__name__)
parser = setup_cli_parser()

if __name__ == '__main__':
    # Parse arguments from the command line
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    if args.subprogram == "boil_the_frog":
        pass
    elif args.subprogram == "mix_pcap":
        pass
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)

    logger.info("Okay")
