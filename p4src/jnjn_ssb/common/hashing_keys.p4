// Constants need udpate after tests to max size of tofino stage
// TABLE_SIZE 64K and HASH_SIZE 16 bits
// tests: TABLE_SIZE 16 and HASH_SIZE 4 bits
#define TABLE_SIZE 94000
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
    //in  header_t   hdr,
    in qtrp_h      qtrp,
    out bit<HASH_SIZE>    sel_hash)
{
    Hash<bit<HASH_SIZE>>(HASH_ALG) key_hash;
    
    apply {
        sel_hash = key_hash.get((bit<HASH_SIZE>)qtrp.fld01_uint32);
    }
}

control group_hash(  
    //in  header_t   hdr,
    in qtrp_h      qtrp,
    out bit<HASH_SIZE>    sel_hash)
{
    Hash<bit<HASH_SIZE>>(HASH_ALG) group_key_hash;
    
    apply {
        sel_hash = group_key_hash.get((bit<HASH_SIZE>)qtrp.fld06_uint32);
    }
}