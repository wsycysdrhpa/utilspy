#-*- coding: utf8 -*-


import random
import requests

from utilspy.log.logger import Logger


class ProxyManager(object):
    def __init__(self):
        self._proxy_cach = []
        pass

    def get_proxy_cach(self):
        response = requests.get("http://10.10.10.114:8090/proxy-service/?c=1000&d=1&l=0")
        if response.status_code == 200:
            return [proxy.split(",")[0] for proxy in response.text.split(";")]
        else:
            Logger.info("get proxy wrong")

    def get_a_proxy(self):
        if self._proxy_cach:
            return self._proxy_cach[random.randint(0, len(self._proxy_cach)-1)]
        else:
            self._proxy_cach = self.get_proxy_cach()
            return self._proxy_cach[random.randint(0, len(self._proxy_cach)-1)]


if __name__ == "__main__":
    pass
