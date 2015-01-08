from itertools import combinations,product
import os
from subprocess import Popen,PIPE
import sys
import time

from nic_of_time.helper import mkdir_p

def sync_config(opts):
    print("  + Syncing config")
    for node in opts.nodes:
        p = Popen(["scp", "-r",
                   opts.local_config_scripts_dir+"/.",
                   "{}:{}/".format(node.external_address,
                                  opts.remote_config_scripts_dir)],
                  stdout=PIPE,stderr=PIPE)
        out = p.communicate()
        if p.returncode != 0:
            print(out)
            return p.returncode
    return 0

def init_ethtool(opts,eth_opt_str,eth_log_fname):
    print("  + Initializing ethtool")
    log_f = open(eth_log_fname,"w")
    for node in opts.nodes:
        cmd = ["ssh", node.external_address,
               "sudo {}/ethtool.sh {} \"{}\" {} {} {}".format(
                   opts.remote_config_scripts_dir,
                   opts.device.interface_name,
                   eth_opt_str,
                   opts.mtu,
                   opts.txqueuelen,
                   node.internal_address)]
        p = Popen(cmd,stdout=PIPE,stderr=PIPE)
        out = p.communicate()
        if p.returncode != 0:
            print(cmd)
            print(out)
            return p.returncode

        # Log ethtool -i and ethtool -k from nodes
        p = Popen(["ssh", node.external_address,
                   "sudo ethtool -i {}; sudo ethtool -k {}".format(
                       opts.device.interface_name,
                       opts.device.interface_name)],
                  stdout=PIPE,stderr=PIPE)
        out = p.communicate()
        log_f.write("\n\n==={}===\n\n".format(node.external_address))
        log_f.write(out[0].decode())
        if p.returncode != 0:
            print(cmd)
            print(out)
            return p.returncode
    log_f.close()
    return 0

def runExp(opts,exp_num,eth_opt_tups,dev_opts):
    print("=== Running experiment {} ===".format(exp_num))
    eth_opt_str = " ".join([x[1] + " on" for x in eth_opt_tups] + \
                       [x[1] + " off" for x in opts.ethtool_opts
                        if x not in eth_opt_tups])
    module_opt_str = opts.device.get_opt_str(dev_opts)

    if opts.kill_cmd:
        print("  + Sending '{}' to all nodes.".format(opts.kill_cmd))
        for node in opts.nodes:
            cmd = ["ssh", node.external_address, "sudo {}".format(opts.kill_cmd)]
            p = Popen(cmd,stdout=PIPE,stderr=PIPE)
            p.communicate()

    eth_log_fname = "{}/{}/ethtool.log".format(opts.data_output_dir,exp_num)
    err = opts.device.init(opts,dev_opts)
    if err != 0: return err
    err = init_ethtool(opts,eth_opt_str,eth_log_fname)
    if err != 0: return err

    print("  + Starting server processes.")
    fds = []
    server_procs = []
    for server_node in [n for n in opts.nodes if n.is_server]:
        print("    + node: {} ({})".format(server_node.external_address,server_node.internal_address))
        procs = []
        for cmd in server_node.commands:
            print("      + {}".format(cmd))
            f_out = open("{}/{}/{}-{}-stdout".format(opts.data_output_dir,
                                                     exp_num,
                                                     server_node.external_address,
                                                     len(procs)),"w")
            f_err = open("{}/{}/{}-{}-stderr".format(opts.data_output_dir,
                                                     exp_num,
                                                     server_node.external_address,
                                                     len(procs)),"w")
            procs.append(
                Popen(["ssh",
                       server_node.external_address,
                       "sudo {}".format(cmd)],
                      stdout=f_out,stderr=f_err))
        server_procs.append(procs)

    if opts.sleep_after_server_seconds:
        print("  + Sleeping for {} seconds.".format(opts.sleep_after_server_seconds))
        time.sleep(opts.sleep_after_server_seconds)

    print("  + Starting client processes.")
    client_procs = []
    for client_node in [n for n in opts.nodes if not n.is_server]:
        print("    + node: {} ({})".format(client_node.external_address,client_node.internal_address))
        procs = []
        for cmd in client_node.commands:
            print("      + {}".format(cmd))
            f_out = open("{}/{}/{}-{}-stdout".format(opts.data_output_dir,
                                                     exp_num,
                                                     client_node.external_address,
                                                     len(procs)),"w")
            f_err = open("{}/{}/{}-{}-stderr".format(opts.data_output_dir,
                                                     exp_num,
                                                     client_node.external_address,
                                                     len(procs)),"w")
            fds += [f_out,f_err]
            procs.append(
                Popen(["ssh",
                       client_node.external_address,
                       "sudo {}".format(cmd)],
                      stdout=f_out,stderr=f_err))
        client_procs.append(procs)

    if opts.timeout_seconds:
        print("  + Sleeping for {} seconds.".format(opts.timeout_seconds))
        time.sleep(opts.timeout_seconds)

    print("  + Killing all processes.")
    for node_procs in server_procs + client_procs:
        for proc in node_procs:
            proc.terminate()
    time.sleep(1)

    for f in fds:
        f.close()

    return 0

def get_ethtool_combinations(opts):
    c = []
    for i in range(0,len(opts.ethtool_opts)+1):
        c += list(combinations(opts.ethtool_opts,i))
    return c

def run(opts):
    mkdir_p(opts.data_output_dir)

    err  = sync_config(opts)
    if err != 0:
        raise Exception("Unable to synchronize config scripts.")

    exp_num = 1
    err_f = open(opts.data_output_dir+"/error-combinations.txt",'w')
    opt_combinations = [get_ethtool_combinations(opts)] + \
                       opts.device.get_combinations()
    all_combinations = list(product(*opt_combinations))
    exp_num = 1

    start_time_secs = time.time()
    total_exps = len(all_combinations)
    for tup in all_combinations:
        mkdir_p("{}/{}".format(opts.data_output_dir,exp_num))
        with open("{}/{}/options.txt".format(opts.data_output_dir,exp_num),'w') as f:
            f.write("{}\n".format(tup))

        eth_opts = tup[0]
        dev_opts = tup[1:]
        err = runExp(opts,exp_num,eth_opts,dev_opts)
        if err != 0:
            err_f.write("{}: {}".format(exp_num,tup))
            err_f.write("\n")
            err_f.flush()

        current_time_secs = time.time()
        total_time = current_time_secs - start_time_secs
        print("+ Time since start: {} seconds".format(total_time))
        print("+ Finished Experiment {} of {}".format(exp_num,total_exps))
        print("+ Estimated Time Remaining: {} seconds".format(
            (total_time/exp_num)*(total_exps-exp_num)))

        exp_num += 1
    err_f.close()
