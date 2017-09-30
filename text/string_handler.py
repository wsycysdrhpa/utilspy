# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '14-6-17'


class StringHandler():
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

    @staticmethod
    def chinese2digits(uchars_chinese):
        common_used_numerals = {u'零':0, u'一':1, u'二':2, u'两':2, u'三':3, u'四':4, u'五':5, u'六':6,
                                u'七':7, u'八':8, u'九':9, u'十':10, u'百':100, u'千':1000, u'万':10000, u'亿':100000000}
        total = 0
        unit = 1                           #表示单位：个十百千...
        for i in range(len(uchars_chinese) - 1, -1, -1):
            val = common_used_numerals.get(uchars_chinese[i])
            if val >= 10 and i == 0:    #应对 十三 十四 十*之类
                if val > unit:
                    unit = val
                    total = total +  val
                else:
                    unit = unit * val
                    #total =total +  r * x
            elif val >= 10:
                if val > unit:
                    unit = val
                else:
                    unit = unit * val
            else:
                total = total +  unit * val
        return total


if __name__ == "__main__":
    print StringHandler.chinese2digits(u"两百三十二")
    pass