#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: "2018/8/13"
# @description:
#  1.匹配日期并转换
#  2.匹配单位
#    - 单位的位置需要变化的（eg:￥123 -> 123元）
#    - 不需要变化的（eg:23km -> 23公里）
#  3.特别长，或者零开头的数字转成数字串
#  4.其余数字转成数值型的

import re
import sys

from utilspy.regularization.normalization.base import Transform
from utilspy.regularization.normalization.num2words.lang_cn import Num2Words_CN


# Set python default encode
# reload(sys)
# sys.setdefaultencoding("utf-8")


class TransformCN(Transform):

    def __init__(self, unit_file, unit_need_change_file, num_words_file):
        super(TransformCN, self).__init__(unit_file, unit_need_change_file, num_words_file)

        # 长度大于MAX_LEN的数字转成数字串，an2cn最长支持16位数字
        self.MAX_LEN = 16

        self.tool = Num2Words_CN()

        # join 单位和数字
        self.join_str = u""

        # 匹配年份（eg: 2012年）
        self.re_year = re.compile(u"\d{2,4}年")
        # 匹配日期（eg: 2012-12-12）
        self.re_date = re.compile(u"\d{4}\-\d{1,2}\-\d{1,2}")

    def transform(self, line):
        if not self.re_pure_num.search(line):
            return line
        try:
            line = self.trans_date(line)
            line = self.trans_units(line)
            line = self.trans_number(line)
        except ValueError as e:
            print(ValueError, e, line)
        return line

    # 日期转换
    def trans_date(self, line):
        line = self.re_year.sub(self._to_year, line)
        line = self.re_date.sub(self._to_date, line)
        return line

    def _to_year(self, matched):
        matched_str = matched.group()
        return self.tool.to_numerical_string(matched_str[:-1]) + matched_str[-1]

    def _to_date(self, matched):
        matched_str_array = matched.group().split("-")
        year = self.tool.to_numerical_string(matched_str_array[0])
        month = self.tool.to_numerical_value(matched_str_array[1])
        day = self.tool.to_numerical_value(matched_str_array[2])
        return year + u"年" + month + u"月" + day + u"日"


if __name__ == "__main__":
    pass
    run = TransformCN(r"rules/cn/cn_units", r"rules/cn/cn_units_need_change", r"rules/cn/cn_num_words_dict")
    s = u"2018-12-32 1234年美国51区456.1234北京-001理工大学是1座好城市3d哈 98-0987这台电脑卖￥-4329.5，100% 32℃，有14km，500m, 09282625"
    # BUG 后面包含前面部分如：500m 1500m
    # s = u"2018-12-32 1234年美国51区456.1234北京-001理工大学是1座好城市3d哈 98-0987这台电脑卖￥-4329.5，100% 32℃，有14km，500m, 09282625 1500m"
    print(s)
    print(run.transform(s))
