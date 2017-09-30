#!/usr/bin/python
# -*- coding:utf-8 -*-


# @version: 1.0
# @author:
# @date: '14-4-10'


import re


class NumParser():
    def __init__(self):
        self._number_pattern = re.compile(r"[0-9]+")

    def extract_number(self, input_string):
        if type(input_string) is int:
            input_string = str(input_string)
        match = self._number_pattern.search(input_string)
        if match:
            return int(match.group())

if __name__ == "__main__":
    num_parser = NumParser()
    test_string = "第45集"
    print "math is " + str(num_parser.extract_number(test_string))
