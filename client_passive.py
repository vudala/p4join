from scapy.all import *
from scapy.layers.l2 import Ether
from tables import *

interface = 'veth24'

bind_layers(Ether, JoinControl, type=ETHER_JOINCTL_TYPE)

hash_table = {}
result = []

def stop_condition(packet):
  if JoinControl in packet:
    # Register the datetime to calculate processing time
    joinctl = packet[JoinControl]
    return joinctl.stage == 0


def build(packet):
  if JoinControl in packet:
    joinctl = packet[JoinControl]

    key = joinctl.build_key

    if joinctl.stage == 1:
      global hash_table 
      hash_table[key] = 'Set'
      print(f"Set key {key}")


def probe(packet):
  if JoinControl in packet:
    joinctl = packet[JoinControl]
    key = joinctl.probe_key

    packet.show()
    print()

    global hash_table
    global result

    if joinctl.stage > 1 and key in hash_table:
      result.append(packet)


print("Sniffing packets for build")
sniff(iface=interface, prn=build, stop_filter=stop_condition)
print("Build done")

print("Sniffing packets for probe 1")
sniff(iface=interface, prn=probe, stop_filter=stop_condition)
print("Probe done")

print(f"Matched {len(result)} packets")


print("Building hash table from intermediary join")
hash_table.clear()

for p in result:
  joinctl = p[JoinControl]
  key = joinctl.build_key
  hash_table[key] = 'Set'

result.clear()

print("Sniffing packets for probe 2")
sniff(iface=interface, prn=probe, stop_filter=stop_condition)
print("Probe done")

print("Query done")

print(f"Query resulted in {len(result)} matched packets")
