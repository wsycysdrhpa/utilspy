#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/2/24'
# @description:


import re


class EnPreprocessor(object):
    """
    英文预处理，只针对大小写英文和数字
    已考虑到的特殊情况举例： l've, 1st, 20th, 30's, doctor's, doctors'
    """
    def __init__(self, lower=True):
        self.lower = lower
        self.re_useless = re.compile(u'[^0-9a-zA-Z\'\.]')
        self.re_muti_space = re.compile(u'\s+')
        # 处理 doctors' 这种情况，以下情况基本不会出现，可忽略，说话内容用单引号，结尾是名词复数的所有格
        # 忽略情形如: 'Yes, it is doctors''
        self.noun_plural_possessive = re.compile(u'^[a-zA-Z]+s\'$')

    def seg_sent(self, row_sent):
        """
        处理英文字符串，用空格替换非英文
        :param row_sent: 英文字符串，unicode编码
        :return: unicode字符串
        """
        if self.lower:
            row_sent = row_sent.lower()
        sent = row_sent.strip()
        sent = self.repl_useless_character(sent, u' ')
        words = sent.split(u' ')
        for i in range(len(words)):
            if self.noun_plural_possessive.match(words[i]):
                continue
            words[i] = words[i].strip(u'\'')
        sent = u' '.join(words)
        # 去除多余空格
        sent = self.re_muti_space.sub(u' ', sent).strip()
        return sent

    def repl_useless_character(self, uni_sent, repl=u' '):
        """
        替换unicode字符串中的无效字符
        :param uni_sent: 输入unicode字符串
        :param repl: 被替换的字符串，unicode，默认是u' '
        :return: unicode字符串
        """
        sent = self.re_useless.sub(repl, uni_sent)
        # 去除多余空格
        sent = self.re_muti_space.sub(u' ', sent).strip()
        return sent


if __name__ == "__main__":
    pass
    en_preprocessor = EnPreprocessor(lower=True)
    # test_cent = u"##$Q!hello! man ,$!@you are!! 30 a baby's haha!~!!#my son's,moment's, Don't 5th 2st haha! "
    test_cent = u"I've got it. 'Yes, ma'am.' the-waiter said.'好Yes, 3.4 is doctors'.' 'Yes, it is doctors'' he said."
    # test_cent = u"haha, \"www.qq@123.google.com\" tt2th 3st !"

    print test_cent
    print en_preprocessor.seg_sent(test_cent)
