#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Test(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    pass
    import sys

    from dotenv import load_dotenv
    import project_root_finder

    CURRENT_PROJECT_PATH = project_root_finder.root.as_posix()
    sys.path.append(CURRENT_PROJECT_PATH)

    load_dotenv()
