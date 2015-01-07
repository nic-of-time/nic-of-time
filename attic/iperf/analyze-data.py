#!/usr/bin/env python3

import argparse
import itertools
import glob
import os
import re
import sys
import json
import statistics
from operator import add

sys.path.insert(0,"../../benchmarks/shared")
from analysis import EthtoolOpts,ModuleOpts,mkdir_p,flatmap

mkdir_p("analysis")

class IperfRun:
  def __init__(self,name):
    #print("\n\n=== IperfRun")
    #print(name)
    self.name = name
    with open(name,'r') as f:
      try:
        self.data = json.load(f)
      except:
        self.data = {}
    r = re.search(".*/output-(\d*)-(\S*)-(\d*)",name)
    if r:
      self.numCpu = int(r.group(1))
      self.protocol = r.group(2)
      self.numParallel = int(r.group(3))
    else:
      raise Exception("Unable to parse: {}".format(name))

class IperfExp:
  def __init__(self,num,results_dir):
    self.num = num
    self.ethtool = EthtoolOpts(results_dir,num)
    self.module_opts = ModuleOpts(results_dir,num)
    self.output_names = sorted(glob.glob("{}/{}/output-*.json".format(
      results_dir,num)))
    self.output = list(map(IperfRun,self.output_names))
    #print(self.output)

def get_bandwidth_gbps_from_json(iperfRun,padding_seconds):
  #print(iperfRun.name)
  duration = iperfRun.data['server_output_json']['start']['test_start']['duration']
  intervals = iperfRun.data['server_output_json']['intervals']
  rounded_interval = [x for x in intervals if
    int(round(x['sum']['end'])) >= padding_seconds and
    int(round(x['sum']['end'])) <= duration-padding_seconds]
  intervals_bytes = [i['sum']['bytes'] for i in rounded_interval]
  intervals_seconds = [i['sum']['seconds'] for i in rounded_interval]
  intervals_gbps = [float(b*8)/(1E9*float(s)) for b,s in \
                    zip(intervals_bytes,intervals_seconds)]
  return intervals_gbps

def get_bw(exp,protocol,numParallel,padding_seconds):
  #print(exp_num)
  runs = list(filter(
    lambda x: x.protocol == protocol and x.numParallel == numParallel,
    exp.output))
  try:
    core_gbps = list(map(lambda x:
                           get_bandwidth_gbps_from_json(x,padding_seconds),
                         runs))
    if len(core_gbps) == 0:
      return None
    interval_gbps = [0.0] * len(core_gbps[0])
    for core_interval_gbps in core_gbps:
      for idx,val in enumerate(core_interval_gbps):
        interval_gbps[idx] += val
  except:
    raise
  return (statistics.mean(interval_gbps), statistics.stdev(interval_gbps),
          interval_gbps, exp)

def get_cpu(exp,protocol,numParallel):
  #print(exp.num,protocol,numParallel)
  runs = list(filter(
    lambda x: x.protocol == protocol and x.numParallel == numParallel,
    exp.output))
  try:
    host_cpu = []; remote_cpu = []
    for run in runs:
      host_cpu.append(
        run.data['end']['cpu_utilization_percent']['host_total'])
      remote_cpu.append(
        run.data['end']['cpu_utilization_percent']['remote_total'])
  except:
    raise
  if len(host_cpu) == 0:
    print("err")
    return None
  return (
    statistics.mean(host_cpu), statistics.stdev(host_cpu), max(host_cpu),
    statistics.mean(remote_cpu), statistics.stdev(remote_cpu), max(remote_cpu),
    host_cpu, remote_cpu, exp)


def get_experiments(results_dir,padding_seconds):
  all_experiments = list(map(lambda x: IperfExp(x,results_dir),
                             sorted(map(int,os.listdir(results_dir)))))
  # Assume first experiment is correct.
  good_exp = all_experiments[0]
  experiments = list(filter(lambda exp:len(good_exp.output)==len(exp.output),
                            all_experiments))
  print("{} total experiments, {} failed.".format(
    len(all_experiments),len(all_experiments)-len(experiments)))
  return experiments

