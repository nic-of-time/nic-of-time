#!/usr/bin/env python3

import argparse
import copy
import sys

sys.path.append("..")
import nic_of_time as nt
import nic_of_time.result_parsers.ycsb
import nic_of_time.devices.igb
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
opts.retry = 4
opts.nodes = [nt.Node('s-h4',internal_address="10.51.1.28",is_server=True),
              nt.Node('s-h5',internal_address="10.51.1.8")]

opts.txqueuelen = 10000 # Length of the transmit queue.
opts.mtu = 9000 # Maximum transmission unit.

opts.result_parser = nt.result_parsers.ycsb.YcsbRun
opts.kill_cmd = 'sudo pkill redis; sudo pkill ycsb'

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
opts.device = nt.devices.igb.Igb("eth0")
opts.device.dev_opts = [
    ['rss','RSS','8']
]

opts.timeout_seconds = None
opts.sleep_after_server_seconds = 10

opts.analyses = [
    nt.Analysis(lambda exp: exp.get_data(),
                output_dir = "data",
                sort_by_key = 'throughput')
]
opts.plot_dir = "ycsb-igb/plot"

server_address = opts.nodes[0].internal_address
opts.nodes[0].commands = ["redis-server --bind 0.0.0.0"]
#ycsb_root = "/usr/local/share/YCSB"
ycsb_root = "/users/bamos/ycsb-0.1.4"
ycsb_bin = ycsb_root+"/bin/ycsb"
workload = ycsb_root+"/workloads/workloadf"
config = "-p 'redis.host={}' -p 'redis.port=6379' -p 'recordcount=10000' -p 'operationcount=1000000'".format(server_address)
#opts.nodes[1].commands = ["sleep 10000"]
opts.nodes[1].commands = [
    "{} load redis -s -P {} {} && {} run redis -s -P {} {}".format(
        ycsb_bin,workload,config,ycsb_bin,workload,config)]
prefix = "ycsb-igb"
opts.data_dir = prefix + "/data"
opts.analysis_dir = prefix + "/analysis"
if args.drive:
    nt.drive_experiment(opts)
if args.analyze:
    nt.analyze(opts)
if args.plot:
    nt.plot.grouped_bars(
        opts = [opts],
        analyses = ["data/throughput.csv"],
        stats = ["Min","None","All","Max"],
        stat_colors = ["#6497b1","#005b96","#03396c","#011f4b"],
        ylabel = "Bandwidth (Gbps)",
        xlabel = "Number of Parallel Connections",
        output_files = ["throughput.bars.tcp.png","throughput.bars.tcp.pdf"]
    )

    nt.plot.cdf(
        opts = [opts],
        analyses = ["data/throughput.csv"],
        colors = ["#B2B2FF"],
        xlabel = "Throughput",
        output_files = ["throughput.cdf.png","throughput.cdf.pdf"]
    )
