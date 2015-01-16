import glob
import json
import os
import statistics
import sys

import nic_of_time as nt
import nic_of_time.result_parsers

class YcsbRun:
    def __init__(self,exp_num,path,opts):
        self.exp_num = exp_num
        self.path = path
        self.ethtool = nt.result_parsers.EthtoolOpts(path+"/ethtool.log",opts)
        if not self.ethtool.is_valid:
            self.is_valid = False
            return

        self.device_opts = opts.device.get_exp_opts(path)

        # TODO: YCSB-specific code.
        # with open("{}/{}-0-stdout".format(
        #         path,opts.nodes[0].external_address),"r") as f:
        #     for line in f.readlines():
        #         if "Total transferred" in line:
        #             self.is_valid = True
        #             return
        self.is_valid = True
