#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2020/02/12'
# @description: 


import re
import logging
import codecs
import sys
import os

import jieba


CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)
CURRENT_PROJECT_PATH = os.path.dirname(CURRENT_DIR_PATH)
PARENT_PROJECT_PATH = os.path.dirname(CURRENT_PROJECT_PATH)

sys.path.append(PARENT_PROJECT_PATH)


from utilspy.text.cn_preprocessor import CnPreprocessor
from utilspy.text.en_preprocessor import EnPreprocessor


LOGGER = logging.getLogger('consoleOnly')


class CnEnPreprocessor(object):
    def __init__(self, seg_dict='', flag='load', lower=True, HMM=False, break_up_dict=''):
        self.lower = lower
        # jieba.cut方法是否开启HMM，Ture or False，默认不开启
        self.HMM = HMM
        self.re_useless = re.compile('[^0-9a-zA-Z\'\u4e00-\u9fa5]')
        self.re_muti_space = re.compile('\s+')
        self.re_cn_phrase = re.compile('[\u4e00-\u9fa5]+')
        self.cn_preprocessor = CnPreprocessor()
        self.en_preprocessor = EnPreprocessor()
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
        if break_up_dict:
            self.dict_map = self.build_map(break_up_dict)
        else:
            self.dict_map = {}

    def seg_sent_to_single(self, row_sent):
        if self.lower:
            row_sent = row_sent.lower()
        sent = row_sent.strip()
        sent = self.repl_useless_character(sent, ' ')
        # 处理中文，将匹配到的中文短语进行分词，为了和其他字符分割，前后添加空格
        sent = self.re_cn_phrase.sub(self._cut_to_single_and_add_blank, sent)
        # 处理英文
        words = sent.split(' ')
        for i in range(len(words)):
            if self.en_preprocessor.noun_plural_possessive.match(words[i]):
                continue
            words[i] = words[i].strip('\'')
        sent = ' '.join(words)
        # 去除多余空格
        sent = self.re_muti_space.sub(' ', sent).strip()
        return sent

    def seg_sent(self, row_sent):
        if self.lower:
            row_sent = row_sent.lower()
        sent = row_sent.strip()
        sent = self.repl_useless_character(sent, ' ')
        # 处理中文，将匹配到的中文短语进行分词，为了和其他字符分割，前后添加空格
        sent = self.re_cn_phrase.sub(self._cut_and_add_blank, sent)
        # 处理英文
        words = sent.split(' ')
        for i in range(len(words)):
            if self.en_preprocessor.noun_plural_possessive.match(words[i]):
                continue
            words[i] = words[i].strip('\'')
        sent = ' '.join(words)
        # 去除多余空格
        sent = self.re_muti_space.sub(' ', sent).strip()
        return sent

    def seg_sent_and_break_up(self, row_sent):
        sent = self.seg_sent(row_sent)
        if self.dict_map:
            tokens = sent.split()
            temp = []
            for token in tokens:
                if self.dict_map.get(token, -1) == 1:
                    temp.append(token)
                else:
                    # token中包含中文才需要进行打散
                    if self.re_cn_phrase.search(token):
                        temp.extend(self.break_up_token(token, self.dict_map))
                    else:
                        temp.append(token)

                    # 无论token是否包含中文，都进行打散
                    # temp.extend(self.break_up_token(token, self.dict_map))

            sent = ' '.join(temp)
        return sent

    def _cut_and_add_blank(self, matched):
        src_uni = matched.group()
        dst_uni = ' '.join(jieba.cut(src_uni, HMM=self.HMM))
        dst_uni = ' %s ' % dst_uni
        return dst_uni

    def _cut_to_single_and_add_blank(self, matched):
        src_uni = matched.group()
        dst_uni = self.cn_preprocessor.seg_sent_to_single(src_uni)
        dst_uni = ' %s ' % dst_uni
        return dst_uni

    def repl_useless_character(self, uni_sent, repl=' '):
        """
        替换unicode字符串中的无效字符
        :param uni_sent: 输入unicode字符串
        :param repl: 被替换的字符串，unicode，默认是u' '
        :return: unicode字符串
        """
        sent = self.re_useless.sub(repl, uni_sent)
        # 去除多余空格
        sent = self.re_muti_space.sub(' ', sent).strip()
        return sent

    def break_up_token(self, word, dict_map):
        temp = []
        if len(word) == 0:
            return []
        count = len(word)
        # 倒序，匹配map中最长字符串
        while count > 0:
            # 字典中有，则退出循环
            if dict_map.get(word[:count], -1) != -1:
                break
            else:
                count -= 1
        if count == 0:
            count = 1
        temp.append(word[:count])
        # 递归调用
        remain = self.break_up_token(word[count:], dict_map)
        temp.extend(remain)
        return temp

    def build_map(self, src_dict_file):
        dict_map = {}
        with codecs.open(src_dict_file, 'rb', 'utf-8') as src_fp:
            for line in src_fp:
                line = line.strip()
                if line:
                    dict_map[line] = 1
        return dict_map


if __name__ == "__main__":
    pass
    import os
    from utilspy.log.logger import Logger

    CURRENT_FILE_PATH = os.path.abspath(__file__)
    CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)

    # 使用默认分词字典
    seg_dict_file = r""

    # Dict absoluate path
    # seg_dict_file = os.path.join(CURRENT_DIR_PATH, 'data/dict/lenovo/words_for_seg.txt')

    # 不使用打散字典
    break_up_dict_file = r""

    # 使用打散字典
    # break_up_dict_file = os.path.join(CURRENT_DIR_PATH, 'data/dict/lenovo/words_for_lm_yd.txt')

    Logger.load_configure()

    cn_en_preprocessor = CnEnPreprocessor(seg_dict=seg_dict_file, flag='set', lower=True, HMM=False,
                                          break_up_dict=break_up_dict_file)

    test_sent = "I've got it. 这个非常好，!中国科学院自动化研究所3d全民k歌。'Yes, ma'am.' the-waiter said.'好Yes, " \
                "3 is可以'￥21的QUchu'所有的非中文标记！！! doctors'.' 'Yes, it is doctors'' he said."
    print(test_sent)

    test_sent_2 = cn_en_preprocessor.repl_useless_character(test_sent)
    print(test_sent_2)

    test_sent_3 = cn_en_preprocessor.seg_sent(test_sent)
    print(test_sent_3)

    test_sent_4 = cn_en_preprocessor.seg_sent_to_single(test_sent)
    print(test_sent_4)

    line = "中国科学院自动化研究所是21三体综合症的研究基地3aab所长不是我helloworld每周一好的啊"
    line = cn_en_preprocessor.seg_sent_and_break_up(line)
    print(line)
