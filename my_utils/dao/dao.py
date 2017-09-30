#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: Aruan
# @date: '2015/11/24'


import re


class Dao(object):
    """
    数据库访问对象
    """
    def __init__(self):
        pass

    @staticmethod
    def db_column_2_file(db_helper, sql, column_number, out_file_path):
        """
        将数据库中某列数据写入到文件中
        :param db_helper: 数据库助手对象
        :param sql: 查询语句
        :param column_number: 数据库中第几列, 从0开始
        :param out_file_path: 输出文件路径
        :return: 无
        """
        fout = open(out_file_path, 'w')
        data_tuples = db_helper.read(sql)
        for data_tuple in data_tuples:
            data = data_tuple[column_number]
            # 数据库中读出的数据为unicode类型
            if isinstance(data, str) or isinstance(data, unicode):
                # 去除句子中的换行符号
                data = re.sub(r'\n', u' ', data)
                # 去除句尾空格
                data.strip(u' ')
            if data is not None and data != u'':
                fout.write(data + '\n')

    def read_all(self, db_helper, table):
        sql = "SELECT * FROM " + table
        infos = db_helper.read(sql)
        return infos


if __name__ == "__main__":
    pass