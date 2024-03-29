#!/usr/bin/env python3

import argparse
import itertools
import os
import re

# http://stackoverflow.com/questions/1624883
def grouper(n, iterable, fillvalue=None):
  args = [iter(iterable)] * n
  return itertools.zip_longest(*args, fillvalue=fillvalue)

class EthtoolOpts:
  def __init__(self,results_dir,num):
    with open("{}/{}/ethtool_opts.txt".format(results_dir,num),"r") as f:
      #print("\n\n=== EthtoolOpts")
      self.raw = list(grouper(2,f.readline().split()))
      self.enabled_opts = []
      self.disabled_opts = []
      for tup in self.raw:
        if tup[1] == "on":
          self.enabled_opts.append(tup[0])
        else:
          self.disabled_opts.append(tup[0])
      #print(self.raw)
      #print(self.enabled_opts)
      #print(self.disabled_opts)

class ModuleOpts:
  def __init__(self,results_dir,num):
    #print("\n\n=== ModuleOpts")
    with open("{}/{}/module_opts.txt".format(results_dir,num),"r") as f:
      self.raw = f.readline().split()
      #print(self.raw)


def mkdir_p(path):
  try:
    os.makedirs(path)
  except:
    pass

def flatmap(func,l):
  return list(filter(lambda x: x is not None, map(func, l)))
