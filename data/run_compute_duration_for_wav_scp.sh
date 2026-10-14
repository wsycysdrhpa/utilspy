#!/bin/bash


wav_scp_file=$1


cat ${wav_scp_file} | awk '{print $2}' |  awk '{print "sox "$1" -n stat"}' > compute_duration.sh

. compute_duration.sh 2> duration.log

grep Length duration.log | awk -F ':' '{sum+=$2} END {print sum"s"}'
grep Length duration.log | awk -F ':' '{sum+=$2} END {print sum/3600"h"}'


rm compute_duration.sh
rm duration.log
