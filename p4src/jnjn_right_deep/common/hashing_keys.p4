// Constants need udpate after tests to max size of tofino stage
// TABLE_SIZE 64K and HASH_SIZE 16 bits
// tests: TABLE_SIZE 16 and HASH_SIZE 4 bits
#define TABLE_SIZE 65536
#define HASH_SIZE 16
#define HASH_ALG HashAlgorithm_t.CRC16

// enum HashAlgorithm_t {
//     IDENTITY,
//     RANDOM,
//     CRC8,
//     CRC16,
//     CRC32,
//     CRC64,
//     CUSTOM
// }

// ---------------------------------------------------------------------------
// Calculating Hash
// ---------------------------------------------------------------------------
control join_hash(  
    in join_control_h     join_control,
    out bit<HASH_SIZE>    sel_hash)
{
    Hash<bit<HASH_SIZE>>(HASH_ALG) build_hash;
    Hash<bit<HASH_SIZE>>(HASH_ALG) probe_hash;
    
    apply {
        if (join_control.stage == 1) {
            sel_hash = build_hash.get(join_control.build_key);
        }
        else {
            sel_hash = probe_hash.get(
                join_control.probe_key[join_control.curr_pipeline]
            );
        }
    }
}
