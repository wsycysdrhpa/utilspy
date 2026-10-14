# coding=utf-8


import os
import codecs
from glob import glob
from os.path import join
import re
import json
from typing import FrozenSet

import pandas as pd
from bnlp.corpus import stopwords, punctuations, letters, digits
from bnlp import CleanText


clean_text = CleanText(
   fix_unicode=True,
   unicode_norm=True,
   unicode_norm_form="NFKC",
   remove_url=False,
   remove_email=False,
   remove_emoji=False,
   remove_number=False,
   remove_digits=False,
   remove_punct=True,
   replace_with_url="<URL>",
   replace_with_email="<EMAIL>",
   replace_with_number="<NUMBER>",
   replace_with_digit="<DIGIT>",
   replace_with_punct = ""
)

re_muti_space = re.compile("\s+", re.UNICODE)

# for train
src_file = "/data/workspace/haipeng/haipeng/work/data/other/bengali/bengaliai/bengaliai-speech/train_split_train.csv"
out_file_prefix = "/data/workspace/haipeng/haipeng/work/data/other/bengali/bengaliai/bengaliai-speech.processed/train"

# for dev
# src_file = "/data/workspace/haipeng/haipeng/work/data/other/bengali/bengaliai/bengaliai-speech/train_split_valid.csv"
# out_file_prefix = "/data/workspace/haipeng/haipeng/work/data/other/bengali/bengaliai/bengaliai-speech.processed/valid"

audio_path_prefix = "/data/workspace/haipeng/haipeng/work/data/other/bengali/bengaliai/bengaliai-speech/train_mp3s"

out_file_wav = os.path.join(out_file_prefix, "wav.scp")
out_file_text = os.path.join(out_file_prefix, "text")
out_file_json = os.path.join(out_file_prefix, "data.list")

with codecs.open(out_file_wav, 'w') as out_file_wav_fp, \
    codecs.open(out_file_text, 'w') as out_file_text_fp, \
    codecs.open(out_file_json, 'w') as out_file_json_fp:
    df = pd.read_csv(src_file)
    for index, row in df.iterrows():
        file_name = row['id'].strip()
        text = row['sentence'].strip()
        utt_type = row['split'].strip()
        try:
            if (text == "" or
                text == 'Overlap' or
                text == 'Foreign' or
                text == 'Noise' or
                text == 'Unknown' or
                text == 'TTS' or
                text == 'Silence'):
                continue

            text_ori = text
            text = clean_text(text)
            text = re_muti_space.sub(" ", text)
            text = text.strip()
            if text_ori != text:
                pass
                print('text_ori:', text_ori)
                print('text____:', text)

            audio_path = os.path.join(audio_path_prefix, file_name+".mp3")

            out_file_wav_fp.write("%s %s\n" % (file_name, audio_path))
            out_file_text_fp.write("%s %s\n" % (file_name, text))
            json_data = {
                        "key": file_name,
                        "wav": audio_path,
                        "txt": text,
                        }
            str_data = json.dumps(json_data, ensure_ascii=False)
            out_file_json_fp.write("%s\n" % (str_data))
        except Exception as e:
            print(e)

        # break
