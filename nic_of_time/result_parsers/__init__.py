import os
import re

from nic_of_time.helper import grouper

class EthtoolOpts:
    def __init__(self,ethtool_opts_file):
        if not os.path.isfile(ethtool_opts_file):
            self.is_valid = False
            return

        with open(ethtool_opts_file,"r") as f:
            self.all_opts = {}
            node = None
            node_opts = None
            for line in f.readlines():
                r = re.search("^===(\S*)===$",line)
                if r:
                    if node:
                        self.all_opts[node] = node_opts
                    node = r.group(1)
                    node_opts = {'enabled': [], 'disabled': []}
                r = re.search("(\S*): (\S*)",line)
                if r:
                    opt = r.group(1)
                    status = r.group(2)
                    if status == "on":
                        node_opts['enabled'].append(opt)
                    elif status == "off":
                        node_opts['disabled'].append(opt)
            self.all_opts[node] = node_opts

        reference_ethtool_node = None
        for node in self.all_opts:
            if not reference_ethtool_node:
                reference_ethtool_node = self.all_opts[node]
                self.opts = reference_ethtool_node
            else:
                for switch in self.all_opts[node]:
                    if self.all_opts[node][switch] != reference_ethtool_node[switch]:
                        self.is_valid = False
                        return

        self.is_valid = True


class ModuleOpts:
    def __init__(self,module_file):
        with open(module_file,"r") as f:
            self.raw = f.readline().split()
