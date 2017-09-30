# -*- coding:utf-8 -*-


# @version: 1.0
# @author:
# @date: '14-4-10'


import re


class HtmlCoder():
    def __init__(self):
        pass

    @staticmethod
    def html_to_unicode(html, charset="utf-8"):
        """将html转化成unicode
        :param html: 输入的网页HTML
        :param charset:网页的编码，默认会自动检测
        :rtype : 转化为unicode后的HTML
        """
        #match = re.compile(r'''<meta\s+http-equiv=["']Content-Type["']\s+content=["'][^"']*?charset=([a-zA-z\d\-]+)["']''', re.IGNORECASE).search(html)
        match = re.compile(r'''<meta[^><]+charset=\"?(?P<encoding>[a-zA-Z0-9-]+)[^><]+/?>''', re.IGNORECASE).search(html)
        if match:
            charset = match.group("encoding").strip().lower()
        return HtmlCoder.to_unicode(html, charset)

    @staticmethod
    def to_unicode(input, encoding="utf-8"):
        """将一个字符串转成Unicode编码格式
        :rtype : 转为Unicode格式的字符串
        """

        if isinstance(input, basestring):
            if not isinstance(input, unicode):
                input = input.decode(encoding, 'ignore')
        return input