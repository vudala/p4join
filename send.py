from scapy.all import *
from scapy.layers.l2 import Ether

from tables import Lineorder, TableType

interface = 'veth1'
destiny = '00:00:00:00:00:01'

bind_layers(Ether, Lineorder, type=TableType.LINEORDER)

lines = []

import csv
with open('lineorder.sample.csv', mode ='r')as file:
  csvFile = csv.reader(file, delimiter=',')
  for line in csvFile:
    lines.append(line)

ether_frame = Ether(dst=destiny)
packets = []
for l in lines:
  payload = Lineorder(
    lo_orderkey = int(l[0]),
    lo_linenumber = int(l[1]),
    lo_custkey = int(l[2]),
    lo_partkey = int(l[3]),
    lo_suppkey = int(l[4]), 
    lo_orderdate = l[5],
    lo_orderpriority = l[6],
    lo_shippriority = l[7],
    lo_quantity = int(l[8]),
    lo_extendedprice = int(l[9]),
    lo_ordtotalprice = int(l[10]),
    lo_discount = int(l[11]),
    lo_revenue = int(l[12]),
    lo_supplycost = int(l[13]),
    lo_tax = int(l[14]),
    lo_commitdate = l[15],
    lo_shipmode = l[16],  
  )

  packt = ether_frame / payload

  packt.show()

  sendp(packt, iface=interface)
