import glob
import json
import os
import statistics
import sys

import nic_of_time as nt
import nic_of_time.result_parsers
from nic_of_time.helper import flatmap

class IperfRun:
    def __init__(self,exp_num,path,opts):
        self.exp_num = exp_num
        self.path = path
        self.ethtool = nt.result_parsers.EthtoolOpts(path+"/ethtool.log",opts)
        if not self.ethtool.is_valid:
            self.is_valid = False
            return

        self.device_opts = opts.device.get_exp_opts(path)
        self.json_results = []
        for result in glob.glob("{}/{}-*-stdout".format(
                path,opts.nodes[1].external_address)):
            with open(result,'r') as f:
                try:
                    thread_results = json.load(f)
                    self.json_results.append(thread_results)
                    if "error" in thread_results and \
                       "No route to host" in thread_results["error"]:
                        self.is_valid = False
                        return
                except:
                    self.is_valid = False
                    return

        if len(self.json_results) != len(opts.nodes[1].commands):
            self.is_valid = False
        else:
            self.is_valid = True

    def get_bandwidth_gbps(self,padding_seconds):
        def get_interval_bandwidth_gbps(data,padding_seconds):
            if 'server_output_json' not in data:
                return None
            else:
                duration = data['server_output_json']['start']['test_start']['duration']
                intervals = data['server_output_json']['intervals']
                rounded_interval = [x for x in intervals if
                  int(round(x['sum']['end'])) >= padding_seconds and
                  int(round(x['sum']['end'])) <= duration-padding_seconds]
                intervals_bytes = [i['sum']['bytes'] for i in rounded_interval]
                intervals_seconds = [i['sum']['seconds'] for i in rounded_interval]
                intervals_gbps = [float(b*8)/(1E9*float(s)) for b,s in \
                                  zip(intervals_bytes,intervals_seconds)]
                return intervals_gbps

        assert(self.is_valid)
        core_gbps = flatmap(lambda x:
                            get_interval_bandwidth_gbps(x,padding_seconds),
                            self.json_results)
        interval_gbps = [0.0] * len(core_gbps[0])
        for core_interval_gbps in core_gbps:
            for idx,val in enumerate(core_interval_gbps):
                interval_gbps[idx] += val
        return {
            'mean': statistics.mean(interval_gbps),
            'stdev': statistics.stdev(interval_gbps),
            'raw': interval_gbps
        }

    def get_cpu(self):
        assert(self.is_valid)
        host_cpu = []; remote_cpu = []; combined_cpu = []
        for run in self.json_results:
          if 'cpu_utilization_percent' in run['end']:
            host_cpu.append(
              run['end']['cpu_utilization_percent']['host_total'])
            remote_cpu.append(
              run['end']['cpu_utilization_percent']['remote_total'])
            combined_cpu.append(host_cpu[-1]+remote_cpu[-1])
        return {
            'host_mean': statistics.mean(host_cpu),
            'host_stdev': statistics.stdev(host_cpu),
            'host_max': max(host_cpu),
            'remote_mean': statistics.mean(remote_cpu),
            'remote_stdev': statistics.stdev(remote_cpu),
            'combined_mean': statistics.mean(combined_cpu),
            'combined_stdev': statistics.stdev(combined_cpu),
            'remote_max': max(remote_cpu),
            'host_raw': host_cpu,
            'remote_raw': remote_cpu
        }
