#!/usr/bin/env python3

import argparse
import sys

sys.path.append("..")
import nic_of_time as nt
import nic_of_time.result_parsers.iperf
import nic_of_time.devices.mlx4

parser = argparse.ArgumentParser()
parser.add_argument("--drive",action='store_true')
parser.add_argument("--plot",action='store_true')
args = parser.parse_args()

if not args.drive and not args.plot:
    args.drive = args.plot = True

opts = nt.Options() # nic-of-time options.
opts.resume = True # Resume the experiment from an intermediate data state.
opts.nodes = [nt.Node('s-h0',internal_address="10.1.1.2",is_server=True),
              nt.Node('s-h1',internal_address="10.1.1.3")]

opts.txqueuelen = 10000 # Length of the transmit queue.
opts.mtu = 9000 # Maximum transmission unit.

opts.result_parser = nt.result_parsers.iperf
opts.kill_cmd = 'pkill iperf'

opts.output_stdout = True # Archive stdout from all commands.
opts.output_files = [[],[]] # Files to archive.

# Iterate through combinations of these ethtool options.
opts.ethtool_opts = [
    ['rx-checksumming','rx'],
    ['tx-checksumming','tx'],
    ['scatter-gather','sg'],
    ['tcp-segmentation-offload','tso'],
    ['generic-segmentation-offload','gso'],
    ['generic-receive-offload','gro'],
    #['rx-vlan-offload','rxvlan'],
    #['tx-vlan-offload','txvlan'],
    ['receive-hashing','rxhash']
]
opts.device = nt.devices.mlx4.Mlx4("fge0")
opts.device.en_opts = [
    ['udp-rss','udp_rss','1']
]
opts.device.core_opts = [
    ['flow-steering','log_num_mgm_entry_size','-1']
]

# iperf-specific options.
num_iperf_procs = 8
time_secs = 15
opts.timeout_seconds = time_secs+2
opts.sleep_after_server_seconds = 10
server_address = opts.nodes[0].internal_address

for num_clients in {1,2,4}:
    # iperf TCP
    opts.nodes[0].commands = []
    opts.nodes[1].commands = []
    for cpu in range(1,2*num_iperf_procs+1,2):
        port = 5200+cpu
        opts.nodes[0].commands.append(
            "iperf3 -s -J -f M -i 1 -p {} -A {} -D".format(port,cpu))
        opts.nodes[1].commands.append(
            ("iperf3 -c {} -J -P {} --time {} -i 1 -f M " +
             "-p {} --get-server-output -M 8960 -w 256K -l 256K").format(
                 server_address,num_clients,time_secs,port))
    opts.data_output_dir = "iperf/tcp/{}-procs/{}-clients/data".format(
        num_iperf_procs,num_clients)
    opts.plot_output_dir = "iperf/tcp/{}-procs/{}-clients/plots".format(
        num_iperf_procs,num_clients)
    if args.drive:
        nt.drive_experiment(opts)
    if args.plot:
        nt.plot(opts)

    # iperf UDP
    opts.nodes[0].commands = []
    opts.nodes[1].commands = []
    for cpu in range(1,2*num_iperf_procs+1,2):
        port = 5200+cpu
        opts.nodes[0].commands.append(
            "iperf3 -s -J -f M -i 1 -p {} -A {} -D".format(port,cpu))
        opts.nodes[1].commands.append(
            ("iperf3 -c {} -u -J -b 0 -P {} --time {} -i 1 -f M " +
             "-p {} --get-server-output -l 8K").format(
                 server_address,num_clients,time_secs,port))
    opts.data_output_dir = "iperf/udp/{}-procs/{}-clients/data".format(
        num_iperf_procs,num_clients)
    opts.plot_output_dir = "iperf/udp/{}-procs/{}-clients/plots".format(
        num_iperf_procs,num_clients)
    if args.drive:
        nt.drive_experiment(opts)
    if args.plot:
        nt.plot(opts)
