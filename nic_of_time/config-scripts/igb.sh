#!/bin/bash
#
# This script runs on the server and client and
# sets module options for the mlx4 ethernet device.

die() { echo $*; exit -1; }
[[ $# == 3 ]] || \
  die "Usage: $0 <ethernet device> <module options> <ip address>"
DEVICE=$1
MODULE_OPTS=$2
IP_ADDRESS=$3

{
  ifconfig $DEVICE down;
  modprobe -r igb;
  modprobe igb $MODULE_OPTS;
  sleep 5;
  ifconfig $DEVICE up;
  ifconfig $DEVICE up $IP_ADDRESS;
} & disown

# check if we need to enable in-kernel RPS
if [[ $MODULE_OPTS != *"RSS"* ]]; then
  # here we need to enable the kernel-based RPS
  for QUEUE_DIR in /sys/class/net/$DEVICE/queues/rx-*; do
    #TODO: Generalize the mask
    echo 7fff > $QUEUE_DIR/rps_cpus
    cat $QUEUE_DIR/rps_cpus > /tmp/t
  done
fi
