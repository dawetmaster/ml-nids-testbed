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
        pass

    # boil_the_frog.boil_the_frog_linear_rps_constant_bytes("10.5.0.2", 80, min_rps=3000, max_rps=80000, increment_size=100)
    # smuggler.smuggle_packets(
    #     "10.5.0.2", 
    #     default_port=80,
    #     many_protocol_types=True, 
    #     other_packet_type=[ProtocolType.UDP, ProtocolType.TCP], 
    #     smuggled_packet_type=ProtocolType.HTTP, 
    #     smuggled_packet_probability=0.05, 
    #     src_ip_range="10.5.0.0/24", 
    #     rps=300, 
    #     time_limit=60
    #     )
    logger.info("Okay")
