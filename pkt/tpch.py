from scapy.fields import *
from scapy.packet import Packet


class Part(Packet):
    fields_desc = [
        IntField("p_partkey", 0),
        StrField("p_name", None),
        StrFixedLenField("p_mfgr", None, 25),
        StrFixedLenField("p_brand", None, 10),
        StrField("p_type", None),
        IntField("p_size", 0),
        StrFixedLenField("p_container", None, 10),
        StrField("p_retailprice", None),
        StrField("p_comment", None),
    ]


class Supplier(Packet):
    fields_desc = [
        IntField("s_suppkey", 0),
        StrFixedLenField("s_name", None, 25),
        StrField("s_address", None),
        IntField("s_nationkey", 0),
        StrFixedLenField("s_phone", None, 15),
        StrField("s_acctbal", None),
        StrField("s_comment", None),
    ]


class PartSupp(Packet):
    fields_desc = [
        IntField("ps_partkey", 0),
        IntField("ps_suppkey", 0),
        IntField("ps_availqty", 0),
        StrField("ps_supplycost", None),
        StrField("ps_comment", None),
    ]


class Customer(Packet):
    fields_desc = [
        IntField("c_custkey", 0),
        StrField("c_name", None),
        StrField("c_address", None),
        IntField("c_nationkey", 0),
        StrFixedLenField("c_phone", None, 15),
        StrField("c_acctbal", None),
        StrFixedLenField("c_mktsegment", None, 10),
        StrField("c_comment", None),
    ]


class Order(Packet):
    fields_desc = [
        IntField("o_orderkey", 0),
        IntField("o_custkey", 0),
        StrFixedLenField("o_orderstatus", None, 1),
        StrField("o_totalprice", None),
        StrField("o_orderdate", None),
        StrFixedLenField("o_orderpriority", None, 15),
        StrFixedLenField("o_clerk", None, 15),
        IntField("o_shippriority", 0),
        StrField("o_comment", None),
    ]


class LineItem(Packet):
    fields_desc = [
        IntField("l_orderkey", 0),
        IntField("l_partkey", 0),
        IntField("l_suppkey", 0),
        IntField("l_linenumber", 0),
        StrField("l_quantity", None),
        StrField("l_extendedprice", None),
        StrField("l_discount", None),
        StrField("l_tax", None),
        StrFixedLenField("l_returnflag", None, 1),
        StrFixedLenField("l_linestatus", None, 1),
        StrField("l_shipdate", None),
        StrField("l_commitdate", None),
        StrField("l_receiptdate", None),
        StrFixedLenField("l_shipinstruct", None, 25),
        StrFixedLenField("l_shipmode", None, 10),
        StrField("l_comment", None),
    ]


class Nation(Packet):
    fields_desc = [
        IntField("n_nationkey", 0),
        StrFixedLenField("n_name", None, 25),
        IntField("n_regionkey", 0),
        StrField("n_comment", None),
    ]


class Region(Packet):
    fields_desc = [
        IntField("r_regionkey", 0),
        StrFixedLenField("r_name", None, 25),
        StrField("r_comment", None),
    ]
