from scapy.all import *
from scapy.layers.l2 import Ether
from pkt.types import *

interface = 'veth24'

class Test(Packet):
    name = 'Test'
    fields_desc = [
        IntField('index', -1)
    ]

bind_layers(Ether, Test, type=0x8234)

count = 0

# Define a callback function to process each sniffed packet
def process_packet(pkt):
    pkt.show()

    global count
    count += 1
    print(count)

# Start sniffing packets
print("Sniffing Ethernet frames...")
sniff(prn=process_packet, iface=interface)
