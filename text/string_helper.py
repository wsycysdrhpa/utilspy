#!/usr/bin/python
#-*- coding: utf8 -*-


# @version: 1.0
# @author: luojie
# @date: '14-4-11'


from yzs_utils.text.string_handler import StringHandler


class StringHelper:
    def __init__(self):
        pass

    def is_empty(self, string):
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


if __name__ == "__main__":
    print StringHelper.to_class_name("redis_file_saver")
    pass