#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @update: '2017/7/17'
# @description:


class Test(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    pass
    import os
    import logging

    from utilspy.env.environment import Environment

    LOGGER = logging.getLogger('dual')

    CURRENT_FILE_PATH = os.path.abspath(__file__)

    Environment.get_instance().init(CURRENT_FILE_PATH, 3)

    LOGGER.debug(u'hello')
    LOGGER.info(u'hello')
    LOGGER.warning(u'hello')
    LOGGER.error(u'hello')
    LOGGER.critical(u'hello')
