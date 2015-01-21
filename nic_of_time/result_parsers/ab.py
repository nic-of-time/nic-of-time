import glob
import json
import os
import statistics
import sys

import nic_of_time as nt
import nic_of_time.result_parsers

class AbRun:
    def __init__(self,exp_num,path,opts):
        self.exp_num = exp_num
        self.path = path
        self.ethtool = nt.result_parsers.EthtoolOpts(path+"/ethtool.log",opts)
        if not self.ethtool.is_valid:
            self.is_valid = False
            return

        self.device_opts = opts.device.get_exp_opts(path)

        # TODO: Parse file.
        results_file = "{}/{}-0-stdout".format(path,opts.nodes[1].external_address)
        if os.path.isfile(results_file):
            with open(results_file,"r") as f:
                for line in f.readlines():
                    if "Total transferred" in line:
                        print(line)
                        self.is_valid = True
                        return
        self.is_valid = False
