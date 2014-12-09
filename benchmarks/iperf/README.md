# UDP Benchmarks.

## iperf: Increasing number of client threads
### Running the experiment
The experimentation is driven completely from a non-susitna computer,
and no results are stored on susitna.

`./drive-iperf-exp.py` will
remotely launch `iperf` on two nodes and collect data locally
while exploring all combinatorial options off offload features.
This is implemented by calling `iperf-impl.sh`.
The directory structure is
`iperf/<experiment number>/{server,client}-{tcp,udp}-<client threads>.csv`,
where the experiment directory contains additional metadata.
For example:

```
benchmarks/iperf [master*] » tree iperf
iperf
└── 1
    ├── ethtool_opts.txt
    ├── client.ethtool.txt
    └── server.ethtool.txt
    ├── plot-data.csv
    ├── client-tcp-1.csv
    ├── client-tcp-25.csv
    ├── client-udp-1.csv
    ├── client-udp-25.csv
    ├── ...
    ├── server-tcp-1.csv
    ├── server-tcp-25.csv
    ├── server-udp-1.csv
    ├── server-udp-25.csv 
    ├── ...
└── ...
```

### Plotting data
Once the experiment completes, `./iperf-analyze-data.py` parses
the output from `iperf` and outputs an analysis and csv files.
`./iperf-plots.r` will read the csv files and create plots (unfinished).

## UDP Fragmentation Offload Test
TODO: `uthtool-ufo` offers this setting.

## Media Streaming
Idea: Use ffmpeg to stream a video file from YouTube over UDP.
TODO: How does this sound?

## UDT file transfer
Use http://udt.sourceforge.net/ to transfer a randomly sized file over UDP.
TODO: How does this sound?

## Routing
TODO
