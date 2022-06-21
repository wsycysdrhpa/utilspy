#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: luojie
# @date: '14-4-11'


import ahocorasick

from utilspy.string_lib.string_handler import StringHandler


class StringHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def is_empty(string):
        # or 遇真则真, and 遇假则假
        return string == "" or string == " " or string is None

    @staticmethod
    def slice(string, rule):
        # 截取规则rule: start_index:end_index,
        # start_index缺省则从0开始，end_index缺省则默认到结尾
        parts = rule.split(":")
        start_index = StringHandler.none_to_zero(parts[0])
        if not parts[-1]:
            end_index = None
        else:
            end_index = int(parts[1])
        return string[start_index:end_index]

    @staticmethod
    def to_class_name(string):
        # part_part..._part -> PartPart...Part
        class_name = ""
        parts = string.split("_")
        for part in parts:
            class_name += (part[0].upper()+part[1:])
        return class_name

    @staticmethod
    def build_actree(word_list):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(word_list):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree


if __name__ == "__main__":
    pass
    s = ''
    print(StringHelper.is_empty(s))
    print()

    s = 'hello!'
    print(StringHelper.slice(s, '1:5'))
    print(s[1:5])
    print()

    print(StringHelper.to_class_name("redis_file_saver"))
    print()

    # AC test
    word_list = 'he her hers she'.split()
    actree = StringHelper.build_actree(word_list)
    haystack = "she is a hestudent"
    for end_index, (insert_order, original_value) in actree.iter(haystack):
        start_index = end_index - len(original_value) + 1
        print((start_index, end_index, (insert_order, original_value)))
