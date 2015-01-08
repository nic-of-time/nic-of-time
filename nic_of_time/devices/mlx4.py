from itertools import combinations
from subprocess import Popen,PIPE

class Mlx4:
    def __init__(self,interface_name):
        self.interface_name = interface_name
        self.en_opts = None
        self.core_opts = None

    def get_combinations(self):
        en_c = []
        for i in range(0,len(self.en_opts)+1):
            en_c += list(combinations(self.en_opts,i))
        core_c = []
        for i in range(0,len(self.core_opts)+1):
            core_c += list(combinations(self.core_opts,i))
        return [en_c, core_c]

    def get_opt_str(self,opt_tup):
        moduleOpts = ""
        en_c,core_c = opt_tup
        if en_c:
            moduleOpts = "options mlx4_en "
            for x in en_c:
                moduleOpts += x[1] + "=" + x[2]
                moduleOpts += ","
                moduleOpts = moduleOpts[:-1]
                moduleOpts += "\n"
        if core_c:
            moduleOpts += "options mlx4_core "
            for x in core_c:
                moduleOpts += x[1] + "=" + x[2]
                moduleOpts += ","
            moduleOpts = moduleOpts[:-1]
        return moduleOpts

    def init(self,opts,module_opt_str):
        print("  + Initializing mlx4")
        for node in opts.nodes:
            cmd = ["ssh", node.external_address,
                   "sudo {}/mlx4.sh {} \"{}\"".format(
                       opts.remote_config_scripts_dir,
                       opts.device.interface_name,
                       module_opt_str)]
            p = Popen(cmd,stdout=PIPE,stderr=PIPE)
            out = p.communicate()
            if p.returncode != 0:
                print(cmd)
                print(out)
                return p.returncode
        return 0
