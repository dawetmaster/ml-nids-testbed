from enum import Enum, auto

class ProtocolType(Enum):
    ICMP = "ICMP"
    TCP = "TCP"
    UDP = "UDP"
    RAW = "RAW"
    HTTPS = "HTTPS"
    HTTP = "HTTP"