#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2018/11/7'
# @description: 


import random
import codecs


NUMERALS_DICT = {
    u'0': u'零',
    u'1': u'一',
    u'2': u'二',
    u'3': u'三',
    u'4': u'四',
    u'5': u'五',
    u'6': u'六',
    u'7': u'七',
    u'8': u'八',
    u'9': u'九',
}


class NumberHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def gen_rand_num_str(length=4, cn=False):
        start = 10 ** (length - 1)
        end = 10 ** length - 1
        num_str = str(random.randint(start, end))
        # print num_str
        if cn:
            num_list = list(num_str)
            for i in range(len(num_list)):
                num_list[i] = NUMERALS_DICT[num_list[i]]

            num_str = u''.join(num_list)
            # print num_str
        return num_str

    def batch_gen_rand_num_str(self, dst_file, length, amount, cn):
        with codecs.open(dst_file, "wb", "utf-8") as dst_fp:
            for i in xrange(amount):
                num_str = self.gen_rand_num_str(length=length, cn=cn)
                dst_fp.write(num_str + u'\n')


if __name__ == "__main__":
    pass
    number_helper = NumberHelper()

    # NumberHelper.gen_rand_num_str(cn=True)

    number_helper.batch_gen_rand_num_str(r'out_l-6.txt', length=6, amount=100, cn=True)
