#!/usr/bin/env python3

from itertools import combinations
from subprocess import Popen,PIPE
import sys

opts = [
	['rx-checksumming','rx'],
	['tx-checksumming','tx'],
	['scatter-gather','sg'],
	['tcp-segmentation-offload','tso'],
	['generic-segmentation-offload','gso'],
	['generic-receive-offload','gro'],
#	['rx-vlan-offload','rxvlan'],
#	['tx-vlan-offload','txvlan'],
	['receive-hashing','rxhash']
]

mlx4EnOpts = [
	['udp-rss','udp_rss','1']
]

mlx4CoreOpts = [
  ['flow-steering','log_num_mgm_entry_size','-1']
]

def runExp(exp_num,expOptTups,expMlx4EnOptTups,expMlx4CoreOptTups):
  ethOpts = " ".join([x[1] + " on" for x in expOptTups] + [x[1] + " off" for x in opts if x not in expOptTups])
  moduleOpts = ""
  if expMlx4EnOptTups:
    moduleOpts = "options mlx4_en "
    for x in expMlx4EnOptTups:
      moduleOpts += x[1] + "=" + x[2]
      moduleOpts += ","
    moduleOpts = moduleOpts[:-1]
    moduleOpts += "\n"
  if expMlx4CoreOptTups:
    moduleOpts += "options mlx4_core "
    for x in expMlx4CoreOptTups:
      moduleOpts += x[1] + "=" + x[2]
      moduleOpts += ","
    moduleOpts = moduleOpts[:-1]
  try:
    p = Popen(['./autobench-impl.sh', str(exp_num), ethOpts, moduleOpts])
    p.communicate()
  except KeyboardInterrupt:
    p.terminate()
    raise

  return p.returncode
	#print ("=== OUTPUT ", str(exp_num), "===\n", ethOpts, "\n", moduleOpts, "\n")
	#return 0

exp_num = 1

with open("error-combinations.txt",'w') as f:
	for i in range(0,len(opts)+1):
		print("=== {} ===".format(i))
		for tups in combinations(opts,i):
			for j in range(0,len(mlx4EnOpts)+1):
				print("=== {} ===".format(j))
				for mlx4EnTups in combinations(mlx4EnOpts, j):
					for k in range(0,len(mlx4CoreOpts)+1):
						print("=== {} ===".format(k))
						for mlx4CoreTups in combinations(mlx4CoreOpts, k):
							print("	 {}: {} {} {}".format(exp_num,tups,mlx4EnTups,mlx4CoreTups))
							ret = runExp(exp_num,tups,mlx4EnTups,mlx4CoreTups)
							print(ret)
							if ret != 0:
								f.write(str(tups + mlx4EnTups + mlx4CoreTups)+"\n")
								f.flush()
							else:
								exp_num+=1
