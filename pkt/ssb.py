# 3rd party
from scapy.all import *
from scapy.layers.l2 import Ether

# SF * 6_000_000
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


# SF * 30_000
class Customer(Packet):
    name = 'Customer'
    fields_desc = [
        IntField('c_custkey', 0),
        StrFixedLenField('c_name', None, length=25),
        StrFixedLenField('c_address', None, length=25),
        StrFixedLenField('c_city', None, length=10),
        StrFixedLenField('c_nation', None, length=15),
        StrFixedLenField('c_region', None, length=12),
        StrFixedLenField('c_phone', None, length=15),
        StrFixedLenField('c_mktsegment', None, length=10)
    ]


# SF * 2_000
class Supplier(Packet):
    name = 'Supplier'
    fields_desc = [
        IntField('s_suppkey', 0),
        StrFixedLenField('s_name', None, length=25),
        StrFixedLenField('s_address', None, length=25),
        StrFixedLenField('s_city', None, length=10),
        StrFixedLenField('s_nation', None, length=15),
        StrFixedLenField('s_region', None, length=12),
        StrFixedLenField('s_phone', None, length=15),
    ]


# SF * 7 * 365 (7 years days)
class Date(Packet):
    name = 'Date'
    fields_desc = [
        StrFixedLenField('d_datekey', None, length=12),
        StrFixedLenField('d_date', None, length=18),
        StrFixedLenField('d_dayofweek', None, length=9),
        StrFixedLenField('d_month', None, length=9),
        IntField('d_year', 0),
        IntField('d_yearmonthnum', 0),
        StrFixedLenField('d_yearmonth', None, length=7),
        IntField('d_daynuminweek', 0),
        IntField('d_daynuminmonth', 0),
        IntField('d_daynuminyear', 0),
        IntField('d_monthnuminyear', 0),
        IntField('d_weeknuminyear', 0),
        StrFixedLenField('d_sellingseason', None, length=12),
        StrFixedLenField('d_lastdayinweekfl', None, length=1),
        StrFixedLenField('d_lastdayinmonthfl', None, length=1),
        StrFixedLenField('d_holidayfl', None, length=1),
        StrFixedLenField('d_weekdayfl', None, length=1),
    ]
