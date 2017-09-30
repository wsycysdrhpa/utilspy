# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '2016/8/11'


import logging
import logging.config
import os


def project_dir(keyword='README.md', path='.', prevpath=None):
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    file_path = os.path.join(path, keyword)
    if os.path.exists(file_path):
        return path
    return project_dir(keyword, os.path.dirname(path), path)

log_config = "conf/logging.conf"
dir = project_dir(log_config)
logging.config.fileConfig(os.path.join(dir, log_config))

logger = logging.getLogger()

for log in logging.getLogger().manager.loggerDict.values():
    if isinstance(log, logging.Logger):
        handlers = log.handlers
        for handler in handlers:
            if isinstance(handler, logging.FileHandler):
                dir_path = os.path.dirname(handler.baseFilename)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
del log_config
del dir

FIELD_SPLIT = '\x01'

def log_format(*args):
    clean_args = []
    for arg in args:
        if isinstance(arg, unicode):
            clean_args.append(arg.encode("utf8"))
        elif isinstance(arg, str):
            clean_args.append(arg)
        else:
            clean_args.append(str(arg))
    return FIELD_SPLIT.join(clean_args)


if __name__ == "__main__":
    pass