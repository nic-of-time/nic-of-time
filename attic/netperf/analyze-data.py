#!/usr/bin/env python3

import argparse
import itertools
import os
import re
import sys

sys.path.insert(0,"../shared")
from analysis import EthtoolOpts,ModuleOpts,mkdir_p

parser = argparse.ArgumentParser()
parser.add_argument('results_dir')

args = parser.parse_args()

mkdir_p("analysis")

experiments = sorted(map(int, os.listdir(args.results_dir)))

class NetperfTSV:
  # Recv   Send    Send                          Utilization       Service Demand
  # Socket Socket  Message  Elapsed              Send     Recv     Send    Recv
  # Size   Size    Size     Time     Throughput  local    remote   local   remote
  # bytes  bytes   bytes    secs.    10^6bits/s  % S      % S      us/KB   us/KB
  def __init__(self,num,fname):
    self.headers = ["recv_sock","send_sock", "send_msg", "time",
                    "throughput", "util_send",
                    "util_recv", "service_send", "demand_recv"]
    #print("\n\n=== NetperfTSV")
    with open("{}/{}/{}".format(args.results_dir,num,fname),'r') as f:
      lines = f.readlines()
      self.data = lines[-1].split()
      for i,x in enumerate(self.data):
        try: self.data[i] = float(x)
        except: pass
      assert(len(self.data)==len(self.headers))
      self.dataMap = dict(zip(self.headers,self.data))
      #print(self.dataMap)

class NetperfCSV:
  def __init__(self,num,fname):
    #print("\n\n=== NetperfCSV")
    with open("{}/{}/{}".format(args.results_dir,num,fname),'r') as f:
      lines = f.readlines()
      #self.headers = lines[1].split(",")
      self.headers = ["local_send_sock","remote_recv_sock",
                      "send_msg", "time",
                      "throughput", "throughput_units",
                      "util_send", "util_send_method",
                      "util_recv", "util_recv_method",
                      "service_send", "demand_recv", "demand_units"]
      #print(num)
      self.data = lines[2].split(",")
      for i,x in enumerate(self.data):
        try: self.data[i] = float(x)
        except: pass
      self.dataMap = dict(zip(self.headers,self.data))
      #print(self.dataMap)

class NetperfExp:
  def __init__(self,num):
    self.num = num
    self.ethtool = EthtoolOpts(args.results_dir,num)
    self.module_opts = ModuleOpts(args.results_dir,num)
    self.data = {}
    try: self.data['tcp_sendfile'] = NetperfTSV(num,"client_TCP_SENDFILE.csv")
    except: self.data['tcp_sendfile'] = None
    try: self.data['tcp_stream'] = NetperfCSV(num,"client_TCP_STREAM.csv")
    except: self.data['tcp_stream'] = None
    try: self.data['udp_stream'] = NetperfCSV(num,"client_UDP_STREAM.csv")
    except: self.data['udp_stream'] = None

  def get_response(self,mode,response):
    mode_data = self.data[mode]
    if mode_data:
      try:
        response_idx = mode_data.headers.index(response)
      except:
        print(response,mode_data.headers)
        raise
      return mode_data.data[response_idx]
    else:
      return None

exps = list(map(NetperfExp, sorted(map(int,os.listdir(args.results_dir)))))

def output_analysis(mode,response):
  all_results = []
  for exp in exps:
    val = exp.get_response(mode,response)
    if val:
      all_results.append((val,exp))
  sorted_results = sorted(all_results,key=lambda x: x[0],reverse=True)
  with open("analysis/{}.{}.txt".format(mode,response),'w') as f:
    for val,exp in sorted(all_results,key=lambda x: x[0],reverse=True):
      f.write("\n\n=== {} ===\n".format(val))
      f.write("  + exp_num: {}\n".format(exp.num))
      f.write("  + Enabled Ethtool: {}\n".format(exp.ethtool.enabled_opts))
      f.write("  + Module Opts: {}\n".format(exp.module_opts.raw))
  with open("analysis/{}.{}.csv".format(mode,response),'w') as f:
    f.write(",".join([str(x[0]) for x in all_results])+"\n")
  with open("analysis/{}.{}.none.all.max.min.csv".format(mode,response),'w') as f:
    f.write(",".join([str(x[0]) for x in [
      all_results[0],all_results[-1],
      sorted_results[0],sorted_results[-1]
    ]])+"\n")

for mode,response in itertools.product(
    ["tcp_sendfile","tcp_stream","udp_stream"],
    ["throughput","util_send","util_recv","service_send","demand_recv"]):
  output_analysis(mode,response)
