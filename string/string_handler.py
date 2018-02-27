# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '14-6-17'


class StringHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def none_to_zero(input_string):
        if not input_string:
            return 0
        return int(input_string)

    @staticmethod
    def empty_to_zero(input_string):
        if not input_string:
            return 0
        return int(input_string)

    @staticmethod
    def none_to_empty(input_string):
        if not input_string:
            return ""
        return str(input_string)

    @staticmethod
    def none_to_empty(input_string):
        if input_string:
            return str(input_string)
        else:
            return ""

    @staticmethod
    def string_to_int(input_string, default):
        if not input_string:
            return default
        try:
            return int(input_string)
        except ValueError:
            return default

    @staticmethod
    def string_to_float(input_string, default):
        if not input_string:
            return default
        try:
            return float(input_string)
        except ValueError:
            return default

    @staticmethod
    def none_to_float_zero(input_string):
        if input_string:
            return float(input_string)
        else:
            return 0.0

    @staticmethod
    def to_boolean(input_value):
        if input_value:
            return True
        else:
            return False


if __name__ == "__main__":
    pass
