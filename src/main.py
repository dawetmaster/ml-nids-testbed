from scapy.all import *
import random

# Define the target IP and port
target_ip = "192.168.0.1"
target_port = 80

def split_string(string, randomised=False, substr_length=5):
    if randomised:
        i = 0
        while i < len(string):
            length = random.randint(0, len(string) - i)
            yield string[i:i+length]
            i += length

# Create an incomplete HTTP GET request
http_get = "GET / HTTP/1.1\r\nHost: {}\r\n".format(target_ip)

# Fragment the request into parts
fragments = list(split_string(http_get, True))
print(fragments)

# Function to send fragments
def send_fragments(ip, port, fragments):
    seq = 1000  # Starting sequence number
    for frag in fragments:
        ip_layer = IP(dst=ip)
        tcp_layer = TCP(dport=port, seq=seq, flags="PA")
        packet = ip_layer/tcp_layer/frag
        send(packet, verbose=0)
        seq += len(frag)

# Send the fragments
# send_fragments(target_ip, target_port, fragments)
