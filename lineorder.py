from scapy.all import *

LINEORDER_TYPE = 0x8321

class LineOrder(Packet):
    name = 'LineOrder'
    fields_desc = [
        LongField('lo_orderkey', 0),
        IntField('lo_linenumber', 0),
        IntField('lo_custkey', 0),
        IntField('lo_partkey', 0),
        IntField('lo_suppkey', 0),
        StrFixedLenField('lo_orderdate', None, length=12),
        StrFixedLenField('lo_orderpriority', None, length=15),
        StrFixedLenField('lo_shippriority', None, length=1),
        IntField('lo_quantity', 0),
        LongField('lo_extendedprice', 0),
        LongField('lo_ordtotalprice', 0),
        LongField('lo_discount', 0),
        LongField('lo_revenue', 0),
        LongField('lo_supplycost', 0),
        LongField('lo_tax', 0),
        StrFixedLenField('lo_commitdate', None, length=12),
        StrFixedLenField('lo_shipmode', None, length=10),
    ]
