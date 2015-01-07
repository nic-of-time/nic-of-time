#!/usr/bin/env python3

import argparse
from collections import defaultdict

analyze_data = __import__("analyze-data")

if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--padding-seconds',type=int,default=3)
  parser.add_argument('results_dir')
  parser.add_argument('type')
  parser.add_argument('protocol')
  parser.add_argument('num_parallel',type=int)
  parser.add_argument('slice_start',type=float)
  parser.add_argument('slice_end',type=float)

  args = parser.parse_args()

  experiments = analyze_data.get_experiments(args.results_dir,args.padding_seconds)

  if args.type == 'bw':
    exps_bw = [analyze_data.get_bw(exp,args.protocol,
                                   args.num_parallel,args.padding_seconds)
               for exp in experiments]
    filtered_exps = list(filter(lambda tup: # mean, stdev, segments, exp
                                tup[0] >= args.slice_start and
                                tup[0] <= args.slice_end,
                                exps_bw))
    print("Total Filtered: {}".format(len(filtered_exps)))
    opts = defaultdict(int)
    for mean, stdev, segments, exp in filtered_exps:
      for opt in exp.ethtool.enabled_opts:
        opts[opt] += 1
      for opt in exp.module_opts.raw:
        if opt != 'options':
          opts[opt] += 1
    print(opts)
  else:
    raise Exception("Only available type is 'bw'")
