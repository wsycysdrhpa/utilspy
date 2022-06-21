#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2020/2/12'
# @description:


import re
import codecs


class TextFilter(object):
    def __init__(self):
        self.re_zh = re.compile('[\u4e00-\u9fa5]')
        self.re_en = re.compile('[a-zA-Z]')
        self.re_num = re.compile('[0-9]')

    def run(self, src_file, dst_file):
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(dst_file, 'wb', 'utf-8') as dst_fp:
            for line in src_fp:
                line = line.strip()
                # line = self.filt_line_en(line)
                # line = self.filt_line_num(line)
                line = self.keep_line_ce(line)
                if line:
                    dst_fp.write(line + '\n')

    # 滤除包含中文的句子
    def filt_line_none_cn(self, line):
        if self.re_zh.search(line):
            return ''
        else:
            return line

    # 滤除包含英文的句子
    def filt_line_en(self, line):
        if self.re_en.search(line):
            return ''
        else:
            return line

    # 滤除包含数字的句子
    def filt_line_num(self, line):
        if self.re_num.search(line):
            return ''
        else:
            return line

    # 保留包含中文和英文的句子
    def keep_line_ce(self, line):
        if self.re_zh.search(line) and self.re_en.search(line):
            return line
        else:
            return ''


if __name__ == "__main__":
    pass
    text_filter = TextFilter()
    src = r''
    dst = r''
    text_filter.run(src, dst)
