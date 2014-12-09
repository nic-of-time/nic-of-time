Do we need all the hardware acceleration
that are present in today's high end network interface cards (NICs)?
With the increasing number and complexity of networking protocols, we
have naturally
progressed towards pushing more and more operations away from the CPU (and
hence from the kernel) to the NIC.
Offloading features to the NIC may sacrifice flexibility
for performance.
This repository presents the **NIC of Time**
profiling utility
to study the impact of NIC features on benchmark and application performance.

![](https://raw.githubusercontent.com/nic-of-time/nic-of-time/master/figures/architecture.png?raw=true)

# Results Archive
Future work is to host the results and analysis.
See #2 to further discuss.

# Running benchmarks or applications
The benchmarks directory contains benchmarks and applications
NIC of Time current implements.
Collecting and analyzing the an application can be done with
the following procedure.

1. Modify the implementation script `*impl.sh` to connect to your servers.
2. Modify the driving script, `drive*.py` to explore the
NIC features you're interested in.
3. Run `./drive*.py` to collect the raw data.
4. Run `./analyze-data.py` to parse and interpret the data.
5. Run `./analyze-data.r` to produce CDF's and plot the data.

# Adding benchmarks or applications
Better sharing components is future work, see #3.
