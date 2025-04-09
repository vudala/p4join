# standard
from enum import Enum

# 3rd party
from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.fields import *
from scapy.packet import Packet

# self
import pkt.ssb as ssb
import pkt.tpch as tpch

class TableType(Enum):
    SSB_LINEORDER = 1
    SSB_CUSTOMER = 2
    SSB_SUPPLIER = 3
    SSB_DATE = 4

    TPCH_PART = 5
    TPCH_SUPPLIER = 6
    TPCH_PARTSUPP = 7
    TPCH_CUSTOMER = 8
    TPCH_ORDER = 9
    TPCH_LINEITEM = 10
    TPCH_NATION = 11
    TPCH_REGION = 12


ETHER_JOINCTL_LD = 0x8200
ETHER_JOINCTL_RD = 0x8201

ETHER_BENCHMARK_LD = 0X8210
ETHER_BENCHMARK_RD = 0x8211

ETHER_TEST = 0x8234

KEY_SIZE = 4


class JoinControlLeftDeep(Packet):
    name = 'JoinControl'
    fields_desc = [
        BitField('table_t', 0x00, 8),
        BitField('stage', 0x00, 8),
        BitField('build_key', 0x00, 32),
        BitField('probe_key', 0x00, 32),
    ]


class JoinControlRightDeep(Packet):
    name = 'JoinControl'
    fields_desc = [
        BitField('table_t', 0x00, 8),
        BitField('stage', 0x00, 8),
        StrFixedLenField('build_key', None, KEY_SIZE),
        StrFixedLenField('probe1_key', None, KEY_SIZE),
        StrFixedLenField('probe2_key', None, KEY_SIZE),
    ]


class Timestamps(Packet):
    name = 'Timestamps'
    fields_desc = [
        BitField('t0', 0x00, 48),
        BitField('t1', 0x00, 48),
        BitField('t2', 0x00, 32),
        BitField('t3', 0x00, 32),
        BitField('t4', 0x00, 48),
        BitField('t5', 0x00, 48),
    ]


class BenchmarkLD(Packet):
    name = 'Benchmark'
    fields_desc = [
        PacketField("timestamps", Timestamps(), Timestamps),
        PacketField("join_control", JoinControlLeftDeep(), JoinControlLeftDeep)
    ]


class BenchmarkRD(Packet):
    name = 'Benchmark'
    fields_desc = [
        PacketField("timestamps", Timestamps(), Timestamps),
        PacketField("join_control", JoinControlRightDeep(), JoinControlRightDeep)
    ]


class Test(Packet):
    name = 'Test'
    fields_desc = [
        IntField('index', -1)
    ]

bind_layers(Ether, Test, type=ETHER_TEST)


# Ether binds
bind_layers(Ether, JoinControlLeftDeep, type=ETHER_JOINCTL_LD)
bind_layers(Ether, JoinControlRightDeep, type=ETHER_JOINCTL_RD)

bind_layers(Ether, BenchmarkLD, type=ETHER_BENCHMARK_LD)
bind_layers(Ether, BenchmarkRD, type=ETHER_BENCHMARK_RD)

# JoinControl binds
bind_layers(JoinControlLeftDeep, ssb.LineOrder, table_t=TableType.SSB_LINEORDER.value)
bind_layers(JoinControlLeftDeep, ssb.Customer, table_t=TableType.SSB_CUSTOMER.value)
bind_layers(JoinControlLeftDeep, ssb.Supplier, table_t=TableType.SSB_SUPPLIER.value)
bind_layers(JoinControlLeftDeep, ssb.Date, table_t=TableType.SSB_DATE.value)

bind_layers(JoinControlRightDeep, ssb.LineOrder, table_t=TableType.SSB_LINEORDER.value)
bind_layers(JoinControlRightDeep, ssb.Customer, table_t=TableType.SSB_CUSTOMER.value)
bind_layers(JoinControlRightDeep, ssb.Supplier, table_t=TableType.SSB_SUPPLIER.value)
bind_layers(JoinControlRightDeep, ssb.Date, table_t=TableType.SSB_DATE.value)

# To let scapy know timestamps doesnt transport payload
bind_layers(Timestamps, Padding)
