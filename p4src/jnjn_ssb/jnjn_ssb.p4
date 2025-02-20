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
#include "common/hashing_keys.p4"

/* ===================================================== Ingress ===================================================== */

// ---------------------------------------------------------------------------
// Join Control
// ---------------------------------------------------------------------------
control Join(
    /* User */
    inout join_control_h      join_control,
    /* Intrinsic */
    inout bit<3>      drop_ctl)
    /* Number of distinct entries*/
    (bit<32> table_size)
{
    join_hash() join_key;

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

    #define CREATE_HASH_TABLE(N)                                                \
    Register<bit<32>, bit<HASH_SIZE>>(table_size)  hash_table_##N;              \
                                                                                \
    RegisterAction<bit<32>, bit<HASH_SIZE>, bit<32>>(hash_table_##N)            \
        build_##N = {                                                           \
            void apply(inout bit<32> register_data, out bit<32> inserted){      \
                inserted = 0;                                                   \
                if(register_data == 0){                                         \
                    register_data = join_control.data;                          \
                    /* any data so it doesnt trigger build  on next table*/     \
                    inserted = 1;                                               \
                }                                                               \
            }                                                                   \
    };                                                                          \
                                                                                \
    RegisterAction<bit<32>, bit<HASH_SIZE>, bit<32>>(hash_table_##N)            \
        probe_##N = {                                                           \
            void apply(inout bit<32> register_data, out bit<32> result){        \
                result = register_data;                                         \
            }                                                                   \
    };                                                                          \
                                                                                \
    RegisterAction<bit<32>, bit<HASH_SIZE>, bit<32>>(hash_table_##N)            \
        flush_##N = {                                                           \
            void apply(inout bit<32> register_data, out bit<32> result){        \
                register_data = 0;                                              \
                result = 0;                                                     \
            }                                                                   \
    };

    CREATE_HASH_TABLE(1)
    CREATE_HASH_TABLE(2)
    CREATE_HASH_TABLE(3)
    CREATE_HASH_TABLE(4)
    CREATE_HASH_TABLE(5)

    apply {
        if(join_control.isValid() && (drop_ctl != 1)) {
            @atomic {
                join_key.apply(join_control, join_control.hash_key);                                                             

                
                #define CREATE_JOIN_LOGIC(N)                                              \
                /* BUILD */                                                               \
                if (join_control.ctl_type == ControlType.BUILD) {                         \
                    /* if build, and not inserted yet */                                  \
                    if(join_control.inserted == 0) {                                      \
                        join_control.inserted = build_##N.execute(join_control.hash_key); \
                    }                                                                     \
                }                                                                         \
                /* PROBE */                                                               \
                else if (join_control.ctl_type == ControlType.PROBE) {                    \
                    /* if not probed in previous table */                                 \
                    if (join_control.inserted == 0)                                       \
                        join_control.inserted = probe_##N.execute(join_control.hash_key); \
                }                                                                         \
                /* FLUSH */                                                               \
                else if (join_control.ctl_type == ControlType.FLUSH) {                    \
                    /* execute the action on every entry in the register */               \
                    flush_##N.sweep();                                                    \
                }                                                                         

                CREATE_JOIN_LOGIC(1)
                CREATE_JOIN_LOGIC(2)
                CREATE_JOIN_LOGIC(3)
                CREATE_JOIN_LOGIC(4)
                CREATE_JOIN_LOGIC(5)

                /* Packet used during build, wont be forwarded */
                if(join_control.ctl_type == ControlType.BUILD){
                    tb_drop.apply();
                }
                /* Packet probed the table */
                else if(join_control.ctl_type == ControlType.PROBE){
                    /* If probed index doesnt contain same data, drop*/
                    if (join_control.inserted != join_control.data)
                        tb_drop.apply();
                }
                // /* If flushing the table, drop */
                else if(join_control.ctl_type == ControlType.FLUSH){
                    tb_drop.apply();
                }

                /* If packet has reached this point, it means it has probed successfully */

            } // @atomic hint
        } // Packet validation 
    } // Apply


} // Join control

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

    Join(TABLE_SIZE) join1;

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
        forward.apply();

        if (hdr.join_control.isValid())
            join1.apply(hdr.join_control, ig_dprsr_md.drop_ctl);
    }
}

/* ===================================================== Egress ===================================================== */

// ---------------------------------------------------------------------------
// Egress Control
// ---------------------------------------------------------------------------
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
    apply {}
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
