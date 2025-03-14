#
#
#  COMMANDS JUST FOR REFERENCE
#
#

# Create symlink
ln -s path/to/src symname

# Up veths
cd ~/bf-sde-9.9.0/install/bin/
sudo ./veth_setup.sh

# Build
export P4TARGET=jnjn_left_deep
# or
export P4TARGET=jnjn_right_deep
# or
export P4TARGET=forward

cd ~/src
./../p4_build.sh $P4TARGET

# Run switchd
cd ~/bf-sde-9.9.0
./run_switchd.sh -p jnjn_ssb -c $SDE_INSTALL/share/p4/targets/tofino2/jnjn_ssb/jnjn_ssb.conf --arch tf2

# Run tofino model
# Use -f to point to ports config
cd ~/bf-sde-9.9.0
./run_tofino_model.sh -p jnjn_ssb -c $SDE_INSTALL/share/p4/targets/tofino2/jnjn_ssb/jnjn_ssb.conf --arch tf2 \
    -f /home/dev/Documents/p4join/p4src/jnjn_ssb/ports.json

# Control plane set ports mapping
bfrt_python /home/dev/Documents/p4join/p4src/$P4TARGET/bfrt_python/setup.py true

