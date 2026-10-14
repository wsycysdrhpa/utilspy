import os
import codecs
from glob import glob
from os.path import join
import re
import json
from typing import FrozenSet
import sys

from urduhack.urdu_characters import URDU_ALPHABETS, URDU_DIGITS


URDU_ALL_CHARACTERS: FrozenSet[str] = frozenset().union(URDU_ALPHABETS, URDU_DIGITS)
URDU_ALL_CHARACTERS_STR = "".join(URDU_ALL_CHARACTERS)
re_useless_char_pattern = f'[^{URDU_ALL_CHARACTERS_STR}0-9\s]+'

re_useless_char = re.compile(re_useless_char_pattern, flags=re.U)
re_muti_space = re.compile("\s+", flags=re.U)


src_file = sys.argv[1]
dst_file = sys.argv[2]


with codecs.open(src_file, 'r') as src_fp, \
    codecs.open(dst_file, 'w') as dst_fp:
    for line in src_fp:
        text = line.strip()

        text = re_useless_char.sub(" ", text)
        text = re_muti_space.sub(" ", text)
        text = text.strip()

        if text:
            dst_fp.write(text + '\n')
