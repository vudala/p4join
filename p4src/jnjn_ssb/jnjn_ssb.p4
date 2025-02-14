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
                if(join_control.build == 1){                                              \
                    /* entry is not empty, go to next hash table */                       \
                    if(join_control.inserted == 0){                                       \
                        join_control.inserted = build_##N.execute(join_control.hash_key); \
                    }                                                                     \
                /* PROBE */                                                               \
                }else{                                                                    \
                    /* key did not match, probe the next hash table */                    \
                    if(join_control.inserted != join_control.data){                       \
                        join_control.inserted = probe_##N.execute(join_control.hash_key); \
                    }                                                                     \
                }

                CREATE_JOIN_LOGIC(1)
                CREATE_JOIN_LOGIC(2)
                CREATE_JOIN_LOGIC(3)
                CREATE_JOIN_LOGIC(4)
                CREATE_JOIN_LOGIC(5)

                /* key not found in probe */
                if(join_control.inserted != join_control.data){
                    tb_drop.apply();
                }
                else if(join_control.build == 1){
                    tb_drop.apply();
                }
                /* Return flag to probe phase (fld07_uint16 - 1) for the case of sequence of joins.
                Otherwise, in case of a single join the packet is shipped to the server anyway*/
                join_control.build = join_control.build - 1;


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
