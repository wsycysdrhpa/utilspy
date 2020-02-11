#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: "2018/8/13"
# @description:
#  1.匹配美元符号（eg: $ one hundred -> one hundred dollars）
#  2.匹配序数词并转换
#  3.TODO 匹配日期并转换
#  4.匹配单位
#    - 单位的位置需要变化的（eg:$ 123 ->  dollar）
#    - 不需要变化的（eg:23% -> 23 percent）
#    - TODO 判断哪些英文单位需要判断单复数，是否加s
#  5.特别长，或者零开头的数字转成数字串
#  6.其余数字转成数值型的

import re
from utilspy.regularization.normalization.base import Transform
from utilspy.regularization.normalization.num2words.lang_en import Num2Words_EN


class TransformEN(Transform):

    def __init__(self, unit_file, unit_need_change_file, num_words_file):
        super(TransformEN, self).__init__(unit_file, unit_need_change_file, num_words_file)

        # 长度大于MAX_LEN的数字转成数字串，an2en最长支持18位数字，超过自动转成数字串
        self.MAX_LEN = 18

        self.tool = Num2Words_EN()

        # join 单位和数字
        self.join_str = u" "

        self.num_dict = ["point", "and", "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                         "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million", "billion"]

        # 匹配美元符号（eg: $ one hundred）
        re_dollar_str = u"\$ [" + "|".join(self.num_dict) + u"|\s]+"
        self.re_dollar = re.compile(re_dollar_str)

        # 匹配零点几
        self.re_zero_point = re.compile(u"zero point ")

        # 匹配序数词
        self.re_ordinal = re.compile(u"(\s+\d{0,}(1st|2nd|3rd|[4567890]th|11th|12th|13th))")
        self.ordinal_dict = {u"one": u"first",
                             u"two": u"second",
                             u"three": u"third",
                             u"five": u"fifth",
                             u"eight": u"eighth",
                             u"nine": u"ninth",
                             u"twelve": u"twelfth"}

    def transform(self, line):
        if not Transform.re_pure_num.search(line):
            return line
        line = self.trans_dollar(line)
        line = self.trans_ordinal(line)
        line = self.trans_units(line)
        line = self.trans_number(line)
        return line

    # 处理美元符号（eg: $ one hundred -> one hundred dollars）
    def trans_dollar(self, line):
        re_dollar_search = self.re_dollar.search(line)
        if re_dollar_search:
            raw_line = re_dollar_search.group(0)
        else:
            return line
        words = raw_line.split()
        new_line = ""
        for i in range(len(words)):
            if words[i] not in self.num_dict and i != 0:
                break
            if i == 0:
                continue
            new_line += words[i] + " "
        new_line = new_line[:-4] if new_line.endswith("and ") and not new_line.endswith("thousand ") else new_line
        if new_line == "one " or self.re_zero_point.search(new_line):
            new_line += "dollar"
            return line.replace("$ " + new_line[:-7], new_line)
        else:
            new_line += "dollars"
            return line.replace("$ " + new_line[:-8], new_line)

    # 序数词转换
    def trans_ordinal(self, line):
        return self.re_ordinal.sub(self._trans_ordinal_number, line)

    def _trans_ordinal_number(self, matched):
        matched_str = matched.group().strip()
        pure_number_list = self.tool.to_numerical_value(matched_str[:-2]).split()
        last_word = pure_number_list[-1]
        if last_word in self.ordinal_dict.keys():
            last_word = self.ordinal_dict[last_word]
        else:
            if last_word[-1] == u"y":
                last_word = last_word[:-1] + u"ie"
            last_word += u"th"
        pure_number_list[-1] = last_word
        return u" " + u" ".join(pure_number_list)


if __name__ == "__main__":
    pass
    run = TransformEN(r"rules/en/en_units", r"rules/en/en_units_need_change", r"rules/en/en_num_words_dict")
    s = u"3d $ twenty thousand 3-d and 1 three 34-39287-98-0987 Today is 32℃, 80% of the 45th students have toys. This computer sales $999 3d"
    print(s)
    print(run.transform(s))
