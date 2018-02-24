# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


import os
import codecs


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


if __name__ == "__main__":
    pass
    in_file = '__init__.py'
    print TextFileHelper.read_all(in_file)

    data = u"为了test！"
    TextFileHelper.write(data, 'test.txt')

    TextFileHelper.append_file(data, 'test.txt')

    TextFileHelper.remove_file('test.txt')
