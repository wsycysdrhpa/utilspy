# -*- coding:utf-8 -*-


# @version: 1.0
# @author: daichi
# @date: '14-7-31'
from yzs_utils.logger import Logger


def logAnnotation(log_str):
    def _logAnnotation_deco(func):
        def __logAnnotation_deco(*a):
            ret = func(*a)
            ret_str = ''
            if isinstance(ret, list):
                if isinstance(ret[0], list):
                    for feild in ret:
                        ret_str += '\t'.join(feild) + '\t'
                else:
                    ret_str = '\t'.join(ret)
            else:
                ret_str = ret
            Logger.info(log_str + " result: " + str(ret_str))
            return ret
        return __logAnnotation_deco
    return _logAnnotation_deco

@logAnnotation("log")
def testLog():
    print "test"


if __name__ == "__main__":
    testLog()