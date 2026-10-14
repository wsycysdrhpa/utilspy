import os
import codecs
from glob import glob
from os.path import join
import re
import json
from typing import FrozenSet
import os

import pandas as pd
from urduhack.urdu_characters import URDU_ALPHABETS, URDU_DIGITS


URDU_ALL_CHARACTERS: FrozenSet[str] = frozenset().union(URDU_ALPHABETS, URDU_DIGITS)
URDU_ALL_CHARACTERS_STR = "".join(URDU_ALL_CHARACTERS)
re_useless_char_pattern = f'[^{URDU_ALL_CHARACTERS_STR}0-9\s]+'

re_useless_char = re.compile(re_useless_char_pattern, flags=re.U)
re_muti_space = re.compile("\s+", flags=re.U)

re_en_word = re.compile("[a-zA-Z0-9\']+")

src_dir = "/home/haipeng/work/data/urdu/asr/speechocean/speechocean-annot/batch_1_10h/merged_10h/valid"
audio_path_prefix = "/data/workspace/hongjie/data/urdu/unlabeled/pak-to-annot-speechocean"

out_file_prefix = "/home/haipeng/work/data/urdu/asr/speechocean/speechocean-annot/batch_1_10h/merged_10h"
out_file_wav = os.path.join(out_file_prefix, "wav.scp")
out_file_text = os.path.join(out_file_prefix, "text")
out_file_json = os.path.join(out_file_prefix, "data.list")

map_file = "/home/haipeng/work/data/urdu/asr/speechocean/speechocean-annot/batch_1_10h/speechocean_map/1_Urdu-English-words320.xlsx"


en_ur_map = dict()
df = pd.read_excel(map_file, 'Sheet1', index_col=None, na_values=['NA'])
df = df.dropna()
for index, row in df.iterrows():
    en = row['en'].strip().lower()
    ur = row['ur'].strip()
    en_ur_map[en] = ur

with codecs.open(out_file_wav, 'w') as out_file_wav_fp, \
    codecs.open(out_file_text, 'w') as out_file_text_fp, \
    codecs.open(out_file_json, 'w') as out_file_json_fp:
    for src_file in sorted(glob(join(src_dir, '*.txt'))):
        # print(src_file)
        with codecs.open(src_file, 'r') as src_fp:
            lines = src_fp.readlines()
            # skip header
            for line in lines[1:]:
                try:
                    line = line.strip()
                    file_name = os.path.basename(src_file)[:-4]
                    time_span, role, text = line.split('\t')

                    text = text.strip()
                    if (text == "" or
                        text == 'Overlap' or
                        text == 'Foreign' or
                        text == 'Noise' or
                        text == 'Unknown' or
                        text == 'TTS' or
                        text == 'Silence'):
                        continue

                    time_span = time_span.strip()
                    time_span = time_span.strip('[').strip(']').strip()
                    start, end = time_span.split('-')
                    role = role.strip('[').strip(']').strip()

                    # sub en to ur
                    text = text.lower()
                    words = text.split()
                    for i in range(len(words)):
                        if words[i] in en_ur_map:
                            words[i] = en_ur_map[words[i]]
                        elif re_en_word.match(words[i]):
                            words[i] = ''
                        else:
                            pass
                    text = " ".join(words)

                    text = re_useless_char.sub(" ", text)
                    text = re_muti_space.sub(" ", text)
                    text = text.strip()

                    key_seg = '%s_%s_%s' % (file_name, start, end)
                    audio_path = os.path.join(audio_path_prefix, file_name+".wav")

                    if text:
                        out_file_wav_fp.write("%s %s\n" % (key_seg, audio_path))
                        out_file_text_fp.write("%s %s\n" % (key_seg, text))
                        json_data = {"key": key_seg,
                                    "wav": audio_path,
                                    "txt": text,
                                    "start": float(start),
                                    "end": float(end),
                                    "role": role}
                        str_data = json.dumps(json_data, ensure_ascii=False)
                        out_file_json_fp.write("%s\n" % (str_data))
                except Exception as e:
                    print(e, line)

            # break
