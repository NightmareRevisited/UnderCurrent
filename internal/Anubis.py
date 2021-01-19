#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Anubis.py
# @time: 2021/1/13 14:05
import re

from internal.base.AnubisRoot import AnubisRoot
from internal.configs.Config import *
from internal.node.Node import Node
from threading import Semaphore, Thread
from internal.exception.ErrorStack import ErrorStack
from pkg.log.Log import Log
import time


class Anubis(AnubisRoot):
    def __init__(self, taskName, param):
        '''
        初始化
        :param str taskName:
        :param dict param:
        '''
        self.taskName = taskName
        self.params = param
        self.nodes = []
        self.startTime = time.ctime()
        self.startTimeStamp = time.time()

        self.load_config()

    def load_config(self):
        PARAM_KEY = getKey(self.taskName)
        KEY = self.params[PARAM_KEY]
        config = loadConfig(self.taskName, KEY)
        self.registParam(config['params'])
        self.name = config['name']
        self.desc = config['desc']
        self.plugins = config.get("plugins", [])
        for nodeInfo in config['nodes']:
            self.nodes.append(Node(self.taskName, nodeInfo, self.params))
        self.semaphore = Semaphore(max(0, 1 - len(self.nodes)))

    def registParam(self, paramDefine):
        '''
        注册参数
        :param dict paramDefine:
        :return:
        '''
        p = {}
        for pName, define in paramDefine.items():
            if "default" in define:
                p[pName] = self.checkParam(self.params.get(pName, define['default']), define['type'])
            else:
                p[pName] = self.checkParam(self.params[pName], define['type'])
        self.params = p

    def checkParam(self, value, type):
        if type == "string":
            return str(value)
        elif type == "int":
            return int(value)
        elif type == "float":
            return float(value)
        elif type == "list":
            return list(json.loads(value))
        elif type == "dict":
            return json.loads(value)

    def run(self):
        def runNode(node):
            try:
                node.run()
            except Exception as e:
                ErrorStack().add(e)
            self.semaphore.release()

        for node in self.nodes:
            t = Thread(target=runNode, args=[node])
            t.start()
        self.finish()

    def finish(self):
        for i in range(len(self.nodes)):
            self.semaphore.acquire()
        self.endTime = time.ctime()
        if len(ErrorStack()) > 0:
            ErrorStack().logError()
            Log().error(self.taskName, self.name, self.desc, self.startTime, time.ctime())
        else:
            Log().log(self.taskName, self.name, self.desc, self.startTime, time.time() - self.startTimeStamp)
        Log().exit()
