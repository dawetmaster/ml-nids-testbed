from utils.packets import PacketSequence
from scapy.all import *
from utils.generate_packet import generate_tcp, generate_udp, generate_icmp
import time
import random
import secrets
import copy

KNOWN_PACKET_TYPES = ["TCP", "UDP", "ICMP"]

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
):
    packet_seq = PacketSequence()
    initial_timestamp = time.time()
    for time_in_sec in range(0, duration):
        # Determine current RPS
        current_rps = min(max_rps, round(initial_rps + (rps_increment_per_second * time_in_sec)))
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
):
    packet_seq = PacketSequence()
    initial_timestamp = time.time()
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
        rps_yshift: float = 600
):
    packet_seq = PacketSequence()
    initial_timestamp = time.time()
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

def generate_boil_the_frog(
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
        increment_method: str = "linear", # Also supports exponential and sinusoidal wave packets
        initial_rps: int = 1,
        max_rps: int = 65535,
        rps_increment_per_second: float = 1,
        rps_exponent_per_second: float = 1,
        rps_amplitude: float = 300,
        rps_period: float = 3,
        rps_yshift: int = 100
) -> PacketSequence:
    packet_seq = PacketSequence()
    if increment_method == "linear":
        return generate_boil_the_frog_linear(
            src_ip=src_ip,
            dst_ip=dst_ip,
            dst_port=dst_port,
            duration=duration,
            default_packet_size=default_packet_size,
            varying_packet_size=varying_packet_size,
            varying_destination_ports=varying_destination_ports,
            packet_type=packet_type,
            tcp_flags=tcp_flags,
            obfuscate_packets=obfuscate_packets,
            obfuscation_probability=obfuscation_probability,
            initial_rps=initial_rps,
            max_rps=max_rps,
            rps_increment_per_second=rps_increment_per_second
        )
    elif increment_method == "exponential":
        return generate_boil_the_frog_exponential(
            src_ip=src_ip,
            dst_ip=dst_ip,
            dst_port=dst_port,
            duration=duration,
            default_packet_size=default_packet_size,
            varying_packet_size=varying_packet_size,
            varying_destination_ports=varying_destination_ports,
            packet_type=packet_type,
            tcp_flags=tcp_flags,
            obfuscate_packets=obfuscate_packets,
            obfuscation_probability=obfuscation_probability,
            initial_rps=initial_rps,
            max_rps=max_rps,
            rps_exponent_per_second=rps_exponent_per_second
        )
    elif increment_method == "sinusoidal":
        return generate_boil_the_frog_sinusoidal(
            src_ip=src_ip,
            dst_ip=dst_ip,
            dst_port=dst_port,
            duration=duration,
            default_packet_size=default_packet_size,
            varying_packet_size=varying_packet_size,
            varying_destination_ports=varying_destination_ports,
            packet_type=packet_type,
            tcp_flags=tcp_flags,
            obfuscate_packets=obfuscate_packets,
            obfuscation_probability=obfuscation_probability,
            rps_amplitude=rps_amplitude,
            rps_period=rps_period,
            rps_yshift=rps_yshift,
        )
    else:
        raise ValueError(f"Increment method {increment_method} is not supported.")

def generate_smuggler():
    pass
