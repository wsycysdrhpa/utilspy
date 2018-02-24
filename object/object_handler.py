# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-10'


class ObjectHandler(object):

    def __init__(self):
        pass

    @staticmethod
    def none_to_default(obj, default_value):
        return obj if obj else default_value


if __name__ == "__main__":
    print ObjectHandler.none_to_default('a', '1')
    print ObjectHandler.none_to_default('', '1')
    print ObjectHandler.none_to_default(None, '1')
