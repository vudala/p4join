from scapy.all import *
from scapy.layers.l2 import Ether
from lineorder import LineOrder, LINEORDER_TYPE

interface = 'veth0'

bind_layers(Ether, LineOrder, type=LINEORDER_TYPE)

# Define a callback function to process each sniffed packet
def process_packet(packet):
    packet.show()

# Start sniffing packets
print("Sniffing Ethernet frames...")
sniff(prn=process_packet, iface=interface)
