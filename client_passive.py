from scapy.all import *
from scapy.layers.l2 import Ether
from tables import *

interface = 'veth24'

bind_layers(Ether, JoinControl, type=ETHER_JOINCTL_TYPE)

hash_table = {}

def stop_condition(packet):
  if JoinControl in packet:
    # Register the datetime to calculate processing time
    joinctl = packet[JoinControl]
    return joinctl.stage == ControlType.CLOSE.value


def process_packet(packet):
  if JoinControl in packet:
    joinctl = packet[JoinControl]

    key = joinctl.data

    if joinctl.stage == 1:  
      hash_table[key] = 'Set'
    elif joinctl.stage > 1:
      if key in hash_table:
        return True
  
  return False


print("Sniffing Ethernet frames...")

result = sniff(iface=interface,
                lfilter=process_packet,
                stop_filter=stop_condition)

print("Done")
print(f"Join resulted in {len(result)} packets")
