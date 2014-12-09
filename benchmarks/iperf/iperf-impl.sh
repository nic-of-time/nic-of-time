#!/bin/bash

CLIENT=s-h0
SERVER=s-h1
#SERVER_IP=$(ssh s-h4 ip addr show fge0 \
#  | grep 'inet ' | sed -e 's/ *inet \([^\/]*\).*/\1/g')
CLIENT_IP=192.168.1.2
SERVER_IP=192.168.1.1
TIME_SECS=15
TX=10000
MTU=9000
NUM_IPERF_PROCS=8 #TODO: RPS options need to reflect this change

die() { echo $*; exit -1; }


trap 'killall' INT
killall() {
  # http://unix.stackexchange.com/questions/55558
  trap '' INT TERM
  echo "**** Shutting down... ****"
  kill -TERM 0
  wait
  echo DONE
  exit
}

[[ $# == 3 ]] || die "Usage: $0 <experiment number> <ethtool options> <module options>"
EXP_NUM=$1
ETHTOOL_OPTS=$2
MODULE_OPTS=$3

ssh $SERVER pkill -f -9 iperf; ssh $CLIENT pkill -f -9 iperf
set -x
mkdir -p iperf/$EXP_NUM
echo -e $ETHTOOL_OPTS > iperf/$EXP_NUM/ethtool_opts.txt
echo -e $MODULE_OPTS > iperf/$EXP_NUM/module_opts.txt

runIperfTCP() {
  # read a post about a bug not allowing binding to 0th CPU
  local MAX_CPUS=$1
  local PIDS=""
  for CPU in $(seq 1 2 $(($MAX_CPUS*2-1))); do
    ssh $SERVER iperf3 -s -J -f M -i 1 -p 520$CPU -A $CPU -D
  done
  sleep 1
  for CPU in $(seq 1 2 $(($MAX_CPUS*2-1))); do
    ssh $CLIENT iperf3 -c $SERVER_IP -J -P $NUM_CLIENTS \
        --time $TIME_SECS -i 1 -f M -p 520$CPU \
        --get-server-output -M 8960 -w 256K -l 256K \
        > iperf/$EXP_NUM/output-$CPU-tcp-$NUM_CLIENTS.json &
    PIDS+=" "
    PIDS+=$!
  done

  sleep $(($TIME_SECS + 8))

  EXP_RESULT=0
  for PID in $PIDS; do
    [[ -d /proc/$PID ]] && EXP_RESULT=-1
  done

  sync
  ssh $SERVER pkill -f -9 iperf; ssh $CLIENT pkill -f -9 iperf

  for CPU in $(seq 1 2 $(($MAX_CPUS*2-1))); do
    [[ ! -s iperf/$EXP_NUM/output-$CPU-tcp-$NUM_CLIENTS.json ]] && EXP_RESULT=-1
  done
}

runIperfUDP() {
  # read a post about a bug not allowing binding to 0th CPU
  local MAX_CPUS=$1
  local PIDS=""
  for CPU in $(seq 1 2 $(($MAX_CPUS*2-1))); do
    ssh $SERVER iperf3 -s -J -f M -i 1 -p 520$CPU -A $CPU -D
  done
  sleep 1
  for CPU in $(seq 1 2 $(($MAX_CPUS*2-1))); do
    ssh $CLIENT iperf3 -c $SERVER_IP -u -J -b 0 \
        -P $NUM_CLIENTS --time $TIME_SECS \
        -i 1 -f M -p 520$CPU --get-server-output \
        -l 8K > iperf/$EXP_NUM/output-$CPU-udp-$NUM_CLIENTS.json &
    PIDS+=" "
    PIDS+=$!
  done

  sleep $(($TIME_SECS + 8))

  EXP_RESULT=0
  for PID in $PIDS; do
    [[ -d /proc/$PID ]] && EXP_RESULT=-1
  done

  sync
  ssh $SERVER pkill -f -9 iperf; ssh $CLIENT pkill -f -9 iperf

  for CPU in $(seq 1 2 $(($MAX_CPUS*2-1))); do
    [[ ! -s iperf/$EXP_NUM/output-$CPU-udp-$NUM_CLIENTS.json ]] && EXP_RESULT=-1
  done
}

prepareAndRunExperiment() {
  ssh -t $SERVER sudo tee /etc/modprobe.d/mlx4.conf<<EOF
softdep mlx4_core post: mlx4_en
$MODULE_OPTS
EOF
  ssh -t $CLIENT sudo tee /etc/modprobe.d/mlx4.conf<<EOF
softdep mlx4_core post: mlx4_en
$MODULE_OPTS
EOF
  ssh -t $SERVER "sudo ifconfig fge0 down"
  ssh -t $CLIENT "sudo ifconfig fge0 down"
  ssh $SERVER sudo rmmod mlx4_{en,ib,core}
  ssh $SERVER sudo modprobe mlx4_{en,ib,core}
  ssh $CLIENT sudo rmmod mlx4_{en,ib,core}
  ssh $CLIENT sudo modprobe mlx4_{en,ib,core}

  # check if we need to enable in-kernel RFS
  if [[ $MODULE_OPTS != *"log_num_mgm_entry_size"* ]]; then
    # here we need to enable the kernel-based RFS
    echo 32768 | ssh -t $SERVER sudo tee /proc/sys/net/core/rps_sock_flow_entries
    echo 32768 | ssh -t $CLIENT sudo tee /proc/sys/net/core/rps_sock_flow_entries
    for QUEUE_DIR in /sys/class/net/fge0/queues/rx-*; do
      echo 2048 | ssh -t $SERVER sudo tee $QUEUE_DIR/rps_flow_cnt
      echo 2048 | ssh -t $CLIENT sudo tee $QUEUE_DIR/rps_flow_cnt
    done
  fi

  # check if we need to enable in-kernel RPS
  if [[ $MODULE_OPTS != *"udp_rss"* ]]; then
    # here we need to enable the kernel-based RPS
    for QUEUE_DIR in /sys/class/net/fge0/queues/rx-*; do
      #TODO: fix the mask being echo'd
      echo 7fff | ssh -t $SERVER sudo tee $QUEUE_DIR/rps_cpus
      echo 7fff | ssh -t $CLIENT sudo tee $QUEUE_DIR/rps_cpu
    done
  fi

  ssh -t $SERVER "sudo ifconfig fge0 up"
  ssh -t $SERVER "sudo ifconfig fge0 mtu $MTU"
  ssh -t $SERVER "sudo ifconfig fge0 txqueuelen $TX"
  ssh -t $SERVER "sudo ifconfig fge0 $SERVER_IP"

  ssh -t $CLIENT "sudo ifconfig fge0 up"
  ssh -t $CLIENT "sudo ifconfig fge0 mtu $MTU"
  ssh -t $CLIENT "sudo ifconfig fge0 txqueuelen $TX"
  ssh -t $CLIENT "sudo ifconfig fge0 $CLIENT_IP"

  ssh -t $SERVER "sudo ethtool -K fge0 $ETHTOOL_OPTS" \
    || die "Unable to configure $SERVER with $ETHTOOL_OPTS."
  ssh -t $SERVER "sudo ethtool -K fge0 $ETHTOOL_OPTS" \
    || die "Unable to configure $SERVER with $ETHTOOL_OPTS."
  ssh -t $CLIENT "sudo ethtool -K fge0 $ETHTOOL_OPTS" \
    || die "Unable to configure $CLIENT with $ETHTOOL_OPTS."
  ssh -t $CLIENT "sudo ethtool -K fge0 $ETHTOOL_OPTS" \
    || die "Unable to configure $CLIENT with $ETHTOOL_OPTS."
  ssh -t $SERVER "ethtool -i fge0" > iperf/$EXP_NUM/server.ethtool.txt
  ssh -t $SERVER "ethtool -k fge0" >> iperf/$EXP_NUM/server.ethtool.txt
  ssh -t $CLIENT "ethtool -i fge0" > iperf/$EXP_NUM/client.ethtool.txt
  ssh -t $CLIENT "ethtool -k fge0" >> iperf/$EXP_NUM/client.ethtool.txt

  sleep 5

  for I in {1,2,4}; do
    local NUM_CLIENTS=$I

    runIperfUDP $NUM_IPERF_PROCS

    if [[ $EXP_RESULT -ne 0 ]]; then
      echo "Error: Nonzero return from UDP experiment. Retrying once."
      runIperfUDP $NUM_IPERF_PROCS
      if [[ $EXP_RESULT -ne 0 ]]; then
        exit -1
      fi
    fi

    runIperfTCP $NUM_IPERF_PROCS

    if [[ $EXP_RESULT -ne 0 ]]; then
      echo "Error: Nonzero return from TCP experiment. Retrying once."
      runIperfTCP $NUM_IPERF_PROCS
      if [[ $EXP_RESULT -ne 0 ]]; then
        exit -1
      fi
    fi
  done
}

# Subtle errors will occur if this isn't set twice,
# for example:
#
#    > ssh -t s-h1 'sudo ethtool -K fge0 gso off rx off sg on gro off rxvlan off rxhash off'
#    Connection to s-h1 closed.
#    Killed by signal 1.
#    benchmarks/udp [master*] » echo $?
#    0
#    > ssh -t s-h1 'sudo ethtool -K fge0 gso on rx off sg off gro off rxvlan off rxhash off'
#    Actual changes:
#    scatter-gather: off
#    tx-scatter-gather: off
#    Connection to s-h1 closed.
#    Killed by signal 1.
#    > echo $?
#    0
#    > ssh -t s-h1 'sudo ethtool -K fge0 gso on rx off sg off gro off rxvlan off rxhash off'
#    Could not change any device features
#    Connection to s-h1 closed.
#    Killed by signal 1.
#    > echo $?
#    1

# Here we also need to configure the RSS and RFS for the kernel and the NIC. The NIC configuration
# is done by rmmod'ing the driver, changing the conf file and modprobing it again.

prepareAndRunExperiment
if [[ $EXP_RESULT -ne 0 ]]; then
  echo "Error: Nonzero return from experiment."
  echo "Failing with nonzero status."
  exit -1
fi
