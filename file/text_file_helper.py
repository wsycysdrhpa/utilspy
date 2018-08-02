# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


import os
import codecs
import random
import sys


# Set python default encode
reload(sys)
sys.setdefaultencoding('utf-8')


class TextFileHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def read_all(src_file):
        with codecs.open(src_file, "rb", encoding='utf-8', errors='ignore') as src_fp:
            lines = src_fp.readlines()
            if lines:
                result = "".join(lines)
            else:
                result = ""
        return result

    # 用于一次性写入大文件
    @staticmethod
    def write(data, dst_file):
        with codecs.open(dst_file, "wb") as dst_fp:
            dst_fp.write(data + "\n")

    @staticmethod
    def append_file(data, dst_file):
        with codecs.open(dst_file, "ab") as dst_fp:
            dst_fp.write(data + "\n")

    @staticmethod
    def remove_file(src_file):
        if os.path.exists(src_file):
            os.remove(src_file)

    @staticmethod
    def random_extract_file_data(src_file, proportion=0.0, number=0, extracted_file='', remain_file=''):
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp:
            lines = src_fp.readlines()
            # 抽取数量
            extract_num = 0
            # 存储抽取出的数据
            extracted_list = []
            # 按比例抽取
            if proportion:
                extract_num = int(proportion * len(lines))
            # 按数量抽取
            if number:
                extract_num = number
            for _ in range(extract_num):
                end = len(lines) - 1
                pop_index = random.randint(0, end)
                extracted = lines.pop(pop_index)
                extracted_list.append(extracted)
        if extracted_file:
            with codecs.open(extracted_file, 'wb') as dev_fp:
                # 此时extracted和line都包含换行符
                for extracted in extracted_list:
                    dev_fp.write(extracted)
        if remain_file:
            with codecs.open(remain_file, 'wb') as dst_fp:
                for line in lines:
                    dst_fp.write(line)
        extracted_list = [ele.strip() for ele in extracted_list]
        lines = [line.strip() for line in lines]
        # extracted_list中元素顺序是打乱的, lines和src_file顺序一致
        return extracted_list, lines

    @staticmethod
    def pick_columns_of_file(src_file, col_list, dst_file):
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp,\
                codecs.open(dst_file, 'wb') as dst_fp:
            for line in src_fp:
                line = line.strip()
                if not line:
                    dst_fp.write(u'\n')
                else:
                    new_line = u''
                    line_array = line.split(u'\t')
                    for col in col_list:
                        new_line += u'\t' + line_array[col]
                    new_line = new_line.strip()
                    dst_fp.write(new_line + u'\n')


if __name__ == "__main__":
    pass
    # in_file = '__init__.py'
    # print TextFileHelper.read_all(in_file)

    # data = u"为了test！"
    # TextFileHelper.write(data, 'test.txt')

    # TextFileHelper.append_file(data, 'test.txt')

    # TextFileHelper.remove_file('test.txt')

    src_file = r''
    proportion = 0.0
    number = 0
    extracted_file = r''
    remain_file = r''
    extracted_list, lines = TextFileHelper.random_extract_file_data(src_file=src_file,
                                                                    proportion=proportion,
                                                                    number=number,
                                                                    extracted_file=extracted_file,
                                                                    remain_file=remain_file)
