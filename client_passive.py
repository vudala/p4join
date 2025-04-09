# Native
from datetime import datetime

# 3rd party
from scapy.all import *
from scapy.layers.l2 import Ether

# Local
from pkt.binds import *

interface = 'veth24'

hash_table = {}
result = []

first_time = None
last_time = None

def stop_condition(packet):
  if JoinControlLeftDeep in packet:
    # Register the datetime to calculate processing time
    joinctl = packet[JoinControlLeftDeep]
    return joinctl.stage == 0


def build(packet):
  global first_time
  global last_time
  global hash_table 

  if JoinControlLeftDeep in packet:
    joinctl = packet[JoinControlLeftDeep]

    key = joinctl.build_key

    if joinctl.stage == 1:
      hash_table[key] = True 

    if first_time == None:
      first_time = datetime.now()

    last_time = datetime.now()


def probe(packet):
  global first_time
  global last_time
  global hash_table
  global result

  if JoinControlLeftDeep in packet:
    joinctl = packet[JoinControlLeftDeep]
    key = joinctl.probe_key

    if joinctl.stage > 1 and key in hash_table:
      result.append(packet)

    if first_time == None:
      first_time = datetime.now()

    last_time = datetime.now()


print("Sniffing packets for build")
sniff(iface=interface, prn=build, stop_filter=stop_condition)
print("Build done")
print(f"Start: {first_time} End: {last_time}")
print(f"Elapsed time: {last_time - first_time}")

first_time = None

print("Sniffing packets for probe 1")
sniff(iface=interface, prn=probe, stop_filter=stop_condition)
print("Probe done")
print(f"Matched {len(result)} packets")
print(f"Start: {first_time} End: {last_time}")
print(f"Elapsed time: {last_time - first_time}")

first_time = None

print("Building hash table from intermediary join")
first_time = datetime.now()
hash_table.clear()
for p in result:
  joinctl = p[JoinControlLeftDeep]
  key = joinctl.build_key
  hash_table[key] = True
result.clear()
last_time = datetime.now()
print(f"Start: {first_time} End: {last_time}")
print(f"Elapsed time: {last_time - first_time}")

first_time = None
print("Sniffing packets for probe 2")
sniff(iface=interface, prn=probe, stop_filter=stop_condition)
print("Probe done")
print(f"Start: {first_time} End: {last_time}")
print(f"Elapsed time: {last_time - first_time}")

print("Query done")

print(f"Query resulted in {len(result)} matched packets")
