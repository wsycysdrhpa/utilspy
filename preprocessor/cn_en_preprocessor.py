#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/2/24'
# @description: 


import os
import re
import codecs

import jieba


CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)

# Dict absoluate path
SEG_DICT_FILE = os.path.join(CURRENT_DIR_PATH, 'data/dict/lenovo/lm_dict/words_for_seg.txt')


class CnEnPreprocessor(object):
    def __init__(self, seg_dict=SEG_DICT_FILE):
        # Set user dict, use jieba dict
        # jieba.load_userdict(seg_dict)
        # Set user dict, do not use jieba dict
        # jieba.set_dictionary(seg_dict)
        self.re_discard_punct = re.compile(u'[^\u4e00-\u9fa5A-Za-z0-9]')
        self.re_muti_blank = re.compile(u'\s+')

    def seg_line(self, line, HMM=False):
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

    def seg_file_pick_line(self, src_file, column, dst_file, HMM=False):
        """
        # 列之间以tab分割
        :param src_file: 
        :param column: 
        :param dst_file: 
        :param HMM: 
        :return: 
        """
        with codecs.open(src_file, 'rb', 'utf-8') as fin_fp, \
                codecs.open(dst_file, 'wb') as dst_fp:
            for line in fin_fp:
                elements = line.split('\t')
                elements[column] = self.seg_line(elements[column].strip(), HMM=HMM)
                seged_clean_line = '\t'.join(elements).strip()
                dst_fp.write(seged_clean_line + '\n')


if __name__ == "__main__":
    pass
    cn_en_preprocessor = CnEnPreprocessor()
