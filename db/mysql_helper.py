#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2025/04/03'
# @description:


from typing import Optional, Any, List, Tuple, Dict, Generator, Union
import logging
from contextlib import contextmanager
from _sqlite3 import ProgrammingError, IntegrityError

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor


LOGGER = logging.getLogger('dual')


class MySqlHelper:
    """
    MySQL数据库助手类，提供数据库连接和基本操作功能
    """
    def __init__(self) -> None:
        """
        初始化数据库连接对象
        """
        self._conn: Optional[Connection] = None

    def create_db(self, host: str, db_name: str, user: str, password: str) -> None:
        """
        创建数据库
        :param host: 数据库主机地址
        :param db_name: 数据库名称
        :param user: 用户名
        :param password: 密码
        """
        with pymysql.connect(host=host, user=user, password=password, charset="utf8") as conn:
            with conn.cursor() as cur:
                cur.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
            conn.commit()

    def open(self, host: str = 'localhost', port: int = 3306, user: str = '',
             password: str = '', database: str = '', charset: str = 'utf8') -> Connection:
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
        if self._conn is not None:
            self.close()

        self._conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=database,
            charset=charset
        )
        return self._conn

    def open_by_db_setting(self, db_setting: Dict[str, str]) -> Connection:
        """
        通过配置字典打开数据库连接
        :param db_setting: 数据库配置字典
        :return: 数据库连接对象
        """
        return self.open(
            host=db_setting["host"],
            database=db_setting["database"],
            user=db_setting["user"],
            password=db_setting["password"]
        )

    @contextmanager
    def get_cursor(self) -> Generator[Cursor, None, None]:
        """
        获取数据库游标的上下文管理器
        :return: 数据库游标
        """
        if self._conn is None:
            raise RuntimeError("Database connection is not established")

        cursor = self._conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def read(self, sql: str, params: Optional[Union[Tuple, Dict]] = None) -> Tuple:
        """
        执行查询并返回所有结果
        :param sql: SQL查询语句
        :param params: 查询参数
        :return: 查询结果
        """
        with self.get_cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def yield_read(self, sql: str, params: Optional[Union[Tuple, Dict]] = None) -> Generator:
        """
        生成器方式读取查询结果
        :param sql: SQL查询语句
        :param params: 查询参数
        :return: 查询结果生成器
        """
        with self.get_cursor() as cur:
            cur.execute(sql, params)
            while True:
                result = cur.fetchone()
                if result is None:
                    break
                yield result

    def import_data_from_sql(self, sql_file_name: str) -> None:
        """
        从SQL文件导入数据
        :param sql_file_name: SQL文件路径
        """
        with open(sql_file_name, "r", encoding='utf-8') as sql_file:
            sql = "".join(sql_file.readlines())
        self.execute(sql)

    def execute(self, sql: str, params: Optional[Union[Tuple, Dict]] = None) -> None:
        """
        执行SQL语句
        :param sql: SQL语句
        :param params: 参数
        """
        with self.get_cursor() as cur:
            try:
                cur.execute(sql, params)
                self._conn.commit()
            except (ProgrammingError, IntegrityError) as e:
                LOGGER.error(f"执行SQL失败: {str(e)}\nSQL: {sql}\n参数: {params}")
                self._conn.rollback()
                raise
            except Exception as e:
                LOGGER.error(f"执行SQL失败(未知错误): {str(e)}\nSQL: {sql}\n参数: {params}")
                self._conn.rollback()
                raise

    def execute_many(self, sql: str, params_list: List[Union[Tuple, Dict]]) -> None:
        """
        批量执行SQL语句
        :param sql: SQL语句
        :param params_list: 参数列表
        """
        if not params_list:
            raise ValueError("参数列表不能为空")

        with self.get_cursor() as cur:
            try:
                cur.executemany(sql, params_list)
                self._conn.commit()
            except (ProgrammingError, IntegrityError) as e:
                LOGGER.error(f"批量执行SQL失败: {str(e)}\nSQL: {sql}\n参数: {params_list[0]}")
                self._conn.rollback()
                raise
            except Exception as e:
                LOGGER.error(f"批量执行SQL失败(未知错误): {str(e)}\nSQL: {sql}\n参数: {params_list[0]}")
                self._conn.rollback()
                raise

    def get_max_value(self, key_field_name: str, table_name: str) -> Any:
        """
        获取指定字段的最大值
        :param key_field_name: 字段名
        :param table_name: 表名
        :return: 最大值
        """
        sql = f"SELECT MAX({key_field_name}) FROM {table_name}"
        result = self.read(sql)
        return result[0][0]

    def close(self) -> None:
        """
        关闭数据库连接
        """
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def get_insert_id(self) -> int:
        """
        获取最后插入的ID
        :return: 最后插入的ID
        """
        if self._conn is None:
            raise RuntimeError("Database connection is not established")
        return self._conn.insert_id()

    def __enter__(self) -> 'MySqlHelper':
        """
        上下文管理器入口
        :return: MySqlHelper实例
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        上下文管理器出口
        """
        self.close()

    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        向表中插入单条数据
        :param table_name: 表名
        :param data: 要插入的数据字典，键为字段名，值为字段值
        :return: 插入的记录的ID
        """
        if not data:
            raise ValueError("插入数据不能为空")

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        self.execute(sql, tuple(data.values()))
        return self.get_insert_id()

    def insert_many(self, table_name: str, data_list: List[Dict[str, Any]]) -> None:
        """
        向表中批量插入数据
        :param table_name: 表名
        :param data_list: 要插入的数据字典列表
        """
        if not data_list:
            raise ValueError("插入数据列表不能为空")

        # 确保所有字典的键相同
        keys = data_list[0].keys()
        if not all(set(d.keys()) == set(keys) for d in data_list):
            raise ValueError("所有数据字典的键必须相同")

        columns = ', '.join(keys)
        placeholders = ', '.join(['%s'] * len(keys))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # 准备参数列表
        params_list = [tuple(d[k] for k in keys) for d in data_list]
        self.execute_many(sql, params_list)

    def insert_ignore(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        向表中插入单条数据，如果记录已存在则忽略
        :param table_name: 表名
        :param data: 要插入的数据字典
        :return: 插入的记录的ID，如果记录已存在则返回0
        """
        if not data:
            raise ValueError("插入数据不能为空")

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"

        self.execute(sql, tuple(data.values()))
        return self.get_insert_id()

    def insert_many_ignore(self, table_name: str, data_list: List[Dict[str, Any]]) -> None:
        """
        向表中批量插入数据，如果记录已存在则忽略
        :param table_name: 表名
        :param data_list: 要插入的数据字典列表
        """
        if not data_list:
            raise ValueError("插入数据列表不能为空")

        keys = data_list[0].keys()
        if not all(set(d.keys()) == set(keys) for d in data_list):
            raise ValueError("所有数据字典的键必须相同")

        columns = ', '.join(keys)
        placeholders = ', '.join(['%s'] * len(keys))
        sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"

        params_list = [tuple(d[k] for k in keys) for d in data_list]
        self.execute_many(sql, params_list)

    def replace(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        替换表中的数据（如果记录存在则替换，不存在则插入）
        :param table_name: 表名
        :param data: 要插入/替换的数据字典
        :return: 插入/替换的记录的ID
        """
        if not data:
            raise ValueError("插入数据不能为空")

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"

        self.execute(sql, tuple(data.values()))
        return self.get_insert_id()

    def replace_many(self, table_name: str, data_list: List[Dict[str, Any]]) -> None:
        """
        批量替换表中的数据
        :param table_name: 表名
        :param data_list: 要插入/替换的数据字典列表
        """
        if not data_list:
            raise ValueError("插入数据列表不能为空")

        keys = data_list[0].keys()
        if not all(set(d.keys()) == set(keys) for d in data_list):
            raise ValueError("所有数据字典的键必须相同")

        columns = ', '.join(keys)
        placeholders = ', '.join(['%s'] * len(keys))
        sql = f"REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"

        params_list = [tuple(d[k] for k in keys) for d in data_list]
        self.execute_many(sql, params_list)


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



    # 单条插入
    data = {
        'name': '张三',
        'age': 25,
        'email': 'zhangsan@example.com'
    }
    insert_id = mysql_helper.insert('users', data)

    # 批量插入
    data_list = [
        {'name': '李四', 'age': 30, 'email': 'lisi@example.com'},
        {'name': '王五', 'age': 28, 'email': 'wangwu@example.com'}
    ]
    mysql_helper.insert_many('users', data_list)

    # 插入忽略（如果记录已存在则忽略）
    mysql_helper.insert_ignore('users', data)

    # 替换（如果记录存在则替换，不存在则插入）
    mysql_helper.replace('users', data)
