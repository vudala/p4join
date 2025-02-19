from scapy.all import *
from scapy.layers.l2 import Ether
import csv

from tables import *

interface = 'veth0'
destiny = '00:00:00:00:00:03'

ether_frame = Ether(dst=destiny)

########    FLUSH    ##########

join_ctl = JoinControl(
    table_t = 0x00,
    ctl_type = ControlType.FLUSH.value,
    hash_key = 0x00,
    inserted = 0x00,
    data = 0x00
)

packt = ether_frame / join_ctl

packt.show()

sendp(packt, iface=interface)
