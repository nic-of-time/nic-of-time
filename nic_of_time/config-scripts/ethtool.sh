#!/bin/bash
#
# This script runs on the server and client and
# sets ethtool options the ethernet device.

die() { echo $*; exit -1; }
[[ $# == 4 ]] || \
  die "Usage: $0 <ethernet device> <ethtool options> <mtu> <tx>"
DEVICE=$1
ETHTOOL_OPTS=$2
MTU=$3
TX=$4

echo "config-offload-options running on $HOSTNAME"
echo "$DEVICE $ETHTOOL_OPTS $MTU $TX"
exit 0

ifconfig $DEVICE up
ifconfig $DEVICE mtu $MTU
ifconfig $DEVICE txqueuelen $TX
ifconfig $DEVICE $SERVER_IP

ethtool -K $DEVICE $ETHTOOL_OPTS || \
  die "Unable to configure with $ETHTOOL_OPTS."
ethtool -K $DEVICE $ETHTOOL_OPTS \
  || die "Unable to configure with $ETHTOOL_OPTS."
