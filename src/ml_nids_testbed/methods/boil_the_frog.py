import math
import threading
import time
import random
import secrets

from scapy.all import *
from utils.fabricate import *
from enums.protocol_type import ProtocolType

def boil_the_frog_discrete_incremental_bytes(
        ip: str, 
        port: int, 
        min_bytes: int=0, 
        max_bytes: int=65535, 
        increment_size: int=2, 
        packets_per_stage: int=100, 
        delay: float=0.1,
        src_ip: Optional[str]=None,
        protocol_type: ProtocolType=ProtocolType.UDP
        ):
    start_time = time.time()
    print("Starting boil the frog operation...")
    print(f"IP: {ip}")
    print(f"Port: {port}")
    print(f"Min Bytes: {min_bytes}")
    print(f"Max Bytes: {max_bytes}")
    for i in range(min_bytes, max_bytes+1, increment_size):
        for _ in range(packets_per_stage):
            print(f"Sending a packebytes_in_packet *= exponent_factort with {i} bytes to {ip}:{port} at time {time.time() - start_time}")
            fabricate(dst=ip, port=port, src=src_ip, payload=secrets.token_bytes(i), protocol_type=protocol_type)
            time.sleep(delay)

def boil_the_frog_linear_bytes(
        ip: str, 
        port: int, 
        min_bytes: int=0, 
        max_bytes: int=65535,  
        delay: float=0.1,
        src_ip: Optional[str]=None,
        protocol_type: ProtocolType=ProtocolType.UDP
        ):
    start_time = time.time()
    print("Starting boil the frog operation...")
    print(f"IP: {ip}")
    print(f"Port: {port}")
    print(f"Min Bytes: {min_bytes}")
    print(f"Max Bytes: {max_bytes}")
    for i in range(min_bytes, max_bytes+1):
        print(f"Sending a packet with {i} bytes to {ip}:{port} at time {time.time() - start_time}")
        fabricate(dst=ip, port=port, src=src_ip, payload=secrets.token_bytes(i), protocol_type=protocol_type)
        time.sleep(delay)

def boil_the_frog_exponential_bytes(
        ip: str, 
        port: int, 
        min_bytes: int=1, 
        max_bytes: int=65535,  
        exponent_factor: float=1.5,
        packets_per_stage: int=100, 
        delay: float=0.1,
        src_ip: Optional[str]=None,
        protocol_type: ProtocolType=ProtocolType.UDP
        ):
    start_time = time.time()
    print("Starting boil the frog operation...")
    print(f"IP: {ip}")
    print(f"Port: {port}")
    print(f"Min Bytes: {min_bytes}")
    print(f"Max Bytes: {max_bytes}")
    bytes_in_packet = min_bytes
    while bytes_in_packet <= max_bytes:
        rounded_packet_size = round(bytes_in_packet)
        for _ in range(packets_per_stage):
            print(f"Sending a packet with {rounded_packet_size} bytes to {ip}:{port} at time {time.time() - start_time}")
            fabricate(dst=ip, port=port, src=src_ip, payload=secrets.token_bytes(rounded_packet_size), protocol_type=protocol_type)
            time.sleep(delay)
        bytes_in_packet *= exponent_factor

