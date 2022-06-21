#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: "2018/8/18"
# @description:


from utilspy.regularization.normalization.num2words.tools.an2cn import an2cn
from utilspy.regularization.normalization.num2words.base import Num2Words


class Num2Words_CN(Num2Words):

    def __init__(self):
        self.NUMBER = [u"零", u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"]
        self.join_str = u""

    # 转成数值型数字
    def to_numerical_value(self, num):
        if num.startswith("-"):
            return u"负" + an2cn(num[1:])
        else:
            return an2cn(num)
