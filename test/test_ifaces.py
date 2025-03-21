from scapy.all import *
from scapy.layers.l2 import Ether

class Test(Packet):
    name = 'Test'
    fields_desc = [
        IntField('index', -1)
    ]

bind_layers(Ether, Test, type=0x8234)

for i in range(64):
    ethf = Ether(dst="00:00:00:00:00:03")
    tst = Test(index = i)
    sendp(ethf / tst, iface = f'veth{i}')
    print(f"Sent on iface veth{i}")
