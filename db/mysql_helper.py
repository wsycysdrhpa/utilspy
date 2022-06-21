#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2022/3/29'
# @description:


import logging
from _sqlite3 import ProgrammingError, IntegrityError

import pymysql

LOGGER = logging.getLogger('dual')


class MySqlHelper(object):
    """
    mysql数据库助手
    """
    def __init__(self):
        """
        构造方法，清空类内数据库连接对象
        """
        self._conn = None

    def create_db(self, host, db_name, user, password):
        conn = pymysql.connect(host=host, user=user, password=password, charset="utf8")
        cur = conn.cursor()
        cur.execute('create database if not exists ' + db_name)
        conn.commit()

    def open(self, host='localhost', port=0, user='', password='', database='', charset='utf8'):
        """
        打开数据库
        :param host: string，主机名或ip地址，本机为localhost或127.0.0.1
        :param port: int，端口
        :param user: string，用户名，一般为root
        :param password: string，密码
        :param database: string，数据库名字
        :param charset: string，使用字符集，一般为"utf8"
        :return: class，连接成功，返回数据库连接对象，类型为<pymysql.connections.Connection>
        """
        self._conn = pymysql.connect(host=host,
                                     port=port,
                                     user=user,
                                     passwd=password,
                                     db=database,
                                     charset=charset)
        return self._conn

    def open_by_db_setting(self, db_setting):
        return self.open(host=db_setting["host"],
                         database=db_setting["database"],
                         user=db_setting["user"],
                         password=db_setting["password"])

    def read(self, sql, params=None):
        """
        读数据库
        :param sql: string, 标准sql语句
        :param params: tuple，传入参数
        :return: tuple，返回全部读取结果
        """
        cur = self._conn.cursor()
        cur.execute(sql, params)
        # 使用 fetchall() 方法获取所有数据
        result = cur.fetchall()
        cur.close()
        return result

    def yield_read(self, sql, params=None):
        cur = self._conn.cursor()
        cur.execute(sql, params)
        while True:
            result = cur.fetchone()
            if result is None:
                break
            yield result
        cur.close()

    def import_data_from_sql(self, sql_file_name):
        sql_file = open(sql_file_name, "r")
        sql = "".join(sql_file.readlines())
        sql_file.close()
        self.execute(sql)

    def execute(self, sql, params=None):
        """
        执行sql语句
        :param sql: string，query to execute on server，如：
               sql_1: "INSERT INTO table_name(id，name) VALUES(%s, %s)"
               sql_2: "INSERT INTO table_name(id，name) VALUES(%s, %s)" % ("id_value", "name_value")
        :param params: tuple，传入参数，sql为形式1时向SQL语句中传递参数:，sql为形式2时为空，
        """
        # 使用cursor()方法获取操作游标
        cur = self._conn.cursor()
        sql_info = str(sql) + "\t" + str(params)
        try:
            # 执行SQL语句
            cur.execute(sql, params)
            # 提交到数据库执行
            self._conn.commit()
        except ProgrammingError as e:
            LOGGER.error("执行sql失败：" + str(e) + "\tsql=" + sql_info)
            # Rollback in case there is error
            self._conn.rollback()
        except IntegrityError as e:
            LOGGER.error("执行sql失败IntegrityError：" + str(e) + "\tsql=" + sql_info)
            self._conn.rollback()
        except Exception as e:
            LOGGER.error("执行sql失败 未知错误：" + str(e) + "\tsql=" + sql_info)
            self._conn.rollback()
        cur.close()

    def execute_many(self, sql, params_list=None):
        if not params_list:
            LOGGER.error("paramsList is None")
        cur = self._conn.cursor()
        try:
            cur.executemany(sql, params_list)
            self._conn.commit()
        except ProgrammingError as e:
            LOGGER.error("执行sql失败：" + str(e) + str(params_list[0]))
        except IntegrityError as e:
            LOGGER.error("执行sql失败IntegrityError：" + str(e) + str(params_list[0]))
        except Exception as e:
            LOGGER.error("执行sql失败 未知错误：" + str(e) + str(params_list[0]))

    def get_max_value(self, key_field_name, table_name):
        sql = "select max(" + key_field_name + ") from " + table_name
        result = self.read(sql)
        return result[0][0]

    def close(self):
        """
        关闭数据库连接
        """
        if self._conn:
            self._conn.close()

    def get_insert_id(self):
        return self._conn.insert_id()


if __name__ == "__main__":
    pass
    import os
    from os.path import dirname

    from utilspy.environment.environment import Environment

    CURRENT_FILE_PATH = os.path.abspath(__file__)

    conf_path_list = []
    conf = os.path.join(dirname(dirname(CURRENT_FILE_PATH)), "environment/conf/ref.ini")
    conf_path_list.append(conf)
    Environment.get_instance(load_user_configure=True, conf_path_list=conf_path_list).init(CURRENT_FILE_PATH, 3)

    host = Environment.get_instance().get_configure_value("mysql", "host").strip()
    port = int(Environment.get_instance().get_configure_value("mysql", "port").strip())
    user = Environment.get_instance().get_configure_value("mysql", "user").strip()
    password = Environment.get_instance().get_configure_value("mysql", "password").strip()
    database = Environment.get_instance().get_configure_value("mysql", "database").strip()

    mysql_helper = MySqlHelper()
    mysql_helper.open(host, port, user, password, database)

    # test_read_sql = "select * from ics_intent"
    # data = mysql_helper.read(test_read_sql)
    # for d in data:
    #     print(d)
    # mysql_helper.close()
