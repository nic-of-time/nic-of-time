from collections import defaultdict
import glob
import json
import os
import re
import statistics
import sys

import nic_of_time as nt
import nic_of_time.result_parsers

class PerfRun:
    def __init__(self,path,nodes):
        self.results = defaultdict(int) # Node-Counter -> Value
        for node in nodes:
            node_results = {} # Counter -> Value
            if not os.path.isfile("{}/{}-perf".format(path,node.external_address)):
                self.is_valid = False
                return
            with open("{}/{}-perf".format(path,node.external_address),"r") as f:
                for line in f.readlines():
                    line = line.strip()
                    line = line.replace(",","")
                    r = re.search("(\d+) (\S+)",line)
                    if r:
                        key = r.group(2)
                        node_key = node.external_address+"-"+key
                        val = int(r.group(1))
                        self.results[node_key] = val
                        self.results[key] += val
            e = node.external_address
            key = e+"-cache-miss-ratio"
            self.results[key] = float(self.results[e+"-cache-misses"]) / float(self.results[e+"-cache-references"])
        # TODO: Check if cache-misses and cache-references are in results
        self.results["cache-miss-ratio"] = float(self.results["cache-misses"]) / float(self.results["cache-references"])
        # TODO: Validate self.results
        self.is_valid = True
