#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: Aruan
# @date: '2015/11/21'


import re


class EnglishPreprocessor(object):
    """
    文字预处理
    """
    def __init__(self):
        pass

    def seg_sent(self, row_sent):
        """ 
        将输入的英文句子进行分词，空格分开，返回分词后的unicode句子字符串
        :param row_sent: 输入句子字符串，可为str或unicode编码
        :return: 返回分词后的unicode句子字符串
        """
        # 必须要将str类型解码为unicode类型
        if isinstance(row_sent, str):
            row_sent = row_sent.decode()
        row_sent = row_sent.strip('\n')
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
    english_preprocessor = EnglishPreprocessor()
    test_cent = u"##$Q!hello! man ,$!@you are!! a baby's haha!~!!"
    # test_cent = english_preprocessor.repl_non_letter_characters(test_cent, repl=u' ')
    # print test_cent
    
    print english_preprocessor.seg_sent(test_cent)