if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--padding-seconds',type=int,default=3)
  parser.add_argument('results_dir')

  args = parser.parse_args()

  experiments = get_experiments(args.results_dir,args.padding_seconds)
  cpu = {}
  for protocol,numParallel in itertools.product(['udp','tcp'],[1,2,4]):
    this_cpu = flatmap(lambda x: get_cpu(x,protocol,numParallel), experiments)
    cpu[(protocol,numParallel)] = this_cpu
    for idx,tup in enumerate(
        ["meanH", "stdevH", "maxH", "meanR", "stdevR", "maxR"]):
      with open('analysis/{}.{}.cpu.{}.txt'.format(
          protocol,numParallel,tup),'w') as f:
        for results in sorted(this_cpu,key=lambda x: x[idx],reverse=True):
          meanH, stdevH, maxH, meanR, stdevR, maxR, h, r, e = results
          f.write("\n\n=== {} ===\n".format(results[idx]))
          f.write("  + Num: {}\n".format(e.num))
          f.write("  + Enabled Ethtool: {}\n".format(e.ethtool.enabled_opts))
          f.write("  + Module Opts: {}\n".format(e.module_opts.raw))
          f.write("  + meanH, stdevH, maxH, meanR, stdevR, maxR: {}, {}, {}, {}, {}, {}\n".format(meanH, stdevH, maxH, meanR, stdevR, maxR))
          f.write("  + Host CPU: {}\n".format(h))
          f.write("  + Remote CPU: {}\n".format(r))
      with open("analysis/{}.{}.cpu.{}.csv".format(
          protocol,numParallel,tup),'w') as f:
        f.write(",".join([str(x[idx]) for x in this_cpu])+"\n")
      with open("analysis/{}.{}.cpu.none.all.csv".format(
          protocol,numParallel),'w') as f:
        f.write(",".join([str(this_cpu[0][0]),str(this_cpu[-1][0])])+"\n")

  bw = {}
  for protocol,numParallel in itertools.product(['udp','tcp'],[1,2,4]):
    with open('analysis/{}.{}.bw.txt'.format(protocol,numParallel),'w') as f:
      this_bw = flatmap(lambda x:
                        get_bw(x,protocol,numParallel,args.padding_seconds),
                        experiments)
      bw[(protocol,numParallel)] = this_bw
      sorted_bw = sorted(this_bw,key=lambda x: x[0],reverse=True)
      for v_mean,v_stdev,lst,exp in sorted_bw:
        f.write("\n\n=== {} ({}) ===\n".format(v_mean,v_stdev))
        f.write("  + Num: {}\n".format(exp.num))
        f.write("  + Enabled Ethtool: {}\n".format(exp.ethtool.enabled_opts))
        f.write("  + Module Opts: {}\n".format(exp.module_opts.raw))
        f.write("  + Vals: {}\n".format(lst))

    with open("analysis/{}.{}.bw.means.csv".format(
        protocol,numParallel),'w') as f:
      f.write(",".join([str(x[0]) for x in this_bw])+"\n")

    with open("analysis/{}.{}.bw.none.all.max.min.csv".format(
        protocol,numParallel),'w') as f:
      f.write(",".join([str(x) for x in [this_bw[0][0],this_bw[-1][0],
                                         sorted_bw[0][0],sorted_bw[-1][0]]
                      ])+"\n")

    filtered_indices = []
    for idx,tup in enumerate(this_bw):
      exp = tup[3]
      if 'tx' in exp.ethtool.enabled_opts and \
          'sg' in exp.ethtool.enabled_opts and \
          'tso' in exp.ethtool.enabled_opts:
        filtered_indices.append(idx)
    with open("analysis/tx-sg-tso.bw-indices.csv","w") as f:
      f.write(",".join([str(x) for x in filtered_indices])+"\n")

    filtered_indices = []
    for idx,tup in enumerate(this_bw):
      exp = tup[3]
      if 'tx' in exp.ethtool.enabled_opts and \
          'sg' in exp.ethtool.enabled_opts and \
          'tso' in exp.ethtool.enabled_opts and \
          'gro' in exp.ethtool.enabled_opts and \
          'rxhash' in exp.ethtool.enabled_opts:
        filtered_indices.append(idx)
    with open("analysis/tx-sg-tso-gro-rxhash.bw-indices.csv","w") as f:
      f.write(",".join([str(x) for x in filtered_indices])+"\n")
