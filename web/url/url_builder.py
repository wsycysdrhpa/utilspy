#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2016/12/8'
# @description:


class UrlBuilder(object):
    def __init__(self):
        pass

    @staticmethod
    def build_urls(url_template, start_number, end_number, step=1):
        if not step:
            step = 1
        urls = []
        for number in range(start_number, end_number+step, step):
            url = url_template.format(number)
            urls.append(url)
        return urls


if __name__ == "__main__":
    pass
    url_builder = UrlBuilder()
    url_template = 'http://{0}-{0}'
    urls = url_builder.build_urls(url_template, 1, 10, 2)
    for url in urls:
        print url
