#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/1/30'
# @description:


import codecs
import re


class TextFilter(object):
    def __init__(self):
        self.re_zh = re.compile(u'[\u4e00-\u9fa5]')
        self.re_en = re.compile(u'[a-zA-Z]')
        self.re_num = re.compile(u'[0-9]')

    def run(self, src_file, dst_file):
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(dst_file, 'wb') as dst_fp:
            for line in src_fp:
                line = line.strip()
                # line = self.filt_line_en(line)
                # line = self.filt_line_num(line)
                line = self.keep_line_ce(line)
                if line:
                    dst_fp.write(line + u'\n')

    # 滤除包含中文的句子
    def filt_line_none_cn(self, line):
        if self.re_zh.search(line):
            return u''
        else:
            return line

    # 滤除包含英文的句子
    def filt_line_en(self, line):
        if self.re_en.search(line):
            return u''
        else:
            return line

    # 滤除包含数字的句子
    def filt_line_num(self, line):
        if self.re_num.search(line):
            return u''
        else:
            return line

    # 保留包含中文和英文的句子
    def keep_line_ce(self, line):
        if self.re_zh.search(line) and self.re_en.search(line):
            return line
        else:
            return u''


if __name__ == "__main__":
    pass
    text_filter = TextFilter()
    src = r'../test/levoice.txt'
    # dst = r'../test/levoice_pure_cn.txt'
    dst = r'../test/levoice_mix_ce.txt'
    text_filter.run(src, dst)
