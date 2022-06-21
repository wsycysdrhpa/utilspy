#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: "2018/8/13"
# @description:
#  通用：
#    - 加载单位词典
#    - 单位转换
#    - 数字转换（数值 & 数字串）

import re
import codecs

from utilspy.regularization.normalization.num2words.lang_cn import Num2Words_CN


class Transform(object):

    # 匹配纯数字，包括正负整数或小数（小数包括.3这种形式）
    re_pure_num_str = u"[-]{0,1}\d{0,}[.]{0,1}\d+"
    re_pure_num = re.compile(re_pure_num_str)

    # 匹配特殊的数字串（eg: 39-02898-0938-38 或多个零开头的数字串）
    re_special_numberical_str = re.compile(u"(\d{1,}\-[0-9\-]+\d{1,})|([-]{0,1}0{2,}\d{0,}[.]{0,1}\d+)")

    def __init__(self, unit_file, unit_need_change_file, num_words_file):

        # 长度大于MAX_LEN的数字转成数字串
        self.MAX_LEN = 18

        self.tool = Num2Words_CN()

        # 单位
        self.units, todo = self.load_units(unit_file)
        self.units_before, self.units_after = self.load_units(unit_need_change_file)

        # 词典中带有数字的词（不需要转换）
        self.num_words_dict = self.load_num_words(num_words_file)
        self.re_num_words = re.compile(u"|".join(self.num_words_dict))

        # join 单位和数字
        self.join_str = u""

    def transform(self, line):
        if not self.re_pure_num.search(line):
            return line
        line = self.trans_units(line)
        line = self.trans_number(line)
        return line

    # 单位转换
    def trans_units(self, line):
        line = self._units_change(self.units_before, line, flag="before_need_change")
        line = self._units_change(self.units_after, line, flag="after_need_change")
        line = self._units_change(self.units, line, flag="after")
        return line

    def _units_change(self, units_dict, line, flag="before_need_change"):
        for key in units_dict.keys():
            if flag == "before_need_change":
                re_ = re.compile(key + u"[\s]{0,}" + Transform.re_pure_num_str)
                for matched_str in re_.findall(line):
                    current_unit = units_dict[key]
                    current_num = matched_str[len(key):]
                    changed_str = current_num + self.join_str + current_unit
                    line = line.replace(matched_str, changed_str)
            elif flag == "after_need_change":
                re_ = re.compile(Transform.re_pure_num_str + u"[\s]{0,}" + key)
                for matched_str in re_.findall(line):
                    current_unit = units_dict[key]
                    current_num = matched_str[:-len(key)]
                    changed_str = current_unit + self.join_str + current_num
                    line = line.replace(matched_str, changed_str)
            elif flag == "after":
                re_ = re.compile(Transform.re_pure_num_str + u"[\s]{0,}" + key)
                for matched_str in re_.findall(line):
                    tail_matched_str_index = line.index(matched_str) + len(matched_str)
                    if tail_matched_str_index < len(line):
                        char_after_key = line[tail_matched_str_index]
                        if char_after_key.encode("utf-8").isalpha():
                            continue
                    current_unit = units_dict[key]
                    current_num = matched_str[:-len(key)]
                    changed_str = current_num + self.join_str + current_unit
                    line = line.replace(matched_str, changed_str)
        return line

    def _replace_units(self, matched):
        return self.join_str + self.units[matched.group()]

    def _replace_units_repeat(self, matched):
        return self.join_str + self.units_repeat[matched.group()]

    # 数字转换，在词典中的词语不转换
    def trans_number(self, line):
        num_words_group = [(m.group(), m.span()) for m in self.re_num_words.finditer(line)]
        if len(num_words_group) == 0:
            return self._trans_number(line)
        else:
            sub_line_list = []
            begin = 0
            for matched_group in num_words_group:
                sub_line_list.append([line[begin: matched_group[1][0]], True])
                sub_line_list.append([matched_group[0], False])
                begin = matched_group[1][1]
            sub_line_list.append([line[begin:], True])
            for sub_line_group in sub_line_list:
                if sub_line_group[1]:
                    sub_line_group[0] = self._trans_number(sub_line_group[0])
            return u"".join([m[0] for m in sub_line_list])

    def _trans_number(self, line):
        if not self.re_pure_num.search(line):
            return line
        try:
            line = Transform.re_special_numberical_str.sub(self._trans_special_numberical_str, line)
        except Exception as e:
            print("Error line: ", line)
            raise e
        line = Transform.re_pure_num.sub(self._trans_numberical_value, line)
        return line

    def _trans_special_numberical_str(self, matched):
        matched_str = matched.group()
        return self.tool.to_numerical_string(matched_str)

    def _trans_numberical_value(self, matched):
        matched_str = matched.group()
        if (matched_str[0] == "0" and len(matched_str) > 1 and matched_str[1] != "." ) or len(matched_str) > self.MAX_LEN:
            return self.tool.to_numerical_string(matched_str)
        else:
            return self.tool.to_numerical_value(matched_str)

    # 加载单位
    def load_units(self, units_file):
        units1, units2, flag = {}, {}, True
        with codecs.open(units_file, "rb", "utf-8") as file:
            for line in file:
                line_array = line.strip().split()
                if line_array[0] == "======":
                    flag = False
                    continue
                if flag:
                    units1[line_array[0]] = line_array[1]
                else:
                    units2[line_array[0]] = line_array[1]
        return units1, units2

    # 加载含有数字的词典
    def load_num_words(self, num_words_file):
        return [word.strip() for word in codecs.open(num_words_file, "rb", "utf-8").readlines()]
