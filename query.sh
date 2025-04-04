sudo python3 send_rd.py --stage 1 -c dataset_samples/customers.sample.csv \
    -bk c_custkey -pk null null &

sudo python3 send_rd.py --stage 2 -s dataset_samples/supplier.sample.csv \
    -bk s_suppkey -pk null null &
