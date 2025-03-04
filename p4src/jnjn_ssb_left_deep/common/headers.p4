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

const ether_type_t ETHERTYPE_JOIN_CONTROL = 0x8200;

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


header join_control_h {
    bit<8> table_id;    // which table it refers to
    bit<8> stage;       // stage (0,1,2,3) (done, build, probe/build, probe)
    bit<32> build_key;  // key to be used on build
    bit<32> probe_key;  // key to be used on probe
    bit<16> hash_key;   // ffw store hash crc 16
    bit<32> found;      // ffw pkt found value
}

struct header_t {
    ethernet_h ethernet;
    join_control_h join_control;
}

struct metadata_t {}

#endif /* _HEADERS_ */
