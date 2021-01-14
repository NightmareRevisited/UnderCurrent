#!/usr/bin/env python
# -*- coding:utf-8 -*-

# @author: NightmareRevisited
# @project: UnderCurrent
# @file: cli
# @time: 2019/4/28 9:19
# @Software: PyCharm

from __future__ import print_function
from internal.consts import LOG_PATH, ERRORLOG_PATH
from internal.Anubis import Anubis
from pkg.log.Log import Log

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    param_dict = {i[0]: i[1] for i in map(lambda x: x.split('='), sys.argv[1:]) if i[1]}
    taskName = param_dict.get("task")
    Log().registLog(open(LOG_PATH, 'a'))
    Log().registErrorLog(open(ERRORLOG_PATH, 'a'))
    if not taskName:
        raise NameError("TaskName missed!")
    Anubis(taskName, param_dict).run()
