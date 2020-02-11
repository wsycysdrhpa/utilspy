# -*- coding:utf-8 -*-

# @version: 1.0
# @author: luojie
# @date: '2020/02/10'


class StringConverter(object):
    def __init__(self):
        pass

    full_half_dict = {
        u"”": u'"',
        u"“": u'"',
        u"‘": u"'",
        u"’": u"'",
        u"【": u"[",
        u"】": u"]",
        u"：": u":",
        u"℃": u"°C",
        u"・": u"·",
        u"（": u"(",
        u"）": u")",
        u"；": u";",
        # u"。": u".",

        # negligible
        # u"，": u","
        # u"！": u"!",
        # u"？": u"?",
    }

    @staticmethod
    def full_to_half(string):
        """全角转半角"""
        rstring = u""
        for uchar in string:
            inside_code = ord(uchar)
            if inside_code == 12288:
                # 全角空格直接转换
                char = chr(32)
            elif StringConverter.full_half_dict.get(uchar):
                char = StringConverter.full_half_dict.get(uchar)
            elif 65281 <= inside_code <= 65374:
                # 全角字符（除空格）根据关系转化
                char = chr(inside_code-65248)
            else:
                char = uchar

            rstring += char
        return rstring

    @staticmethod
    def half_to_full(string):
        """半角转全角"""
        rstring = ""
        for uchar in string:
            inside_code = ord(uchar)
            if inside_code == 32:
                # 半角空格直接转化
                inside_code = 12288
            elif 32 <= inside_code <= 126:
                # 半角字符（除空格）根据关系转化
                inside_code += 65248

            rstring += chr(inside_code)
        return rstring


if __name__ == "__main__":
    pass
    text = u"你好！今天气温36℃。他说：“Hello!”２００１年在很多玩家的心中都留下了纯朴９：００－１８：００；" \
        u"电话处理时间是７×２４当您可爱，哈哈！好吗？作为中国游戏市场上第一款３Ｄ网游qq产品。ＱＱ的,Ｍｏｒｅ！？。网游作品."
    print(text)
    print(StringConverter.full_to_half(text))
    # print StringConverter.half_to_full(text)
