#!/bin/bash
#
# This script runs on the server and client and
# sets module options for the mlx4 ethernet device.

die() { echo $*; exit -1; }
[[ $# == 2 ]] || \
  die "Usage: $0 <ethernet device> <module options>"
DEVICE=$1
MODULE_OPTS=$2

ifconfig $DEVICE down
modprobe -r igb # remove the module
modprobe igb $MODULE_OPTS

# check if we need to enable in-kernel RPS
if [[ $MODULE_OPTS != *"RSS"* ]]; then
  # here we need to enable the kernel-based RPS
  for QUEUE_DIR in /sys/class/net/$DEVICE/queues/rx-*; do
    #TODO: Generalize the mask
    echo 7fff > $QUEUE_DIR/rps_cpus
  done
fi
