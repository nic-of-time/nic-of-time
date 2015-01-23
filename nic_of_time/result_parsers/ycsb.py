import glob
import json
import os
import re
import statistics
import sys

import nic_of_time as nt
import nic_of_time.result_parsers

class YcsbRun:
    def __init__(self,exp_num,path,opts):
        self.throughput_key='Throughput(ops/sec)'
        self.runtime_key='RunTime(ms)'
        self.latency_key='AverageLatency(us)'

        self.exp_num = exp_num
        self.path = path
        self.ethtool = nt.result_parsers.EthtoolOpts(path+"/ethtool.log",opts)
        if not self.ethtool.is_valid:
            self.is_valid = False
            return

        self.device_opts = opts.device.get_exp_opts(path)

        self.data = {}
        inExperiment = False
        raw_fname = "{}/{}-0-stdout".format(path,opts.nodes[1].external_address)
        if not os.path.isfile(raw_fname):
            self.is_valid = False
            return

        data = {}
        with open(raw_fname,"r") as f:
            for line in f.readlines():
                if not inExperiment:
                    if re.search("Command line:.*-t$",line):
                        inExperiment = True
                else:
                    r = re.search("\[OVERALL\], (.*), (.*)",line)
                    if not r:
                        r = re.search("\[UPDATE\], (.*), (.*)",line)
                    if r:
                        data[r.group(1)] = float(r.group(2))
        if self.throughput_key in data and self.runtime_key in data \
                and self.latency_key in data \
                and data[self.throughput_key] > 0:
            self.data = data
            self.is_valid = True
        else:
            self.is_valid = False

    def get_data(self):
        assert(self.is_valid)
        return {
            'throughput': self.data[self.throughput_key],
            'latency': self.data[self.latency_key],
            'runtime': self.data[self.runtime_key]
        }
