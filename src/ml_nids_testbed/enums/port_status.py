from enum import Enum

class PortStatus(Enum):
    FILTERED = -1
    CLOSED = 0
    TCP_OPEN = 1
    UDP_OPEN = 2
    ICMP_OPEN = 3