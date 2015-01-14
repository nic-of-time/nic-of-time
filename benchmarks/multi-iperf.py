#!/usr/bin/env python3

import argparse
import copy
import sys

sys.path.append("..")
import nic_of_time as nt
import nic_of_time.result_parsers.iperf
import nic_of_time.devices.mlx4
import nic_of_time.plot

parser = argparse.ArgumentParser()
parser.add_argument("--drive",action='store_true')
parser.add_argument("--analyze",action='store_true')
parser.add_argument("--plot",action='store_true')
args = parser.parse_args()

if not args.drive and not args.analyze and not args.plot:
    args.drive = args.analyze = args.plot = True

opts = nt.Options() # nic-of-time options.
opts.resume = True # Resume the experiment from an intermediate data state.
opts.nodes = [nt.Node('s-h0',internal_address="10.1.1.2",is_server=True),
              nt.Node('s-h1',internal_address="10.1.1.3")]

opts.txqueuelen = 10000 # Length of the transmit queue.
opts.mtu = 9000 # Maximum transmission unit.

opts.result_parser = nt.result_parsers.iperf.IperfRun
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

opts.analyses = [
    nt.Analysis(lambda exp: exp.get_bandwidth_gbps(padding_seconds=2),
                output_dir = "bw",
                sort_by_key = 'mean',
                header_func = lambda bw: "{} ({})".format(bw['mean'],bw['stdev'])),
    nt.Analysis(lambda exp: exp.get_cpu(),
                output_dir = "cpu",
                sort_by_key = 'host_mean',
                header_func = None)
]
opts.plot_dir = "iperf/plot"

tcp_data = {}
udp_data = {}
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
    prefix = "iperf/tcp/{}-procs/{}-clients".format(num_iperf_procs,num_clients)
    opts.data_dir = prefix + "/data"
    opts.analysis_dir = prefix + "/analysis"
    if args.drive:
        nt.drive_experiment(opts)
    if args.analyze:
        nt.analyze(opts)
    tcp_data[num_clients] = copy.deepcopy(opts)

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
    prefix = "iperf/udp/{}-procs/{}-clients".format(num_iperf_procs,num_clients)
    opts.data_dir = prefix + "/data"
    opts.analysis_dir = prefix + "/analysis"
    if args.drive:
        nt.drive_experiment(opts)
    if args.analyze:
        nt.analyze(opts)
    udp_data[num_clients] = copy.deepcopy(opts)

nt.plot.grouped_bars(
    opts = [tcp_data[1], tcp_data[2], tcp_data[4]],
    analyses = ["bw/mean.csv"]*3,
    data_labels = ["1 Parallel", "2 Parallel", "4 Parallel"],
    stats = ["Min","None","All","Max"],
    stat_colors = ["#6497b1","#005b96","#03396c","#011f4b"],
    ylabel = "Bandwidth (Gbps)",
    xlabel = "Number of Parallel Connections",
    output_files = ["tcp.bars.png","tcp.bars.pdf"]
)

nt.plot.grouped_bars(
    opts = [udp_data[1], udp_data[2], udp_data[4]],
    analyses = ["bw/mean.csv"]*3,
    data_labels = ["1 Parallel", "2 Parallel", "4 Parallel"],
    stats = ["Min","None","All","Max"],
    stat_colors = ["#6497b1","#005b96","#03396c","#011f4b"],
    ylabel = "Bandwidth (Gbps)",
    xlabel = "Number of Parallel Connections",
    output_files = ["udp.bars.png","udp.bars.pdf"]
)
