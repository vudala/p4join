# P4 JoinJoin

## Overview 

Aside from the source .p4 files that are used by the bf-p4c compiler to generate
the data plane binaries, this repo contains scripts that can be used to test it.

## Dependencies
- python3.10 with pip (to install and use scapy)
- cmake (to compile ssb-dbgen)

I am also assuming that you execute the commands on a proper Tofino 2 simulation
environment.

Use https://github.com/p4lang/open-p4studio as reference to understand and
possibly setup the environment.

## Installation 
```bash
git clone git@github.com:vudala/p4join.git --recursive
cd p4join

pip install -r requirements.txt
```

## Simulation setup

Once you have installed the dependencies and cloned this repository, you are
ready to execute the simulation.

The simulation is constructed via multiple steps. Each one of them must be 
executed in order.


### Step 1 - Create virtual ethernet interfaces (veths)

For the Tofino 2 model to be able to receive traffic on its ports, it must have
an interface that we can interact with. We will use virtual ethernet interfaces
to send and receive traffic that goes through the switch's ports.

The following script creates 64 veths named veth0 up to veth63:

```bash
cd ~/bf-sde-9.9.0/install/bin/
sudo ./veth_setup.sh
```

The number of veths is confirgurable, but the default is 64.

### Step 2 - Compile the P4 program

In the compilations targets folder of the machine (~/src in my case) that
you are running this setup, create symlinks that points to the projects in this
repository, wherever you cloned it. Something like this:

```bash
cd ~/src
ln -s ~/Documents/p4join/p4src/jnjn_left_deep jnjn_left_deep
ln -s ~/Documents/p4join/p4src/jnjn_right_deep jnjn_right_deep
ln -s ~/Documents/p4join/p4src/forward forward
```

Then use a env var to select which one of the you would like to use:

```bash
export P4TARGET=jnjn_left_deep
# or
export P4TARGET=jnjn_right_deep
# or
export P4TARGET=forward
```

Compile the P4 program, use the following command:
```bash
cd ~/src
./../p4_build.sh $P4TARGET
```

### Step 3 - Run switchd

Once the binaries are properly compiled, run switchd. It manages the 
simulated switch and enables us to execute the control plane for Tofino 2.

Create a terminal session (1) and execute the following command:

```bash
cd ~/bf-sde-9.9.0
./run_switchd.sh -p $P4TARGET -c $SDE_INSTALL/share/p4/targets/tofino2/$P4TARGET/$P4TARGET.conf --arch tf2
```

### Step 4 - Run Tofino 2 model

To run the tofino model, create another terminal session (2) and run the 
following commands. The exact path location of ports.json may differ based on
where you cloned this repo.

```bash
cd ~/bf-sde-9.9.0
./run_tofino_model.sh -p $P4TARGET -c $SDE_INSTALL/share/p4/targets/tofino2/$P4TARGET/$P4TARGET.conf --arch tf2 \
    -f /home/dev/Documents/p4join/p4src/ports.json
```

### Step 5 - Update the routing tables via control plane

Go back to terminal 1, and wait until you are able to interact with the bfshell.
This process might take tens of seconds, so be patient.
Once you are, execute the following script to upda      te the routing tables of the
switch:

```bash
bfrt_python /home/dev/Documents/p4join/p4src/jnjn_left_deep/bfrt_python/setup.py true
bfrt_python /home/dev/Documents/p4join/p4src/jnjn_right_deep/bfrt_python/setup.py true
bfrt_python /home/dev/Documents/p4join/p4src/forward/bfrt_python/setup.py true
```

This also takes a while, but once you are able to interact with the bfrt shell
again, the setup is done.
Then you can start sending packets through the switch.

### Optional step

After setting up the simulation, you can run the command `bfrt` on terminal 1,
then you will be able to inspect the routing tables, the ports and other aspects
of the managed switch.

## Testing

### `gen_datasets.sh`

Generate SSB datasets in datasets directory

### `send.py`
Read a SSB csv and send it through veths. It is intended to be used as a
building block for larger queries.

Example 1:
```bash
# Performs build on Ingress stage
sudo python3 send.py --stage 1 -c dataset_samples/customers.sample.csv \
    -bk c_custkey -pk null --threads 4

# Probe during Ingress and Egress stage
sudo python3 send.py --stage 3 -l dataset_samples/lineorder.sample.csv \
    -bk c_custkey -pk lo_custkey --threads 4

# End join
sudo python3 send.py --stage 0 -l null -bk null -pk null
```

Example 2:
```bash
# Performs build on Ingress stage
sudo python3 send.py --stage 1 -c dataset_samples/customers.sample.csv \
    -bk c_custkey -pk null --threads 4

# Probe during Ingress and build during Egress stage
sudo python3 send.py --stage 2 -l dataset_samples/lineorder.small.sample.csv \
    -bk lo_suppkey -pk lo_custkey --threads 4

# Probe during Ingress and Egress stage
sudo python3 send.py --stage 3 -s dataset_samples/supplier.sample.csv \
    -bk null -pk s_suppkey --threads 4

# End join
sudo python3 send.py --stage 0 -l null -bk null -pk null
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
