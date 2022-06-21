# -*- coding:utf-8 -*-


# @version: 1.0
# @author:
# @date: '14-4-10'


import urllib2
from urllib2 import URLError as URLError
import random
import contextlib
import StringIO
import gzip

from utilspy.log.logger import Logger
from utilspy.web.http.html_coder import HtmlCoder


class HttpDownloader(object):

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
            'Opera/9.80 (Windows NT 5.1; U; ja) Presto/2.6.30 Version/10.63']


    @staticmethod
    def download(url, proxy=None, data=None, headers=None, encoding=None, retry_times=3, timeout=15):
        """
        通过HTTP协议和给定参数进行下载
        :param url: 下载的目标URL地址。
        :param proxy: 代理信息。例如：58.60.192.221:8080
        :param data: 基于HTTP协议要上传的数据，例如网页里的表单数据，字典格式。{"username":"xiaowang", "password":"123456"}
        :param headers: 要发送的HTTP头信息。例如{"cookie":"daefdljsldjlaj"}
        :param encoding: 目标网页的编码信息。一般不用设置，程序会自动检测。
        :param retry_times: 下载重试次数，默认是3次。
        :param timeout: 下载超时设定，默认是30秒。
        :param user_agent_type: 下载选择的user_gents类型：wap or pc，默认pc
        :return: 下载的网页源码
        """
        if not url:
            Logger.info("downloader url is empty")
            return

        # setup proxy
        opener = urllib2.build_opener()
        if proxy:
            if url.lower().startswith('https://'):
                opener.add_handler(urllib2.ProxyHandler({'https': proxy}))
            else:
                opener.add_handler(urllib2.ProxyHandler({'http': proxy}))

        # setup headers
        headers = headers or {}
        for key, value in HttpDownloader.default_headers.items():
            if key not in headers:
                if key == "Referer":
                    value = url
                headers[key] = value
        headers["User-agent"] = random.choice(HttpDownloader.user_agents)

        # downloader
        html = ""
        for retry_time in range(0, retry_times):
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

            except urllib2.HTTPError, e:
                Logger.info("The target web server is not stable,  has retried %d times,url is %s, proxy is %s,"
                            " errorMessage:%s" % (retry_time + 1, url, proxy, e.message))
                continue
            except URLError, e:
                Logger.info("Retried %d times, proxy is %s, url is %s" % (retry_time + 1, proxy, url))
                continue
            except Exception, e:
                Logger.error("Retried %d times, Download Error %s : %s" % (retry_time + 1, url, e))
                continue
            break
        return html


if __name__ == "__main__":
    pass
