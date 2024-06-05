import argparse
import time

def setup_cli_parser():
    parser = argparse.ArgumentParser(
        add_help=True,
        prog="main.py",
        description="Test suite for network IDS",
        epilog="Use it wisely!"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        dest="test",
    )
    
    # Implement subprograms
    subprograms = parser.add_subparsers(dest="subprogram")
    
    ## Delay adjuster
    adjust_delay_parser = subprograms.add_parser("adjust_delay")
    
    ### Subprograms
    adjust_delay_subprogram = adjust_delay_parser.add_subparsers(
        dest="adjust_delay_subprogram"
    )
    
    #### Scale delay
    scale_delay_parser = adjust_delay_subprogram.add_parser("scale_by")
    scale_delay_parser.add_argument(
        'factor',
        type=float,
        help="Delay factor",
    )
    scale_delay_parser.add_argument(
        "-i",
        "--input-file",
        dest="input_file",
        required=True,
        help="Input file",
    )
    scale_delay_parser.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        required=True,
        help="Output file",
    )

    #### Shift delay
    shift_delay_parser = adjust_delay_subprogram.add_parser("shift_by")
    shift_delay_parser.add_argument(
        'constant',
        type=float,
        help="Delay shift constant",
    )
    shift_delay_parser.add_argument(
        "-i",
        "--input-file",
        required=True,
        dest="input_file",
        help="Input file",
    )
    shift_delay_parser.add_argument(
        "-o",
        "--output-file",
        required=True,
        dest="output_file",
        help="Output file",
    )

    ## Set new packet_timestamp and normalise
    normalise_timestamp_parser = subprograms.add_parser("normalise_timestamp")
    normalise_timestamp_parser.add_argument(
        "-i",
        "--input-file",
        dest="input_file",
        help="Input file",
    )
    normalise_timestamp_parser.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        help="Output file",
    )
    normalise_timestamp_parser.add_argument(
        "--new-start_timestamp",
        type=float,
        dest="new_start_timestamp",
        help="New start timestamp in UNIX notation. Default value is now.",
    )

    ## Boil the frog
    boil_the_frog_parser = subprograms.add_parser("boil_the_frog")

    ### Subprogram
    boil_the_frog_subprogram = boil_the_frog_parser.add_subparsers(
        dest="btf_subprogram",
        description="Simulate DDoS by slowly increasing RPS (like slow boil in boiling frog syndrome)"
    )

    #### Linear boil
    linear_boil = boil_the_frog_subprogram.add_parser("linear")
    linear_boil.add_argument(
        "-o",
        "--output-file",
        required=True,
        dest="output_file",
        help="Output file",
    )
    linear_boil.add_argument(
        "--src-ip",
        type=str,
        required=True,
        dest="src_ip",
        help="Source IP",
    )
    linear_boil.add_argument(
        "--dst-ip",
        type=str,
        required=True,
        dest="dst_ip",
        help="Destination IP",
    )
    linear_boil.add_argument(
        "--dst-port",
        type=int,
        default=80,
        dest="dst_port",
        help="Destination port. Default is 80.",
    )
    linear_boil.add_argument(
        "--duration",
        type=int,
        default=60,
        dest="duration",
        help="Duration",
    )
    linear_boil.add_argument(
        "--default-packet-size",
        type=int,
        default=128,
        dest="default_packet_size",
        help="Default packet size in bytes. Default is 128",
    )
    linear_boil.add_argument(
        "--varying-packet-size",
        action="store_true",
        dest="varying_packet_size",
        help="Varying packet size (content) between 0 to 65000.",
    )
    linear_boil.add_argument(
        "--varying-destination-ports",
        action="store_true",
        dest="varying_destination_ports",
        help="Varying destination ports ranging from 1 to 65535",
    )
    linear_boil.add_argument(
        "--packet-type",
        type=str,
        default="TCP",
        choices=["TCP", "UDP", "ICMP"],
        dest="packet_type",
        help="Packet type",
    )
    linear_boil.add_argument(
        "--tcp-flags",
        type=str,
        dest="tcp_flags",
        default="S",
        help="TCP flags. Options provided are 'S', 'A', and 'F', can be combined. By default, tcp_flags is S (denotes SYN)",
    )
    linear_boil.add_argument(
        "--obfuscate_packets",
        type=str,
        dest="obfuscate_packets",
        help="Choose whether to generate obfuscated packets or not.",
    )
    linear_boil.add_argument(
        "--obfuscation-probability",
        type=float,
        default=0.05,
        dest="obfuscation_probability",
        help="Obfuscation probability - Send packets not on primary type. Default value is 0.05.",
    )
    linear_boil.add_argument(
        "--initial-rps",
        type=int,
        default=1,
        dest="initial_rps",
        help="Initial RPS. Use this as starting request per second. Default value is 1.",
    )
    linear_boil.add_argument(
        "--max-rps",
        type=int,
        default=65535,
        dest="max_rps",
        help="Max RPS. Use this as the upper limit for the packet RPS. Default is 65535.",
    )
    linear_boil.add_argument(
        "--rps-increment-per-second",
        type=float,
        default=1.0,
        dest="rps_increment_per_second",
        help="RPS increment per second",
    )
    linear_boil.add_argument(
        "--initial-timestamp",
        type=float,
        default=time.time(),
        dest="initial_timestamp",
        help="Initial timestamp in UNIX notation. Default is now.",
    )

    #### Exponential boil
    exponential_boil = boil_the_frog_subprogram.add_parser("exponential")
    exponential_boil.add_argument(
        "-o",
        "--output-file",
        required=True,
        dest="output_file",
        help="Output file",
    )
    exponential_boil.add_argument(
        "--src-ip",
        type=str,
        required=True,
        dest="src_ip",
        help="Source IP",
    )
    exponential_boil.add_argument(
        "--dst-ip",
        type=str,
        required=True,
        dest="dst_ip",
        help="Destination IP",
    )
    exponential_boil.add_argument(
        "--dst-port",
        type=int,
        default=80,
        dest="dst_port",
        help="Destination port. Default is 80.",
    )
    exponential_boil.add_argument(
        "--duration",
        type=int,
        default=60,
        dest="duration",
        help="Duration",
    )
    exponential_boil.add_argument(
        "--default-packet-size",
        type=int,
        default=128,
        dest="default_packet_size",
        help="Default packet size in bytes. Default is 128",
    )
    exponential_boil.add_argument(
        "--varying-packet-size",
        action="store_true",
        dest="varying_packet_size",
        help="Varying packet size (content) between 0 to 65000.",
    )
    exponential_boil.add_argument(
        "--varying-destination-ports",
        action="store_true",
        dest="varying_destination_ports",
        help="Varying destination ports ranging from 1 to 65535",
    )
    exponential_boil.add_argument(
        "--packet-type",
        type=str,
        default="TCP",
        choices=["TCP", "UDP", "ICMP"],
        dest="packet_type",
        help="Packet type",
    )
    exponential_boil.add_argument(
        "--tcp-flags",
        type=str,
        dest="tcp_flags",
        default="S",
        help="TCP flags. Options provided are 'S', 'A', and 'F', can be combined. By default, tcp_flags is S (denotes SYN)",
    )
    exponential_boil.add_argument(
        "--obfuscate_packets",
        type=str,
        dest="obfuscate_packets",
        help="Choose whether to generate obfuscated packets or not.",
    )
    exponential_boil.add_argument(
        "--obfuscation-probability",
        type=float,
        default=0.05,
        dest="obfuscation_probability",
        help="Obfuscation probability - Send packets not on primary type. Default value is 0.05.",
    )
    exponential_boil.add_argument(
        "--initial-rps",
        type=int,
        default=1,
        dest="initial_rps",
        help="Initial RPS. Use this as starting request per second. Default value is 1.",
    )
    exponential_boil.add_argument(
        "--max-rps",
        type=int,
        default=65535,
        dest="max_rps",
        help="Max RPS. Use this as the upper limit for the packet RPS. Default is 65535.",
    )
    exponential_boil.add_argument(
        "--rps-exponent-per-second",
        type=float,
        dest="rps_exponent_per_second",
        help="RPS exponent per second",
    )
    exponential_boil.add_argument(
        "--initial-timestamp",
        type=float,
        default=time.time(),
        dest="initial_timestamp",
        help="Initial timestamp in UNIX notation. Default is now.",
    )

    #### Sinusoidal boil
    sinusoidal_boil = boil_the_frog_subprogram.add_parser("sinusoidal")
    sinusoidal_boil.add_argument(
        "-o",
        "--output-file",
        required=True,
        dest="output_file",
        help="Output file",
    )
    sinusoidal_boil.add_argument(
        "--src-ip",
        type=str,
        required=True,
        dest="src_ip",
        help="Source IP",
    )
    sinusoidal_boil.add_argument(
        "--dst-ip",
        type=str,
        required=True,
        dest="dst_ip",
        help="Destination IP",
    )
    sinusoidal_boil.add_argument(
        "--dst-port",
        type=int,
        default=80,
        dest="dst_port",
        help="Destination port. Default is 80.",
    )
    sinusoidal_boil.add_argument(
        "--duration",
        type=int,
        default=60,
        dest="duration",
        help="Duration",
    )
    sinusoidal_boil.add_argument(
        "--default-packet-size",
        type=int,
        default=128,
        dest="default_packet_size",
        help="Default packet size in bytes. Default is 128",
    )
    sinusoidal_boil.add_argument(
        "--varying-packet-size",
        action="store_true",
        dest="varying_packet_size",
        help="Varying packet size (content) between 0 to 65000.",
    )
    sinusoidal_boil.add_argument(
        "--varying-destination-ports",
        action="store_true",
        dest="varying_destination_ports",
        help="Varying destination ports ranging from 1 to 65535",
    )
    sinusoidal_boil.add_argument(
        "--packet-type",
        type=str,
        default="TCP",
        choices=["TCP", "UDP", "ICMP"],
        dest="packet_type",
        help="Packet type",
    )
    sinusoidal_boil.add_argument(
        "--tcp-flags",
        type=str,
        dest="tcp_flags",
        default="S",
        help="TCP flags. Options provided are 'S', 'A', and 'F', can be combined. By default, tcp_flags is S (denotes SYN)",
    )
    sinusoidal_boil.add_argument(
        "--obfuscate_packets",
        type=str,
        dest="obfuscate_packets",
        help="Choose whether to generate obfuscated packets or not.",
    )
    sinusoidal_boil.add_argument(
        "--obfuscation-probability",
        type=float,
        default=0.05,
        dest="obfuscation_probability",
        help="Obfuscation probability - Send packets not on primary type. Default value is 0.05.",
    )
    sinusoidal_boil.add_argument(
        "--rps-amplitude",
        type=int,
        default=100,
        dest="rps_amplitude",
        help="RPS Amplitude (farthest distance from equillibrium). Default value is 100.",
    )
    sinusoidal_boil.add_argument(
        "--rps-yshift",
        type=int,
        default=100,
        dest="rps_yshift",
        help="RPS Y-Shift (the Y-shift of the packet RPS). Default value is 100.",
    )
    sinusoidal_boil.add_argument(
        "--rps-period",
        type=float,
        default=3.0,
        dest="rps_period",
        help="Period of the RPS oscillation in seconds. Default is 3.0.",
    )
    sinusoidal_boil.add_argument(
        "--initial-timestamp",
        type=float,
        default=time.time(),
        dest="initial_timestamp",
        help="Initial timestamp in UNIX notation. Default is now.",
    )

    ## Mix PCAPs, also functions as filtering
    mix_pcap_parser = subprograms.add_parser("mix_pcap")
    mix_pcap_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
    )
    mix_pcap_parser.add_argument(
        "-i",
        "--input-file",
        action="append",
        dest="input_file",
        help="Input PCAP file(s) to mix. For more inputs, use this more than once.",
    )
    mix_pcap_parser.add_argument(
        "-o",
        "--output-file",
        required=True,
        dest="output_file",
        help="Output file",
    )
    mix_pcap_parser.add_argument(
        "-m",
        "--mixing-method",
        default="sorted",
        choices=["sorted", "random", "round_robin"],
        dest="mixing_method",
        help="PCAP mixing method. By default, mixing returns sorted timestamp.",
    )

    parser_dict = {
        "main": parser,
        "boil_the_frog": {
            "main": boil_the_frog_parser,
            "linear": linear_boil,
            "exponential": exponential_boil,
            "sinusoidal": sinusoidal_boil,
        },
        "adjust_delay": {
            "main": adjust_delay_parser,
            "scale": scale_delay_parser,
            "shift": shift_delay_parser,
        },
        "mix_pcap": {
            "main": mix_pcap_parser,
        },
        "normalise_timestamp": {
            "main": normalise_timestamp_parser,
        }
    }
    
    return parser_dict
