from scapy.layers.inet import IP, TCP, ICMP, Packet, sr1
from enums.port_status import PortStatus
import threading
from typing import Tuple

def scan_tcp_port(dst_ip: str, dst_port: int) -> Tuple[str, int, int]:
    # 0 means port closed, 1 means port open, -1 means port obfuscated
    destination_ip = IP(dst=dst_ip)
    destination_port = TCP(port=dst_port, flags="S") # denotes a SYN
    packet: Packet = destination_ip / destination_port
    response = sr1(packet, timeout=3, verbose=0)
    if response is None:
        return (dst_ip, dst_port, -1)
    elif response.haslayer(ICMP):
        return (dst_ip, dst_port, 0)

def scan_ports(dst_ip: str, ports: list=[i for i in range(65536)]):
    pass
