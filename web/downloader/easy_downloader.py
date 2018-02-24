#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2015/12/24'
# @description:


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
    easy_downloader = EasyDownloader()
    url = 'https://www.baidu.com/'
    html = easy_downloader.download(url)
    print html
