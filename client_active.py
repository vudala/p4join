from scapy.all import *
from scapy.layers.l2 import Ether
from tables import *

interface = 'veth24'

bind_layers(Ether, JoinControl, type=ETHER_JOINCTL_TYPE)


def stop_condition(packet):
  return False
  if JoinControl in packet:
    joinctl = packet[JoinControl]
    return joinctl.ctl_type == ControlType.CLOSE.value
  

# def process_packet(packet):
#   if JoinControl in packet:
#     joinctl = packet[JoinControl]

#     key = joinctl.data

#     return True


def prnt(packet):
  packet.show()

print("Sniffing Ethernet frames...")

result = sniff(iface=interface,
                prn=prnt,
                stop_filter=stop_condition)

print("Done")
print(f"Join resulted in {len(result)} packets")
