# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


class ListUtil(object):
    def __init__(self):
        pass

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


if __name__ == "__main__":
    pass
    a = 'abc'
    b = ListUtil.single_to_list(a)
    print b, type(b)
