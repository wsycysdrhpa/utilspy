#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2016/12/8'
# @description:


import re
import codecs


class Dao(object):
    """
    数据库访问对象
    """
    def __init__(self):
        pass

    @staticmethod
    def db_2_file(db_helper, table, dst_file, column=0):
        """
        将数据库中某列数据写入到文件中
        :param db_helper: 数据库助手对象
        :param table: 表名
        :param dst_file: 输出文件路径
        :param column: 数据库中第几列, 从1开始, 默认0为输出所有信息
        :return:
        """
        data = Dao.read_all(db_helper, table)
        with codecs.open(dst_file, 'wb') as dst_fp:
            for d_tuple in data:
                if column >= 1:
                    # 数据库中读出的字符为unicode类型，但是若有数字等其他格式，需要进行转换
                    info = unicode(d_tuple[column-1])
                    # 去除句子中的换行符号
                    info = re.sub(u'\n', u' ', info)
                    info = info.strip()
                    if info:
                        dst_fp.write(info + u'\n')
                else:
                    info = u''
                    for i in range(len(d_tuple)):
                        info += u'\t' + unicode(d_tuple[i])
                    info = info.strip()
                    dst_fp.write(info + u'\n')

    @staticmethod
    def read_all(db_helper, table):
        sql = "SELECT * FROM " + table
        infos = db_helper.read(sql)
        return infos


if __name__ == "__main__":
    pass
    from utilspy.db.mysql_helper import MySqlHelper
    mysql_helper = MySqlHelper()
    mysql_helper.open("an_mo")
    table = 'biao_xian'

    # data = Dao.read_all(mysql_helper, table)
    # for d in data:
    #     print d
    # mysql_helper.close()

    dst_file = r'out.txt'
    column = 2
    Dao.db_2_file(mysql_helper, table=table, dst_file=dst_file, column=column)
    mysql_helper.close()
