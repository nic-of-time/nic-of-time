from itertools import combinations
from subprocess import Popen,PIPE

class Mlx4:
    def __init__(self,interface_name):
        self.interface_name = interface_name
        self.en_opts = None
        self.core_opts = None

    def get_opts(self): return self.en_opts+self.core_opts

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
            if node.explore_options:
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
            else:
                print("Not setting mlx4 options for node: {}".format(node.external_address))
        return 0

    def get_exp_opts(self,exp_dir):
        with open(exp_dir+"/options.txt","r") as f:
            opts = eval(f.readline())
        return (opts[1], opts[2])

    def is_none(self,dev_opts):
        en_opts,core_opts = dev_opts
        return len(en_opts) == 0 \
            and len(core_opts) == 0

    def is_all(self,dev_opts):
        en_opts,core_opts = dev_opts
        return len(en_opts) == len(self.en_opts) \
            and len(core_opts) == len(self.core_opts)
