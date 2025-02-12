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

/* ===================================================== Ingress ===================================================== */

// ---------------------------------------------------------------------------
// Join Control
// ---------------------------------------------------------------------------
// control Join(
//     /* User */
//     inout qtrp_h      qtrp,
//     /* Intrinsic */
//     inout bit<3>      drop_ctl)
//     /* Number of distinct entries*/
//     (bit<32> table_size)
// {
//     join_hash() join_key;

//     action drop() {
//         drop_ctl = 1;
//     }

//     table tb_drop {
//         actions = {
//             drop;
//         }
//         default_action = drop();
//         size = 1;
//     }


//     /************************ hash tables ************/
//     /* bit<32> data and bit<16> register index */

//     /* Generic header considering a 6-field table with different types */
//     // header qtrp_h {
//     //     bit<32>     fld01_uint32;   // FIELD TO BE HASHED
//     //     bit<32>     fld02_uint32;
//     //     bit<32>     fld03_uint32;
//     //     bit<16>     fld04_uint16;   // Hash key for max 65k table size in tofino-2, STORE HASHED FIELD
//     //     bit<32>     fld05_uint32;   // INSERTED OR NOT
//     //     bit<32>     fld06_uint32;   // former fld06_date field, now used for group key (moved to field 10)
//     //     bit<16>     fld07_uint16;   /* Field 7 build/probe flag */ 1 BUILD, != 1 PROBE
//     //     bit<16>     fld08_uint16;   /* Field 8 group hash */
//     //     bit<16>     fld09_uint16;   /* Field 9 choose operation */
//     //     bit<16>     fld10_uint16;   /* Field 10 groupkey */    
//     //     bit<16>     fld11_uint16;   /* Query id */ 
//     // }

//     #define CREATE_HASH_TABLE(N)                                                \
//     Register<bit<32>, bit<HASH_SIZE>>(table_size)  hash_table_##N;              \
//                                                                                 \
//     RegisterAction<bit<32>, bit<HASH_SIZE>, bit<32>>(hash_table_##N)            \
//         build_##N = {                                                           \
//             void apply(inout bit<32> register_data, out bit<32> inserted){      \
//                 inserted = 0;                                                   \
//                 if(register_data == 0){                                         \
//                     register_data = qtrp.fld01_uint32;                          \
//                     inserted = 1;                                               \
//                 }                                                               \
//             }                                                                   \
//     };                                                                          \
//                                                                                 \
//     RegisterAction<bit<32>, bit<HASH_SIZE>, bit<32>>(hash_table_##N)            \
//         probe_##N = {                                                           \
//             void apply(inout bit<32> register_data, out bit<32> result){        \
//                 result = register_data;                                         \
//             }                                                                   \
//     };                                                                          \

//     CREATE_HASH_TABLE(1)
//     CREATE_HASH_TABLE(2)
//     CREATE_HASH_TABLE(3)
//     CREATE_HASH_TABLE(4)
//     CREATE_HASH_TABLE(5)
//     CREATE_HASH_TABLE(6)
//     CREATE_HASH_TABLE(7)
//     CREATE_HASH_TABLE(8)
//     CREATE_HASH_TABLE(9)
//     CREATE_HASH_TABLE(10)
//     CREATE_HASH_TABLE(11)
//     CREATE_HASH_TABLE(12)
//     CREATE_HASH_TABLE(13)
//     CREATE_HASH_TABLE(14)
//     CREATE_HASH_TABLE(15)
//     CREATE_HASH_TABLE(16)
//     CREATE_HASH_TABLE(17)
//     CREATE_HASH_TABLE(18)
//     CREATE_HASH_TABLE(19)
//     CREATE_HASH_TABLE(20)

//     apply {
//         if(qtrp.isValid() && (drop_ctl != 1)) {
//             @atomic {
//                 join_key.apply(qtrp, qtrp.fld04_uint16);                                                             


//                 /*
//                 * Using qtrp.fld07_uint16 to keep the table name. Value 1 means build, otherwise probe.
//                 */
//                 #define CREATE_JOIN_LOGIC(N)
//                 /* BUILD */                                      \
//                 if(qtrp.fld07_uint16 == 1){                                       \
//                     /* entry is not empty, go to next hash table */               \
//                     if(qtrp.fld05_uint32 == 0){                                   \
//                         qtrp.fld05_uint32 = build_##N.execute(qtrp.fld04_uint16); \
//                     }
//                 /* PROBE */                                                       \
//                 }else{                                                            \
//                     /* key did not match, probe the next hash table */            \
//                     if(qtrp.fld05_uint32 != qtrp.fld01_uint32){                   \
//                         qtrp.fld05_uint32 = probe_##N.execute(qtrp.fld04_uint16); \
//                     }                                                             \
//                 }  

//                 CREATE_JOIN_LOGIC(1)
//                 CREATE_JOIN_LOGIC(2)
//                 CREATE_JOIN_LOGIC(3)
//                 CREATE_JOIN_LOGIC(4)
//                 CREATE_JOIN_LOGIC(5)
//                 CREATE_JOIN_LOGIC(6)
//                 CREATE_JOIN_LOGIC(7)
//                 CREATE_JOIN_LOGIC(8)
//                 CREATE_JOIN_LOGIC(9)
//                 CREATE_JOIN_LOGIC(10)
//                 CREATE_JOIN_LOGIC(11)
//                 CREATE_JOIN_LOGIC(12)
//                 CREATE_JOIN_LOGIC(13)
//                 CREATE_JOIN_LOGIC(14)
//                 CREATE_JOIN_LOGIC(15)
//                 CREATE_JOIN_LOGIC(16)
//                 CREATE_JOIN_LOGIC(17)
//                 CREATE_JOIN_LOGIC(18)
//                 CREATE_JOIN_LOGIC(19)
//                 CREATE_JOIN_LOGIC(20)

//                 /* key not found in probe */
//                 if(qtrp.fld05_uint32 != qtrp.fld01_uint32){
//                     tb_drop.apply();
//                 }else if(qtrp.fld07_uint16 == 1){
//                     tb_drop.apply();
//                 }
//                 /* Return flag to probe phase (fld07_uint16 - 1) for the case of sequence of joins.
//                 Otherwise, in case of a single join the packet is shipped to the server anyway*/
//                 qtrp.fld07_uint16 = qtrp.fld07_uint16 - 1;


//             } // @atomic hint
//         } // Packet validation 
//     } // Apply


// } // Join control

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
