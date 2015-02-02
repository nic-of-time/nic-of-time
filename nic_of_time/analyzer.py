from collections import defaultdict
from itertools import combinations
import copy
import os
import re
import sys

from nic_of_time.helper import mkdir_p
import nic_of_time.plot

def get_valid_experiments(opts):
    exps = []
    # Use total_exps rather than counting the files in opts.data_dir
    # because not every file is an experiment.
    total_exps = 0
    if os.path.isdir(opts.data_dir):
        for d in os.listdir(opts.data_dir):
            if re.match("^\d*$",d):
                exp_num = int(d)
                exp = opts.result_parser(exp_num,opts.data_dir+"/"+d,opts)
                if exp.is_valid:
                    exps.append(exp)
                total_exps += 1
    print("  + Experiments: {} valid out of {} total.".format(len(exps),total_exps))
    return sorted(exps,key=lambda res_parser: res_parser.exp_num)

def run(opts):
    print("Analyzing data.")
    exps = get_valid_experiments(opts)
    if len(exps) == 0:
        return

    for analysis in opts.analyses:
        responses = []
        all_opts_exp_idx = -1
        for exp in exps:
            responses.append((analysis.exp_func(exp),exp))
            if len(exp.ethtool.opts['enabled']) == len(opts.ethtool_opts) \
               and opts.device.is_all(exp.device_opts):
                all_opts_exp_idx = len(responses)-1

        if len(exps[0].ethtool.opts['enabled']) == 0 and opts.device.is_none(exps[0].device_opts):
            no_opts_exp_idx = 0
        else:
            no_opts_exp_idx = -1
        if no_opts_exp_idx == -1:
            print("Warning: Unable to find experiment with no options enabled.")
        if all_opts_exp_idx == -1:
            print("Warning: Unable to find experiment with all options enabled.")

        sorted_responses = sorted(responses,
                                  key=lambda x: float(x[0][analysis.sort_by_key]),
                                  reverse=analysis.reverse_sort)
        out = opts.analysis_dir+"/"+analysis.output_dir
        mkdir_p(out)
        with open(out+"/"+analysis.sort_by_key+".sorted.txt","w") as f:
            for response,exp in sorted_responses:
                if analysis.header_func:
                    f.write("\n\n=== {} ===\n".format(analysis.header_func(response)))
                else:
                    f.write("\n\n=== {} ===\n".format(response[analysis.sort_by_key]))
                f.write("  + Num: {}\n".format(exp.exp_num))
                f.write("  + Enabled Ethtool: {}\n".format(exp.ethtool.opts['enabled']))
                f.write("  + Module Opts: {}\n".format(exp.device_opts))
                for k,v in sorted(response.items()):
                    f.write("  + {}: {}\n".format(k,v))

        sorted_responses.reverse() # Writes back into sorted_responses!
        labels = []
        all_opt_data = []
        for opt in opts.ethtool_opts + opts.device.get_opts():
            labels.append(opt[0])
            opt_data = []
            for response,exp in sorted_responses:
                #if opt in
                all_opt_keys = copy.deepcopy(exp.ethtool.opts['enabled'])
                for device_opt_category in exp.device_opts:
                    for device_opt in device_opt_category:
                        all_opt_keys.append(device_opt[0])
                #print(opt[0],all_opt_keys)
                if opt[0] in all_opt_keys: opt_data.append("1")
                else: opt_data.append("0")
            all_opt_data.append(opt_data)
        out_plots = ["tiles.{}.{}".format(analysis.sort_by_key,ext)
               for ext in ["pdf","png"]]
        nic_of_time.plot.tile(opts,all_opt_data,labels,out_plots)

        with open(out+"/"+analysis.sort_by_key+".csv","w") as f:
            f.write(",".join([str(x[0][analysis.sort_by_key]) for x in responses]))
            f.write("\n")
            if no_opts_exp_idx != -1:
                f.write("{}\n".format(responses[no_opts_exp_idx][0][analysis.sort_by_key]))
            else:
                f.write("0\n")
            if all_opts_exp_idx != -1:
                f.write("{}\n".format(responses[all_opts_exp_idx][0][analysis.sort_by_key]))
            else:
                f.write("0\n")

        # Category analysis.
        for category,enabled_options in opts.categories.items():
            filtered_responses = []
            for i in range(0,len(enabled_options)+1):
                for combination in combinations(enabled_options,i):
                    for response,exp in responses:
                        response_options = copy.deepcopy(exp.ethtool.opts['enabled'])
                        for dev_opt in exp.device_opts:
                            response_options += [x[0] for x in dev_opt]
                        if response_options == list(combination):
                            filtered_responses.append((response,exp))
            with open(out+"/"+analysis.sort_by_key+".category."+category+".csv","w") as f:
                f.write(",".join([str(x[0][analysis.sort_by_key]) for x in filtered_responses]))
                f.write("\n")
