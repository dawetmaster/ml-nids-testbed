from scapy.all import *
import logging

logger = logging.getLogger(__name__)

class PacketSequence(object):
    def __init__(self, packets=None):
        all_packets = True
        for p in packets:
            if not isinstance(p, Packet):
                all_packets = False
                break
        if isinstance(packets, list) and all_packets:
            self.__packets = packets
        else:
            self.__packets = []
            logger.warning("No packets is in this object because the provided packet sequence is invalid or empty")
            
    def add_packet(self, packet: Packet, position: int=-1):
        if position < 0:
            self.__packets.append(packet)
        elif position >= len(self.__packets):
            raise ValueError("Invalid packet position")
        else:
            self.__packets.insert(position, packet)
    def remove_packet(self, position: int):
        if position < 0 or position >= len(self.__packets):
            raise ValueError("Invalid packet position")
        else:
            self.__packets.pop(position)
    def reset_timestamp(self):
        first_packet_timestamp = self.__packets[0].time
        for packet in self.__packets:
            packet.time = packet.time - first_packet_timestamp
    def uniformise_delay(self, delay: float=1.0):
        for i in range(1, len(self.__packets)):
            self.__packets[i].time = self.__packets[i-1].time + delay
    def scale_delays(self, delay_factor: float=1.0):
        timestamps = [p.time for p in self.__packets]
        for i in range(1, len(self.__packets)):
            self.__packets[i].time += delay_factor * (timestamps[i] - timestamps[i-1])
    def shift_delays(self, shift_constant: float=1.0):
        timestamps = [p.time for p in self.__packets]
        for i in range(1, len(self.__packets)):
            self.__packets[i].time += shift_constant + (timestamps[i] - timestamps[i-1])
        