# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


import re


class RegexHelper(object):
    def __init__(self):
        # chinese character
        self.re_cn = re.compile(u'[\u4e00-\u9fa5]')
        # english character
        self.re_en = re.compile(u'[a-zA-Z]')
        # digit character
        self.re_digit = re.compile(u'[0-9]')
        # chinese, english, digit character
        self.re_cn_en_digit = re.compile(u'[0-9a-zA-Z\u4e00-\u9fa5]')
        # 多个空格
        self.re_muti_space = re.compile(u'\s+')
        # punctuation
        self.re_punct = re.compile(u'[,.;\'"!，。；：？！‘’“”]')

    # finditer方法会搜索string, 返回一个顺序访问每一个匹配结果（Match对象）的迭代器;
    # 类似的，findall方法会搜索string, 以列表形式返回全部能匹配的子串;
    # 返回全部能匹配的子串列表
    @staticmethod
    def find_all(regex, source):
        result = []
        for matchResult in regex.finditer(source):
            result.append(matchResult.group())
        return result

    # 这个方法将从string的pos下标处起尝试匹配pattern;
    # 如果pattern结束时仍可匹配, 则返回一个Match对象;
    # 如果匹配过程中pattern无法匹配, 或者匹配未结束就已到达endpos, 则返回None;
    # 这个方法并不是完全匹配, 当pattern结束时若string还有剩余字符, 仍然视为成功;
    @staticmethod
    def match_content(regex, source):
        match = regex.match(source)
        if match:
            return match.group()
        return u""

    # 从string的pos下标处起尝试匹配pattern, 如果pattern结束时仍可匹配, 则返回一个Match对象;
    # 若无法匹配, 则将pos加1后重新尝试匹配, 直到pos=endpos时仍无法匹配则返回None;
    @staticmethod
    def search_single(regex, source):
        match = regex.search(source)
        if match:
            return match.group()
        return u""


if __name__ == "__main__":
    pass
    pat = re.compile(r'\d+')
    text = u'one1two2three3four4'
    print(RegexHelper.search_single(pat, text))

    text = u'123abc'
    print(RegexHelper.match_content(pat, text))

    text = u'one1two2three3four4'
    print(RegexHelper.find_all(pat, text))

    text = u'one1two2three3four4'
    re_digit = re.compile(u'[0-9]')
