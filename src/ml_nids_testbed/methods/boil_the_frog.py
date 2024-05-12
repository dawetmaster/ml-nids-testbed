import math
import threading
import time
import random
import secrets

from scapy.all import *
from utils.fabricate import *

# dummy functions, to be deleted when the function has implemenented in another module
def send_tcp(ip, port, size):
    pass

def delay(seconds):
    pass

def boil_the_frog_discrete_incremental_bytes(
        ip: str, 
        port: int, 
        min_bytes: int=0, 
        max_bytes: int=65535, 
        increment_size: int=2, 
        packets_per_stage: int=100, 
        delay: int=0.1,
        src_ip: Optional[str]=None
        ):
    start_time = time.time()
    print("Starting boil the frog operation...")
    print(f"IP: {ip}")
    print(f"Port: {port}")
    print(f"Min Bytes: {min_bytes}")
    print(f"Max Bytes: {max_bytes}")
    for i in range(min_bytes, max_bytes+1, increment_size):
        for _ in range(packets_per_stage):
            print(f"Sending a packet with {i} bytes to {ip}:{port} at time {time.time() - start_time}")
            fabricate_udp(dst=ip, port=port, src=src_ip, payload=secrets.token_bytes(i))
            time.sleep(delay)

def dummy_boil_the_frog(min_bytes=0, max_bytes=1024):
    pass

def dummy_boil_the_frog_incremental(ip, port, min_bytes=0, max_bytes=1024, increment_size=2, delay=0.1, packets_per_stage=100):
    for i in range(min_bytes, max_bytes+1, increment_size):
        for _ in range(packets_per_stage):
            send_tcp(ip, port, i)
            delay(delay)

def dummy_boil_the_frog_exponential(ip, port, min_bytes=1, max_bytes=1024, factor=1.3, delay=0.1, packets_per_stage=100):
    bytes_in_packet = min_bytes
    while bytes_in_packet <= max_bytes:
        for _ in range(packets_per_stage):
            send_tcp(ip, port, bytes_in_packet)
            delay(delay)
        bytes_in_packet *= factor

def dummy_boil_the_frog_logarithmic(ip, port, min_bytes=1, max_bytes=1024, factor=1.3, delay=0.1, packets_per_stage=100):
    bytes_in_packet = min_bytes
    while bytes_in_packet <= max_bytes:
        for _ in range(packets_per_stage):
            send_tcp(ip, port, bytes_in_packet)
            delay(delay)
        bytes_in_packet = int(bytes_in_packet * factor)

def send_packet(number, bytes, time, ip, port):
    packet = IP(dst=ip) / TCP(dport=port, flags="S") / (b"A" * bytes)
    print(f"Worker number {number} with {bytes} bytes on timestamp {time}")
    send(packet)

def dummy_boil_the_frog_sinusoidal_amplitude_bytes(ip, port, median_bytes=1024, min_amplitude=256, max_amplitude=512, period=3):
    pass

def worker(number, bytes, time):
    print(f"Worker number {number} with {bytes} bytes on timestamp {time}")

if __name__ == '__main__':
    boil_the_frog_discrete_incremental_bytes("10.5.0.2", 80)
    # import threading
    # import time
    # import random
    # PERIOD=4
    # AMPLITUDE=4
    # YSHIFT=8
    # counter=0
    # start_time = time.time()
    # while True:
    #     time.sleep(0.5)
    #     requests = round(math.sin((time.time() - start_time)/PERIOD) * AMPLITUDE + YSHIFT)
    #     print(requests)
    #     for _ in range(requests):
    #         threading.Thread(target=send_packet, args=(counter, random.randint(512,2048), time.time() - start_time, "10.5.0.2", 80)).start()
    #         counter += 1