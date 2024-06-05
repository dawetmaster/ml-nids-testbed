from utils.pcap import PCAPHandler
from utils.packets import PacketSequence
import time
import logging

logger = logging.getLogger(__name__)

def normalise_timestamp(
        input_pcap_handler: PCAPHandler,
        output_pcap_handler: PCAPHandler,
        start_timestamp: float = time.time()
):
    input_ps = PacketSequence(input_pcap_handler.packets)
    logger.info("Normalising packet sequence with starting timestamp: %s" % start_timestamp)
    input_ps.normalise_timestamp(start_timestamp)
    logger.info("Finished normalising packet sequence.")
    output_pcap_handler.write_from_packet(input_ps.get_packet_sequence())