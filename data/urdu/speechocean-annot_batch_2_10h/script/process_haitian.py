import os
import codecs
from glob import glob
from os.path import join
import re
import json
from typing import FrozenSet

from urduhack.urdu_characters import URDU_ALPHABETS, URDU_DIGITS


URDU_ALL_CHARACTERS: FrozenSet[str] = frozenset().union(URDU_ALPHABETS, URDU_DIGITS)
URDU_ALL_CHARACTERS_STR = "".join(URDU_ALL_CHARACTERS)
re_useless_char_pattern = f'[^{URDU_ALL_CHARACTERS_STR}0-9\s]+'

re_useless_char = re.compile(re_useless_char_pattern, flags=re.U)
re_muti_space = re.compile("\s+", flags=re.U)


src_dir = "/home/haipeng/work/data/urdu/asr/speechocean/speechocean-annot/batch_2_10h/opay_urdu_20230515_2.06h/valid"
audio_path_prefix = "/home/haipeng/work/data/urdu/asr/unlabeled/barwaqt/voip/wiz/20230410/audio_left_ge30_le200_left_seg_ge2_le20"

out_file_prefix = "/home/haipeng/work/data/urdu/asr/speechocean/speechocean-annot/batch_2_10h/opay_urdu_20230515_2.06h"
out_file_wav = os.path.join(out_file_prefix, "wav.scp")
out_file_text = os.path.join(out_file_prefix, "text")
out_file_json = os.path.join(out_file_prefix, "data.list")


with codecs.open(out_file_wav, 'w') as out_file_wav_fp, \
    codecs.open(out_file_text, 'w') as out_file_text_fp, \
    codecs.open(out_file_json, 'w') as out_file_json_fp:
    for src_file in sorted(glob(join(src_dir, '*.txt'))):
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
                    # all is customer audio
                    # role = "Customer1"

                    text = re_useless_char.sub(" ", text)
                    text = re_muti_space.sub(" ", text)
                    text = text.strip()

                    key_seg = '%s_%s_%s' % (file_name, start, end)
                    audio_path = os.path.join(audio_path_prefix, file_name+".wav")

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
