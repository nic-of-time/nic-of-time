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
