#!/bin/bash

set -x -e

mkdir -p analysis/slices
RESULTS=../../results/results-dec-7/iperf

for PAR in {1,2,4}; do
  LOW=22.75; HIGH=23
  ./analyze-data-slice.py $RESULTS bw udp $PAR $LOW $HIGH \
                          &> analysis/slices/bw-udp-$PAR-$LOW-$HIGH.txt &
done

PAR=4; LOW=17.6; HIGH=19.4
./analyze-data-slice.py $RESULTS bw udp $PAR $LOW $HIGH \
                        &> analysis/slices/bw-udp-$PAR-$LOW-$HIGH.txt &

PAR=2; LOW=17.2; HIGH=18.6
./analyze-data-slice.py $RESULTS bw tcp $PAR $LOW $HIGH \
  &> analysis/slices/bw-tcp-$PAR-$LOW-$HIGH.txt &

wait
