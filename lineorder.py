from scapy.all import *

LINEORDER_TYPE = 0x8321

class LineOrder(Packet):
    name = 'LineOrder'
    fields_desc = [
        XLongField('lo_orderkey', 0),
        LongField('lo_linenumber', 0),
        LongField('lo_custkey', 0),
        LongField('lo_partkey', 0),
        LongField('lo_suppkey', 0), 
        StrFixedLenField('lo_orderdate', None, length=12),
        StrFixedLenField('lo_orderpriority', None, length=15),
        StrFixedLenField('lo_shippriority', None, length=1),
        LongField('lo_quantity', 0),
        XLongField('lo_extendedprice', 0),
        XLongField('lo_ordtotalprice', 0),
        XLongField('lo_discount', 0),
        XLongField('lo_revenue', 0),
        XLongField('lo_supplycost', 0),
        XLongField('lo_tax', 0),
        StrFixedLenField('lo_commitdate', None, length=12),
        StrFixedLenField('lo_shipmode', None, length=10),
    ]

# CREATE TABLE lineorder (
#   lo_orderkey      BIGINT, -- Consider SF 300+
#   lo_linenumber    INTEGER,
#   lo_custkey       INTEGER, -- FK to C_CUSTKEY
#   lo_partkey       INTEGER, -- FK to P_PARTKEY
#   lo_suppkey       INTEGER, -- FK to S_SUPPKEY
#   lo_orderdate     DATE,    -- FK to D_DATEKEY
#   lo_orderpriority CHAR(15),
#   lo_shippriority  CHAR(1),
#   lo_quantity      INTEGER,
#   lo_extendedprice NUMERIC,
#   lo_ordtotalprice NUMERIC,
#   lo_discount      NUMERIC,
#   lo_revenue       NUMERIC,
#   lo_supplycost    NUMERIC,
#   lo_tax           NUMERIC,
#   lo_commitdate    DATE, -- FK to D_DATEKEY
#   lo_shipmode       CHAR(10), 
# );

# LO_ORDERKEY numeric (int up to SF 300) first 8 of each 32 keys populated
# LO_LINENUMBER numeric 1-7
# LO_CUSTKEY numeric identifier FK to C_CUSTKEY
# LO_PARTKEY identifier FK to P_PARTKEY
# LO_SUPPKEY numeric identifier FK to S_SUPPKEY
# LO_ORDERDATE identifier FK to D_DATEKEY
# LO_ORDERPRIORITY fixed text, size 15 (See pg 91:
# 5 Priorities: 1-URGENT, etc.)
# LO_SHIPPRIORITY fixed text, size 1
# LO_QUANTITY numeric 1-50 (for PART)
# LO_EXTENDEDPRICE numeric ≤ 55,450 (for PART)
# LO_ORDTOTALPRICE numeric ≤ 388,000 (ORDER)
# LO_DISCOUNT numeric 0-10 (for PART, percent)
# LO_REVENUE numeric (for PART: (lo_extendedprice*(100-lo_discnt))/100)
# LO_SUPPLYCOST numeric (for PART)
# LO_TAX numeric 0-8 (for PART)
# LO_COMMITDATE FK to D_DATEKEY
# LO_SHIPMODE fixed text, size 10 (See pg. 91: 7, Modes: REG AIR, AIR, etc.)