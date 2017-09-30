#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: Aruan
# @email: ruanhp1@lenovo.com
# @update: '2017/8/17'
# @description: 


import re
import codecs


class DictProcessor(object):
    def __init__(self):
        # For check pure english
        self.re_pure_english = re.compile(u'^[a-zA-Z]+$')

    def generate_dict_for_lm(self, src_file, dst_file):
        with codecs.open(src_file, 'rb', 'utf-8') as src_fp:
            words = set([])
            for line in src_fp:
                word = line.split(' ')[0].strip()
                words.add(word)
            sorted_words = sorted(words)
        with codecs.open(dst_file, 'wb') as dst_fp:
            for sorted_word in sorted_words:
                dst_fp.write(sorted_word + '\n')

    def genenrate_dict_for_seg(self, src_file, dst_file):
        with codecs.open(src_file, 'rb', 'utf-8') as src_fp, \
                codecs.open(dst_file, 'wb') as dst_fp:
            for word in src_fp:
                word = word.strip()
                if self.re_pure_english.search(word):
                    continue
                else:
                    dst_fp.write(word + ' 1' + '\n')


if __name__ == "__main__":
    dict_processor = DictProcessor()
    # dict_processor.generate_dict_for_lm('../test/test_data/dict_processor/CEDICT_CMU_utf-8.txt', 'words_for_lm.txt')
    # dict_processor.genenrate_dict_for_seg('words_for_lm.txt', 'words_for_seg.txt')
