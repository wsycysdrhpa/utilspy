# -*- coding:utf-8 -*-


# @version: 1.0
# @author: renhe
# @date: '14-7-9'


class UrlBuilder():
    def __init__(self):
        pass

    #@staticmethod
    #def build_urls(url_template, start_number, end_number, step=1):
    #    if not step:
    #        step = 1
    #    urls = []
    #    for number in range(start_number, end_number+step, step):
    #        url = url_template % (str(number))
    #        urls.append(url)
    #    return urls

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
    print "http://{0}_{0}".format(1)
    pass

