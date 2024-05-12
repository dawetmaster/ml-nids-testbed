from scapy.all import *
from typing import Optional
from enums.protocol_type import ProtocolType
import socket
import http.client

def fabricate(dst: str, port: int, payload: bytes, src: Optional[str]=None, protocol_type: ProtocolType=ProtocolType.UDP):
    match protocol_type:
        case ProtocolType.UDP:
            fabricate_udp(dst, port, payload, src)
        case ProtocolType.TCP:
            fabricate_tcp(dst, port, payload, src)
        case ProtocolType.ICMP:
            fabricate_icmp(dst, payload, src)
        case ProtocolType.HTTPS:
            fabricate_https(dst, port)
        case ProtocolType.HTTP:
            fabricate_http(dst, port)
        case ProtocolType.RAW:
            fabricate_raw(dst, payload, src)
        case _:
            raise ValueError(f"Protocol {protocol_type} is not supported.")

def fabricate_raw(dst: str, payload: bytes, src: Optional[str]=None) -> None:
    if src is None:
        host = IP(dst=dst)
    else:
        host = IP(src=src, dst=dst)
    raw_payload = Raw(load=payload)
    send(host/raw_payload)

def fabricate_tcp(dst: str, port: int, payload: bytes, src: Optional[str]=None, flags: str = "S") -> None:
    if src is None:
        host = IP(dst=dst)
    else:
        host = IP(src=src, dst=dst)
    tcp = TCP(dport=port, flags=flags)
    send(host/tcp/payload)

def fabricate_udp(dst: str, port: int, payload: bytes, src: Optional[str]=None) -> None:
    if src is None:
        host = IP(dst=dst)
    else:
        host = IP(src=src, dst=dst)
    udp = UDP(dport=port)
    send(host/udp/payload)

def fabricate_icmp(dst: str, payload: bytes, src: Optional[str]=None) -> None:
    if src is None:
        host = IP(dst=dst)
    else:
        host = IP(src=src, dst=dst)
    icmp = ICMP()
    send(host/icmp/payload)

def fabricate_https(dst: str, port: int=443, method: str="GET", uri: str="/") -> None:
    connection = http.client.HTTPSConnection(dst, port)
    connection.request(method, uri)
    response = connection.getresponse()
    print(response.read())

def fabricate_http(dst: str, port: int=80, method: str="GET", uri: str="/") -> None:
    connection = http.client.HTTPConnection(dst, port)
    connection.request(method, uri)
    response = connection.getresponse()
    print(response.read())
    
    