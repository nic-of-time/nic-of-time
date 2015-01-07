#!/usr/bin/env python3

import argparse
import nic_of_time as nt

parser = argparse.ArgumentParser()
parser.add_argument("--drive",action='store_true')
parser.add_argument("--plot",action='store_true')
args = parser.parse_args()

if not args.drive and not args.plot:
    args.drive = args.plot = True

# nic-of-time library options.
opts = nt.options()
opts.server_external='derecho.elijah.cs.cmu.edu'
opts.client_external='derecho.elijah.cs.cmu.edu'
opts.server_internal=opts.server_external
opts.client_internal=opts.server_internal
opts.tx = 10000
opts.mtu = 9000

opts.results = nc.result_parsers.iperf
opts.kill_cmd = 'pkill iperf'

opts.output_stdout = True # Archive stdout from all commands.
opts.output_files.server = [] # Files on the server to archive.
opts.output_files.client = [] # Files on the client to archive.

opts.ethtool_opts = [
	['rx-checksumming','rx'],
	['tx-checksumming','tx'],
	['scatter-gather','sg'],
	['tcp-segmentation-offload','tso'],
	['generic-segmentation-offload','gso'],
	['generic-receive-offload','gro'],
#	['rx-vlan-offload','rxvlan'],
#	['tx-vlan-offload','txvlan'],
	['receive-hashing','rxhash']
]
opts.ethernet_device = "fge0"
opts.ethernet_device_model = nt.devices.mlx4
opts.mlx4EnOpts = [
	['udp-rss','udp_rss','1']
]
opts.mlx4CoreOpts = [
  ['flow-steering','log_num_mgm_entry_size','-1']
]

# iperf-specific options.
num_iperf_procs = 8
time_secs = 15

for num_clients in {1,2,4}:
    # iperf TCP
    opts.server_commands = []
    opts.client_commands = []
    for cpu in range(1,2*num_iperf_procs+1,2):
        opts.server_commands.append(
            "iperf3 -s -J -f M -i 1 -p 520{} -A {} -D".format(cpu,cpu))
        opts.client_commands.append(
            ("iperf3 -c {} -J -P {} --time {} -i 1 -f M " +
             "-p 520{} --get-server-output -M 8960 -w 256K -l 256K").format(
                 server,num_clients))
    opts.data_output_dir = "iperf/tcp/{}/{}".format(num_iperf_procs,num_clients)
    opts.plot_output_dir = "iperf/tcp/{}/{}".format(num_iperf_procs,num_clients)
    if args.drive:
        nt.drive_experiment(opts)
    if args.plot:
        nt.plot(opts)

    # iperf UDP
    opts.server_commands = []
    opts.client_commands = []
    for cpu in range(1,2*num_iperf_procs+1,2):
        opts.server_commands.append(
            "iperf3 -s -J -f M -i 1 -p 520{} -A {} -D".format(cpu,cpu))
        opts.client_commands.append(
            ("iperf3 -c {} -u -J -b 0 -P {} --time {} -i 1 -f M " +
             "-p 520{} --get-server-output -l 8K").format(
                 server,time_secs,num_clients))
    opts.data_output_dir = "iperf/udp/{}/{}".format(num_iperf_procs,num_clients)
    opts.plot_output_dir = "iperf/udp/{}/{}".format(num_iperf_procs,num_clients)
    if args.drive:
        nt.drive_experiment(opts)
    if args.plot:
        nt.plot(opts)
        nt.plot_slice(opts)
