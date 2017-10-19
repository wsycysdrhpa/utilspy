#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# @version: 1.0
# @author: Aruan
# @date: '2015/12/24'


import urllib


class EasyDownloader(object):
    def __init__(self):
        pass

    @staticmethod
    def download(url):
        """
        下载网页源码
        :param url: 输入网址
        :return: 返回源码
        """
        html = urllib.urlopen(url).read()
        return html


if __name__ == "__main__":
    pass
