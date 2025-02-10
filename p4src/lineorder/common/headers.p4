#ifndef _HEADERS_
    #define _HEADERS_

typedef bit<48> mac_addr_t;
typedef bit<16> ether_type_t;

const ether_type_t ETHERTYPE_IPV4 = 16w0x0800;
const ether_type_t ETHERTYPE_LINEORDER = 16w0x8321;

header ethernet_h {
    mac_addr_t dst_addr;
    mac_addr_t src_addr;
    bit<16> ether_type;
}

/*****************************************/

typedef bit<32> uint32;
typedef bit<64> uint64;
typedef bit<8> char;

header lineorder_h {
    uint64 lo_orderkey; // int64
    uint32 lo_linenumber; // int32
    uint32 lo_custkey; // int32
    uint32 lo_partkey; // int32
    uint32 lo_suppkey; // int32    
    bit<96> lo_orderdate; // str len 12
    bit<120> lo_orderpriority; // str len 15
    char lo_shippriority; // str len 1
    uint32 lo_quantity; // int32
    uint64 lo_extendedprice; // int64
    uint64 lo_ordtotalprice; // int64
    uint64 lo_discount; // int64
    uint64 lo_revenue; // int64
    uint64 lo_supplycost; // int64
    uint64 lo_tax; // int64
    bit<96> lo_commitdate; // str len 12
    bit<80> lo_shipmode; // str len 10
}

struct header_t {
    ethernet_h ethernet;
    lineorder_h lineorder;
}

struct metadata_t {}

#endif /* _HEADERS_ */
