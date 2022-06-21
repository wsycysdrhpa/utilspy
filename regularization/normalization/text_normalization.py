#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname
from os.path import join

from utilspy.regularization.normalization.trans_cn import TransformCN
from utilspy.regularization.normalization.trans_en import TransformEN


class TextNormalization(object):

    def __init__(self, lang='cn'):
        module_path = dirname(__file__)

        if lang == 'cn':
            unit_file = join(module_path, r'rules/cn/cn_units')
            unit_need_change_file = join(module_path, r'rules/cn/cn_units_need_change')
            num_words_file = join(module_path, r'rules/cn/cn_num_words_dict')
            self.tool = TransformCN(unit_file, unit_need_change_file, num_words_file)
        elif lang == 'en':
            unit_file = join(module_path, r'rules/en/en_units')
            unit_need_change_file = join(module_path, r'rules/en/en_units_need_change')
            num_words_file = join(module_path, r'rules/en/en_num_words_dict')
            self.tool = TransformEN(unit_file, unit_need_change_file, num_words_file)
        else:
            self.tool = None

    def transform(self, line):
        if self.tool:
            return self.tool.transform(line)
        else:
            return None
