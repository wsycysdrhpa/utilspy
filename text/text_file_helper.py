# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


import os


class TextFileHelper():

    def __init__(self):
        pass

    @staticmethod
    def read_all(file_name):
        with open(file_name, "r") as target_file:
            lines = target_file.readlines()
            if lines:
                result = "".join(lines)
            else:
                result = ""
        return result

    @staticmethod
    def write(file_name, line):
        with open(file_name, "w") as target_file:
            target_file.write(line)

    @staticmethod
    def append_file(file_name, line):
        with open(file_name, "a") as target_file:
            target_file.write(line + "\n")

    @staticmethod
    def remove_file(file_name):
        if os.path.exists(file_name):
            os.remove(file_name)


if __name__ == "__main__":
    pass