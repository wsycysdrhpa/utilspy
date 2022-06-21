#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2020/02/12'
# @description:


import re
import logging

import jieba


LOGGER = logging.getLogger('consoleOnly')


class CnPreprocessor(object):
    """
    中文预处理，只针对纯中文, 阿拉伯数字也不包括
    """
    def __init__(self, seg_dict='', flag='load', HMM=False):
        # jieba.cut方法是否开启HMM，Ture or False，默认不开启
        self.HMM = HMM
        self.re_non_cn = re.compile('[^\u4e00-\u9fa5]')
        self.re_muti_space = re.compile('\s+')
        if seg_dict:
            if flag == 'load':
                # load user dict and use jieba dict
                jieba.load_userdict(seg_dict)
                LOGGER.info("Load user dict and use jieba default dict, successfully set")
            elif flag == 'set':
                # Set user dict and do not use jieba dict
                jieba.set_dictionary(seg_dict)
                LOGGER.info("Set user dict and do not use jieba default dict, successfully set")
            else:
                pass

    def seg_sent_to_single(self, row_sent):
        sent = row_sent.strip()
        # 先把句子按照非中文符号拆分成短句序列
        repled_sent = self.repl_non_chinese_character(sent)
        w_list = list(repled_sent)
        return self.re_muti_space.sub(' ', ' '.join(w_list)).strip()

    def seg_sent(self, row_sent):
        """
        将输入的句子分成短句，再进行分词，返回分词后unicode字符串
        :param row_sent: 输入unicode字符串
        :return: 分词后的unicode字符串
        """
        sent = row_sent.strip()
        # 先把句子按照非中文符号拆分成短句序列
        repled_sent = self.repl_non_chinese_character(sent)
        short_sents = repled_sent.split(' ')
        # 对所有短句序列进行分词，然后拼接成一个unicode字符串
        storer = []
        for short_sent in short_sents:
            seged_short_sent = ' '.join(jieba.cut(short_sent, HMM=self.HMM))
            storer.append(seged_short_sent)
        result = ' '.join(storer)
        return result

    def repl_non_chinese_character(self, uni_sent, repl=' '):
        """
        替换unicode字符串中的非汉字字符
        :param uni_sent: unicode字符串
        :param repl: 被替换的字符串，默认是u' '
        :return: 替换后的unicode字符串
        """
        sent = self.re_non_cn.sub(repl, uni_sent)
        # 去除多余空格
        sent = self.re_muti_space.sub(' ', sent).strip()
        return sent


if __name__ == "__main__":
    pass
    import os
    from utilspy.log.logger import Logger

    CURRENT_FILE_PATH = os.path.abspath(__file__)
    CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)

    # Dict absoluate path
    seg_dict_file = os.path.join(CURRENT_DIR_PATH, 'data/dict/lenovo/words_for_seg.txt')

    Logger.load_configure()

    cn_preprocessor = CnPreprocessor(seg_dict=seg_dict_file, flag='set', HMM=False)

    test_sent = "这个非常好，可以'￥21的QUchu'所有的非中文标记！！!!中国科学院自动化研究所。"
    print(test_sent)
    test_sent = cn_preprocessor.repl_non_chinese_character(test_sent)
    print(test_sent)

    print(cn_preprocessor.seg_sent(test_sent))
    print(cn_preprocessor.seg_sent_to_single(test_sent))
