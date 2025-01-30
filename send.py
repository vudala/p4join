from scapy.all import *
from scapy.layers.l2 import Ether

from lineorder import LINEORDER_TYPE, LineOrder

interface = 'eth0'
destiny = "02:42:ac:14:00:02"

bind_layers(Ether, LineOrder, type=LINEORDER_TYPE)

lines = []

import csv
with open('lineorder.csv', mode ='r')as file:
  csvFile = csv.reader(file, delimiter=',')
  for line in csvFile:
    lines.append(line)

ether_frame = Ether(dst=destiny)
packets = []
for l in lines[:10]:
  payload = LineOrder(
    lo_orderkey = l[0],
    lo_linenumber = l[1],
    lo_custkey = l[2],
    lo_partkey = l[3],
    lo_suppkey = l[4], 
    lo_orderdate = l[5],
    lo_orderpriority = l[6],
    lo_shippriority = l[7],
    lo_quantity = l[8],
    lo_extendedprice = l[9],
    lo_ordtotalprice = l[10],
    lo_discount = l[11],
    lo_revenue = l[12],
    lo_supplycost = l[13],
    lo_tax = l[14],
    lo_commitdate = l[15],
    lo_shipmode = l[16],  
  )

  packt = ether_frame / payload

  packets.append(packt)

packets[0].show()

for p in packets:
  sendp(p, iface=interface)

# Send the pa = cket
# sendp(packt, iface=interface)