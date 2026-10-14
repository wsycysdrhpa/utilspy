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


batchs = [
          'batch_1_marketing_4.96h',
          'batch_2_marketing_10.3h',
          'batch_3_marketing_7.28h',
        #   'batch_4_marketing_14.74h',
        ]

for batch in batchs:
    root_dir = '/workspace/haipeng/haipeng/work/data/indonesia/asr/speechocean/speechocean-annot/marketing'
    src_dir = join(root_dir, batch, 'valid')

    # 2023 batch 1-15
    # src_audio_dir = '/home/yangsen/data/asr/speechocean/speechocean-annot/indonesia/{}/wav'.format(batch)
    # 2024 batch 1-3
    src_audio_dir = '/workspace/haipeng/haipeng/work/data/indonesia/asr/to_label/marketing_20240603-20240603/audio_left_seged'
    # 2024 batch_4
    # src_audio_dir = '/workspace/haipeng/haipeng/work/data/indonesia/asr/to_label/voicemail/0629_5-10s_10k/audio_left'

    src_audio_postfix = '.wav'

    out_file_prefix = join(root_dir, batch, 'valid_out')
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
                        time_span, role, text = line.split('\t')

                        text = text.strip()
                        if (text == "" or
                            text == 'Overlap' or
                            text == 'Foreign' or
                            text == 'Noise' or
                            text == 'Unknown' or
                            text == 'TTS' or
                            text == 'Silence' or
                            text == 'BackgroundSpeech'):
                            continue

                        text = re_useless_char.sub(" ", text)
                        text = re_muti_space.sub(" ", text)
                        text = text.upper()
                        text = text.strip()

                        time_span = time_span.strip()
                        time_span = time_span.strip('[').strip(']').strip()
                        start, end = time_span.split('-')

                        role = role.strip('[').strip(']').strip()
                        # all is customer audio
                        # role = "Customer1"

                        out_wav_file = "{}/{}_{}_{}.wav".format(out_seg_dir, file_prefix, start, end)
                        cmd = "sox {} {} trim {} {}".format(src_audio_path, out_wav_file, start, round(float(end)-float(start), 2))
                        # print(cmd)
                        # _, _  = subprocess.getstatusoutput(cmd)

                        wav_scp_key = '%s_%s_%s' % (file_prefix, start, end)
                        out_file_wav_fp.write("%s %s\n" % (wav_scp_key, out_wav_file))
                        out_file_text_fp.write("%s %s\n" % (wav_scp_key, text))
                        json_data = {"key": wav_scp_key,
                                    "wav": out_wav_file,
                                    "txt": text,
                                    "role": role}
                        str_data = json.dumps(json_data, ensure_ascii=False)
                        out_file_json_fp.write("%s\n" % (str_data))

                    except Exception as e:
                        print(e, line)

                # break
