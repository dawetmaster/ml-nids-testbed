from utils.packets import PacketSequence
from utils.pcap import PCAPHandler
import logging

logger = logging.getLogger(__name__)

def scale_delay(
        input_file_handler: PCAPHandler,
        output_file_handler: PCAPHandler,
        factor: float,
):
    input_file_handler.read()
    input_ps = PacketSequence(input_file_handler.packets)
    input_ps.scale_delays(factor)
    output_file_handler.write_from_packet(input_ps.get_packet_sequence())

def shift_delay(
        input_file_handler: PCAPHandler,
        output_file_handler: PCAPHandler,
        constant: float,
):
    input_file_handler.read()
    input_ps = PacketSequence(input_file_handler.packets)
    input_ps.shift_delays(constant)
    output_file_handler.write_from_packet(input_ps.get_packet_sequence())