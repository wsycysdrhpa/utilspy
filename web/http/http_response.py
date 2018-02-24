# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '2016/8/26'


class HttpResponse(object):
    def __init__(self):
        self.url = ""
        self.headers = dict()
        self.status = 200
        self.message = "OK"
        self.content = ""


if __name__ == "__main__":
    pass
