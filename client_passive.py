from scapy.all import *
from scapy.layers.l2 import Ether
from tables import *
from functools import partial

interface = 'veth24'

bind_layers(Ether, JoinControl, type=ETHER_JOINCTL_TYPE)

def stop_condition(packet):
  if JoinControl in packet:
    # Register the datetime to calculate processing time
    joinctl = packet[JoinControl]
    return joinctl.stage == 0


def build(hash_table, packet):
  if JoinControl in packet:
    joinctl = packet[JoinControl]

    key = joinctl.build_key

    if joinctl.stage == 1:  
      hash_table[key] = 'Set'
  
  return False


def probe(hash_table, packet):
  if JoinControl in packet:
    joinctl = packet[JoinControl]
    key = joinctl.probe_key

    if joinctl.stage > 1 and key in hash_table:
        return True

  return False


print("Sniffing Ethernet frames...")

print("Sniffing packets for build")
ht = {}
sniff(iface=interface, lfilter=partial(build, ht), stop_filter=stop_condition)
print("Build done")

print("Sniffing packets for probe 1")
join1_result = sniff(
            iface=interface,
            lfilter=partial(probe, ht),
            stop_filter=stop_condition
          )
print("Probe done")

print("Sniffing packets for probe 2")

ht.clear()
for p in join1_result:
  joinctl = packet[JoinControl]
  key = joinctl.build_key
  ht[key] = 'Set'

join2_ht = sniff(
            iface=interface,
            lfilter=partial(probe, ht),
            stop_filter=stop_condition
          )
print("Probe done")

print("Query done")

print(f"Query resulted in {len(join2_ht)} matched packets")
