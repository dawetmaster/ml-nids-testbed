from argparse import ArgumentParser
from utils.log import setup_logging
from utils.cli import setup_cli_parser
from utils.generate_pcap import generate_boil_the_frog_linear, generate_boil_the_frog_exponential, generate_boil_the_frog_sinusoidal
from utils.pcap import PCAPHandler
from utils.mix_pcap import mix_pcap
import logging
import sys


setup_logging()

logger = logging.getLogger(__name__)
parser_dict = setup_cli_parser()
parser = parser_dict["main"]

def display_help_and_exit(parser: ArgumentParser):
    parser.print_help(sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    # Parse arguments from the command line
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        display_help_and_exit(parser)
    if args.test:
        logger.info("Running in test mode")
        print(args)
        sys.exit(0)
    
    if args.subprogram == "boil_the_frog":
        if len(sys.argv) == 2:
            display_help_and_exit(parser_dict["boil_the_frog"]["main"])
        if args.btf_subprogram == "linear":
            logger.info("Running linear boil-the-frog traffic generator")
            ps = generate_boil_the_frog_linear(
                src_ip=args.src_ip,
                dst_ip=args.dst_ip,
                duration=args.duration,
                default_packet_size=args.default_packet_size,
                varying_packet_size=args.varying_packet_size,
                varying_destination_ports=args.varying_destination_ports,
                packet_type=args.packet_type,
                tcp_flags=args.tcp_flags,
                obfuscate_packets=args.obfuscate_packets,
                obfuscation_probability=args.obfuscation_probability,
                initial_rps=args.initial_rps,
                max_rps=args.max_rps,
                rps_increment_per_second=args.rps_increment_per_second,
                initial_timestamp=args.initial_timestamp,
            )
            logger.info("Handling PCAP writing...")
            ph = PCAPHandler(args.output_file)
            ph.write_from_packet(ps.get_packet_sequence())
        elif args.btf_subprogram == "exponential":
            logger.info("Running exponential boil-the-frog traffic generator")
            ps = generate_boil_the_frog_exponential(
                src_ip=args.src_ip,
                dst_ip=args.dst_ip,
                duration=args.duration,
                default_packet_size=args.default_packet_size,
                varying_packet_size=args.varying_packet_size,
                varying_destination_ports=args.varying_destination_ports,
                packet_type=args.packet_type,
                tcp_flags=args.tcp_flags,
                obfuscate_packets=args.obfuscate_packets,
                obfuscation_probability=args.obfuscation_probability,
                initial_rps=args.initial_rps,
                max_rps=args.max_rps,
                rps_exponent_per_second=args.rps_increment_per_second,
                initial_timestamp=args.initial_timestamp,
            )
            logger.info("Handling PCAP writing...")
            ph = PCAPHandler(args.output_file)
            ph.write_from_packet(ps.get_packet_sequence())
        elif args.btf_subprogram == "sinusoidal":
            logger.info("Running sinusoidal boil-the-frog traffic generator")
            ps = generate_boil_the_frog_sinusoidal(
                src_ip=args.src_ip,
                dst_ip=args.dst_ip,
                duration=args.duration,
                default_packet_size=args.default_packet_size,
                varying_packet_size=args.varying_packet_size,
                varying_destination_ports=args.varying_destination_ports,
                packet_type=args.packet_type,
                tcp_flags=args.tcp_flags,
                obfuscate_packets=args.obfuscate_packets,
                obfuscation_probability=args.obfuscation_probability,
                rps_amplitude=args.rps_amplitude,
                rps_period=args.rps_period,
                rps_yshift=args.rps_yshift,
                initial_timestamp=args.initial_timestamp,
            )
            logger.info("Handling PCAP writing...")
            ph = PCAPHandler(args.output_file)
            ph.write_from_packet(ps.get_packet_sequence())
        else:
            parser_dict["boil_the_frog"]["main"].print_help(sys.stderr)
            sys.exit(1)
    elif args.subprogram == "mix_pcap":
        if len(sys.argv) == 2:
            display_help_and_exit(parser_dict["mix_pcap"]["main"])
        if args.input_file is None:
            parser_dict["mix_pcap"]["main"].print_help(sys.stderr)
            logger.error("No input file specified. Please specify at least one PCAP file.")
            sys.exit(1)
        logger.debug("Starting pcap handlers")
        pcap_handlers = [PCAPHandler(ipath) for ipath in args.input_file]
        output_pcap_handler = PCAPHandler(args.output_file)
        logger.info("Handling PCAP mixing...")
        mix_pcap(pcap_handlers, output_pcap_handler, args.mixing_method)
    elif args.subprogram == "normalise_timestamp":
        if len(sys.argv) == 2:
            display_help_and_exit(parser_dict["normalise_timestamp"]["main"])
    elif args.subprogram == "adjust_delay":
        if len(sys.argv) == 2:
            display_help_and_exit(parser_dict["adjust_delay"]["main"])
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)
