#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: Aruan
# @date: '2015/11/25'


class Calculate(object):
    def __init__(self):
        pass

    def cal_inverse_number(self, l1):
        cnt = 0
        for current_number in l1:
            for rear_number in l1[l1.index(current_number)+1:]:
                if current_number > rear_number:
                    cnt += 1
        return cnt


if __name__ == "__main__":
    pass
    calculate = Calculate()
    # a =[4,3,2,1]
    # print calculate.cal_inverse_number(a)
