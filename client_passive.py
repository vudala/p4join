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
    return joinctl.stage == 0


def build(packet):
  if JoinControl in packet:
    joinctl = packet[JoinControl]

    key = joinctl.build_key

    if joinctl.stage == 1:
      global hash_table 
      hash_table[key] = 'Set'
  
  return True


def probe(packet):
  if JoinControl in packet:
    joinctl = packet[JoinControl]
    key = joinctl.probe_key

    global hash_table
    if joinctl.stage > 1 and key in hash_table:
      return True

    if joinctl.stage == 0:
      return True

  return False


print("Sniffing Ethernet frames...")

print("Sniffing packets for build")

sniff(iface=interface, lfilter=build, stop_filter=stop_condition)
print("Build done")

print("Sniffing packets for probe 1")
join1_result = sniff(
            iface=interface,
            lfilter=probe,
            stop_filter=stop_condition
          )
# Remove last packet, which is included so the stop filter can work
join1_result = join1_result[:-1]
print("Probe done")


print("Building hash table from intermediary join")
hash_table.clear()
for p in join1_result:
  joinctl = p[JoinControl]
  key = joinctl.build_key
  hash_table[key] = 'Set'

print("Sniffing packets for probe 2")
join2_result = sniff(
            iface=interface,
            lfilter=probe,
            stop_filter=stop_condition
          )
# Remove last packet, which is included so the stop filter can work
join2_result = join2_result[:-1]
print("Probe done")

print("Query done")

print(f"Query resulted in {len(join2_result)} matched packets")
