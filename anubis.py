#!/usr/bin/env python
# -*- coding:utf-8 -*-

# @author: NightmareRevisited
# @project: UnderCurrent
# @file: cli
# @time: 2019/4/28 9:19
# @Software: PyCharm

from __future__ import print_function
from internal.Controller import AnubisController

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    AnubisController().run()
