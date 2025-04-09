#include <core.p4>
#if __TARGET_TOFINO__ == 3
#include <t3na.p4>
#elif __TARGET_TOFINO__ == 2
#include <t2na.p4>
#else
#include <tna.p4>
#endif

#include "common/headers.p4"
#include "common/parser.p4"

#define TABLE_SIZE 65536
#define HASH_SIZE 16
#define HASH_ALG HashAlgorithm_t.CRC16

/* 
REFERENCE

https://www.cidrdb.org/cidr2019/papers/p142-lerner-cidr19.pdf
*/

// ---------------------------------------------------------------------------
// Join Control
// ---------------------------------------------------------------------------

control Join(
    /* User */
    inout join_control_h    join_control,
    inout metadata_t        meta,
    /* Intrinsic */
    inout bit<3>      drop_ctl)
{
    Hash<bit<HASH_SIZE>>(HASH_ALG) hasher1;
    Hash<bit<HASH_SIZE>>(HASH_ALG) hasher2;
    Hash<bit<HASH_SIZE>>(HASH_ALG) hasher3;

    action drop() {
        drop_ctl = 1;
    }

    table tb_drop {
        actions = {
            drop;
        }
        default_action = drop();
        size = 1;
    }


    /************************ hash tables ************/

    #define CREATE_HASH_TABLE(N)                                                        \
    Register<bit<KEY_SIZE>, bit<HASH_SIZE>>(TABLE_SIZE)  hash_table_##N;                \
                                                                                        \
    RegisterAction<bit<KEY_SIZE>, bit<HASH_SIZE>, bit<KEY_SIZE>>(hash_table_##N)        \
        build_##N = {                                                                   \
            void apply(inout bit<KEY_SIZE> register_data, out bit<KEY_SIZE> found) {    \
                found = 0;                                                              \
                if(register_data == 0){                                                 \
                    register_data = join_control.build_key;                             \
                    /* any data so it doesnt trigger build on next table */             \
                    found = 1;                                                          \
                }                                                                       \
            }                                                                           \
    };                                                                                  \
                                                                                        \
    RegisterAction<bit<KEY_SIZE>, bit<HASH_SIZE>, bit<KEY_SIZE>>(hash_table_##N)        \
        probe_##N = {                                                                   \
            void apply(inout bit<KEY_SIZE> register_data, out bit<KEY_SIZE> result) {   \
                result = register_data;                                                 \
            }                                                                           \
    };                                                                                  \

    CREATE_HASH_TABLE(1)
    CREATE_HASH_TABLE(2)
    CREATE_HASH_TABLE(3)
    CREATE_HASH_TABLE(4)
    CREATE_HASH_TABLE(5)
    CREATE_HASH_TABLE(6)
    CREATE_HASH_TABLE(7)
    CREATE_HASH_TABLE(8)
    CREATE_HASH_TABLE(9)
    CREATE_HASH_TABLE(10)
    CREATE_HASH_TABLE(11)
    CREATE_HASH_TABLE(12)
    CREATE_HASH_TABLE(13)
    CREATE_HASH_TABLE(14)
    CREATE_HASH_TABLE(15)

    apply {
        if(join_control.isValid() && (drop_ctl != 1)) {
            @atomic {
                if (join_control.stage == 1) {
                    meta.hash_key = hasher1.get(join_control.build_key);
                }
                else {
                    /* Ingress */
                    if (meta.pipeline == 0) {
                        meta.hash_key = hasher2.get(join_control.probe1_key);
                    }
                    /* Egress */
                    else {
                        meta.hash_key = hasher3.get(join_control.probe2_key);
                    }
                }

                #define CREATE_JOIN_LOGIC(N)                                \
                /* BUILD */                                                 \
                if (join_control.stage == 1) {                              \
                    /* if build, and not inserted yet */                    \
                    if (meta.found == 0) {                                  \
                        meta.found = build_##N.execute(meta.hash_key);      \
                    }                                                       \
                }                                                           \
                /* PROBE */                                                 \
                else if (join_control.stage == 3) {                         \
                    if (meta.pipeline == 0) {                               \
                        if (meta.found != join_control.probe1_key)          \
                            meta.found = probe_##N.execute(meta.hash_key);  \
                    }                                                       \
                    else {                                                  \
                        if (meta.found != join_control.probe2_key)          \
                            meta.found = probe_##N.execute(meta.hash_key);  \
                    }                                                       \
                }                                                           \

                CREATE_JOIN_LOGIC(1)
                CREATE_JOIN_LOGIC(2)
                CREATE_JOIN_LOGIC(3)
                CREATE_JOIN_LOGIC(4)
                CREATE_JOIN_LOGIC(5)
                CREATE_JOIN_LOGIC(6)
                CREATE_JOIN_LOGIC(7)
                CREATE_JOIN_LOGIC(8)
                CREATE_JOIN_LOGIC(9)
                CREATE_JOIN_LOGIC(10)
                CREATE_JOIN_LOGIC(11)
                CREATE_JOIN_LOGIC(12)
                CREATE_JOIN_LOGIC(13)
                CREATE_JOIN_LOGIC(14)
                CREATE_JOIN_LOGIC(15)

                /* Packet used during build, wont be forwarded */
                if(join_control.stage == 1) {
                    tb_drop.apply();
                }
                else
                if (join_control.stage == 3) {
                    if (meta.pipeline == 0) {
                        if (meta.found != join_control.probe1_key)
                            tb_drop.apply();
                    }
                    else {
                        if (meta.found != join_control.probe2_key)
                            tb_drop.apply();
                    }
                }

                if (join_control.stage != 3 && join_control.stage != 0)
                    join_control.stage = join_control.stage - 1;
            }
        }
    }
}


