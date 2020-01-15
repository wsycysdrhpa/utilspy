#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: "2018/8/18"
# @description:


class Num2Words(object):
    def __init__(self):
        self.NUMBER = []
        self.join_str = u""

    # 转成数值型数字
    def to_numerical_value(self, num):
        pass

    # 转成数字串
    def to_numerical_string(self, num):
        output = []
        for n in num:
            if n.isdigit():
                output.append(self.NUMBER[int(n)])
            else:
                output.append(n)
        return self.join_str.join(output)
