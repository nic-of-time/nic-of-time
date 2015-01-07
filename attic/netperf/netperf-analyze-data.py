#!/usr/bin/env python3

import csv
import glob
import operator
import sys
from fn import _
from fn.uniform import reduce
from fn.iters import tail

headers = [
  'timestamp', 'myIP', 'myPort', 'otherIP', 'otherPort', 'threadNum',
  'timeInterval', 'dataTransferredBytes', 'bandwidthBitsPerSecond',
  'jitterMillisecs', 'lostDatagrams', 'totalDatagramsSent',
  'percentLoss', 'datagramsReceivedOutOfOrder'
]
out_headers = ["Threads","BandwidthBitsPerSecond",
    'DatagramsReceivedOutOfOrder','TotalLostDatagrams','TotalDatagramsSent']
num_client_threads = [1,2,4]
exp_nums = range(1,48)

### Extraction.
for exp_num in exp_nums:
  # print("Exp",exp_num)
  plot_data_name = 'netperf/{}/plot-data.csv'.format(exp_num)
  plot_data = open(plot_data_name,'w')
  plot_data_w = csv.writer(plot_data)
  plot_data_w.writerow(["Threads","BandwidthBitsPerSecond",
    'DatagramsReceivedOutOfOrder','TotalLostDatagrams','TotalDatagramsSent'])
  for threads in num_client_threads:
    # print("  Threads", threads)
    with open("netperf/{}/server-{}.csv".format(exp_num,threads),'r') as s_f:
      with open("netperf/{}/client-{}.csv".format(exp_num,threads),'r') as c_f:
        s_csv_r = csv.reader(s_f)
        c_csv_r = csv.reader(c_f)
        s = [r for r in s_csv_r]
        c = [r for r in c_csv_r]
        s_dict = [dict(list(zip(headers,x))) for x in s]
        c_dict = [dict(list(zip(headers,x))) for x in c]
        if threads == 1:
          summary_row = [c_dict[1]]
        else:
          summary_row = list(filter(_['threadNum'] == '-1', c_dict))
        assert(len(summary_row) == 1)
        summary_row = summary_row[0]

        datagrams = [r for r in c_dict if 'lostDatagrams' in r]
        datagramsReceivedOutOfOrder = \
          reduce(_+_,[r['datagramsReceivedOutOfOrder'] for r in datagrams])
        totalLostDatagrams = reduce(_+_,[r['lostDatagrams'] for r in datagrams])
        totalDatagramsSent = \
            reduce(_+_,[r['totalDatagramsSent'] for r in datagrams])
        plot_data_w.writerow([
          threads,summary_row['bandwidthBitsPerSecond'],
          datagramsReceivedOutOfOrder,totalLostDatagrams,totalDatagramsSent
        ])
  plot_data.close()

### Analysis.
e_dat = []; band_dat_4 = []; outOfOrderRatios_4 = []; lostRatios_4 = []
ethtool_opts = []
for exp_num in exp_nums:
  # print("Exp",exp_num)
  with open('netperf/{}/ethtool_opts.txt'.format(exp_num),'r') as f:
    ethtool_opts.append(f.readline())
  plot_data_name = 'netperf/{}/plot-data.csv'.format(exp_num)
  with open(plot_data_name,'r') as f:
    csv_r = csv.reader(f)
    dat = [dict(list(zip(out_headers,r))) for r in tail(csv_r)]
    e_dat.append(dat)
    band_dat_4.append(dat[-1]['BandwidthBitsPerSecond'])
    outOfOrderRatios_4.append(float(dat[-1]['DatagramsReceivedOutOfOrder'])/
        float(dat[-1]['TotalDatagramsSent']))
    lostRatios_4.append(float(dat[-1]['TotalLostDatagrams'])/
        float(dat[-1]['TotalDatagramsSent']))

def printSorted(tagline,units,arr,reverse):
  print("\n=== {}, everything off ===".format(tagline))
  e_num = 0; val = arr[e_num]
  print("  {}{}: Experiment {}".format(float(val)/1E6,units,e_num))
  print("    + {}".format(ethtool_opts[e_num]))

  print("\n=== {} ===".format(tagline))
  tups = list(sorted([(e,i) for i,e in enumerate(arr)],reverse=reverse))
  for val,e_num in tups[0:5]:
    print("  {}{}: Experiment {}".format(float(val)/1E6,units,e_num))
    print("    + {}".format(ethtool_opts[e_num]))
  print("  ...\n")
  for val,e_num in tups[-5:-1]:
    print("  {}{}: Experiment {}".format(float(val)/1E6,units,e_num))
    print("    + {}".format(ethtool_opts[e_num]))

printSorted("Bandwidth for 4 client threads"," Mbits/sec",band_dat_4,True)
printSorted("Lowest out of order datagram ratio for 4 client threads","",
    outOfOrderRatios_4,False)
printSorted("Lowest lost datagram ratio for 4 client threads","",
    lostRatios_4,False)
