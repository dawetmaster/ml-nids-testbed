from scapy.all import *
import logging
import heapq
import random

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
        if delay_factor <= 0.0:
            raise ValueError("Invalid delay factor. Delay factor must be positive")
        timestamps = [p.time for p in self.__packets]
        for i in range(1, len(self.__packets)):
            self.__packets[i].time += delay_factor * (timestamps[i] - timestamps[i-1])
    def shift_delays(self, shift_constant: float=1.0):
        delays = (self.__packets[i] - self.__packets[i-1] for i in range(1, len(self.__packets)))
        if shift_constant < min(delays):
            raise ValueError("Invalid shift constant. Shift constant must be greater than or equal to the minimum delay")
        timestamps = [p.time for p in self.__packets]
        for i in range(1, len(self.__packets)):
            self.__packets[i].time += shift_constant + (timestamps[i] - timestamps[i-1])

    def mix_packets(self, *packet_sequences: PacketSequence, method=None):
        if method is None: 
            raise ValueError("No mixing method specified")
        if method == "sorted":
            heap_queue = []
            for seq_index, seq in enumerate(packet_sequences):
                if seq:
                    # Insert the first packet of each sequence
                    heapq.heappush(heap_queue, 
                                   (seq[0].time, # First packet timestamp
                                    seq_index, # Index of the provided packet sequence
                                    0, 
                                    seq[0] # The first packet itself
                                    )
                                   )
            while len(heap_queue) > 0:
                _, seq_index, packet_index, packet = heapq.heappop(heap_queue)
                self.__packets.append(packet)
                # Check if still more elements. IF yes, insert to the queue
                if packet_index + 1 < len(packet_sequences[seq_index]):
                    heapq.heappush(heap_queue, (packet_sequences[seq_index][packet_index+1].time, seq_index, packet_index+1, packet_sequences[seq_index][packet_index+1]))
        elif method == "random":
            number_of_sequences = len(packet_sequences)
            all_sequences_exhausted = False
            seq_indices = [0 for _ in packet_sequences]
            non_exhausted_sequences = [i for i in range(number_of_sequences) if seq_indices[i] < len(packet_sequences[i])]
            while len(non_exhausted_sequences) > 0 : # Means that not all sequencesences exhausted
                random_seq_index = random.choice(non_exhausted_sequences)
                self.__packets.append(packet_sequences[random_seq_index][seq_indices[random_seq_index]])
                seq_indices[random_seq_index] += 1
                if seq_indices[random_seq_index] >= len(packet_sequences[random_seq_index]):
                    non_exhausted_sequences.remove(random_seq_index)
        elif method == "round_robin":
            number_of_sequences = len(packet_sequences)
            all_sequences_exhausted = False
            seq_indices = [0 for _ in packet_sequences]
            while not all_sequences_exhausted:
                non_exhausted_sequences = [i for i in range(number_of_sequences) if seq_indices[i] < len(packet_sequences[i])]
                if len(non_exhausted_sequences) == 0:
                    all_sequences_exhausted = True
                for seq_index in non_exhausted_sequences:
                    self.__packets.append(packet_sequences[seq_index][seq_indices[seq_index]])
                    seq_indices[seq_index] += 1
        else:
            raise ValueError("Invalid mixing method")
        