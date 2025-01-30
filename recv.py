from scapy.all import sniff, Ether, Raw

interface = 'eth0'

# Define a callback function to process each sniffed packet
def process_packet(packet):
    packet.show()

# Start sniffing packets
print("Sniffing Ethernet frames...")
sniff(prn=process_packet, iface=interface)