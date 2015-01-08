import os

import nic_of_time.driver

class Options:
    def __init__(self):
        self.nodes = None
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

        self.data_output_dir = None
        self.plot_output_dir = None

        mod_dir = os.path.dirname(os.path.realpath(__file__))
        self.local_config_scripts_dir = mod_dir+"/config-scripts"
        self.remote_config_scripts_dir = "/tmp/nic-of-time-config-scripts"

class Node:
    def __init__(self,external_address,internal_address=None,is_server=False):
        if not internal_address:
            internal_address = external_address
        self.external_address = external_address
        self.internal_address = internal_address
        self.is_server = is_server
        self.commands = []

def drive_experiment(opts):
    driver.run(opts)

def plot(opts):
    print("plot")
