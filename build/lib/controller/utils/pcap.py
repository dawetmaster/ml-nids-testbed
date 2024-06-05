from scapy.all import rdpcap, wrpcap
import logging
import pathlib

logger = logging.getLogger(__name__)

class PCAPHandler():
    def __init__(self, pcap_path: str):
        self.pcap_path = pcap_path
        if not pathlib.Path(self.pcap_path).exists():
            logger.warning("pcap_path does not exist")
    def read(self):
        try:
            logger.info(f"Reading PCAP from disk with path {self.pcap_path}")
            self.packets = rdpcap(self.pcap_path)
        except Exception as e:
            logger.error(e)
    def write(self):
        try:
            logger.info(f"Writing PCAP to disk with path {self.pcap_path}")
            wrpcap(self.pcap_path, self.packets)
        except Exception as e:
            logger.error(e)
    def write_from_packet(self, *packet_seq):
        try:
            logger.info(f"Writing PCAP from packet to disk with path {self.pcap_path}")
            for ps in packet_seq:
                wrpcap(self.pcap_path, ps)
        except Exception as e:
            logger.error(e)