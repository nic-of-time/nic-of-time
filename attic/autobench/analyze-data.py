#!/usr/bin/env python3

import argparse
import itertools
import os
import re
import sys

sys.path.insert(0,"../shared")
from analysis import EthtoolOpts,ModuleOpts,mkdir_p

mkdir_p("analysis")

parser = argparse.ArgumentParser()
parser.add_argument('results_dir')

args = parser.parse_args()

class ABClient:
  def __init__(self,num):
    #print("\n\n=== ABClient")
    self.cpuInfo = []
    self.headers = None
    self.data = []
    with open("{}/{}/client.csv".format(args.results_dir,num),"r") as f:
      for line in f:
        r = re.search("CPU time \[s\]: user (.*) system (.*) \(user", line)
        if r:
          user = float(r.group(1))
          system = float(r.group(2))
          self.cpuInfo.append((user,system))
        elif line.count(",") == 9:
          row = line.strip().split(",")
          if not self.headers:
            self.headers = row
          else:
            row = [float(x) for x in row]
            self.data.append(row)
    assert(len(self.cpuInfo)==len(self.data))
    #print(len(self.cpuInfo))
    #print(self.cpuInfo)
    #print(self.headers)
    #print(len(self.data))
    #print(self.data)

class AutobenchExp:
  def __init__(self,num):
    self.num = num
    self.ethtool = EthtoolOpts(args.results_dir,num)
    self.module_opts = ModuleOpts(args.results_dir,num)
    self.client = ABClient(num)

  def get_responses(self,response_header):
    try:
      h_idx = self.client.headers.index(response_header)
    except:
      print(self.client.headers)
      raise
    return [d[h_idx] for d in self.client.data]

# def obj_50(num):
#   e = AutobenchExp(num)
#   h_idx = e.client.headers.index('req_rate_192.168.1.5')
#   print(e.num)
#   print(len(e.client.data))
#   return (e.client.data[3][h_idx],e)
# dat_50 = list(map(obj_50,experiments))
# with open("exp_50.txt","w") as f:
#   for val,exp in sorted(dat_50,key=lambda x: x[0],reverse=True):
#     f.write("=== {} ===\n".format(val))
#     f.write("  + Num: {}\n".format(exp.num))
#     f.write("  + Enabled Ethtool: {}\n".format(exp.ethtool.enabled_opts))
#     f.write("  + Module Opts: {}\n\n".format(exp.module_opts.raw))

exps=list(map(AutobenchExp,sorted(map(int,os.listdir(args.results_dir)))))

req_rates = exps[0].get_responses('dem_req_rate')
for response_header in ['net_io_192.168.1.5', 'avg_rep_rate_192.168.1.5']:
  all_responses = [[] for x in range(len(req_rates))]
  for exp in exps:
    responses = exp.get_responses(response_header)
    if 'net_io' in response_header:
      responses = [KBps*8/1024 for KBps in responses]
    assert(len(responses) == len(req_rates))
    for idx,val in enumerate(responses):
      all_responses[idx].append(val)
  for idx,req_rate in enumerate(req_rates):
    with open("analysis/{}.{}.csv".format(
        req_rate,response_header),'w') as f:
      f.write(",".join([str(x) for x in all_responses[idx]])+"\n")

    sorted_responses = sorted(zip(all_responses[idx],exps),
                              key=lambda x: x[0], reverse=True)
    with open('analysis/{}.{}.txt'.format(
        req_rate,response_header),'w') as f:
      for response,exp in sorted_responses:
        f.write("\n\n=== {} ===\n".format(response))
        f.write("  + Num: {}\n".format(exp.num))
        f.write("  + Enabled Ethtool: {}\n".format(exp.ethtool.enabled_opts))
        f.write("  + Module Opts: {}\n".format(exp.module_opts.raw))
        f.write("  + Vals: {}\n".format(exp.client.data))

    with open("analysis/{}.{}.none.all.max.min.csv".format(
        req_rate,response_header),'w') as f:
      f.write(",".join([str(x) for x in [
        all_responses[idx][0],all_responses[idx][-1],
        sorted_responses[0][0],sorted_responses[-1][0]]])+"\n")
