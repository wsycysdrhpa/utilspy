#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/2/24'
# @description:


import re


class EnPreprocessor(object):
    """
    英文预处理
    需要特殊注意 l've, 1st, 20th 等形式
    """
    def __init__(self):
        self.re_non_en = re.compile(u'[^a-zA-Z]')

    def seg_sent(self, row_sent):
        """ 
        处理英文字符串，用空格替换非英文，空格分开，返回处理后的unicode句子字符串
        :param row_sent: 英文字符串，unicode编码
        :return: 分词后的unicode句子字符串
        """
        row_sent = row_sent.lower()
        row_sent = row_sent.strip()
        # 把句子先按照标点符号分割成短句序列
        repled_sent = self.repl_non_letter_characters(row_sent, u' ')
        repled_sent = repled_sent.strip(u' ')
        repled_sent = re.sub(u'[ ]+', u' ', repled_sent)
        return repled_sent

    @staticmethod
    def repl_non_letter_characters(uni_sent, repl=u''):
        """
        替换unicode类型字符串中的非英文字母字符
        :param uni_sent: 输入必须是unicode类型字符串
        :param repl: 被替换的字符串，最好设为unicode类型，默认是u''
        :return: 替换后的unicode字符串
        """
        pattern = re.compile(ur'[^a-z]')
        return pattern.sub(repl, uni_sent)


if __name__ == "__main__":
    pass
    en_preprocessor = EnPreprocessor()
    test_cent = u"##$Q!hello! man ,$!@you are!! a baby's haha!~!!#my son's,moment's, Don't 5th 2st haha! I've got it. 'Yes, ma'am.' the waiter said. "
    # test_cent = english_preprocessor.repl_non_letter_characters(test_cent, repl=u' ')
    # print test_cent
    
    print en_preprocessor.seg_sent(test_cent)
