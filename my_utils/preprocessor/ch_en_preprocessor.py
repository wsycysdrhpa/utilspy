#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: Aruan
# @email: ruanhp1@lenovo.com
# @update: '2017/9/30'
# @description: 


import os
import re
import codecs

import jieba


current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
parent_dir_path = os.path.dirname(current_dir_path)

# Dict absoluate path
seg_dict_file = os.path.join(parent_dir_path, 'dict/lenovo/lm_dict/words_for_seg.txt')


class ChEnPreprocessor(object):
    def __init__(self):
        self.re_discard_punct = re.compile(u'[^\u4e00-\u9fa5A-Za-z0-9]')
        self.re_muti_blank = re.compile(u'\s+')

    def seg_line(self, line, HMM=False):
        # Set user dict, use jieba dict
        # jieba.load_userdict(seg_dict_file)
        # Set user dict, do not use jieba dict
        # jieba.set_dictionary(seg_dict_file)
        line = line.strip()
        seged_line = u' '.join(jieba.cut(line, HMM=HMM))
        seged_clean_line = self.re_discard_punct.sub(u' ', seged_line)
        seged_clean_line = self.re_muti_blank.sub(u' ', seged_clean_line).strip()
        return seged_clean_line

    def seg_file_line(self, src_file, dst_file, HMM=False):
        with codecs.open(src_file, 'rb', 'utf-8') as fin_fp, \
                codecs.open(dst_file, 'wb') as dst_fp:
            for line in fin_fp:
                seged_clean_line = self.seg_line(line, HMM=HMM)
                dst_fp.write(seged_clean_line + '\n')


if __name__ == "__main__":
    pass
    ch_en_preprocessor = ChEnPreprocessor()

