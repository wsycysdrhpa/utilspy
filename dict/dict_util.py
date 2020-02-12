# -*- coding:utf-8 -*-

# @version: 1.0
# @author: renhe, arain
# @date: '20-02-12'


import json
import codecs


class DictUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def to_string(src_dict):
        result = "{"
        for key, value in src_dict.items():
            result += key + ":" + str(value) + ","
        result = result[:-1] + "}"
        return result

    @staticmethod
    def print_dict(src_dict):
        print(DictUtil.to_string(src_dict))

    @staticmethod
    def to_line(src_dict, with_line_separator=True):
        try:
            line = json.dumps(src_dict, ensure_ascii=False, default=lambda obj: obj.__dict__)
        except:
            line = json.dumps(src_dict)
        if with_line_separator:
            return (line+"\n").encode("utf8")
        else:
            return line.encode("utf8")

    @staticmethod
    def file2dict(src_file):
        """
        将输入文件中的每一行转化为以行为键，以None为值的字典
        :param src_file: 
        :return: 
        """
        result_dict = {}
        with codecs.open(src_file, 'rb', 'utf-8', errors='ignore') as src_fp:
            for line in src_fp:
                line = line.strip()
                if line in result_dict:
                    continue
                else:
                    result_dict[line] = None
        return result_dict

    @staticmethod
    def cut_str_2_sub_str(src_str):
        """
        将字符串按照长度1, 2, 3, ..., length拆分成字串，返回元组
        :param src_str: 
        :return: 
        """
        results = []
        # sub_str_len 表示子字符串长度
        for sub_str_len in range(1, len(src_str) + 1):
            # offset 表示偏移量
            for offset in range(len(src_str) - sub_str_len + 1):
                results.append((src_str[offset:offset + sub_str_len], offset, offset + sub_str_len))
        return results


if __name__ == "__main__":
    pass
    d = {'a': 1, 'b': 2, 'c': 3}
    s = DictUtil.to_string(d)
    print(s, type(s))

    ln = DictUtil.to_line(d, with_line_separator=True)
    print(ln, type(ln))

    # result = DictUtil.file2dict(r'../text/data/stop_word/stop_word.txt')
    # for ele in result:
    #     print ele

    test_sent = "abc"
    for ele in DictUtil.cut_str_2_sub_str(test_sent):
        print(ele)
