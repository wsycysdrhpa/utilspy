import os
import codecs
from os.path import join, splitext, basename
import argparse
import csv
import re
import json
from tqdm import tqdm


# 字母、数字、空白，以及词内撇号(I'm/don't)
re_useless_char_pattern = r"[^A-Za-z0-9\s']+"

re_useless_char = re.compile(re_useless_char_pattern, flags=re.U)
re_muti_space = re.compile(r'\s+', flags=re.U)
# 非词内的孤立撇号（如引号）
re_dangling_apos = re.compile(r"(?<![A-Za-z0-9])'|'(?![A-Za-z0-9])")

APOSTROPHE_MAP = {
    '\u2018': "'",  # ‘
    '\u2019': "'",  # ’
    '\u201A': "'",  # ‚
    '\u2032': "'",  # ′
    '\u02BC': "'",  # ʼ
    '\uFF07': "'",  # ＇
    '`': "'",
    '´': "'",
}


def normalize_apostrophes(text):
    for src, dst in APOSTROPHE_MAP.items():
        text = text.replace(src, dst)
    return text


def clean_text(text):
    """清洗文本：去掉无用标点（含连字符），保留 I'm、don't 这类词内撇号。"""
    text = normalize_apostrophes(text)
    text = re_useless_char.sub(" ", text)
    text = re_dangling_apos.sub(" ", text)
    text = re_muti_space.sub(" ", text)
    text = text.upper()
    return text.strip()


def utt_key(audio_name):
    """common_voice_pcm_41361476.mp3 -> common_voice_pcm_41361476"""
    return splitext(basename(audio_name))[0]


parser = argparse.ArgumentParser(description='Common Voice tsv 转 wav.scp / text / data.list')
parser.add_argument('--tsv', required=True, help='输入 tsv，如 test.tsv')
parser.add_argument('--src-audio-dir', required=True, dest='src_audio_dir',
                    help='音频目录，与 tsv 的 path 拼接成完整路径')
parser.add_argument('--out-dir', required=True, help='输出目录，写入 wav.scp、text、data.list')
args = parser.parse_args()
src_audio_dir = args.src_audio_dir

out_file_wav = join(args.out_dir, 'wav.scp')
out_file_text = join(args.out_dir, 'text')
out_file_json = join(args.out_dir, 'data.list')

os.makedirs(args.out_dir, exist_ok=True)

n_total = 0
n_filtered = 0
n_written = 0
n_error = 0

with codecs.open(args.tsv, 'r', encoding='utf-8') as src_fp, \
        codecs.open(out_file_wav, 'w', encoding='utf-8') as out_file_wav_fp, \
        codecs.open(out_file_text, 'w', encoding='utf-8') as out_file_text_fp, \
        codecs.open(out_file_json, 'w', encoding='utf-8') as out_file_json_fp:
    reader = csv.DictReader(src_fp, delimiter='\t')
    if reader.fieldnames is None or 'path' not in reader.fieldnames or 'sentence' not in reader.fieldnames:
        raise SystemExit('tsv 需要包含 path 和 sentence 列')

    rows = list(reader)
    for row in tqdm(rows, desc=basename(args.tsv), unit='utt'):
        n_total += 1
        try:
            audio_name = (row.get('path') or '').strip()
            text = (row.get('sentence') or '').strip()
            if not audio_name or not text:
                n_filtered += 1
                continue

            text = clean_text(text)
            if not text:
                n_filtered += 1
                continue

            key = utt_key(audio_name)
            wav_path = join(src_audio_dir, audio_name)

            out_file_wav_fp.write('%s %s\n' % (key, wav_path))
            out_file_text_fp.write('%s %s\n' % (key, text))
            json_data = {
                'key': key,
                'wav': wav_path,
                'txt': text,
            }
            out_file_json_fp.write('%s\n' % json.dumps(json_data, ensure_ascii=False))
            n_written += 1
        except Exception as e:
            n_error += 1
            tqdm.write(f'{e} {row}')

summary = (
    f'[{basename(args.tsv)}] 行数={n_total} 过滤={n_filtered} '
    f'写出={n_written} 异常={n_error}'
)
print(summary)
print(f'wav.scp: {out_file_wav}')
print(f'text:    {out_file_text}')
print(f'data.list: {out_file_json}')
