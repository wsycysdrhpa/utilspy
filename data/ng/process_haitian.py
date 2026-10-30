import os
import codecs
from glob import glob
from os.path import join
import argparse
import re
import json
import subprocess
from tqdm import tqdm


re_useless_char_pattern = r'[^A-Za-z0-9\s]+'

re_useless_char = re.compile(re_useless_char_pattern, flags=re.U)
re_muti_space = re.compile(r'\s+', flags=re.U)


parser = argparse.ArgumentParser()
parser.add_argument('--run-cmd', action='store_true', help='执行 sox 切分音频')
args = parser.parse_args()
run_cmd = args.run_cmd


root_dir = '/work/data/asr/ng/nigerian_pidgin/speechocean/speechocean-annot/collection/2026'
batchs = [
          'vad_output_ng_collection_20260908_ch1_30h_delivery_20260924_19h',
        ]

for batch in batchs:
    src_dir = join(root_dir, batch, 'valid')

    # 2026 collection batch 1
    src_audio_dir = '/work/haipeng/work/business/ng/collection/audio_to_label/20260908/vad_output_ng_collection_20260908_ch1_30h'

    src_audio_postfix = '.wav'

    out_file_prefix = join(root_dir, batch, 'valid_out')
    out_seg_dir = join(out_file_prefix, 'audio_seg')
    out_file_wav = join(out_file_prefix, "wav.scp")
    out_file_text = join(out_file_prefix, "text")
    out_file_json = join(out_file_prefix, "data.list")


    if not os.path.exists(out_seg_dir):
        os.makedirs(out_seg_dir)

    src_files = sorted(glob(join(src_dir, '*.txt')))
    with codecs.open(out_file_wav, 'w') as out_file_wav_fp, \
        codecs.open(out_file_text, 'w') as out_file_text_fp, \
        codecs.open(out_file_json, 'w') as out_file_json_fp:
        for src_file in tqdm(src_files, desc=batch, unit='file'):
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
                        if run_cmd:
                            # print(cmd)
                            _, _ = subprocess.getstatusoutput(cmd)

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
                        tqdm.write(f'{e} {line}')

                # break
