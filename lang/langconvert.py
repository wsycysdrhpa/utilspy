# -*- coding:utf-8 -*-


from langconv import *


class LangConverter():
    def __init__(self):
        pass

    hans_converter = Converter("zh-hans")
    hant_converter = Converter("zh-hant")

    @staticmethod
    def to_hans(hant_line):
        """
        convert zh-hant to zh-hans
        将繁体中文转换为简体中文
        :param hant_line:繁体字符串(unicode编码)
        """
        hansLine = LangConverter.hans_converter.convert(hant_line)
        return hansLine

    @staticmethod
    def to_hant(hans_line):
        """
        convert zh-hans to zh-hant
        将简体中文转换为繁体中文
        :param hans_line:简体字符串(unicode编码)
        """
        hantLine = LangConverter.hant_converter.convert(hans_line)
        return hantLine


if __name__ == "__main__":
    pass