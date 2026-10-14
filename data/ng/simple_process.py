import os
import codecs
import re
import sys


re_useless_char_pattern = f'[^a-zA-Z0-9\s\-\']+'

re_useless_char = re.compile(re_useless_char_pattern, flags=re.U)
re_muti_space = re.compile("\s+", flags=re.U)


src_file = sys.argv[1]
dst_file = sys.argv[2]


with codecs.open(src_file, 'r') as src_fp, \
    codecs.open(dst_file, 'w') as dst_fp:
    for line in src_fp:
        text = line.strip()

        text = text.upper()
        text = re_useless_char.sub(" ", text)
        text = re_muti_space.sub(" ", text)
        text = text.strip()

        if text:
            dst_fp.write(text + '\n')
