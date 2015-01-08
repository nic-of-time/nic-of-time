import nic_of_time.driver

class Options:
    def __init__(self):
        self.nodes = None
        self.txqueuelen = None
        self.mtu = None

        self.result_parser = None
        self.kill_cmd = None

        self.output_stdout = None # Archive stdout from all commands.
        self.output_files = None # Files on the nodes to archive.

        self.ethtool_opts = None
        self.device = None

        self.commands = []

class Node:
    def __init__(self,external_address,internal_address=None,server=False):
        if not internal_address:
            internal_address = external_address
        self.external_address = external_address
        self.internal_address = external_address

def drive_experiment(opts):
    driver.run(opts)

def plot(opts):
    print("plot")
