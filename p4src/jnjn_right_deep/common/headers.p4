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

const ether_type_t ETHERTYPE_JOIN_CONTROL = 0x8201;
const ether_type_t ETHERTYPE_BENCHMARK = 0x8211;

header ethernet_h {
    mac_addr_t dst_addr;
    mac_addr_t src_addr;
    bit<16> ether_type;
}

typedef bit<8> char;
typedef bit<16> uint16;
typedef bit<32> uint32;
typedef bit<64> uint64;

/* Size of the build/probe keys, consequently this is the size of the entries
in the hash tables */
#define KEY_SIZE 32

header join_control_h {
    bit<8> table_id;            // which table it refers to
    bit<8> stage;               // stage (0,1,2,3) (done, build 1, build 2, probe)
    bit<KEY_SIZE> build_key;    // key to be used on build
    bit<KEY_SIZE> probe1_key;   // key to used on probe1
    bit<KEY_SIZE> probe2_key;   // key to used on probe2
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
    bit<16> hash_key;           // store hash crc 16
    bit<KEY_SIZE> found;        // pkt found value
    bit<8> pipeline;            // 0 ingress, 1 egress
}

#endif /* _HEADERS_ */
