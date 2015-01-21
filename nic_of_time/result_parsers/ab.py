import glob
import json
import os
import re
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
        data = {}
        if os.path.isfile(results_file):
            with open(results_file,"r") as f:
                for line in f.readlines():
                    r = re.search("(.*): *([\d\.]*)",line)
                    if r:
                        data[r.group(1)] = r.group(2)

        if 'Requests per second' in data and float(data['Requests per second']) > 0:
            self.data=data
            self.is_valid = True
        else:
            self.is_valid = False

    def get_data(self):
        assert(self.is_valid)
        #TODO: Clean up keys, add more analysis.
        return {
            'requests_per_second': self.data['Requests per second']
        }
