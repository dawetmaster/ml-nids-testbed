from utils.packets import PacketSequence
from scapy.all import *
from utils.generate_packet import generate_tcp, generate_udp, generate_icmp
import time
import random
import secrets
import copy
import logging

KNOWN_PACKET_TYPES = ["TCP", "UDP", "ICMP"]

logger = logging.getLogger(__name__)

def generate_boil_the_frog_linear(
        src_ip: str,
        dst_ip: str,
        duration: int = 60,
        default_packet_size: int = 128,
        dst_port: int = 80,
        varying_packet_size: bool = False,
        varying_destination_ports: bool = False,
        packet_type: str = "TCP",
        tcp_flags: str = "S",
        obfuscate_packets: bool = False,
        obfuscation_probability: float = 0.05,
        initial_rps: int = 1,
        max_rps: int = 65535,
        rps_increment_per_second: float = 1,
        initial_timestamp: float = time.time(),
):
    logger.debug("Initialising packet sequence...")
    packet_seq = PacketSequence()

    logger.info("Generating packet sequence...")
    for time_in_sec in range(0, duration):
        # Determine current RPS
        current_rps = min(max_rps, round(initial_rps + (rps_increment_per_second * time_in_sec)))
        # Make packet timestamps
        packet_timestamps = [initial_timestamp + time_in_sec + (i/current_rps) for i in range(current_rps)]
        # Generate sequence numbers for TCP packets
        tcp_seq_numbers = [0 for _ in range(0, 65535)]
        # Make the packets
        # Determine packet types
        if obfuscate_packets:
            unselected_packets = copy.deepcopy(KNOWN_PACKET_TYPES)
            unselected_packets.remove(packet_type)
            packet_types = [
                random.choice(unselected_packets) if random.random() < obfuscation_probability else packet_type
                for _ in range(current_rps)
            ]
        else:
            packet_types = [packet_type for _ in range(current_rps)]
        # Make the packets
        for i in range(current_rps):
            timestamp = packet_timestamps[i]
            if varying_packet_size:
                payload = secrets.token_bytes(random.randint(0, 65000))
            else:
                payload = secrets.token_bytes(default_packet_size)
            pkt_type = packet_types[i]
            destination_port = random.randint(1, 65535) if varying_destination_ports else dst_port
            if pkt_type == "TCP":
                packet = generate_tcp(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=random.randint(1, 65535),
                    dst_port=destination_port,
                    seq=tcp_seq_numbers[destination_port],
                    flags=tcp_flags,
                    payload=payload,
                    timestamp=timestamp
                )
                tcp_seq_numbers[destination_port] += 1
                packet_seq.add_packet(packet)
            elif pkt_type == "UDP":
                packet = generate_udp(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=random.randint(1, 65535),
                    dst_port=destination_port,
                    payload=payload,
                    timestamp=timestamp
                )
                packet_seq.add_packet(packet)
            elif pkt_type == "ICMP":
                packet = generate_icmp(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=random.randint(1, 65535),
                    dst_port=destination_port,
                    payload=payload,
                    timestamp=timestamp
                )
                packet_seq.add_packet(packet)
            else:
                raise ValueError(f"Packet type {pkt_type} is not supported.")
    # Loop finished. Return the packet sequence
    logger.info("Finished generating packet sequence.")
    return packet_seq

