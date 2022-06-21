#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2020/02/11'
# @description:


import re


# todo 支持小数说法
class Word2Num(object):
    def __init__(self):
        # 匹配数字，小数部分都是0
        self.re_decimals_end_0 = re.compile(r'^[\d]+\.[0]*$')
        # 数字字典
        self.numerals_dict = {
            u'〇': 0,
            u'一': 1,
            u'二': 2,
            u'三': 3,
            u'四': 4,
            u'五': 5,
            u'六': 6,
            u'七': 7,
            u'八': 8,
            u'九': 9,
            u'十': 10,

            u'零': 0,
            u'壹': 1,
            u'贰': 2,
            u'叁': 3,
            u'肆': 4,
            u'伍': 5,
            u'陆': 6,
            u'柒': 7,
            u'捌': 8,
            u'玖': 9,
            u'拾': 10,

            u'幺': 1,
            u'貮': 2,
            u'两': 2,
        }
        # 单位字典
        self.units_dict = {
            u'兆': 1000000000000,
            u'亿': 100000000,
            u'億': 100000000,
            u'万': 10000,
            u'萬': 10000,
            u'千': 1000,
            u'仟': 1000,
            u'百': 100,
            u'佰': 100,
            u'十': 10,
            u'拾': 10,

            # u'元': 1.0,
            # u'块': 1.0,
            # u'毛': 0.1,
            # u'角': 0.1,
            # u'分': 0.01
        }
        # 单位列表，有序，单位从大到小
        self.units_list = [
            u'兆',
            u'亿',
            u'億',
            u'万',
            u'萬',
            u'千',
            u'仟',
            u'百',
            u'佰',
            u'十',
            u'拾',

            # u'元',
            # u'块',
            # u'毛',
            # u'角',
            # u'分'
        ]
        # 数字和单位词典
        self.numerals_units_dict = dict(self.numerals_dict, **self.units_dict)
        # 向下补全知识库
        self.units4tmending = {
            u'兆': u'千亿',
            u'亿': u'千万',
            u'億': u'千萬',
            u'万': u'千',
            u'萬': u'仟',
            u'千': u'百',
            u'仟': u'佰',
            u'百': u'十',
            u'佰': u'拾',
            u'十': u'',
            u'拾': u'',

            # u'元': u'角',
            # u'块': u'毛',
            # u'毛': u'分',
            # u'角': u'分'
        }

    def word2num(self, word):
        """
        汉语数字转为阿拉伯数字
        :param word: 汉语数字
        :return: 阿拉伯数字
        """
        word = self.mend_word(word)
        if set(word) & set(self.units_list):
            result = str(self.word_with_unit_2num(word))
            # 去除小数都为0的部分，如2700.00,转变为2700
            if self.re_decimals_end_0.match(result):
                return result.split(u'.')[0]
            else:
                return result
        else:
            return self.word_without_unit_2num(word)

    # 补全，如：一千五补全为一千五百
    def mend_word(self, word):
        if len(word) == 0:
            return u''
        if len(word) > 2:
            if word[-1] in self.numerals_dict:
                if word[-2] in self.units_dict:
                    word = word + self.units4tmending[word[-2]]
        return word

    # 用于有单位的数字，如：两千七百；必须先补全，违规输入：两千七
    # 也可以用于一、二这种单字
    def word_with_unit_2num(self, word):
        # 若word为空字符串则返回0
        if not word:
            return 0
        for unit in self.units_list:
            # 遍历有序单位列表，若word中存在单位，则按照单位进行拆分，依照单位顺序从高到低递归
            if unit in word:
                parts = word.split(unit)
                left_part = self.word_with_unit_2num(parts[0])
                # if lp == 0 and i not in [u'元', u'块', u'毛', u'角', u'分']:
                # 处理十，十一这样以十开头的word，若以单位十进行拆分后，parts[0]将会是空串，left_part值将为0，需要纠正为1
                # 若word为二十一，parts[0]就会是二，不会是空串，结果正确
                if left_part == 0:
                    left_part = 1
                right_part = self.word_with_unit_2num(parts[1])
                return 1.0 * left_part * self.numerals_units_dict.get(unit, 0) + right_part * 1.0
        # 没有单位，直接返回数字的值，这里写word[-1]是为了处理零五这种情况
        return 1.0 * self.numerals_units_dict.get(word[-1], 0)

    # 用于连续但没有单位的数字，如：一二三零六
    def word_without_unit_2num(self, word):
        result = u''
        word_list = list(word)
        for char in word_list:
            result += str(self.numerals_dict[char])
        return result


