from itertools import combinations
from subprocess import Popen,PIPE

class Igb:
    def __init__(self,interface_name):
        self.interface_name = interface_name
        self.dev_opts = None

    def get_opts(self): return self.dev_opts

    def get_combinations(self):
        dev_c = []
        for i in range(0,len(self.dev_opts)+1):
            dev_c += list(combinations(self.dev_opts,i))
        return [dev_c]

    def get_opt_str(self,opt_tup):
        moduleOpts = ""
        for x in opt_tup[0]:
          moduleOpts += x[1] + "=" + x[2]
          moduleOpts += ","
        moduleOpts = moduleOpts[:-1]
        return moduleOpts

    def init(self,opts,module_opt_str):
        print("  + Skipping igb initialization")
        return 0
        print("  + Initializing igb")
        for node in opts.nodes:
            if node.explore_options:
                cmd = ["ssh", node.external_address,
                       "sudo nohup {}/igb.sh {} \"{}\" {}".format(
                           opts.remote_config_scripts_dir,
                           opts.device.interface_name,
                           module_opt_str,
                           node.internal_address)]
                p = Popen(cmd,stdout=PIPE,stderr=PIPE)
                out = p.communicate()
                if p.returncode != 0:
                    print(cmd)
                    print(out)
                    return p.returncode
            else:
                print("Not setting igb options for node: {}".format(node.external_address))
        return 0

    def get_exp_opts(self,exp_dir):
        with open(exp_dir+"/options.txt","r") as f:
            opts = eval(f.readline())
        return (opts[1])

    def is_none(self,dev_opts):
        return len(dev_opts) == 0

    def is_all(self,dev_opts):
        return len(dev_opts) == len(self.dev_opts)