/* ===================================================== Ingress ===================================================== */

control SwitchIngress(
    /* User */
    inout header_t      hdr,
    inout metadata_t    meta,
    /* Intrinsic */
    in ingress_intrinsic_metadata_t                     ig_intr_md,
    in ingress_intrinsic_metadata_from_parser_t         ig_prsr_md,
    inout ingress_intrinsic_metadata_for_deparser_t     ig_dprsr_md,
    inout ingress_intrinsic_metadata_for_tm_t           ig_tm_md)
{
    /* Forward */
    action hit(PortId_t port) {
        ig_tm_md.ucast_egress_port = port;
    }

    action miss(bit<3> drop) {
        ig_dprsr_md.drop_ctl = drop; // drop packet.
    }

    Join() join1;

    table forward {
        key = {
            hdr.ethernet.dst_addr : exact;
        }

        actions = {
            hit;
            @defaultonly miss;
        }

        const default_action = miss(0x1);
        size = 1024;
    }

    apply {
        // Set timestamps header
        hdr.ethernet.ether_type = ETHERTYPE_BENCHMARK;
        hdr.timestamps.setValid();
        hdr.timestamps = {0, 0, 0, 0, 0, 0};
        
        /* Ingress IEEE 1588 timestamp (in nsec) taken at the ingress MAC. */
        hdr.timestamps.t0 = ig_intr_md.ingress_mac_tstamp;

        /* Global timestamp (ns) taken upon arrival at ingress. */
        hdr.timestamps.t1 = ig_prsr_md.global_tstamp;

        forward.apply();

        // Apply join
        meta = {0, 0, 0};
        join1.apply(hdr.join_control, meta, ig_dprsr_md.drop_ctl);
    }
}

/* ===================================================== Egress ===================================================== */

control SwitchEgress(
    /* User */
    inout header_t      hdr,
    inout metadata_t    meta,
    /* Intrinsic */
    in egress_intrinsic_metadata_t                      eg_intr_md,
    in egress_intrinsic_metadata_from_parser_t          eg_prsr_md,
    inout egress_intrinsic_metadata_for_deparser_t      eg_dprsr_md,
    inout egress_intrinsic_metadata_for_output_port_t   eg_oport_md)
{
    Join() join2;
    
    apply {
        // Time snapshot taken when the packet is enqueued (in nsec).
        hdr.timestamps.t2 = eg_intr_md.enq_tstamp;

        // Time delta between the packet's enqueue and dequeue time.
        hdr.timestamps.t3 = eg_intr_md.enq_tstamp + eg_intr_md.deq_timedelta;

        /* Global timestamp (ns) taken upon arrival at egress. */
        hdr.timestamps.t4 = eg_prsr_md.global_tstamp;

        // Apply join
        meta = {0, 0, 1};
        join2.apply(hdr.join_control, meta, eg_dprsr_md.drop_ctl);
    }
}


/* ===================================================== Final Pipeline ===================================================== */
Pipeline(
    SwitchIngressParser(),
    SwitchIngress(),
    SwitchIngressDeparser(),
    SwitchEgressParser(),
    SwitchEgress(),
    SwitchEgressDeparser()
) pipe;

Switch(pipe) main;
