#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2015/11/21'
# @description:


from gensim import corpora
from gensim import models


class TFIDFTrainer(object):
    """
    train tfidf
    """

    def __init__(self):
        pass

    def file_2_tfidf_model(self, in_file_path, normalize=True):
        """
        用输入的句子文件训练tfidf模型
        :param in_file_path: 输入文件路径，文件格式为分词后的句子，词与词之间用一个空格隔开，一行一句
        :param normalize: 是否归一化, True or False
        :returns: 返回tfidf模型对象
        """
        dictionary = self.file_2_dictionary(in_file_path)
        corpus = self.file_2_id_corpus(in_file_path, dictionary)
        # 基于训练语料计算一个TF-IDF“模型”：
        tfidf_model = models.TfidfModel(corpus, normalize=normalize)
        return tfidf_model

    def file_conn_2_dict(self, tfidf_model, dictionary, in_file_path):
        """
        将输入文件中的分词后的句子连接成一个长句，将长句看成一个查询，计算它的每个词的tfidf值，tf值未除句子长度
        返回字典，键为词，值为对应的tfidf值
        :param tfidf_model: 训练好的tfidf模型
        :param dictionary: 用语料生成的词袋字典，格式为：{‘a': 0, ‘b': 1, ‘c': 2， ‘d': 3}
        :param in_file_path: 输入文件路径，文件格式为分词后的句子，词与词之间用一个空格隔开，一行一句
        :return: 返回长句的tfidf字典，键为词，值为相应的tfidf值
        """
        long_sent = self.conn_sent(in_file_path)
        return self.sent_2_dict(tfidf_model, dictionary, long_sent)

    def file_2_dict_list(self, tfidf_model, dictionary, in_file_path, norm=False):
        """
        将文件中每句话都转化为tfidf的字典，所有字典放入列表中，tf值未除句子长度
        :param tfidf_model: 训练好的tfidf模型
        :param dictionary: 用语料生成的词袋字典，格式为：{‘a': 0, ‘b': 1, ‘c': 2， ‘d': 3}
        :param in_file_path: 输入文件路径，文件格式为分词后的句子，词与词之间用一个空格隔开，一行一句
        :param norm: 是否归一化，除以句子长度，默认不除以句子长度
        :return: 返回字典的列表，字典键为词，值为相应的tfidf值
        """
        tfidf_dict_list = []
        fin = open(in_file_path)
        seged_sents = fin.readlines()
        for seged_sent in seged_sents:
            tfidf_dict_list.append(self.sent_2_dict(tfidf_model, dictionary, seged_sent, norm=norm))
        return tfidf_dict_list

    @staticmethod
    def sent_2_dict(tfidf_model, dictionary, seged_sent, norm=False):
        """
        将句子转化为字典，键为词，值为对应tfidf值
        :param tfidf_model: 训练好的tfidf模型
        :param dictionary: 用语料生成的词袋字典，格式为：{‘a': 0, ‘b': 1, ‘c': 2， ‘d': 3}
        :param seged_sent: 分好词的句子串,str或unicode
        :param norm: 是否归一化，除以句子长度，默认不除以句子长度
        :return: 字典，键为词，值为对应的tfidf值
        """
        tfidf_dict = {}
        seged_sent = seged_sent.decode()
        seged_sent = seged_sent.strip()
        word_list = seged_sent.split(" ")
        seged_sent_list = dictionary.doc2bow(word_list)
        # 如果某个词每句话中都出现，则它将不在seged_sent_tfidfs中
        seged_sent_tfidfs = tfidf_model[seged_sent_list]
        for word_tfidf in seged_sent_tfidfs:
            if norm:
                tfidf_dict[dictionary[word_tfidf[0]]] = word_tfidf[1]/len(word_list)
            else:
                tfidf_dict[dictionary[word_tfidf[0]]] = word_tfidf[1]
        return tfidf_dict

    def file_2_id_corpus(self, in_file_path, dictionary):
        """
        将输入的句子文件转换为用id表示token的tfidf语料
        格式为：[[(0, 1), (1, 1)], [(2, 2), (3, 1)]]; (2, 2)表示第二句中id为2的词出现了2词
        :param in_file_path: 输入文件路径，文件格式为分词后的句子，词与词之间用一个空格隔开，一行一句
        :param dictionary: 用语料生成的词袋字典，格式为：{‘a': 0, ‘b': 1, ‘c': 2， ‘d': 3}
        :returns: 返回tfidf语料，列表的列表格式; token映射id字典对象
        """
        # 用file_2_list方法将文档转为语料列表，字符串列表的列表, 内部元素为unicode编码
        uni_seged_sent_lists = self.file_2_list(in_file_path)
        # 将所有用字符串表示的句子转换为用id表示的句子向量，结构为列表的列表
        corpus = [self.sent_2_id_corpus(uni_seged_sent, dictionary) for uni_seged_sent in uni_seged_sent_lists]
        return corpus

    @staticmethod
    def sent_2_id_corpus(seged_sent, dictionary):
        """
        将分词后的句子转变为用id表示token的tfidf语料
        格式为：[(0, 1), (1, 1)]，(1, 1)表示该句中id为1的词出现了1词
        :param seged_sent: 分词后的句子，词与词之间用一个空格隔开
        :param dictionary: 用语料生成的词袋字典，格式为：{‘a': 0, ‘b': 1, ‘c': 2， ‘d': 3}
        :return: 返回tfidf语料,列表格式，token映射id字典对象
        """
        return dictionary.doc2bow(seged_sent)

    def file_2_dictionary(self, in_file_path):
        """
        将输入的句子文件转换为所有句子的token映射为id的字典
        :param in_file_path: 输入文件路径，文件格式为分词后的句子，词与词之间用一个空格隔开，一行一句
        :return: 用语料生成的词袋字典，格式为：{‘a': 0, ‘b': 1, ‘c': 2， ‘d': 3}
        """
        # 用file_2_list方法将文档转为语料列表，字符串列表的列表, 内部元素为unicode编码
        uni_seged_sent_lists = self.file_2_list(in_file_path)
        # 通过这些句子列表抽取一个“词袋（bag-of-words)”，将句子的token映射为id
        return corpora.Dictionary(uni_seged_sent_lists)

    def file_2_list(self, in_file_path):
        """
        将输入的分好词句子文件转化为字符串列表的列表
        :param in_file_path: 输入文件路径，文件格式为分词后的句子，词与词之间用一个空格隔开，一行一句
        :return: 字符串列表的列表, 内部元素为unicode编码
        """
        uni_sent_lists = []
        fin = open(in_file_path)
        string_sents = fin.readlines()
        for string_sent in string_sents:
            uni_sent_list = self.sent_2_list(string_sent)
            # 将所有unicode字符串列表都添加到列表中，结构为列表的列表
            uni_sent_lists.append(uni_sent_list)
        return uni_sent_lists

    @staticmethod
    def sent_2_list(sent):
        """
        将输入的分词后句子转化为列表
        :param sent: 分好词的句子字符串，空格分割，str或者unicode类型
        :return: 返回转化后的列表，列表中词都为unicode类型
        """
        sent = sent.decode()
        # 去除行末尾换行符
        sent = sent.strip()
        # 用空格将分词后句子字符串拆分成字符串列表
        return sent.split(u' ')

    @staticmethod
    def conn_sent(in_file_path):
        """
        将文件中所有的句子连接成一个句子，两句之间空格隔开
        :param in_file_path: 输入文件路径，文件读入为str类型
        :return: 返回连接后的长句,为unicode类型
        """
        fin = open(in_file_path)
        string_sents = fin.readlines()
        string_long_sent = ''
        for string_sent in string_sents:
            string_sent = string_sent.strip()
            if string_long_sent == '':
                string_long_sent += string_sent
            else:
                string_long_sent += ' ' + string_sent
        return string_long_sent.decode()


