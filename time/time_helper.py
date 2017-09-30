# -*- coding:utf-8 -*-


# @version: 1.0
# @author:
# @date: '14-4-10'


import time
import datetime


class TimeHelper():
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
            time_num = long(input_string[1:])
            standard_time = datetime.datetime(1970, 01, 01)
            max_time = datetime.datetime.utcfromtimestamp(long(time_num) / 1000)
            result = (standard_time - max_time + standard_time).strftime("%Y-%m-%d %H:%M:%S")
            return result
        return datetime.datetime.utcfromtimestamp(long(input_string) / 1000).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    pass

