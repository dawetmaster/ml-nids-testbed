from enum import Enum, auto

class ProtocolType(Enum):
    ICMP = auto
    TCP = auto
    UDP = auto
    RAW = auto
    HTTPS = auto
    HTTP = auto