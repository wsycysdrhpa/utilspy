# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


class CollectionUtil():
    def __init__(self):
        pass

    @staticmethod
    def to_list(obj):
        collection = []
        if obj:
            collection.append(obj)
        return collection

    @staticmethod
    def single_to_list(obj):
        if obj is None:
            return []
        if type(obj) == list:
            return obj
        else:
            collection = list()
            collection.append(obj)
            return collection

    @staticmethod
    def dict_to_str(dictionary):
        line = ""
        if not dictionary:
            return "{}"
        parts = []
        for key in dictionary:
            part = '"{0}":"{1}"'
            value = dictionary[key]
            if type(value) == unicode:
                value = value.encode("utf8")
            part = part.format(key, value)
            parts.append(part)
        line = "{" + ",".join(parts) + "}"
        return line.replace("\n", "").replace("\r", "")


if __name__ == "__main__":
    pass

