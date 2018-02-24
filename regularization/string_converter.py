# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '2015/12/31'


class StringConverter(object):
    def __init__(self):
        pass

    full_half_dict = {
        u"”": u'"',
        u"“": u'"',
        u"‘": u"'",
        u"’": u"'",
        u"！": u"!",
        u"。": u".",
        u"【": u"[",
        u"】": u"]",
        u"：": u":",
        u"℃": u"°C",
        u"・": u"·",
        u"（": u"(",
        u"）": u")",
        u"；": u";",
        u"，": u","
    }

    @staticmethod
    def full_to_half(string):
        """全角转半角"""
        rstring = ""
        for uchar in string:
            inside_code=ord(uchar)
            if inside_code == 12288:
                # 全角空格直接转换
                char = unichr(32)
            elif 65281 <= inside_code <= 65374:
                # 全角字符（除空格）根据关系转化
                char = unichr(inside_code-65248)
            elif StringConverter.full_half_dict.get(uchar):
                char = StringConverter.full_half_dict.get(uchar)
            else:
                char = uchar

            rstring += char
        return rstring

    @staticmethod
    def half_to_full(string):
        """半角转全角"""
        rstring = ""
        for uchar in string:
            inside_code=ord(uchar)
            if inside_code == 32:
                # 半角空格直接转化
                inside_code = 12288
            elif 32 <= inside_code <= 126:
                # 半角字符（除空格）根据关系转化
                inside_code += 65248

            rstring += unichr(inside_code)
        return rstring


if __name__ == "__main__":
    pass
    a = u"你好！今天气温36℃。他说：“Hello!”"
    print a
    print StringConverter.full_to_half(a)
    print StringConverter.half_to_full(a)
