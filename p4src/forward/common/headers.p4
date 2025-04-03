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

const ether_type_t ETHERTYPE_BENCHMARK = 0x8201;

header ethernet_h {
    mac_addr_t dst_addr;
    mac_addr_t src_addr;
    bit<16> ether_type;
}

header timestamps_h {
    bit<48> t0;
    bit<48> t1;
    bit<32> t2;
    bit<32> t3;
    bit<48> t4;
    bit<48> t5;
}

struct header_t {
    ethernet_h ethernet;
    timestamps_h timestamps;
}

struct metadata_t {}

#endif /* _HEADERS_ */
