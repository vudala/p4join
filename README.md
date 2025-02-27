# P4 JoinJoin

## Dependencies
- python3.10 with pip (to install and use scapy)
- cmake (to compile ssb-dbgen)

## Installation 
```bash
git clone git@github.com:vudala/p4join.git --recursive
cd p4join

pip install -r requirements.txt
```

## Overview 

Aside from the source .p4 files that are used by the bf-p4c compiler to generate
the data plane binaries, this repo contains scripts that can be used to test it.

Commands to compile the p4 and run the simulator can be found at
`useful_cmds.sh`.

## Scripts

### `gen_datasets.sh`

Generate SSB datasets in datasets directory

### `send.py`
Read a SSB csv and send it through veths. It is intended to be used as a
building block for larger queries.

Example:
```bash
sudo python3 send.py --build -c dataset_samples/customers.sample.csv \
-k c_custkey --threads 4

sudo python3 send.py --probe -l dataset_samples/lineorder.sample.csv \
-k lo_custkey --threads 4
```

This performs a join between customer.c_custkey and lineorder.lo_custkey.
It happens in the following way:
- customers is sent first in build phase, the workload is split between 4
threads, that will forward packets to the same destination but through different
interfaces.
- then the lineorder table is sent on probe phase, again with 4 threads

With this, a join is made.


### `sniff.py`

Sniff destiny iface and display received packets
