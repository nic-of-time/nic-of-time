import os

import nic_of_time.driver
import nic_of_time.analyzer

class Options:
    def __init__(self):
        self.nodes = None
        self.resume = False
        self.txqueuelen = None
        self.mtu = None

        self.result_parser = None

        self.kill_cmd = None

        self.timeout_seconds = None
        self.sleep_after_server_seconds = None

        self.output_stdout = None # Archive stdout from all commands.
        self.output_files = None # Files on the nodes to archive.

        self.ethtool_opts = None
        self.device = None

        self.data_dir = None
        self.analysis_dir = None
        self.plot_dir = None

        mod_dir = os.path.dirname(os.path.realpath(__file__))
        self.local_config_scripts_dir = mod_dir+"/config-scripts"
        self.remote_config_scripts_dir = "/tmp/nic-of-time-config-scripts"

        self.analyses = None

        self.r_dir = os.path.dirname(os.path.realpath(__file__))+"/r-scripts"

class Node:
    def __init__(self,external_address,internal_address=None,is_server=False):
        if not internal_address:
            internal_address = external_address
        self.external_address = external_address
        self.internal_address = internal_address
        self.is_server = is_server
        self.commands = []

class Analysis:
    def __init__(self,exp_func,sort_by_key,output_dir,plot=True,reverse_sort=True,header_func=None):
        self.exp_func = exp_func
        self.sort_by_key = sort_by_key
        self.output_dir = output_dir
        self.plot = plot
        self.reverse_sort = reverse_sort
        self.header_func = header_func

def drive_experiment(opts):
    driver.run(opts)

def analyze(opts):
    analyzer.run(opts)
