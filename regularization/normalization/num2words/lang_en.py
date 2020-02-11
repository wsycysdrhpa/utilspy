#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: "2018/8/18"
# @description:


import re
from utilspy.regularization.normalization.num2words.tools.an2en import Number
from utilspy.regularization.normalization.num2words.base import Num2Words


class Num2Words_EN(Num2Words):

    def __init__(self):
        self.NUMBER = [u"zero", u"one", u"two", u"three", u"four", u"five", u"six", u"seven", u"eight", u"nine"]
        self.join_str = u" "
        # 判断是否有小数点
        self.re_point = re.compile(u"\.")

    def to_numerical_value(self, num):
        if self.re_point.search(num):
            num = float(num)
        else:
            # num = long(num)
            pass
        return Number(num).convert_to_words()
