from scapy.all import *
from scapy.layers.l2 import Ether
from tables import *

interface = 'veth24'

bind_layers(Ether, JoinControl, type=ETHER_JOINCTL_TYPE)


def stop_condition(packet):
  if JoinControl in packet:
    ctl = packet[JoinControl]
    return ctl.stage == 0

def prnt(packet):
  packet.show()

print("Sniffing Ethernet frames...")

result = sniff(iface=interface,
                prn=prnt,
                stop_filter=stop_condition)

print("Done")
print(f"Join resulted in {len(result)} received packets")