def boil_the_frog_logarithmic_bytes(
        ip: str, 
        port: int, 
        min_bytes: int=100, 
        max_bytes: int=65535,  
        increment_threshold: int=5,
        packets_per_stage: int=100, 
        delay: float=0.1,
        src_ip: Optional[str]=None,
        protocol_type: ProtocolType=ProtocolType.UDP
        ):
    start_time = time.time()
    print("Starting boil the frog operation...")
    print(f"IP: {ip}")
    print(f"Port: {port}")
    print(f"Min Bytes: {min_bytes}")
    print(f"Max Bytes: {max_bytes}")
    bytes_in_packet = min_bytes
    reciproc_factor = 2
    while bytes_in_packet <= max_bytes:
        rounded_packet_size = round(bytes_in_packet)
        for _ in range(packets_per_stage):
            print(f"Sending a packet with {rounded_packet_size} bytes to {ip}:{port} at time {time.time() - start_time}")
            fabricate(dst=ip, port=port, src=src_ip, payload=secrets.token_bytes(rounded_packet_size), protocol_type=protocol_type)
            time.sleep(delay)
        # Simulate logarithmic growth
        increment_bytes = round(min_bytes / reciproc_factor)
        if increment_bytes >= increment_threshold:
            bytes_in_packet += increment_bytes
            reciproc_factor += 1
        else:
            print(f"No significant increment: Increment is below threshold ({increment_threshold})")
            break

def boil_the_frog_sinusoidal_bytes(
        ip: str, 
        port: int, 
        amplitude: int=100, 
        yshift: int=2000,  
        period: float=3,
        max_time_seconds: float=60,
        delay: float=0.1,
        src_ip: Optional[str]=None,
        protocol_type: ProtocolType=ProtocolType.UDP
        ):
    start_time = time.time()
    print("Starting boil the frog operation...")
    print(f"IP: {ip}")
    print(f"Port: {port}")
    print(f"Amplitude: {amplitude}")
    print(f"Y-Shift: {yshift}")
    print(f"Period: {period}")
    while time.time() - start_time <= max_time_seconds:
        current_time = time.time() - start_time
        rounded_packet_size = round(yshift + math.sin(current_time / period) * amplitude)
        print(f"Sending a packet with {rounded_packet_size} bytes to {ip}:{port} at time {time.time() - start_time}")
        fabricate(dst=ip, port=port, src=src_ip, payload=secrets.token_bytes(rounded_packet_size), protocol_type=protocol_type)
        time.sleep(delay)

def boil_the_frog_discrete_incremental_rps_constant_bytes(
        ip: str, 
        port: int, 
        min_rps: int=1, 
        max_rps: int=65535,
        bytes: int=128, 
        increment_size: int=2, 
        attempts_per_stage: int=100, 
        src_ip: Optional[str]=None,
        protocol_type: ProtocolType=ProtocolType.UDP
        ):
    start_time = time.time()
    print("Starting boil the frog operation...")
    print(f"IP: {ip}")
    print(f"Port: {port}")
    print(f"Min RPS: {min_rps}")
    print(f"Max RPS: {max_rps}")
    threads = []
    for rps in range(min_rps, max_rps+1, increment_size):
        for j in range(attempts_per_stage):
            print(f"Attempt {j} to send {rps} packets per second.")
            for _ in range(rps):
                print(f"Sending a packet with {bytes} bytes to {ip}:{port} at time {time.time() - start_time}")
                t = threading.Thread(target=fabricate, args=(ip, port), kwargs={"src": src_ip, "payload": secrets.token_bytes(bytes), "protocol_type": protocol_type})
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            time.sleep(1)

def boil_the_frog_linear_rps_constant_bytes(
        ip: str, 
        port: int, 
        min_rps: int=1, 
        max_rps: int=65535, 
        bytes: int=128, 
        increment_size: int=2, 
        src_ip: Optional[str]=None,
        protocol_type: ProtocolType=ProtocolType.HTTP
        ):
    start_time = time.time()
    print("Starting boil the frog operation...")
    print(f"IP: {ip}")
    print(f"Port: {port}")
    print(f"Min RPS: {min_rps}")
    print(f"Max RPS: {max_rps}")
    threads = []
    for rps in range(min_rps, max_rps+1, increment_size):
        for _ in range(rps):
            print(f"Sending a packet with {bytes} bytes to {ip}:{port} at time {time.time() - start_time}")
            t = threading.Thread(target=fabricate, args=(ip, port), kwargs={"src": src_ip, "payload": secrets.token_bytes(bytes), "protocol_type": protocol_type})
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        time.sleep(1)

