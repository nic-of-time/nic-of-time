#!/usr/bin/env python3

import argparse
import copy
import sys

sys.path.append("..")
import nic_of_time as nt
import nic_of_time.result_parsers.ab
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
opts.retry = 4
opts.nodes = [nt.Node('s-h0',internal_address="10.53.1.32",is_server=True),
              nt.Node('s-h1',internal_address="10.53.1.9")]
server_address = opts.nodes[0].internal_address
opts.nodes[0].commands = [] # nginx running in daemon mode.

opts.txqueuelen = 10000 # Length of the transmit queue.
opts.mtu = 9000 # Maximum transmission unit.

opts.result_parser = nt.result_parsers.ab.AbRun
opts.kill_cmd = 'sudo pkill ab'

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

opts.timeout_seconds = None
opts.sleep_after_server_seconds = 5

opts.analyses = [
    nt.Analysis(lambda exp: exp.get_data(),
                output_dir = "data",
                sort_by_key = 'requests_per_second')
]

opts.categories = {}

exps = [["0_byte.no-keepalive",
   "ab -n 100000 -c 500 http://{}:80/0_byte.file".format(server_address)],
["1_kb.no-keepalive",
   "ab -n 100000 -c 500 http://{}:80/1_kb.file".format(server_address)],
["1_mb.keepalive",
   "ab -n 25000 -k -c 500 http://{}:80/1_mb.file".format(server_address)],
["1_mb.no-keepalive",
   "ab -n 25000 -c 500 http://{}:80/1_mb.file".format(server_address)]]
#exps = [["debug","sleep 10000"]]

exp_opts = {}
opts.plot_dir = "ab/plot"
for tag, cmd in exps:
    opts.nodes[1].commands = [cmd]
    prefix = "ab/"+tag
    opts.data_dir = prefix + "/data"
    opts.analysis_dir = prefix + "/analysis"
    if args.drive:
        nt.drive_experiment(opts)
    if args.analyze:
        nt.analyze(opts)
    if args.plot:
        nt.plot.bars(
            opts = [opts],
            analyses = ["data/requests_per_second.csv"],
            stats = ["Min","None","All","Max"],
            stat_colors = ["#6497b1","#005b96","#03396c","#011f4b"],
            ylabel = "Requests per second",
            output_files = [tag+".rps.bars.png",tag+".rps.bars.pdf"]
        )

        nt.plot.cdf(
            opts = [opts],
            analyses = ["data/requests_per_second.csv"],
            data_labels = [" "],
            colors = ["#000000"],
            xlabel = "Requests per second",
            output_files = [tag+".rps.cdf.png",tag+".rps.cdf.pdf"]
        )
    exp_opts[tag]= copy.deepcopy(opts)

tags = ["0_byte.no-keepalive","1_kb.no-keepalive","1_mb.no-keepalive","1_mb.keepalive"]
labels = ["Empty", "1 kb", "1 mb", "1 mb (keepalive)"]
nt.plot.grouped_bars(
    opts = [exp_opts[x] for x in tags],
    analyses = ["data/requests_per_second.csv"]*4,
    data_labels = labels,
    stats = ["Min","None","All","Max"],
    stat_colors = ["#6497b1","#005b96","#03396c","#011f4b"],
    ylabel = "Requests per Second",
    xlabel = "Requested File Size",
    output_files = ["rps.bars.png","rps.bars.pdf"]
)

tags = ["0_byte.no-keepalive","1_kb.no-keepalive"]
labels = ["Empty", "1 kb"]
nt.plot.grouped_bars(
    opts = [exp_opts[x] for x in tags],
    analyses = ["data/requests_per_second.csv"]*len(tags),
    data_labels = labels,
    stats = ["Min","None","All","Max"],
    stat_colors = ["#6497b1","#005b96","#03396c","#011f4b"],
    ylabel = "Requests per Second",
    xlabel = "Requested File Size",
    output_files = ["rps.bars.small-files."+ext for ext in ["png","pdf"]]
)
tags = ["1_mb.no-keepalive","1_mb.keepalive"]
labels = ["1 mb", "1 mb (keepalive)"]
nt.plot.grouped_bars(
    opts = [exp_opts[x] for x in tags],
    analyses = ["data/requests_per_second.csv"]*len(tags),
    data_labels = labels,
    stats = ["Min","None","All","Max"],
    stat_colors = ["#6497b1","#005b96","#03396c","#011f4b"],
    ylabel = "Requests per Second",
    xlabel = "Requested File Size",
    output_files = ["rps.bars.1mb."+ext for ext in ["png","pdf"]]
)
