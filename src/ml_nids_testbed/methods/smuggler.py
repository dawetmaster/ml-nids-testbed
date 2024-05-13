from scapy.all import *
from enums.protocol_type import ProtocolType
from typing import List
from utils.fabricate import *
import ipaddress
import random
import threading
import time
import secrets

logger = logging.getLogger(__name__)

def smuggle_packets(
        ip: str,
        default_port: int=80,
        primary_packet_type: ProtocolType=ProtocolType.TCP,
        many_protocol_types: bool=False,
        other_packet_type: List[ProtocolType]=[],
        smuggled_packet_type: ProtocolType=ProtocolType.HTTP,
        smuggled_packet_probability: float=0.05,
        randomise_port: bool=False,
        src_ip_range: string="127.0.0.1/32",
        rps: int=300,
        time_limit: int=60,
        url: str="/"
    ):
    primary_packet_types = []
    primary_packet_types.append(primary_packet_type)
    if many_protocol_types:
        primary_packet_types.extend(other_packet_type)
    src_ips = [str(ip) for ip in ipaddress.ip_network(src_ip_range).hosts()]
    start_time = time.time()
    print("Starting smuggle operation...")
    print(f"Primary Packet Type: {primary_packet_type}")
    print(f"Other Packet Types: {other_packet_type}")
    print(f"Smuggled Packet Type: {smuggled_packet_type}")
    print(f"Smuggled Packet Probability: {smuggled_packet_probability}")
    print(f"Randomise Port: {randomise_port}")
    print(f"Source IP Range: {src_ip_range}")
    print(f"RPS: {rps}")
    print(f"Time Limit: {time_limit}")
    threads = []
    while (time.time() - start_time < time_limit):
        for _ in range(rps):
            random_number = random.random()
            if random_number < smuggled_packet_probability:
                packet_type = smuggled_packet_type
            else:
                packet_type = random.choice(primary_packet_types)
            if randomise_port:
                port = random.randint(1024, 65535)
            else:
                port = default_port
            src_ip = random.choice(src_ips)
            logger.debug(f"Sending a {packet_type} packet to {ip}:{port} from {src_ip}")
            t = threading.Thread(target=fabricate, args=(ip, port), kwargs={"src": src_ip, "payload": secrets.token_bytes(128), "protocol_type": packet_type})
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
