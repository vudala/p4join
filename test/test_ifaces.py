from scapy.all import *
from scapy.layers.l2 import Ether

from pkt.binds import *

for i in range(64):
    ethf = Ether(dst="00:00:00:00:00:03")
    tst = Test(index = i)
    sendp(ethf / tst, iface = f'veth{i}')
    print(f"Sent on iface veth{i}")
