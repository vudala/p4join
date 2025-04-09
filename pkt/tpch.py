from scapy.fields import *
from scapy.packet import Packet

# P_PARTKEY		SERIAL,
# P_NAME			VARCHAR(55),
# P_MFGR			CHAR(25),
# P_BRAND			CHAR(10),
# P_TYPE			VARCHAR(25),
# P_SIZE			INTEGER,
# P_CONTAINER		CHAR(10),
# P_RETAILPRICE	DECIMAL,
# P_COMMENT		VARCHAR(23)

class Part(packet):
    fields_desc = [
        IntField("p_partkey", 0),
        StrFixedLenField("p_name", "", 55),
        StrFixedLenField("p_mfgr", "", 25),
        StrFixedLenField("p_brand", "", 10),
        StrField("p_type", ""),
        IntField("p_size", 0),
        StrFixedLenField("p_container", "", 10),
        DecField("p_retailprice", 0.0, 2),
        StrField("p_comment", ""),
    ]

