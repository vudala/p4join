from tables import *
  
def build_lineorder(line: str):
  return Lineorder(
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


def build_customer(line: str):
  return Customer(
    c_custkey = int(line[0]),
    c_name = line[1],
    c_address = line[2],
    c_city = line[3],
    c_nation = line[4],
    c_region = line[5],
    c_phone = line[6],
    c_mktsegment = line[7], 
  )


build_args = {
    TableType.LINEORDER: build_lineorder,
    TableType.CUSTOMER: build_customer,
}

def build_pkt(data_t: TableType, line: str):
  build_fn = build_args[data_t]

  payload = build_fn(line)

  return payload
