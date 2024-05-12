from scapy.all import *
from typing import Optional
import socket

def fabricate_tcp(dst: str, port: int, src: Optional[str]=None, payload: str="", flags: str = "S") -> None:
    if src is None:
        host = IP(dst=dst)
    else:
        host = IP(src=src, dst=dst)
    tcp = TCP(dport=port, flags=flags)
    send(host/udp/payload.encode('utf-8'))

def fabricate_udp(dst: str, port: int, src: Optional[str]=None, payload: str="") -> None:
    if src is None:
        host = IP(dst=dst)
    else:
        host = IP(src=src, dst=dst)
    udp = UDP(dport=port)
    send(host/udp/payload.encode('utf-8'))

def fabricate_http(dst: str, payload: bytes, port: int=80) -> None:
    if 'HTTP' not in [layer.name for layer in conf.layer]:
        load_layer("http")
    
    