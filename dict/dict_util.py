# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


import json


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


if __name__ == "__main__":
    pass
    d = {u'a': 1, u'b': 2, u'c': 3}
    s = DictUtil.to_string(d)
    print s, type(s)

    ln = DictUtil.to_line(d, with_line_separator=True)
    print ln, type(ln)
