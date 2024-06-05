from scapy.layers.inet import IP, TCP, UDP, ICMP
import time
import logging

logger = logging.getLogger(__name__)

def generate_tcp(
        src_ip: str,
        dst_ip: str,
        src_port: int,
        dst_port: int,
        payload: bytes,
        flags: str,
        seq: int=None,
        timestamp: float = time.time(),
):
    ip = IP(src=src_ip, dst=dst_ip)
    tcp = TCP(sport=src_port, dport=dst_port, flags=flags, seq=seq)
    packet = ip/tcp/payload
    if isinstance(timestamp, float):
        packet.time = timestamp
    else:
        logger.warning(f"Invalid timestamp provided: {timestamp}. Using default timestamp (now).")
        packet.time = time.time()
    return packet

def generate_udp(
        src_ip: str,
        dst_ip: str,
        src_port: int,
        dst_port: int,
        payload: bytes,
        timestamp: float = time.time(),
):
    ip = IP(src=src_ip, dst=dst_ip)
    udp = UDP(sport=src_port, dport=dst_port)
    packet = ip/udp/payload
    if isinstance(timestamp, float):
        packet.time = timestamp
    else:
        logger.warning(f"Invalid timestamp provided: {timestamp}. Using default timestamp (now).")
        packet.time = time.time()
    return packet

def generate_icmp(
        src_ip: str,
        dst_ip: str,
        payload: bytes,
        timestamp: float = time.time(),
):
    ip = IP(src=src_ip, dst=dst_ip)
    icmp = ICMP()
    packet = ip/icmp/payload
    if isinstance(timestamp, float):
        packet.time = timestamp
    else:
        logger.warning(f"Invalid timestamp provided: {timestamp}. Using default timestamp (now).")
        packet.time = time.time()
    return packet
