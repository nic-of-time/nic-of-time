from itertools import combinations

class Mlx4:
    def __init__(self,interface_name):
        self.en_opts = None
        self.core_opts = None

                # for j in range(0,len(mlx4enopts)+1):
                #     for mlx4entups in combinations(mlx4enopts, j):
                #         for k in range(0,len(mlx4coreopts)+1):
                #             for mlx4coretups in combinations(mlx4coreopts, k):
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
