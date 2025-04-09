# Native
from datetime import datetime

# 3rd party
from scapy.all import *
from scapy.layers.l2 import Ether

# Local
from pkt.binds import *

interface = 'veth24'

def stop_condition(packet):
  if JoinControlLeftDeep in packet:
    ctl = packet[JoinControlLeftDeep]
    return ctl.stage == 0

last_time = None
def proc(packet):
  global last_time
  if JoinControlLeftDeep in packet:
    ctl = packet[JoinControlLeftDeep]
    if ctl.stage != 0:
      last_time = datetime.now()

print("Sniffing Ethernet frames...")

result = sniff(iface=interface,
                prn=proc,
                stop_filter=stop_condition)

print(f"Done at {last_time}")
print(f"Join resulted in {len(result)} received packets")
