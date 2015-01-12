import os
import re
import sys

from nic_of_time.helper import mkdir_p

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
    return exps

def run(opts):
    print("Analyzing data.")
    exps = get_valid_experiments(opts)

    for analysis in opts.analyses:
        responses = []
        for exp in exps:
            responses.append((analysis.exp_func(exp),exp))
        sorted_responses = sorted(responses,
                                  key=lambda x: x[0][analysis.sort_by_key],
                                  reverse=analysis.reverse_sort)
        out = opts.analysis_dir+"/"+analysis.output_dir
        mkdir_p(out)
        with open(out+"/sorted.txt","w") as f:
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
        with open(out+"/"+analysis.sort_by_key+".csv","w") as f:
            f.write(",".join([str(x[0][analysis.sort_by_key]) for x in responses]))
            f.write("\n")
