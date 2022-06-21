# -*- coding:utf-8 -*-


# @version: 1.0
# @author:
# @date: '14-4-10'


import socket
import urllib2
import random
import contextlib
import StringIO
import gzip

from http_response import HttpResponse
from html_coder import HtmlCoder


class HttpRequest(object):

    def __init__(self):
        pass

    default_headers = {'Accept-encoding': 'gzip', 'Referer': '', 'Accept-Language': 'en-us,en;q=0.5'}

    user_agents = [
            'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; ja; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; ja; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6',
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/536.11 (KHTML, like Gecko) Ubuntu/12.04 Chromium/20.0.1132.47 Chrome/20.0.1132.47 Safari/536.11',
            'Opera/9.80 (Windows NT 5.1; U; ja) Presto/2.6.30 Version/10.63',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0']

    @staticmethod
    def request(url, method=None, proxy=None, data=None, headers=None, encoding=None, timeout=15):
        """
        通过HTTP协议和给定参数进行下载
        :param method:  请求方法: GET, POST
        :param url: 下载的目标URL地址。
        :param proxy: 代理信息。例如：58.60.192.221:8080
        :param data: 基于HTTP协议要上传的数据，例如网页里的表单数据，字典格式。{"username":"xiaowang", "password":"123456"}
        :param headers: 要发送的HTTP头信息。例如{"cookie":"daefdljsldjlaj"}
        :param encoding: 目标网页的编码信息。一般不用设置，程序会自动检测。
        :param timeout: 下载超时设定，默认是30秒。
        :param user_agent_type: 下载选择的user_gents类型：wap or pc，默认pc
        :return: 下载的网页源码
        """
        # method
        if method == "GET":
            url = HttpRequest.build_url(url, data)
            data = None

        # setup proxy
        opener = urllib2.build_opener()
        if proxy:
            if url.lower().startswith('https://'):
                opener.add_handler(urllib2.ProxyHandler({'https': proxy}))
            else:
                opener.add_handler(urllib2.ProxyHandler({'http': proxy}))

        # setup headers
        headers = headers or {}
        for key, value in HttpRequest.default_headers.items():
            if key not in headers:
                if key == "Referer":
                    value = url
                headers[key] = value
        headers["User-agent"] = random.choice(HttpRequest.user_agents)

        # downloader
        http_response = HttpResponse()
        http_response.url = url
        try:
            request = urllib2.Request(url, data, headers)
            with contextlib.closing(opener.open(request, timeout=timeout)) as response:
                html = response.read()
                if response.headers.get('content-encoding') == 'gzip':
                    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
                if encoding:
                    html = html.decode(encoding, 'ignore')
                else:
                    html = HtmlCoder.html_to_unicode(html)
            http_response.content = html
            http_response.status = response.code
            http_response.message = response.msg
            http_response.headers = response.headers.dict
        except urllib2.HTTPError, e:
            http_response.status = e.code
            http_response.message =  e.msg
        except urllib2.URLError, e:
            http_response.status = 400
            http_response.message = str(e.reason)
        except socket.timeout, e:
            http_response.status = 504
            http_response.message = e.message
        except Exception, e:
            http_response.status = 500
            http_response.message = e.message
        return http_response

    @staticmethod
    def build_url(base_url, params):
        if params:
            url = base_url + "?"
            for key in params:
                url += ("%s=%s&" % (key, params[key]))
            return url[:-1]
        else:
            return base_url


if __name__ == "__main__":
    pass
    # url = "http://www.sogou.com/z/q3003583072.htm?sw=%E7%A9%BA%E8%B0%83&ch=new.w.search.9&"
    # headers = {"Referer": "http://wenwen.sogou.com/s/?w=%E7%A9%BA%E8%B0%83&pg=0&ch=sp.pt"}
    # http_response = HttpRequest.request(url, headers=headers)
    # headers = {"Referer": "http://wenwen.sogou.com/s/?w=%E7%A9%BA%E8%B0%83&pg=0&ch=sp.pt"}
    http_response = HttpRequest.request("http://www.google.com")
    print http_response.content
    print http_response.status
    print http_response.message
    print http_response.headers
