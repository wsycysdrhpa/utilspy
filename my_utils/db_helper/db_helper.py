#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: Aruan
# @date: ''


import MySQLdb


class DbHelper(object):
    """
    mysql数据库助手
    """
    def __init__(self):
        """
        构造方法，清空类内数据库连接对象
        """
        self._conn = None

    def open(self, database, host='localhost', user='root', password='123456', charset='utf8'):
        """
        打开数据库
        :param host: string，主机名或ip地址，本机为localhost或127.0.0.1
        :param user: string，用户名，一般为root
        :param password: string，密码
        :param database: string，数据库名字
        :param charset: string，使用字符集，一般为"utf8"
        :return: class，连接成功，返回数据库连接对象，类型为<class 'MySQLdb.connections.Connection'>
        """
        self._conn = MySQLdb.connect(host=host,
                                     user=user, 
                                     passwd=password, 
                                     db=database, 
                                     charset=charset)
        return self._conn

    def execute(self, sql, params=None):
        """
        执行sql语句
        :param sql: string，query to execute on server，如：
               sql_1: "INSERT INTO table_name(id，name) VALUES(%s, %s)"
               sql_2: "INSERT INTO table_name(id，name) VALUES(%s, %s)" % ("id_value", "name_value")
        :param params: tuple，传入参数，sql为形式1时向SQL语句中传递参数:，sql为形式2时为空，
        """
        # 使用cursor()方法获取操作游标
        cursor = self._conn.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql, params)
            # 提交到数据库执行
            self._conn.commit()
        except:
            # Rollback in case there is any error
            self._conn.rollback()
        cursor.close()

    def read(self, sql):
        """
        读数据库
        :param sql: string, 标准sql语句
        :return: tuple，返回全部读取结果
        """
        cursor = self._conn.cursor()
        cursor.execute(sql)
        # 使用 fetchall() 方法获取所有数据
        results = cursor.fetchall()
        cursor.close()
        return results

    def close(self):
        """
        关闭数据库连接
        """
        if self._conn:
            self._conn.close()


if __name__ == "__main__":
    pass
    db_helper = DbHelper()
    db_helper.open("math_util")
    test_read_sql = "select * from souhu"
    data = db_helper.read(test_read_sql)
    print type(data)

    db_helper.close()
