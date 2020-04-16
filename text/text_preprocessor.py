#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2020/02/12'
# @description: 


import os
import codecs
import re
import sys
import importlib


CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIR_PATH = os.path.dirname(CURRENT_FILE_PATH)
CURRENT_PROJECT_PATH = os.path.dirname(CURRENT_DIR_PATH)
PARENT_PROJECT_PATH = os.path.dirname(CURRENT_PROJECT_PATH)

sys.path.append(PARENT_PROJECT_PATH)


from utilspy.text.cn_en_preprocessor import CnEnPreprocessor
from utilspy.text.cn_preprocessor import CnPreprocessor
from utilspy.text.en_preprocessor import EnPreprocessor
from utilspy.dict.dict_util import DictUtil


# Stop word absoluate path
STOP_WORD_FILE = os.path.join(CURRENT_DIR_PATH, r'data/stop_word/stop_word.txt')

# Set python default encode
# importlib.reload(sys)
# sys.setdefaultencoding("utf-8")


class TextPreprocessor(object):
    """
    中英文预处理，针对中文、英文和数字
    """
    def __init__(self, handle='cn_en', args=('', 'load', True, False, '')):
        if handle == 'cn_en':
            # args=('', 'load', True, False, '')
            self.preprocessor = CnEnPreprocessor(seg_dict=args[0], flag=args[1], lower=args[2], HMM=args[3],
                                                 break_up_dict=args[4])
        if handle == 'cn':
            # args=('', 'load', False)
            self.preprocessor = CnPreprocessor(seg_dict=args[0], flag=args[1], HMM=args[2])
        if handle == 'en':
            # args=(True,)
            self.preprocessor = EnPreprocessor(lower=args[0])

        self.re_space = re.compile("\s")
        # [A-Za-z0-9_]
        self.re_en_and_num = re.compile("\w+", re.A)

    def seg_line(self, line):
        return self.preprocessor.seg_sent(line)

    # 按字切分
    def seg_line_to_single(self, line):
        return self.preprocessor.seg_sent_to_single(line)

    # only support ce
    def seg_line_and_break_up(self, line):
        return self.preprocessor.seg_sent_and_break_up(line)

    def seg_file_line(self, src_file, dst_file, mode="seg_line"):
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(dst_file, 'wb', 'utf-8') as dst_fp:
            for line in src_fp:
                line = line.strip()
                seged_line = ""
                if "seg_line" == mode:
                    seged_line = self.seg_line(line)
                if "seg_line_to_single" == mode:
                    seged_line = self.seg_line_to_single(line)
                if "seg_line_and_break_up" == mode:
                    seged_line = self.seg_line_and_break_up(line)
                dst_fp.write(seged_line + '\n')

    def seg_file_column(self, src_file, dst_file, column, mode="seg_line"):
        """
        # 列之间需要以tab分割, 切割完成后与其他列拼接
        :param src_file: 
        :param column: 选取某一列，0为第一列
        :param dst_file: 
        :param mode: 
        :return: 
        """
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(dst_file, 'wb', 'utf-8') as dst_fp:
            for line in src_fp:
                line = line.strip()
                elements = line.split('\t')
                if len(elements) >= column + 1:
                    if "seg_line" == mode:
                        elements[column] = self.seg_line(elements[column].strip())
                    if "seg_line_to_single" == mode:
                        elements[column] = self.seg_line_to_single(elements[column].strip())
                    if "seg_line_and_break_up" == mode:
                        elements[column] = self.seg_line_and_break_up(elements[column].strip())
                # else:
                #     elements.append(u"")

                line = '\t'.join(elements)
                dst_fp.write(line + '\n')

    @staticmethod
    def del_blank_line(src_file, dst_file):
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp, \
                codecs.open(dst_file, 'wb', 'utf-8') as dst_fp:
            for line in src_fp:
                line = line.strip()
                if line:
                    dst_fp.write(line + '\n')

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
                codecs.open(del_stop_seged_file, 'wb', 'utf-8') as dst_fp:
            for seged_sent in src_fp:
                seged_sent = seged_sent.strip()
                del_stop_seged_sent = self.del_sent_stop_word(seged_sent, stop_word_dict)
                dst_fp.write(del_stop_seged_sent + '\n')

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
                codecs.open(del_stop_seged_file, 'wb', 'utf-8') as dst_fp:
            for line in src_fp:
                elements = line.split('\t')
                elements[column] = self.del_sent_stop_word(elements[column].strip(), stop_word_dict)
                line = '\t'.join(elements).strip()
                dst_fp.write(line + '\n')

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
        words = seged_sent.split(' ')
        for word in words:
            if word in stop_word_dict:
                continue
            else:
                tmp.append(word)
        return ' '.join(tmp)

    def file_deseg_to_file(self, src_file, dst_file, en_line_trans=True):
        with codecs.open(src_file, "rb", "utf-8", errors="ignore") as src_fp, \
                codecs.open(dst_file, "wb", 'utf-8') as dst_fp:
            for line in src_fp:
                line = line.strip()
                if not en_line_trans:
                    if self.re_en_and_num.search(line):
                        dst_fp.write(line + "\n")
                        continue
                    else:
                        text = "".join(self.re_space.split(line)[:])
                        dst_fp.write(text + "\n")
                else:
                    text = "".join(self.re_space.split(line)[:])
                    dst_fp.write(text + "\n")

    def file_deseg_colunm_to_file(self, src_file, dst_file, column, en_line_trans=True):
        with codecs.open(src_file, "rb", "utf-8", errors="ignore") as src_fp, \
                codecs.open(dst_file, "wb", 'utf-8') as dst_fp:
            for line in src_fp:
                line = line.strip()
                elements = line.split('\t')
                if len(elements) >= column + 1:
                    if not en_line_trans:
                        if self.re_en_and_num.search(elements[column]):
                            # print(elements[column])
                            dst_fp.write(line + "\n")
                            continue
                        else:
                            elements[column] = "".join(self.re_space.split(elements[column])[:])
                            line = '\t'.join(elements)
                            dst_fp.write(line + '\n')
                    else:
                        elements[column] = "".join(self.re_space.split(elements[column])[:])
                        line = '\t'.join(elements)
                        dst_fp.write(line + '\n')

    # seq = "中国科学院 自动化 研究所"
    # return = "研究所 自动化 中国科学院"
    def rev_seq(self, seq):
        seq = seq.strip()
        seq_list = seq.split(" ")
        rev_seq_list = list(reversed(seq_list))
        rev_seq = " ".join(rev_seq_list)
        return rev_seq

    def rev_seq2file(self, src_file, dst_file):
        with codecs.open(src_file, "rb", "utf-8", errors="ignore") as src_fp, \
                codecs.open(dst_file, "wb", 'utf-8') as dst_fp:
            for seq in src_fp:
                seq = seq.strip()
                if not seq:
                    continue
                else:
                    rev_seq = self.rev_seq(seq)
                    dst_fp.write(rev_seq + "\n")


