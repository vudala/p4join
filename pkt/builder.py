from pkt.binds import TableType
import pkt.ssb as ssb
import pkt.tpch as tpch


##### SSB  #####

def ssb_lineorder(line: str):
  return ssb.LineOrder(
    lo_orderkey = int(line[0]),
    lo_linenumber = int(line[1]),
    lo_custkey = int(line[2]),
    lo_partkey = int(line[3]),
    lo_suppkey = int(line[4]), 
    lo_orderdate = line[5],
    lo_orderpriority = line[6],
    lo_shippriority = line[7],
    lo_quantity = int(line[8]),
    lo_extendedprice = int(line[9]),
    lo_ordtotalprice = int(line[10]),
    lo_discount = int(line[11]),
    lo_revenue = int(line[12]),
    lo_supplycost = int(line[13]),
    lo_tax = int(line[14]),
    lo_commitdate = line[15],
    lo_shipmode = line[16],  
  )


def ssb_customer(line: str):
  return ssb.Customer(
    c_custkey = int(line[0]),
    c_name = line[1],
    c_address = line[2],
    c_city = line[3],
    c_nation = line[4],
    c_region = line[5],
    c_phone = line[6],
    c_mktsegment = line[7], 
  )


def ssb_supplier(line: str):
  return ssb.Supplier(
    s_suppkey = int(line[0]),
    s_name = line[1],
    s_address = line[2],
    s_city = line[3],
    s_nation = line[4],
    s_region = line[5],
    s_phone = line[6],
  )


##### TPC-H #####

def tpch_part(line: str):
  return tpch.Part(
    p_partkey = int(line[0]),
    p_name = line[1],
    p_mfgr = line[2],
    p_brand = line[3],
    p_type = line[4],
    p_size = int(line[5]),
    p_container = line[6],
    p_retailprice = line[7],
    p_comment = line[8],
  )


def tpch_supplier(line: str):
  return tpch.Supplier(
    s_suppkey = int(line[0]),
    s_name = line[1],
    s_address = line[2],
    s_nationkey = int(line[3]),
    s_phone = line[4],
    s_acctbal = line[5],
    s_comment = line[6],
  )


def tpch_partsupp(line: str):
  return tpch.PartSupp(
    ps_partkey = int(line[0]),
    ps_suppkey = int(line[1]),
    ps_availqty = int(line[2]),
    ps_supplycost = line[3],
    ps_comment = line[4],
  )


def tpch_customer(line: str):
  return tpch.Customer(
    c_custkey = int(line[0]),
    c_name = line[1],
    c_address = line[2],
    c_nationkey = int(line[3]),
    c_phone = line[4],
    c_acctbal = line[5],
    c_mktsegment = line[6],
    c_comment = line[7],
  )


def tpch_order(line: str):
  return tpch.Order(
    o_orderkey = int(line[0]),
    o_custkey = int(line[1]),
    o_orderstatus = line[2],
    o_totalprice = line[3],
    o_orderdate = line[4],
    o_orderpriority = line[5],
    o_clerk = line[6],
    o_shippriority = int(line[7]),
    o_comment = line[8],
  )


def tpch_lineitem(line: str):
  return tpch.LineItem(
    l_orderkey = int(line[0]),
    l_partkey = int(line[1]),
    l_suppkey = int(line[2]),
    l_linenumber = int(line[3]),
    l_quantity = line[4],
    l_extendedprice = line[5],
    l_discount = line[6],
    l_tax = line[7],
    l_returnflag = line[8],
    l_linestatus = line[9],
    l_shipdate = line[10],
    l_commitdate = line[11],
    l_receiptdate = line[12],
    l_shipinstruct = line[13],
    l_shipmode = line[14],
    l_comment = line[15],
  )


def tpch_nation(line: str):
  return tpch.Nation(
    n_nationkey = int(line[0]),
    n_name = line[1],
    n_regionkey = int(line[2]),
    n_comment = line[3],
  )


def tpch_region(line: str):
  return tpch.Region(
    r_regionkey = int(line[0]),
    r_name = line[1],
    r_comment = line[2],
  )


build_args = {
  TableType.SSB_LINEORDER: ssb_lineorder,
  TableType.SSB_CUSTOMER: ssb_customer,
  TableType.SSB_SUPPLIER: ssb_supplier,
  
  TableType.TPCH_PART: tpch_part,
  TableType.TPCH_SUPPLIER: tpch_supplier,
  TableType.TPCH_PARTSUPP: tpch_partsupp,
  TableType.TPCH_CUSTOMER: tpch_customer,
  TableType.TPCH_ORDER: tpch_order,
  TableType.TPCH_LINEITEM: tpch_lineitem,
  TableType.TPCH_NATION: tpch_nation,
  TableType.TPCH_REGION: tpch_region,
}


def build_pkt(data_t: TableType, line: str):
  build_fn = build_args[data_t]

  payload = build_fn(line)

  return payload
