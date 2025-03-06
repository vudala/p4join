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
export PROGRAM=jnjn_left_deep
# or
export PROGRAM=jnjn_right_deep
# or
export PROGRAM=forward

cd ~/src
./../p4_build.sh $PROGRAM

# Run switchd
cd ~/bf-sde-9.9.0
./run_switchd.sh -p jnjn_ssb -c $SDE_INSTALL/share/p4/targets/tofino2/jnjn_ssb/jnjn_ssb.conf --arch tf2

# Run tofino model
# Use -f to point to ports config
cd ~/bf-sde-9.9.0
./run_tofino_model.sh -p jnjn_ssb -c $SDE_INSTALL/share/p4/targets/tofino2/jnjn_ssb/jnjn_ssb.conf --arch tf2 \
    -f /home/dev/Documents/p4join/p4src/jnjn_ssb/ports.json

# Control plane set ports mapping
bfrt_python /home/dev/Documents/p4join/p4src/$PROGRAM/bfrt_python/setup.py true

