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

## Usage
`gen_datasets.sh` generate SSB datasets in datasets directory

`send.py` read a SSB csv and send it to iface

`sniff.py` sniff iface and display received packets
