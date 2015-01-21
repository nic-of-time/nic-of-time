#!/bin/bash
#
# This script runs on the server and client and
# sets module options for the mlx4 ethernet device.

die() { echo $*; exit -1; }
[[ $# == 2 ]] || \
  die "Usage: $0 <ethernet device> <module options>"
DEVICE=$1
MODULE_OPTS=$2

tee /etc/modprobe.d/mlx4.conf<<EOF
softdep mlx4_core post: mlx4_en
$MODULE_OPTS
EOF
ifconfig $DEVICE down
rmmod mlx4_{en,ib,core}
modprobe mlx4_{en,ib,core}

# check if we need to enable in-kernel RFS
if [[ $MODULE_OPTS != *"log_num_mgm_entry_size"* ]]; then
  # here we need to enable the kernel-based RFS
  echo 32768 > /proc/sys/net/core/rps_sock_flow_entries
  for QUEUE_DIR in /sys/class/net/$DEVICE/queues/rx-*; do
    echo 2048 > $QUEUE_DIR/rps_flow_cnt
  done
fi

# check if we need to enable in-kernel RPS
if [[ $MODULE_OPTS != *"udp_rss"* ]]; then
  # here we need to enable the kernel-based RPS
  for QUEUE_DIR in /sys/class/net/$DEVICE/queues/rx-*; do
    #TODO: Generalize the mask
    echo 7fff > $QUEUE_DIR/rps_cpus
  done
fi
