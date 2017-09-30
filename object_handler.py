# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-10'


class ObjectHandler():

    def __init__(self):
        pass

    @staticmethod
    def none_to_default(object, default_value):
        return object if object else default_value


if __name__ == "__main__":
    print ObjectHandler.none_to_default("a", "1")

