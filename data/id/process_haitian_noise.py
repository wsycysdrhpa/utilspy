import os
import codecs
from glob import glob
from os.path import join
import re
import json
import subprocess


re_useless_char_pattern = f'[^A-Za-z0-9\s]+'

re_useless_char = re.compile(re_useless_char_pattern, flags=re.U)
re_muti_space = re.compile("\s+", flags=re.U)


batchs = ['batch_1_cuishou_4.7h',
          'batch_2_cuishou_6h',
          'batch_3_cuishou_5h',
          'batch_4_cuishou_5.5h',
          'batch_5_cuishou_6.4h',
          'batch_6_cuishou_11h',
          'batch_7_cuishou_16.7h',
          'batch_8_cuishou_11h',
          'batch_9_airudder_cuishou_5h',
          'batch_10_wiz_cuishou_6h',
          'batch_11_dianxiao_5h',
          'batch_12_dianxiao_airudder_cg',
          'batch_14_dianxiao_airudder_cg',
        ]

# batchs = ['batch_13_cuishou_20231208',
#           'batch_15_cuishou_agent_20231221',
#         ]

for batch in batchs:
    root_dir = '/workspace/haipeng/haipeng/work/data/indonesia/asr/speechocean/speechocean-annot/collection'
    src_dir = join(root_dir, batch, 'invalid')
    src_audio_dir = '/home/yangsen/data/asr/speechocean/speechocean-annot/indonesia/{}/wav'.format(batch)
    src_audio_postfix = '.mp3'
    # batch_13, batch_15
    # src_audio_postfix = '.wav'

    out_file_prefix = join(root_dir, batch, 'invalid_out')
    out_seg_dir = join(out_file_prefix, 'audio_seg')
    out_file_wav = join(out_file_prefix, "wav.scp")
    out_file_text = join(out_file_prefix, "text")
    out_file_json = join(out_file_prefix, "data.list")


    if not os.path.exists(out_seg_dir):
        os.makedirs(out_seg_dir)

    with codecs.open(out_file_wav, 'w') as out_file_wav_fp, \
        codecs.open(out_file_text, 'w') as out_file_text_fp, \
        codecs.open(out_file_json, 'w') as out_file_json_fp:
        for src_file in sorted(glob(join(src_dir, '*.txt'))):
            with codecs.open(src_file, 'r') as src_fp:
                lines = src_fp.readlines()
                file_prefix = os.path.basename(src_file)[:-4]
                src_audio_path = join(src_audio_dir, file_prefix + src_audio_postfix)
                # skip header
                for line in lines[1:]:
                    try:
                        line = line.strip()
                        time_span, invalid_reason = line.split('\t')

                        if (invalid_reason == "" or
                            invalid_reason == 'Overlap' or
                            invalid_reason == 'Foreign' or
                            invalid_reason == 'Unknown' or
                            invalid_reason == 'TTS' or
                            invalid_reason == 'Silence'):
                            continue

                        text = '*'

                        time_span = time_span.strip()
                        time_span = time_span.strip('[').strip(']').strip()
                        start, end = time_span.split('-')

                        out_wav_file = "{}/{}_{}_{}.wav".format(out_seg_dir, file_prefix, start, end)
                        cmd = "sox {} {} trim {} {}".format(src_audio_path, out_wav_file, start, round(float(end)-float(start), 2))
                        # print(cmd)
                        _, _  = subprocess.getstatusoutput(cmd)

                        wav_scp_key = '%s_%s_%s' % (file_prefix, start, end)
                        out_file_wav_fp.write("%s %s\n" % (wav_scp_key, out_wav_file))
                        out_file_text_fp.write("%s %s\n" % (wav_scp_key, text))
                        json_data = {"key": wav_scp_key,
                                    "wav": out_wav_file,
                                    "txt": text,
                                    "invalid_reason": invalid_reason}
                        str_data = json.dumps(json_data, ensure_ascii=False)
                        out_file_json_fp.write("%s\n" % (str_data))

                    except Exception as e:
                        print(e, line)

                # break
