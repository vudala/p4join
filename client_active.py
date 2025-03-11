from scapy.all import *
from scapy.layers.l2 import Ether
from tables import *
from datetime import datetime

interface = 'veth24'

bind_layers(Ether, JoinControl, type=ETHER_JOINCTL_TYPE)


def stop_condition(packet):
  if JoinControl in packet:
    ctl = packet[JoinControl]
    return ctl.stage == 0

last_time = None
def proc(packet):
  global last_time
  if JoinControl in packet:
    ctl = packet[JoinControl]
    if ctl.stage != 0:
      last_time = datetime.now()

print("Sniffing Ethernet frames...")

result = sniff(iface=interface,
                prn=proc,
                stop_filter=stop_condition)

print(f"Done at {last_time}")
print(f"Join resulted in {len(result)} received packets")
