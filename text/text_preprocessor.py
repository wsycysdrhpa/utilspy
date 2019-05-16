#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/2/24'
# @description: 


import os
import codecs
import re
import sys


from utilspy.text.cn_en_preprocessor import CnEnPreprocessor
from utilspy.text.cn_preprocessor import CnPreprocessor
from utilspy.text.en_preprocessor import EnPreprocessor
from utilspy.dict.dict_util import DictUtil


CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)

# Stop word absoluate path
STOP_WORD_FILE = os.path.join(CURRENT_DIR_PATH, r'data/stop_word/stop_word.txt')

# Set python default encode
reload(sys)
sys.setdefaultencoding("utf-8")


class TextPreprocessor(object):
    """
    中英文预处理，针对中文、英文和数字
    """
    def __init__(self, handle='cn_en', args=('', 'load', True, False)):
        if handle == 'cn_en':
            # args=('', 'load', True, False)
            self.preprocessor = CnEnPreprocessor(seg_dict=args[0], flag=args[1], lower=args[2], HMM=args[3])
        if handle == 'cn':
            # args=('', 'load', False)
            self.preprocessor = CnPreprocessor(seg_dict=args[0], flag=args[1], HMM=args[2])
        if handle == 'en':
            # args=(True,)
            self.preprocessor = EnPreprocessor(lower=args[0])

        self.re_space = re.compile(u"\s")
        # [A-Za-z0-9_]
        self.re_en_and_num = re.compile(u"\w+")

    # 按字切分
    def seg_line_to_single(self, line):
        return self.preprocessor.seg_sent_to_single(line)

    def seg_line(self, line):
        return self.preprocessor.seg_sent(line)

    def seg_file_line(self, src_file, dst_file):
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(dst_file, 'wb') as dst_fp:
            for line in src_fp:
                line = line.strip()
                seged_line = self.preprocessor.seg_sent(line)
                dst_fp.write(seged_line + u'\n')

    def seg_file_column(self, src_file, column, dst_file):
        """
        # 列之间以tab分割, 切割完成后与其他列拼接
        :param src_file: 
        :param column: 选取某一列，0为第一列
        :param dst_file: 
        :return: 
        """
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(dst_file, 'wb') as dst_fp:
            for line in src_fp:
                line = line.strip()
                elements = line.split(u'\t')
                elements[column] = self.seg_line(elements[column].strip())
                line = u'\t'.join(elements).strip()
                dst_fp.write(line + u'\n')

    @staticmethod
    def del_blank_line(src_file, dst_file):
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(dst_file, 'wb') as dst_fp:
            for line in src_fp:
                line = line.strip()
                if line:
                    dst_fp.write(line + u'\n')

    def del_file_stop_word(self, seged_file, del_stop_seged_file, stop_word_file=STOP_WORD_FILE):
        """
        加入停用词表, 删除停用词, 输出到文件
        :param seged_file: 分词后的文件路径
        :param del_stop_seged_file: 输出文件路径, 如果删除停用词后结果是空串，输出空行
        :param stop_word_file: 停用词文件路径
        :return: 
        """
        stop_word_dict = DictUtil.file2dict(stop_word_file)
        with codecs.open(seged_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(del_stop_seged_file, 'wb') as dst_fp:
            for seged_sent in src_fp:
                seged_sent = seged_sent.strip()
                del_stop_seged_sent = self.del_sent_stop_word(seged_sent, stop_word_dict)
                dst_fp.write(del_stop_seged_sent + u'\n')

    def del_file_column_stop_word(self, seged_file, column, del_stop_seged_file, stop_word_file=STOP_WORD_FILE):
        """
        加入停用词表, 选择某列并删除停用词, 列之间以tab分割, 处理完成后与其他列拼接
        :param seged_file: 分词后的文件路径
        :param column: 选取某一列，0为第一列
        :param del_stop_seged_file: 输出文件路径, 如果删除停用词后结果是空串，输出空串
        :param stop_word_file: 停用词文件路径
        :return: 
        """
        stop_word_dict = DictUtil.file2dict(stop_word_file)
        with codecs.open(seged_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(del_stop_seged_file, 'wb') as dst_fp:
            for line in src_fp:
                elements = line.split(u'\t')
                elements[column] = self.del_sent_stop_word(elements[column].strip(), stop_word_dict)
                line = u'\t'.join(elements).strip()
                dst_fp.write(line + u'\n')

    @staticmethod
    def del_sent_stop_word(seged_sent, stop_word_dict):
        """
        删除用空格分词后的句子的停用词，返回unicode字符串
        :param seged_sent: 分好词的句子串，unicode
        :param stop_word_dict: 停用词字典
        :return: 返回分词去停用词的unicode字符串
        """
        tmp = []
        seged_sent = seged_sent.strip()
        words = seged_sent.split(u' ')
        for word in words:
            if word in stop_word_dict:
                continue
            else:
                tmp.append(word)
        return u' '.join(tmp)

    def deseg2file(self, src_file, dst_file):
        with codecs.open(src_file, "rb", "utf-8", errors="ignore") as src_fp, \
                codecs.open(dst_file, "wb") as dst_fp:
            for line in src_fp:
                line = line.strip()
                if self.re_en_and_num.search(line):
                    dst_fp.write(line + u"\n")
                    continue
                else:
                    text = u"".join(self.re_space.split(line)[:])
                    dst_fp.write(text + u"\n")

    # seq = "中国科学院 自动化 研究所"
    # return = "研究所 自动化 中国科学院"
    def rev_seq(self, seq):
        seq = seq.strip()
        seq_list = seq.split(u" ")
        rev_seq_list = list(reversed(seq_list))
        rev_seq = u" ".join(rev_seq_list)
        return rev_seq

    def rev_seq2file(self, src_file, dst_file):
        with codecs.open(src_file, "rb", "utf-8", errors="ignore") as src_fp, \
                codecs.open(dst_file, "wb") as dst_fp:
            for seq in src_fp:
                seq = seq.strip()
                if not seq:
                    continue
                else:
                    rev_seq = self.rev_seq(seq)
                    dst_fp.write(rev_seq + u"\n")


if __name__ == "__main__":
    pass
    # Dict absoluate path
    seg_dict_file = os.path.join(CURRENT_DIR_PATH, 'data/dict/lenovo/words_for_seg.txt')

    text_preprocessor = TextPreprocessor('cn_en', args=(seg_dict_file, 'set', True, False))
    # text_preprocessor = TextPreprocessor('cn', args=(seg_dict_file, 'set', False))
    # text_preprocessor = TextPreprocessor('en', args=(True,))

    test_sent = u"I've got it. 这个非常好，!中国科学院自动化研究所。'Yes, ma'am.' the-waiter said.'好Yes, " \
                u"3 is可以'￥21的QUchu'所有的非中文标记！！! doctors'.' 'Yes, it is doctors'' he said."
    print test_sent

    seged_test_sent = text_preprocessor.seg_line(test_sent)
    print seged_test_sent

    single_seged_test_sent = text_preprocessor.seg_line_to_single(test_sent)
    print single_seged_test_sent

    # text_preprocessor.seg_file_line(r'data/test/test_in.txt', r'data/test/test_seg_file_out.txt')

    # result = text_preprocessor.del_sent_stop_word(test_sent, DictUtil.file2dict(r'data/stop_word/stop_word.txt'))
    # print result

    # text_preprocessor.del_file_stop_word(r'data/test/test_seg_file_out.txt', r'data/test/test_del_stop_out.txt')

    # text_preprocessor.del_blank_line(r'data/test/test_del_stop_out.txt', r'data/test/test_del_blank_out.txt')

    # in_file = r""
    # out_file = r""
    # text_preprocessor.deseg2file(in_file, out_file)

    # in_file = r""
    # out_file = r""
    # text_preprocessor.rev_seq2file(in_file, out_file)
