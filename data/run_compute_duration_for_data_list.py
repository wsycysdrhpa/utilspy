import jsonlines
import sys
import subprocess


src_file = sys.argv[1]


duration_all = 0.0
with jsonlines.open(src_file) as f:
    for line in f:
        if 'start' in line and 'end' in line:
            duration = line['end'] - line['start']
        else:
            wav_path = line['wav']
            cmd = "sox %s -n stat 2> .tmp && grep Length .tmp | awk -F ':' '{print $2}' | sed -e 's/^[ \t]*//g' -e 's/[ \t]*$//g'" % wav_path
            _, duration = subprocess.getstatusoutput(cmd)
            duration = round(float(duration), 2)

        duration_all += duration

        # break

print('{}h'.format(duration_all/3600))