if __name__ == "__main__":
    pass
    word2num = Word2Num()
    print(word2num.word2num(u"十"), u"十")
    print(word2num.word2num(u"十八"), u"十八")
    print(word2num.word2num(u"十九"), u"十九")
    print(word2num.word2num(u"二十一"), u"二十一")
    print(word2num.word2num(u"十一"), u"十一")
    print(word2num.word2num(u"一百"), u"一百")
    print(word2num.word2num(u"两千七"), u"两千七")
    print(word2num.word2num(u"一万零五"), u"一万零五")
    print(word2num.word2num(u"十万零三千六百零九"), u"十万零三千六百零九")
    print(word2num.word2num(u"两万一"), u"两万一")
    print(word2num.word2num(u"一亿五"), u"一亿五")
    print(word2num.word2num(u"两千"), u"两千")
    print(word2num.word2num(u"两千三百万"), u"两千三百万")
    print(word2num.word2num(u"一百二十"), u"一百二十")
    print(word2num.word2num(u"二十五"), u"二十五")
    print(word2num.word2num(u"九"), u"九")
    print(word2num.word2num(u"一百二十三"), u"一百二十三")
    print(word2num.word2num(u"一千二百零三"), u"一千二百零三")
    print(word2num.word2num(u"一万一千一百零一"), u"一万一千一百零一")
    print(word2num.word2num(u"一百二十三万四千五百六十七"), u"一百二十三万四千五百六十七")
    print(word2num.word2num(u"一千一百二十三万四千五百六十七"), u"一千一百二十三万四千五百六十七")
    print(word2num.word2num(u"一亿一千一百二十三万四千五百六十七"), u"一亿一千一百二十三万四千五百六十七")
    print(word2num.word2num(u"一百零二亿五千零一万零一千零三十八"), u"一百零二亿五千零一万零一千零三十八")
    print(word2num.word2num(u"一千一百一十一亿一千一百二十三万四千五百六十七"), u"一千一百一十一亿一千一百二十三万四千五百六十七")
    print(word2num.word2num(u"一兆一千一百一十一亿一千一百二十三万四千五百六十七"), u"一兆一千一百一十一亿一千一百二十三万四千五百六十七")
    print(word2num.word2num(u"四一零"), u"四一零")
    print(word2num.word2num(u"四幺零"), u"四幺零")

    print()
    print(word2num.word2num(u"一二三零六"), u"一二三零六")
    print(word2num.word2num(u"幺二三零六"), u"幺二三零六")
    print(word2num.word2num(u"七八九"), u"七八九")

    # 以下情况无法成功转换
    print()
    print(word2num.word2num(u"七八九十"), u"七八九十")
    print(word2num.word2num(u"七八九十十一"), u"七八九十十一")

    # print(word2num.word2num(u"两毛七"), u"两毛七")
    # print(word2num.word2num(u"两毛七分"), u"两毛七分")
    # print(word2num.word2num(u"两千三百万零两毛七分"), u"两千三百万零两毛七分")
    # print(word2num.word2num(u"两千三百万两毛七分"), u"两千三百万两毛七分")
    # print(word2num.word2num(u"一块两毛"), u"一块两毛")
    # print(word2num.word2num(u"一块二"), u"一块二")
    # print(word2num.word2num(u"一元两"), u"一元两")
