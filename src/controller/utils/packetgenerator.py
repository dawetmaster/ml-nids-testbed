from scapy.layers.inet import IP, TCP, UDP, ICMP, Packet

__ALLOWED_PACKET_TYPES = ["TCP", "UDP", "ICMP"]

class PacketGenerator(object):
    def __init__(self, packet_type: str):
        if packet_type in __ALLOWED_PACKET_TYPES:
            self.__packet_type = packet_type
        else:
            raise ValueError(f"Invalid packet type provided: {packet_type}.")
    
    def generate(
            self,
            dst_ip: str,
            dst_port: int,
            payload: bytes | None = None,
            **fields: any,
    ) -> Packet:
        if self.__packet_type == "TCP":
            return self.__generate_tcp(dst_ip, dst_port, payload, **fields)
        elif self.__packet_type == "UDP":
            return self.__generate_udp(dst_ip, dst_port, payload, **fields)
        elif self.__packet_type == "ICMP":
            return self.__generate_icmp(dst_ip, dst_port, payload, **fields)
        else:
            raise ValueError(f"Invalid packet type provided: {self.__packet_type}.")

    def __generate_tcp(
            self,
            dst_ip: str,
            dst_port: int,
            payload: bytes | None = None,
            **fields: any,
    ) -> Packet:
        ip = IP(src=fields["src_ip"], dst=dst_ip)
        tcp_fields = {x: fields[x] for x in fields if x not in ["src_ip", "src_port"]}
        tcp = TCP(sport=fields["src_port"], dport=dst_port, **tcp_fields)
        packet = ip/tcp/payload
        return packet
    
    def __generate_udp(
            self,
            dst_ip: str,
            dst_port: int,
            payload: bytes | None = None,
            **fields: any,
    ) -> Packet:
        ip = IP(src=fields["src_ip"], dst=dst_ip)
        udp_fields = {x: fields[x] for x in fields if x not in ["src_ip", "src_port"]}
        udp = UDP(sport=fields["src_port"], dport=dst_port, **udp_fields)
        packet = ip/udp/payload
        return packet
    
    def __generate_icmp(
            self,
            dst_ip: str,
            dst_port: int,
            payload: bytes | None = None,
            **fields: any,
    ) -> Packet:
        ip = IP(src=fields["src_ip"], dst=dst_ip)
        icmp_fields = {x: fields[x] for x in fields if x not in ["src_ip", "src_port"]}
        icmp = ICMP(sport=fields["src_port"], dport=dst_port, **icmp_fields)
        packet = ip/icmp/payload
        return packet
