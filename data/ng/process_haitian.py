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


def is_header_line(line):
    """首行若不是 [start-end]\\trole\\ttext 格式，视为表头。"""
    parts = line.strip().split('\t')
    if len(parts) < 3:
        return True
    time_span = parts[0].strip().strip('[]')
    if '-' not in time_span:
        return True
    try:
        start, end = time_span.split('-', 1)
        float(start)
        float(end)
        return False
    except ValueError:
        return True


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
    n_files = len(src_files)
    n_files_empty = 0
    n_files_with_data = 0
    n_total = 0
    n_filtered = 0
    n_written = 0
    n_sox_ok = 0
    n_sox_fail = 0
    n_error = 0
    sox_fail_shown = 0

    with codecs.open(out_file_wav, 'w') as out_file_wav_fp, \
        codecs.open(out_file_text, 'w') as out_file_text_fp, \
        codecs.open(out_file_json, 'w') as out_file_json_fp:
        for src_file in tqdm(src_files, desc=batch, unit='file'):
            with codecs.open(src_file, 'r') as src_fp:
                lines = src_fp.readlines()
                file_prefix = os.path.basename(src_file)[:-4]
                src_audio_path = join(src_audio_dir, file_prefix + src_audio_postfix)

                data_lines = []
                for i, raw in enumerate(lines):
                    if not raw.strip():
                        continue
                    if i == 0 and is_header_line(raw):
                        continue
                    data_lines.append(raw)

                if not data_lines:
                    n_files_empty += 1
                    continue
                n_files_with_data += 1

                for line in data_lines:
                    n_total += 1
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
                            n_filtered += 1
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
                            status, output = subprocess.getstatusoutput(cmd)
                            if status != 0 or not os.path.exists(out_wav_file):
                                n_sox_fail += 1
                                if sox_fail_shown < 10:
                                    tqdm.write(
                                        f'sox failed ({status}): {cmd}\n'
                                        f'exists={os.path.exists(out_wav_file)} output={output}'
                                    )
                                    sox_fail_shown += 1
                            else:
                                n_sox_ok += 1

                        wav_scp_key = '%s_%s_%s' % (file_prefix, start, end)
                        out_file_wav_fp.write("%s %s\n" % (wav_scp_key, out_wav_file))
                        out_file_text_fp.write("%s %s\n" % (wav_scp_key, text))
                        json_data = {"key": wav_scp_key,
                                    "wav": out_wav_file,
                                    "txt": text,
                                    "role": role}
                        str_data = json.dumps(json_data, ensure_ascii=False)
                        out_file_json_fp.write("%s\n" % (str_data))
                        n_written += 1

                    except Exception as e:
                        n_error += 1
                        tqdm.write(f'{e} {line}')

                # break

    summary = (
        f'[{batch}] 文件={n_files} 有数据={n_files_with_data} 空文件={n_files_empty} '
        f'标注行数={n_total} 过滤={n_filtered} 写出={n_written} 异常={n_error}'
    )
    if run_cmd:
        summary += f' sox成功={n_sox_ok} sox失败={n_sox_fail}'
    else:
        summary += ' (未执行sox, 加 --run-cmd 切分音频)'
    print(summary)