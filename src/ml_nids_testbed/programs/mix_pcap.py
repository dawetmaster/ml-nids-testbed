from utils.packets import PacketSequence
from utils.pcap import PCAPHandler
from typing import List
import logging

logger = logging.getLogger(__name__)

def mix_pcap(
        pcap_handlers: List[PCAPHandler], 
        output_pcap_handler: PCAPHandler, 
        mix_method: str
):
    try:
        logger.debug(f"PCAP Handlers: {pcap_handlers}")
        for ph in pcap_handlers:
            ph.read()
        input_ps = [ph.packets for ph in pcap_handlers]
        output_ps = PacketSequence()
        output_ps.mix_packets(*input_ps, method=mix_method)
        output_pcap_handler.write_from_packet(output_ps.get_packet_sequence())

    except Exception as e:
        logger.error(e)