if __name__ == "__main__":
    pass

    tfidf_trainer = TFIDFTrainer()
    dictionary_test = tfidf_trainer.file_2_dictionary('data/test/in_test.txt')
    tfidf_model_test = tfidf_trainer.file_2_tfidf_model('data/test/in_test.txt')

    # tfidf_dict_test = tfidf_trainer.file_conn_2_dict(tfidf_model_test, dictionary_test, 'data/test/in_test.txt')
    # for key in tfidf_dict_test:
    #     print key, tfidf_dict_test[key]

    # sent_test = u'Shipment of gold damaged in a fire' \
    #             u'Delivery of silver arrived in a silver truck ' \
    #             u'Shipment of gold arrived in a truck\n'

    sent_test = u'传递 渠道 群众'

    for i in dictionary_test:
        print i, dictionary_test[i]
    print

    tfidf_dict_test = tfidf_trainer.sent_2_dict(tfidf_model_test, dictionary_test, sent_test, norm=False)
    for key in tfidf_dict_test:
        print key, tfidf_dict_test[key]

    # tfidf_dict_test = tfidf_trainer.sent_2_dict(tfidf_model_test, dictionary_test, sent_test, norm=True)
    # for key in tfidf_dict_test:
    #     print key, tfidf_dict_test[key]

    # tfidf_dict_list = tfidf_trainer.file_2_dict_list(tfidf_model_test, dictionary_test, 'data/test/in_test.txt')
    # for tfidf_dict in tfidf_dict_list:
    #     for key in tfidf_dict:
    #         print key, tfidf_dict[key]
