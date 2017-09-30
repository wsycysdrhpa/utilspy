# -*- coding:utf-8 -*-


# @version: 1.0
# @author: daichi
# @date: '14-8-18'
from _mysql_exceptions import OperationalError


def ConnAnnotation(func):
    def _conn_annotation(*args,**kv):
        #必须为MySqlHelper实例
        self = args[0]
        #if not isinstance(self, MySqlHelper):
        #    print('必须为MySqlHelper实例!')
        ret = None
        try:
            ret = func(*args,**kv)
        except Exception as e:
            if isinstance(e, OperationalError):
                #args(2006, 'MySQL server has gone away')
                if 'MySQL server has gone away' in e.args:
                    print('MySQL server has gone away')
                    self.re_open()
                    ret = func(*args, **kv)
                    print("re_open db connection")
                else:
                    print "Error:%s" % e
            else:
                print(e.message)
        return ret
    return _conn_annotation




if __name__ == "__main__":
    pass