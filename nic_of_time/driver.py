from itertools import combinations,product
import sys

def runExp(opts,exp_num,eth_opt_tups,dev_opts):
    ethOpts = " ".join([x[1] + " on" for x in eth_opt_tups] + \
                       [x[1] + " off" for x in opts.ethtool_opts
                        if x not in eth_opt_tups])
    moduleOpts = opts.device.get_opt_str(dev_opts)
    print(ethOpts,moduleOpts)
    # TODO: Log experiment details to file
    # TODO: Init nodes
    # TODO: Log ethtool -i and ethtool -k from nodes
    # TODO: Run experiment
    return 0 # TODO: Return code

def get_ethtool_combinations(opts):
    c = []
    for i in range(0,len(opts.ethtool_opts)+1):
        c += list(combinations(opts.ethtool_opts,i))
    return c

def run(opts):
    exp_num = 1
    err_f = open("error-combinations.txt",'w')
    opt_combinations = [get_ethtool_combinations(opts)] + \
                       opts.device.get_combinations()
    all_combinations = list(product(*opt_combinations))
    exp_num = 1
    for tup in all_combinations:
        eth_opts = tup[0]
        dev_opts = tup[1:]
        ret = runExp(opts,exp_num,eth_opts,dev_opts)
        if ret != 0:
            err_f.write(str(tups + mlx4EnTups + mlx4CoreTups)+"\n")
            err_f.flush()
        exp_num += 1
