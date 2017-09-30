# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-11'


import re


class RegexHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def match_single(regex, source, match_result_group_name):
        matchResult = regex.search(source)
        if matchResult:
            return matchResult.group(match_result_group_name)
        else:
            return None

    @staticmethod
    def match_several(regex, source, match_result_group_name):
        result = []
        for matchResult in regex.finditer(source):
            result.append(matchResult.group(match_result_group_name))
        return result

    @staticmethod
    def match_content(regex, source):
        match = regex.search(source)
        if match:
            return match.group()
        return ""

    @staticmethod
    def match_value(regex, source):
        match = regex.search(source)
        if match:
            return match.groups()[0]
        return ""


if __name__ == "__main__":
    pass