#!/bin/bash


wav_list_file=$1


cat ${wav_list_file} | awk '{print "sox "$1" -n stat"}' > compute_duration.sh

. compute_duration.sh 2> duration.log

grep Length duration.log | awk -F ':' '{sum+=$2} END {print sum"s"}'
grep Length duration.log | awk -F ':' '{sum+=$2} END {print sum/3600"h"}'

# grep Length duration.log | awk '{print $3}' > wav.duration
# paste ${wav_list_file} wav.duration > `dirname ${wav_list_file}`/wav_and_duration.txt
# rm wav.duration

rm compute_duration.sh
rm duration.log
