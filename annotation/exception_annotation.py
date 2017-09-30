# -*- coding:utf-8 -*-


# @version: 1.0
# @author: daichi
# @date: '14-10-23'


#-*- coding: utf8 -*-
__author__ = 'lianghuibin'
def  exceptionReturnEmpty(fun):
    def __deco(*a):
        try:
            re=fun(*a)
            if isinstance(re,unicode):
                re=re.strip()
                re=re.encode("utf8")
            if re == 0:
                return 0
            if re:
                return re
            else:
                return ""
        except Exception as e:
            print e.message
            return None
    return __deco

def  exceptionReturnFalse(fun):
    def __deco(*a):
        try:
            re=fun(*a)
            if isinstance(re,bool):
                return re
            else:
                return False
        except Exception,e:
            print e.message
            return False
    return __deco
