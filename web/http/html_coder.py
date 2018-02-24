#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/2/14'
# @description:


import re


class HtmlCoder(object):
    def __init__(self):
        pass

    @staticmethod
    def html_to_unicode(html, charset="utf-8"):
        """将html转化成unicode
        :param html: 输入的网页HTML
        :param charset:网页的编码，默认会自动检测
        :rtype : 转化为unicode后的HTML
        """
        # match = re.compile(r'''<meta\s+http-equiv=["']Content-Type["']\s+content=["'][^"']*?charset=([a-zA-z\d\-]+)["']''', re.IGNORECASE).search(html)
        match = re.compile(r'''<meta[^><]+charset=\"?(?P<encoding>[a-zA-Z0-9-]+)[^><]+/?>''', re.IGNORECASE).search(html)
        if match:
            charset = match.groups()[0].strip().lower()
        return HtmlCoder.to_inicode(html, charset)

    @staticmethod
    def to_inicode(src_str, encoding="utf-8"):
        """将一个字符串转成Unicode编码格式
        :rtype : 转为Unicode格式的字符串
        """
        if isinstance(src_str, basestring):
            if not isinstance(src_str, unicode):
                src_str = src_str.decode(encoding, 'ignore')
        return src_str


if __name__ == "__main__":
    pass
    import urllib
    url = 'https://www.baidu.com/'
    html = urllib.urlopen(url).read()

    html_coder = HtmlCoder()
    u_html = html_coder.html_to_unicode(html)
    print u_html
    print type(html)
    print type(u_html)
