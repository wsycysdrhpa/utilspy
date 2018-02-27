# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


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
        print DictUtil.to_string(src_dict)

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

    # 将字符串按照长度1, 2, 3, ..., length进行拆分，返回字典
    @staticmethod
    def string2dict(src_uni):
        result_dict = {}
        max_len = len(src_uni)
        uni_len = 1
        while uni_len < max_len+1:
            start = 0
            end = uni_len
            while end < max_len+1:
                if src_uni[start:end] in result_dict:
                    continue
                else:
                    result_dict[src_uni[start:end]] = None
                start += 1
                end += 1
            uni_len += 1
        # print " ".join(word_dict.keys())
        return result_dict


if __name__ == "__main__":
    pass
    d = {u'a': 1, u'b': 2, u'c': 3}
    s = DictUtil.to_string(d)
    print s, type(s)

    ln = DictUtil.to_line(d, with_line_separator=True)
    print ln, type(ln)

    # result = DictUtil.file2dict(r'../text/data/stop_word/stop_word.txt')
    # for ele in result:
    #     print ele

    test_sent = u"好a！"
    for ele in DictUtil.string2dict(test_sent):
        print ele
