#
#
#  COMMANDS JUST FOR REFERENCE
#
#

# Create symlink
ln -s path/to/src symname

cd ~/src
./../p4_build.sh lineorder

cd ~/bf-sde-9.9.0
./run_switchd.sh -p lineorder -c $SDE_INSTALL/share/p4/targets/tofino2/lineorder/lineorder.conf --arch tf2

./run_tofino_model.sh -p lineorder -c $SDE_INSTALL/share/p4/targets/tofino2/lineorder/lineorder.conf --arch tf2

bfrt_python /home/dev/src/lineorder/bfrt_python/setup.py true