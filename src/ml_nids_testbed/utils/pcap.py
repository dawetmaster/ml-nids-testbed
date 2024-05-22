from scapy.all import rdpcap, wrpcap
import logging
import pathlib

logger = logging.getLogger(__name__)

class PCAPHandler():
    def __init__(self, pcap_path: str):
        self.pcap_path = pcap_path
        if not pathlib.Path.exists(pcap_path):
            logger.warning("pcap_path does not exist")
    def read(self):
        try:
            self.packets = rdpcap(self.pcap_path)
        except Exception as e:
            logger.error(e)
    def write(self):
        try:
            wrpcap(self.pcap_path, self.packets)
        except Exception as e:
            logger.error(e)
    def write_from_packet(self, *args):
        packets = list(args)
        try:
            wrpcap(self.pcap_path, packets)
        except Exception as e:
            logger.error(e)