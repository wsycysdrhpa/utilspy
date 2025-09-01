#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2020/2/14'
# @description:


import time
import datetime
from functools import wraps


class TimeHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def str_to_time(input, format):
        return time.strptime(input, format)

    @staticmethod
    def str_to_datetime(input, format):
        return datetime.datetime.strptime(input, format)

    @staticmethod
    def get_min_date():
        return datetime.date.min

    @staticmethod
    def time_to_date(time):
        result = datetime.date(time.year, time.month, time.day)
        return result

    @staticmethod
    def now():
        return TimeHelper.get_formatter_time('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_formatter_time(format):
        return time.strftime(format, time.localtime(time.time()))

    @staticmethod
    def today():
        return datetime.date.today()

    @staticmethod
    def today_string():
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    @staticmethod
    def timestamp_to_date(input_string):
        if input_string[0] == "-":
            time_num = int(input_string[1:])
            standard_time = datetime.datetime(1970, 1, 1)
            max_time = datetime.datetime.utcfromtimestamp(int(time_num) / 1000)
            result = (standard_time - max_time + standard_time).strftime("%Y-%m-%d %H:%M:%S")
            return result
        return datetime.datetime.utcfromtimestamp(int(input_string) / 1000).strftime("%Y-%m-%d %H:%M:%S")

    # Decorator for test runing time: @TimeHelper.fn_timer
    @staticmethod
    def fn_timer(func):
        @wraps(func)
        def function_timer(*args, **kwargs):
            time_begin = time.time()
            result = func(*args, **kwargs)
            time_end = time.time()
            print("Total time of running %s: %s seconds" %(func.__name__, str(time_end - time_begin)))
            return result
        return function_timer


if __name__ == "__main__":
    pass
