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

        hdr.ethernet.ether_type = ETHERTYPE_BENCHMARK;

        hdr.timestamps.setValid();

        hdr.timestamps.t2 = 0;
        hdr.timestamps.t3 = 0;
        hdr.timestamps.t4 = 0;
        hdr.timestamps.t5 = 0;
        
        /* Ingress IEEE 1588 timestamp (in nsec) taken at the ingress MAC. */
        hdr.timestamps.t0 = ig_intr_md.ingress_mac_tstamp;

        /* Global timestamp (ns) taken upon arrival at ingress. */
        hdr.timestamps.t1 = ig_prsr_md.global_tstamp;
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
    apply {
        // Time snapshot taken when the packetis enqueued (in nsec).
        hdr.timestamps.t2 = eg_intr_md.enq_tstamp;
        // Time delta between the packet's enqueue and dequeue time.
        hdr.timestamps.t3 = eg_intr_md.enq_tstamp + eg_intr_md.deq_timedelta;

        /* Global timestamp (ns) taken upon arrival at egress. */
        hdr.timestamps.t4 = eg_prsr_md.global_tstamp;
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