if __name__ == "__main__":
    pass
    # 空将使用默认分词字典，非空则使用自定义分词词典
    seg_dict_file = r""

    # 空将不使用打散字典，非空则使用自定义打散词典
    break_up_dict_file = r""

    text_preprocessor = TextPreprocessor('cn_en', args=(seg_dict_file, 'set', True, False,
                                                        break_up_dict_file))
    # text_preprocessor = TextPreprocessor('cn', args=(seg_dict_file, 'set', False))
    # text_preprocessor = TextPreprocessor('en', args=(True,))

    # test_sent = u"I've got it. 这个非常好，!中国科学院自动化研究所。'Yes, ma'am.' the-waiter said.'好Yes, " \
    #             u"3 is可以'￥21的QUchu'所有的非中文标记！！! doctors'.' 'Yes, it is doctors'' he said."
    # print test_sent

    # seged_test_sent = text_preprocessor.seg_line(test_sent)
    # print seged_test_sent

    # single_seged_test_sent = text_preprocessor.seg_line_to_single(test_sent)
    # print single_seged_test_sent

    # line = u"中国科学院自动化研究所是21三体综合症的研究基地3aab所长不是我helloworld每周一好的啊"
    # line = text_preprocessor.seg_line_and_break_up(line)
    # print line

    # result = text_preprocessor.del_sent_stop_word(test_sent, DictUtil.file2dict(r'data/stop_word/stop_word.txt'))
    # print result

    # text_preprocessor.del_file_stop_word(r'', r'')

    # text_preprocessor.del_blank_line(r'', r'')

    # in_file = r""
    # out_file = r""
    # en_line_trans = True
    # text_preprocessor.file_deseg_to_file(in_file, out_file, en_line_trans)

    # in_file = r""
    # out_file = r""
    # column = 1
    # en_line_trans = True
    # text_preprocessor.file_deseg_colunm_to_file(in_file, out_file, column, en_line_trans)

    # in_file = r""
    # out_file = r""
    # text_preprocessor.rev_seq2file(in_file, out_file)

    # in_file = r""
    # out_file = r""
    # text_preprocessor.seg_file_line(in_file, out_file, mode="seg_line")

    in_file = r""
    out_file = r""
    column = 0
    mode = "seg_line"
    # text_preprocessor.seg_file_column(in_file, out_file, column, mode)

    import getopt

    info = "python3 %s -i <in_file> -o <out_file> [--in_file=] [--out_file=] [--seg_dict_file] [--break_up_dict_file] " \
           "[--preprocessor_flag=cn_en|cn|en] [--column=0] [--mode=seg_line|seg_line_to_single|seg_line_and_break_up] \n" \
           "If your want to use --seg_dict_file、 --break_up_dict_file, you should set --preprocessor_flag as well" % (sys.argv[0])
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["in_file=", "out_file=", "seg_dict_file=",
                                                           "break_up_dict_file=", "preprocessor_flag=", "column=", "mode="])
    except getopt.GetoptError:
        print(info)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print(info)
            sys.exit(0)
        elif opt in ("-i", "--in_file"):
            in_file = arg
        elif opt in ("-o", "--out_file"):
            out_file = arg
        elif opt in ("--seg_dict_file", ):
            seg_dict_file = arg
        elif opt in ("--break_up_dict_file", ):
            break_up_dict_file = arg
        elif opt in ("--preprocessor_flag", ):
            preprocessor_flag = arg
            if preprocessor_flag == "cn_en":
                text_preprocessor = TextPreprocessor('cn_en', args=(seg_dict_file, 'set', True, False,
                                                                    break_up_dict_file))
            elif  preprocessor_flag == "cn":
                text_preprocessor = TextPreprocessor('cn', args=(seg_dict_file, 'set', False))
            elif preprocessor_flag == "en":
                text_preprocessor = TextPreprocessor('en', args=(True,))
        elif opt in ("--column", ):
            column = int(arg)
        elif opt in ("--mode", ):
            mode = arg

    try:
        text_preprocessor.seg_file_column(in_file, out_file, column, mode)
    except FileNotFoundError:
        print(info)
        sys.exit(1)
