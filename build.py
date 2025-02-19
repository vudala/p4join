from scapy.all import *
from scapy.layers.l2 import Ether
import csv

from tables import *

interface = 'veth0'
destiny = '00:00:00:00:00:03'

lines = []
ether_frame = Ether(dst=destiny)

########    BUILD    ##########

with open('./dataset_samples/customers.sample.csv', mode ='r')as file:
  csvFile = csv.reader(file, delimiter='|')
  for line in csvFile:
    lines.append(line)

for l in lines:
  customer = Customer(
    c_custkey = int(l[0]),
    c_name = l[1],
    c_address = l[2],
    c_city = l[3],
    c_nation = l[4],
    c_region = l[5],
    c_phone = l[6],
    c_mktsegment = l[7], 
  )

  join_ctl = JoinControl(
    table_t = TableType.CUSTOMER.value,
    ctl_type = ControlType.BUILD.value,
    hash_key = 0x00,
    inserted = 0x00,
    data = customer.c_custkey
  )

  packt = ether_frame / join_ctl / customer

  packt.show()

  sendp(packt, iface=interface)
