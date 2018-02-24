# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '15-4-14'


import random
import socket
import ssl

import requests

from utilspy.log.logger import Logger
from utilspy.web.http.html_coder import HtmlCoder


class RequestsDownloader():
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
    def download(url, method='GET', proxy=None, data=None, headers=None, encoding=None, retry_times=3, timeout=15):
        """
        通过requests库给定参数进行下载
        @param url: 下载的目标URL地址。
        @param method: requests请求方法，GET or POST，默认是GET
        @param proxy: 代理信息。例如：58.60.192.221:8080
        @param data: 基于HTTP协议要上传的数据，例如网页里的表单数据，字典格式。{"username":"xiaowang", "password":"123456"}
        @param headers: 要发送的HTTP头信息。例如{"cookie":"daefdljsldjlaj"}
        @param encoding: 目标网页的编码信息。一般不用设置，程序会自动检测。
        @param retry_times: 下载重试次数，默认是3次。
        @param timeout: 下载超时设定，默认是30秒。
        @return: 下载的网页源码
        """
        # TODO 增加user_agent_type
        if not url:
            Logger.info("downloader url is empty")
            return

        session = requests.session()
        # set proxy
        if proxy:
            if url.lower().startswith('https://'):
                session.proxies = {"https": "https://" + proxy}
            else:
                session.proxies = {"http": "http://" + proxy}
        else:
            session.proxies = {}

        # set headers
        headers = headers or {}
        for key, value in RequestsDownloader.default_headers.items():
            if key not in headers:
                if key == "Referer":
                    value = url
                headers[key] = value
        headers["User-agent"] = random.choice(RequestsDownloader.user_agents)

        #downloader
        html = ""
        for retry_time in range(0, retry_times):
            try:
                if method == 'GET':
                    response = session.get(
                        url, data=data, headers=headers, timeout=timeout)
                else:
                    response = session.post(
                        url, data=data, headers=headers, timeout=timeout)
                # response.encoding = encoding
                html = response.content
                #if response.headers.get('content-encoding') == 'gzip':
                #    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
                if encoding:
                    html = html.decode(encoding, 'ignore')
                else:
                    html = HtmlCoder.html_to_unicode(html)
            except (socket.timeout, requests.RequestException, ssl.SSLError), e:
                Logger.error("Retried %d times, proxy is %s, url is %s, error_message:%s" %
                             (retry_time + 1, proxy, url, e.message))
                continue
            except Exception, e:
                Logger.error("Retried %d times, proxy is %s, url is %s, error_message:%s" %
                             (retry_time + 1, proxy, url, e.message))
                continue
            break
        return html


if __name__ == "__main__":
    pass
    url = "http://weibo.cn/1785216975/follow?page=16"
    headers = None
    cookie = "_T_WM=a804b16a055815d93078321d74f1dff8;gsid_CTandWM=4uebe7771H7ML1GX8PBcqm0cR8W;SUB=_2A254DI3KDeTxGeNM71YR8S3JzjiIHXVbDhOCrDV6PUJbvNBeLUjukW1gq_Ru7ZwtxD5sFuMH9ilTseokMA..;"
    headers = {"cookie": cookie}
    html = RequestsDownloader.download(url, headers=headers)
