#
#
#  COMMANDS JUST FOR REFERENCE
#
#

# Create symlink
ln -s path/to/src symname

cd ~/src
./../p4_build.sh jnjn_ssb

cd ~/bf-sde-9.9.0
./run_switchd.sh -p jnjn_ssb -c $SDE_INSTALL/share/p4/targets/tofino2/jnjn_ssb/jnjn_ssb.conf --arch tf2

./run_tofino_model.sh -p jnjn_ssb -c $SDE_INSTALL/share/p4/targets/tofino2/jnjn_ssb/jnjn_ssb.conf --arch tf2

bfrt_python /home/dev/Documents/p4join/p4src/jnjn_ssb/bfrt_python/setup.py true