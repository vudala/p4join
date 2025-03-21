# Send build packets
sudo python3 send.py --stage 1 -c datasets/customers.csv \
    -bk c_custkey -pk null --threads 4

sleep 60

# Build done
sudo python3 send.py --stage 0 -l null -bk null -pk null

# Probe on built table
sudo python3 send.py --stage 2 -l datasets/lineorder.csv \
    -bk lo_suppkey -pk lo_custkey --threads 4

sleep 60

# Probe 1 done
sudo python3 send.py --stage 0 -l null -bk null -pk null

# Probe intermediary result
sudo python3 send.py --stage 3 -s datasets/supplier.csv \
    -bk null -pk s_suppkey --threads 4

sleep 60

# Probe 2 done, Query done
sudo python3 send.py --stage 0 -l null -bk null -pk null
