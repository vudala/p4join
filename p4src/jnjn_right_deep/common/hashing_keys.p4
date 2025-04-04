#include "headers.p4"

// Constants need udpate after tests to max size of tofino stage
// TABLE_SIZE 64K and HASH_SIZE 16 bits
// tests: TABLE_SIZE 16 and HASH_SIZE 4 bits


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
// control join_hash(  
//     in bit<KEY_SIZE>      key,
//     out bit<HASH_SIZE>    sel_hash)
// {
//     Hash<bit<HASH_SIZE>>(HASH_ALG) hasher;
    
//     apply {
//         sel_hash = hasher.get(key);
//     }
// }
