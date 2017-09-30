# -*- coding:utf-8 -*-


# @version: 1.0
# @author: daichi
# @date: '14-11-3'


def singleton(cls):
    '''
		对类的单例装饰器
	'''
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton
