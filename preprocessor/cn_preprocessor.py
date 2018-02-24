#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/2/24'
# @description:


import re
import codecs

import jieba


class CnPreprocessor(object):
    """
    中文预处理
    """
    def __init__(self):
        pass
        jieba.set_dictionary()

    def seg_file_sent(self, row_file, seged_file, hmm=True):
        """
        将输入的文本文件进行分词，输出到文件中
        先根据句子中标点符号分成短句，再用jieba进行分词，可在类外用jieba.load_userdict()加载自定义字典增强分词效果
        也可用jieba.set_dictionary()方法在类外定义分词主词典，结巴分词默认词典为dict.txt
        :param row_file: 待分词文件
        :param seged_file: 分词后输出文件
        :param hmm: jieba.cut方法是否开启HMM，Ture or False，默认开启
        :return: 无
        """
        fin = open(row_file)
        fout = open(seged_file, 'w')
        row_sents = fin.readlines()
        fin.close()
        for row_sent in row_sents:
            # 句子进行分词
            sent_storer = self.seg_sent(row_sent, hmm=hmm)
            fout.write(sent_storer + '\n')
        fout.close()

    def seg_sent(self, row_sent, hmm=False):
        """
        将输入的句子进行分词，返回分词后的unicode句子字符串，可在类外用jieba.load_userdict()加载自定义字典增强分词效果
        先根据句子中标点符号分成短句，再用jieba进行分词
        :param row_sent: 输入句子字符串，可为str或unicode编码
        :param hmm: jieba.cut方法是否开启HMM，Ture or False，默认开启
        :return: 返回分词后的unicode句子字符串
        """
        # 必须要将str类型解码为unicode类型
        if isinstance(row_sent, str):
            row_sent = row_sent.decode()
        row_sent = row_sent.strip('\n')
        # 把句子先按照标点符号分割成短句序列
        repled_sent = self.repl_non_chinese_characters(row_sent, u' ')
        repled_sent = repled_sent.strip(u' ')
        repled_sent = re.sub(u'[ ]+', u' ', repled_sent)
        short_sent_list = repled_sent.split(u' ')
        # 对句子中所有短句序列进行分词，然后连接成一个unicode字符串
        sent_storer = u''
        for short_sent in short_sent_list:
            seged_short_sent = u' '.join(jieba.cut(short_sent, HMM=hmm))
            if sent_storer == u'':
                sent_storer += seged_short_sent
            else:
                sent_storer += u' ' + seged_short_sent
        return sent_storer

    def del_file_stop_word(self, seged_file, stop_word_file, del_stop_seged_file):
        """
        加入停用词表，删除停用词,输出到文件中
        :param seged_file: 分词后的文件路径
        :param stop_word_file: 停用词文件路径
        :param del_stop_seged_file: 输出文件路径，存储删除停用词后的分词结果，一句一行，空格隔开
        :return: 无
        """
        stop_word_list = self.build_stop_word(stop_word_file)
        fin = open(seged_file)
        seged_sents = fin.readlines()
        fin.close()
        fout = open(del_stop_seged_file, 'w')
        for seged_sent in seged_sents:
            sent_storer = self.del_sent_stop_word(seged_sent, stop_word_list)
            fout.write(sent_storer + '\n')
        fout.close()

    @staticmethod
    def del_sent_stop_word(seged_sent, stop_word_list):
        """
        删除用空格分好词句子中的停用词，返回unicode类型字符串
        :param seged_sent: 分好词的句子串，str或unicode类型
        :param stop_word_list: 停用词列表, 列表中停用词为unicode编码类型
        :return: 返回unicode类型字符串
        """
        if isinstance(seged_sent, str):
            seged_sent = seged_sent.decode()
        seged_sent = seged_sent.strip('\n')
        seged_words = seged_sent.split(' ')
        sent_storer = u''
        for seged_word in seged_words:
            if seged_word not in stop_word_list:
                if sent_storer == u'':
                    sent_storer = seged_word
                else:
                    sent_storer += u' ' + seged_word
            else:
                continue
        return sent_storer

    @staticmethod
    def repl_non_chinese_characters(uni_sent, repl=u''):
        """
        替换unicode类型字符串中的非汉字字符
        :param uni_sent: 输入必须是unicode类型字符串
        :param repl: 被替换的字符串，最好设为unicode类型，默认是u''
        :return: 替换后的unicode字符串
        """
        pattern = re.compile(ur'[^\u4e00-\u9fa5]')
        return pattern.sub(repl, uni_sent)

    @staticmethod
    def build_stop_word(stop_word_file):
        """
        将输入的停用词文件转为停用词列表, 列表中停用词为unicode编码类型
        :param stop_word_file: 停用词文件路径
        :return: 停用词列表
        """
        fin = open(stop_word_file)
        stop_words = fin.readlines()
        fin.close()
        stop_word_list = []
        for stop_word in stop_words:
            stop_word = stop_word.strip('\n')
            stop_word_list.append(stop_word.decode())
        return stop_word_list

    def sent2dict(self, sent):
        sent_length = len(sent)
        word_length = 1
        word_dict = {}
        while(word_length < sent_length + 1):
            start = 0
            end = word_length
            while(end < sent_length + 1):
                if sent[start:end] not in word_dict:
                    word_dict[sent[start:end]] = None
                start += 1
                end += 1
            word_length += 1
        # print " ".join(word_dict.keys())
        return word_dict


if __name__ == "__main__":
    pass
    cn_preprocessor = CnPreprocessor()
    # test_uni_sent = u"这个非常好，可以'QUchu'所有的非中文标记！！!!"
    # print cn_preprocessor.repl_non_chinese_characters(test_uni_sent)
    # cn_preprocessor.del_file_stop_word('data/test/test_stop_word.txt', 'data/test/cn_test_in.txt', 'data/test/cn_test_out.txt')
    # cn_preprocessor.seg_file_sent('data/test/cn_test_in.txt', 'data/test/cn_test_out.txt', userdict_file=False, hmm=False)
