import argparse

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
        type=int,
        help="Delay factor",
    )
    scale_delay_parser.add_argument(
        "-i",
        "--input-file",
        dest="input_file",
        help="Input file",
    )
    scale_delay_parser.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        help="Output file",
    )
    scale_delay_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="delay",
        help="Debug mode",
    )

    #### Shift delay
    shift_delay_parser = adjust_delay_subprogram.add_parser("shift_by")
    shift_delay_parser.add_argument(
        'constant',
        type=int,
        help="Delay shift constant",
    )
    shift_delay_parser.add_argument(
        "-i",
        "--input-file",
        dest="input_file",
        help="Input file",
    )
    shift_delay_parser.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        help="Output file",
    )
    shift_delay_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="delay",
        help="Debug mode",
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
        "-d",
        "--debug",
        action="store_true",
        dest="delay",
        help="Debug mode",
    )
    normalise_timestamp_parser.add_argument(
        "--new-start_timestamp",
        type=float,
        dest="new_start_timestamp",
        help="New start timestamp",
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
        dest="output_file",
        help="Output file",
    )
    linear_boil.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="debug",
    )
    linear_boil.add_argument(
        "--src-ip",
        type=str,
        dest="src_ip",
        help="Source IP",
    )
    linear_boil.add_argument(
        "--dst-ip",
        type=str,
        dest="dst_ip",
        help="Destination IP",
    )
    linear_boil.add_argument(
        "--dst-port",
        type=int,
        dest="dst_port",
        help="Destination port",
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
        default=80,
        dest="default_packet_size",
        help="Default packet size in bytes",
    )
    linear_boil.add_argument(
        "--varying-packet-size",
        action="store_true",
        dest="varying_packet_size",
        help="Varying packet size",
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
        help="Obfuscate packets",
    )
    linear_boil.add_argument(
        "--obfuscation-probability",
        type=float,
        default=0.05,
        dest="obfuscation_probability",
        help="Obfuscation probability",
    )
    linear_boil.add_argument(
        "--initial-rps",
        type=int,
        default=1,
        dest="initial_rps",
        help="Initial RPS",
    )
    linear_boil.add_argument(
        "--max-rps",
        type=int,
        default=65535,
        dest="max_rps",
        help="Max RPS",
    )
    linear_boil.add_argument(
        "--rps-increment-per-second",
        type=float,
        default=1.0,
        dest="rps_increment_per_second",
        help="RPS increment per second",
    )

    #### Exponential boil
    exponential_boil = boil_the_frog_subprogram.add_parser("exponential")
    exponential_boil.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        help="Output file",
    )
    exponential_boil.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="debug",
    )
    exponential_boil.add_argument(
        "--src-ip",
        type=str,
        dest="src_ip",
        help="Source IP",
    )
    exponential_boil.add_argument(
        "--dst-ip",
        type=str,
        dest="dst_ip",
        help="Destination IP",
    )
    exponential_boil.add_argument(
        "--dst-port",
        type=int,
        dest="dst_port",
        help="Destination port",
    )
    exponential_boil.add_argument(
        "--duration",
        type=int,
        dest="duration",
        help="Duration",
    )
    exponential_boil.add_argument(
        "--default-packet-size",
        type=int,
        dest="default_packet_size",
        help="Default packet size in bytes",
    )
    exponential_boil.add_argument(
        "--varying-packet-size",
        action="store_true",
        dest="varying_packet_size",
        help="Varying packet size",
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
        dest="packet_type",
        help="Packet type",
    )
    exponential_boil.add_argument(
        "--tcp-flags",
        type=str,
        dest="tcp_flags",
        help="TCP flags. Options provided are 'S', 'A', and 'F', can be combined. By default, tcp_flags is S (denotes SYN)",
    )
    exponential_boil.add_argument(
        "--obfuscate_packets",
        type=str,
        dest="obfuscate_packets",
        help="Obfuscate packets",
    )
    exponential_boil.add_argument(
        "--obfuscation-probability",
        type=float,
        dest="obfuscation_probability",
        help="Obfuscation probability",
    )
    exponential_boil.add_argument(
        "--initial-rps",
        type=int,
        dest="initial_rps",
        help="Initial RPS",
    )
    exponential_boil.add_argument(
        "--max-rps",
        type=int,
        dest="max_rps",
        help="Max RPS",
    )
    exponential_boil.add_argument(
        "--rps-exponent-per-second",
        type=float,
        dest="rps_exponent_per_second",
        help="RPS exponent per second",
    )

    #### Sinusoidal boil
    sinusoidal_boil = boil_the_frog_subprogram.add_parser("sinusoidal")
    sinusoidal_boil.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        help="Output file",
    )
    sinusoidal_boil.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="debug",
    )
    sinusoidal_boil.add_argument(
        "--src-ip",
        type=str,
        dest="src_ip",
        help="Source IP",
    )
    sinusoidal_boil.add_argument(
        "--dst-ip",
        type=str,
        dest="dst_ip",
        help="Destination IP",
    )
    sinusoidal_boil.add_argument(
        "--dst-port",
        type=int,
        dest="dst_port",
        help="Destination port",
    )
    sinusoidal_boil.add_argument(
        "--duration",
        type=int,
        dest="duration",
        help="Duration",
    )
    sinusoidal_boil.add_argument(
        "--default-packet-size",
        type=int,
        dest="default_packet_size",
        help="Default packet size in bytes",
    )
    sinusoidal_boil.add_argument(
        "--varying-packet-size",
        action="store_true",
        dest="varying_packet_size",
        help="Varying packet size",
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
        dest="packet_type",
        help="Packet type",
    )
    sinusoidal_boil.add_argument(
        "--tcp-flags",
        type=str,
        dest="tcp_flags",
        help="TCP flags. Options provided are 'S', 'A', and 'F', can be combined. By default, tcp_flags is S (denotes SYN)",
    )
    sinusoidal_boil.add_argument(
        "--obfuscate_packets",
        type=str,
        dest="obfuscate_packets",
        help="Obfuscate packets",
    )
    sinusoidal_boil.add_argument(
        "--obfuscation-probability",
        type=float,
        dest="obfuscation_probability",
        help="Obfuscation probability",
    )
    sinusoidal_boil.add_argument(
        "--rps-amplitude",
        type=int,
        dest="rps_amplitude",
        help="RPS Amplitude (farthest distance from equillibrium)",
    )
    sinusoidal_boil.add_argument(
        "--rps-yshift",
        type=int,
        dest="rps_yshift",
        help="RPS Y-Shift (the Y-shift of the packet RPS)",
    )
    sinusoidal_boil.add_argument(
        "--rps-period",
        type=float,
        dest="rps_period",
        help="Period of the RPS oscillation",
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
    mix_pcap_parser.add_argument(
        "--src-ip",
        type=str,
        action="append",
        dest="src_ip",
        help="Source IP",
    )
    mix_pcap_parser.add_argument(
        "--dst-ip",
        type=str,
        action="append",
        dest="dst_ip",
        help="Destination IP",
    )
    mix_pcap_parser.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        help="Output file",
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
