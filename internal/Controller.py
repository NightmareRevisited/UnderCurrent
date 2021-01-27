#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Controller.py
# @time: 2021/1/27 11:54

from internal.base.AnubisRoot import AnubisRoot
from .Anubis import Anubis
from internal.exception.AnubisError import AnubisError
import internal.consts as Const
import sys

from pkg.log.Log import Log


class AnubisController(AnubisRoot):
    LOG_PATH = Const.LOG_PATH
    ERROR_LOG_PATH = Const.ERRORLOG_PATH
    TaskName = ""
    ConfFile = ""
    TaskParam = {}

    helpInfo = u"""
-h 查看参数帮助
-c 指定配置文件，与-t为互斥参数
-l 指定log文件
-e 指定errorlog文件
-t 指定task名称，与-c为互斥参数
-p job需要参数 以name=value的形式传入,多个参数以空格隔开
"""

    def __init__(self):
        self.registParam()
        self.registLogger()

    def registParam(self):
        i = 1
        while i < len(sys.argv):
            argv = sys.argv[i]
            if argv[0] != '-':
                raise AnubisError("Invalid Input",argv)
            if argv[1:] == "h":
                print(self.helpInfo)
                exit(0)
            elif argv[1:] == "c":
                self.ConfFile = sys.argv[i + 1]
                i += 1
            elif argv[1:] == "l":
                self.LOG_PATH = sys.argv[i + 1]
                i += 1
            elif argv[1:] == "e":
                self.ERROR_LOG_PATH = sys.argv[i + 1]
                i += 1
            elif argv[1:] == "t":
                self.TaskName = sys.argv[i + 1]
                i += 1
            elif argv[1:] == "p":
                self.TaskParam = {i[0]: i[1] for i in map(lambda x: x.split('='), sys.argv[i + 1:]) if i[1]}
                return
            else:
                raise AnubisError("Invalid Choice %s" % argv[1:])
            i += 1

    def registLogger(self):
        Log().registLog(open(self.LOG_PATH, 'a'))
        Log().registErrorLog(open(self.ERROR_LOG_PATH, 'a'))

    def run(self):
        Anubis(self).run()
