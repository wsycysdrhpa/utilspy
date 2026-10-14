"""
输入data.list, 包含start和end, 需要切分音频
输出wav.scp
"""

import os
import codecs
import json
import jsonlines
import sys

# src_file = '/workspace/haipeng/haipeng/work/asr/wenet-v2.2.0/examples/gigaspeech/s0_run/data/test_pidgin_428/data.list'
# dst_dir = '/workspace/haipeng/haipeng/work/asr/wenet-v2.2.0/examples/gigaspeech/s0_run/data/test_pidgin_428'

src_file = '/workspace/haipeng/haipeng/work/test/test_whisper/id_test_3888/test_cuishou_4h/data.list'
dst_dir = '/workspace/haipeng/haipeng/work/test/test_whisper/id_test_3888/test_cuishou_4h'

dst_wav_file = os.path.join(dst_dir, 'wav.scp')
dst_wav_dir = os.path.join(dst_dir, 'audio')

if not os.path.exists(dst_wav_dir):
    print(dst_wav_dir)
    os.makedirs(dst_wav_dir)

with codecs.open(dst_wav_file, 'w') as dst_fp, \
    jsonlines.open(src_file, 'r') as src_fp:
    for line in src_fp:
        # print(line)
        key = line['key']
        old_wav = line['wav']
        wav_prefix = old_wav[:-4]

        # wav format better, mp3 format may occur onnx decoding error
        # wav_suffix = old_wav[-3:]
        wav_suffix = 'wav'

        start = line['start']
        end = line['end']
        wav = os.path.join(dst_wav_dir, '{}_{}_{}.{}'.format(os.path.basename(wav_prefix), start, end, wav_suffix))
        # print(wav)

        dst_fp.write('{} {}\n'.format(key, wav))

        cmd = 'sox {} {} trim {} {}'.format(old_wav, wav, start, float(end)-float(start))
        print(cmd)
        if not os.path.exists(wav):
            os.system(cmd)

        # break
