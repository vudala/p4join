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

#define KEY_SIZE 32

const ether_type_t ETHERTYPE_JOIN_CONTROL = 0x8200;
const ether_type_t ETHERTYPE_BENCHMARK = 0x8210;

header ethernet_h {
    mac_addr_t dst_addr;
    mac_addr_t src_addr;
    bit<16> ether_type;
}

header join_control_h {
    bit<8> table_id;    // which table it refers to
    bit<8> stage;       // stage (0,1,2,3) (done, build, probe/build, probe)
    bit<KEY_SIZE> build_key;  // key to be used on build
    bit<KEY_SIZE> probe_key;  // key to be used on probe
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
    join_control_h join_control;
}

struct metadata_t {
    bit<16> hash_key;       // ffw store hash crc 16
    bit<KEY_SIZE> found;    // ffw pkt found value
}

#endif /* _HEADERS_ */
