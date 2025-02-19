#ifndef _HEADERS_
    #define _HEADERS_

#include <core.p4>
#include <v1model.p4>

#if __TARGET_TOFINO__ == 3
#include <t3na.p4>
#elif __TARGET_TOFINO__ == 2
#include <t2na.p4>
#else
#include <tna.p4>
#endif

typedef bit<48> mac_addr_t;
typedef bit<16> ether_type_t;

const ether_type_t ETHERTYPE_IPV4 = 16w0x0800;
const ether_type_t ETHERTYPE_JOIN_CONTROL = 16w0x8200;

header ethernet_h {
    mac_addr_t dst_addr;
    mac_addr_t src_addr;
    bit<16> ether_type;
}

/*****************************************/
/*

ssb description: https://www.cs.umb.edu/~poneil/StarSchemaB.PDF

                                         */
/*****************************************/

typedef bit<8> char;
typedef bit<16> uint16;
typedef bit<32> uint32;
typedef bit<64> uint64;

enum bit<8> TableType {
    LINEORDER_TABLE = 8w0x1,
    CUSTOMER_TABLE = 8w0x2,
    SUPPLIER_TABLE = 8w0x3
}

enum bit<32> ControlType {
    BUILD = 1,
    PROBE = 2,
    FLUSH = 3
}


header join_control_h {
    bit<8> table_t;     // which table it refers to
    bit<32> ctl_type;   // build/probe/flush flag
    uint16 hash_key;    // store hash
    bit<32> inserted;   // pkt inserted flag
    bit<32> data;       // key to be hashed
}


/* SF * 6_000_000 */
header lineorder_h {
    uint64 lo_orderkey;         // int64
    uint32 lo_linenumber;       // int32
    uint32 lo_custkey;          // int32
    uint32 lo_partkey;          // int32
    uint32 lo_suppkey;          // int32    
    bit<96> lo_orderdate;       // str len 12
    bit<120> lo_orderpriority;  // str len 15
    char lo_shippriority;       // str len 1
    uint32 lo_quantity;         // int32
    uint64 lo_extendedprice;    // int64
    uint64 lo_ordtotalprice;    // int64
    uint64 lo_discount;         // int64
    uint64 lo_revenue;          // int64
    uint64 lo_supplycost;       // int64
    uint64 lo_tax;              // int64
    bit<96> lo_commitdate;      // str len 12
    bit<80> lo_shipmode;        // str len 10
}


/* SF * 30_000 */
header customer_h {
    uint32 c_custkey;           // int32
    bit<200> c_name;            // str len 25
    bit<200> c_address;         // str len 25
    bit<80> c_city;             // str len 10
    bit<120> c_nation;          // str len 15
    bit<96> c_region;           // str len 12
    bit<120> c_phone;           // str len 15
    bit<80> c_mktsegment;       // str len 10
}
 

/* SF * 2_000 */
header supplier_h {
    uint32 s_suppkey;       // int32
    bit<200> s_name;        // str len 25
    bit<200> s_address;     // str len 25
    bit<80> s_city;         // str len 10
    bit<120> s_nation;      // str len 15
    bit<96> s_region;       // str len 12
    bit<120> s_phone;       // str len 15
}

// header_union table_u {
//     lineorder_h lineorder;
//     customer_h customer;
//     supplier_h supplier;
// }

struct header_t {
    ethernet_h ethernet;
    join_control_h join_control;
//    table_u op_table;
}

struct metadata_t {}

#endif /* _HEADERS_ */
