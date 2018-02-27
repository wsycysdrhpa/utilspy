#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/2/26'
# @description: 


import re
import logging

import jieba

from utilspy.text.en_preprocessor import EnPreprocessor


LOGGER = logging.getLogger('consoleOnly')


class CnEnPreprocessor(object):
    def __init__(self, seg_dict='', flag='load', lower=True, HMM=False):
        self.lower = lower
        # jieba.cut方法是否开启HMM，Ture or False，默认不开启
        self.HMM = HMM
        self.re_useless = re.compile(u'[^0-9a-zA-Z\'\u4e00-\u9fa5]')
        self.re_muti_space = re.compile(u'\s+')
        self.re_cn_phrase = re.compile(u'[\u4e00-\u9fa5]+')
        self.en_preprocessor = EnPreprocessor()
        if seg_dict:
            if flag == 'load':
                # load user dict and use jieba dict
                jieba.load_userdict(seg_dict)
                LOGGER.info(u"Load user dict and use jieba default dict, successfully set")
            elif flag == 'set':
                # Set user dict and do not use jieba dict
                jieba.set_dictionary(seg_dict)
                LOGGER.info(u"Set user dict and do not use jieba default dict, successfully set")
            else:
                pass

    def seg_sent(self, row_sent):
        if self.lower:
            row_sent = row_sent.lower()
        sent = row_sent.strip()
        sent = self.repl_useless_character(sent, u' ')
        # 处理中文，将匹配到的中文短语进行分词，为了和其他字符分割，前后添加空格
        sent = self.re_cn_phrase.sub(self._add_blank, sent)
        # 处理英文
        words = sent.split(u' ')
        for i in range(len(words)):
            if self.en_preprocessor.noun_plural_possessive.match(words[i]):
                continue
            words[i] = words[i].strip(u'\'')
        sent = u' '.join(words)
        # 去除多余空格
        sent = self.re_muti_space.sub(u' ', sent).strip()
        return sent

    def _add_blank(self, matched):
        src_uni = matched.group()
        dst_uni = u' '.join(jieba.cut(src_uni, HMM=self.HMM))
        dst_uni = u' ' + dst_uni + u' '
        return dst_uni

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
    import os
    from utilspy.log.logger import Logger

    CURRENT_FILE_PATH = os.path.abspath(__file__)
    CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)

    # Dict absoluate path
    seg_dict_file = os.path.join(CURRENT_DIR_PATH, 'data/dict/lenovo/words_for_seg.txt')

    Logger.load_configure(CURRENT_DIR_PATH)

    cn_en_preprocessor = CnEnPreprocessor(seg_dict=seg_dict_file, flag='set', lower=True, HMM=False)

    test_sent = u"I've got it. 这个非常好，!中国科学院自动化研究所。'Yes, ma'am.' the-waiter said.'好Yes, " \
                u"3 is可以'￥21的QUchu'所有的非中文标记！！! doctors'.' 'Yes, it is doctors'' he said."
    print test_sent

    test_sent = cn_en_preprocessor.repl_useless_character(test_sent)
    print test_sent

    test_sent = cn_en_preprocessor.seg_sent(test_sent)
    print test_sent
