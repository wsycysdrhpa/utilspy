# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


import json


class DictUtil():
    def __init__(self):
        pass

    @staticmethod
    def to_string(dict):
        result = "{"
        for key, value in dict.items():
            result += key + ":" + str(value) + ","
        result = result[:-1] + "}"
        return result

    @staticmethod
    def print_dict(dict):
        print DictUtil.to_string(dict)

    @staticmethod
    def to_line(dict, with_line_separator=True):
        try:
            line = json.dumps(dict, ensure_ascii=False, default=lambda obj: obj.__dict__)
        except:
            line = json.dumps(dict)
        if with_line_separator:
            return (line+"\n").encode("utf8")
        else:
            return line.encode("utf8")


if __name__ == "__main__":
    pass