def generate_boil_the_frog_exponential(
        src_ip: str,
        dst_ip: str,
        duration: int = 60,
        default_packet_size: int = 128,
        dst_port: int = 80,
        varying_packet_size: bool = False,
        varying_destination_ports: bool = False,
        packet_type: str = "TCP",
        tcp_flags: str = "S",
        obfuscate_packets: bool = False,
        obfuscation_probability: float = 0.05,
        initial_rps: int = 1,
        max_rps: int = 65535,
        rps_exponent_per_second: float = 1,
        initial_timestamp: float = time.time(),
):
    packet_seq = PacketSequence()
    for time_in_sec in range(0, duration):
        # Determine current RPS
        current_rps = min(max_rps, round(initial_rps * (rps_exponent_per_second ** time_in_sec)))
        # Make packet timestamps
        packet_timestamps = [initial_timestamp + time_in_sec + (i/current_rps) for i in range(current_rps)]
        # Determine packet types
        if obfuscate_packets:
            unselected_packets = copy.deepcopy(KNOWN_PACKET_TYPES)
            unselected_packets.remove(packet_type)
            packet_types = [
                random.choice(unselected_packets) if random.random() < obfuscation_probability else packet_type
                for _ in range(current_rps)
            ]
        else:
            packet_types = [packet_type for _ in range(current_rps)]
        # Make the packets
        for i in range(current_rps):
            timestamp = packet_timestamps[i]
            if varying_packet_size:
                payload = secrets.token_bytes(random.randint(0, 65000))
            else:
                payload = secrets.token_bytes(default_packet_size)
            pkt_type = packet_types[i]
            destination_port = random.randint(1, 65535) if varying_destination_ports else dst_port
            if pkt_type == "TCP":
                packet = generate_tcp(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=random.randint(1, 65535),
                    dst_port=destination_port,
                    flags=tcp_flags,
                    payload=payload,
                    timestamp=timestamp
                )
                packet_seq.add_packet(packet)
            elif pkt_type == "UDP":
                packet = generate_udp(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=random.randint(1, 65535),
                    dst_port=destination_port,
                    payload=payload,
                    timestamp=timestamp
                )
                packet_seq.add_packet(packet)
            elif pkt_type == "ICMP":
                packet = generate_icmp(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=random.randint(1, 65535),
                    dst_port=destination_port,
                    payload=payload,
                    timestamp=timestamp
                )
                packet_seq.add_packet(packet)
            else:
                raise ValueError(f"Packet type {pkt_type} is not supported.")
    # Loop finished. Return the packet sequence
    return packet_seq

def generate_boil_the_frog_sinusoidal(
        src_ip: str,
        dst_ip: str,
        duration: int = 60,
        default_packet_size: int = 128,
        dst_port: int = 80,
        varying_packet_size: bool = False,
        varying_destination_ports: bool = False,
        packet_type: str = "TCP",
        tcp_flags: str = "S",
        obfuscate_packets: bool = False,
        obfuscation_probability: float = 0.05,
        rps_amplitude: float = 300,
        rps_period: float = 3,
        rps_yshift: float = 600,
        initial_timestamp: float = time.time(),
):
    packet_seq = PacketSequence()
    for time_in_sec in range(0, duration):
        # Determine current RPS
        current_rps = max(1, round(rps_yshift + (rps_amplitude * math.sin(time_in_sec / rps_period * math.pi))))
        # Make packet timestamps
        packet_timestamps = [initial_timestamp + time_in_sec + (i/current_rps) for i in range(current_rps)]
        # Determine packet types
        if obfuscate_packets:
            unselected_packets = copy.deepcopy(KNOWN_PACKET_TYPES)
            unselected_packets.remove(packet_type)
            packet_types = [
                random.choice(unselected_packets) if random.random() < obfuscation_probability else packet_type
                for _ in range(current_rps)
            ]
        else:
            packet_types = [packet_type for _ in range(current_rps)]
        # Make the packets
        for i in range(current_rps):
            timestamp = packet_timestamps[i]
            if varying_packet_size:
                payload = secrets.token_bytes(random.randint(0, 65000))
            else:
                payload = secrets.token_bytes(default_packet_size)
            pkt_type = packet_types[i]
            destination_port = random.randint(1, 65535) if varying_destination_ports else dst_port
            if pkt_type == "TCP":
                packet = generate_tcp(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=random.randint(1, 65535),
                    dst_port=destination_port,
                    flags=tcp_flags,
                    payload=payload,
                    timestamp=timestamp
                )
                packet_seq.add_packet(packet)
            elif pkt_type == "UDP":
                packet = generate_udp(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=random.randint(1, 65535),
                    dst_port=destination_port,
                    payload=payload,
                    timestamp=timestamp
                )
                packet_seq.add_packet(packet)
            elif pkt_type == "ICMP":
                packet = generate_icmp(
                    src_ip=src_ip,
                    dst_ip=dst_ip,
                    src_port=random.randint(1, 65535),
                    dst_port=destination_port,
                    payload=payload,
                    timestamp=timestamp
                )
                packet_seq.add_packet(packet)
            else:
                raise ValueError(f"Packet type {pkt_type} is not supported.")
    # Loop finished. Return the packet sequence
    return packet_seq
