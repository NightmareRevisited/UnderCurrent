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
from pkg.thread.ThreadPool import ThreadPool
from pkg.plugin.PluginManager import PluginManager
from internal.graph.Graph import Graph
import time


class Anubis(AnubisRoot):

    def __init__(self, controller):
        '''
        初始化
        :param AnubisController controller:
        '''
        self.controller = controller
        self.params = controller.TaskParam
        self.nodes = []
        self.exitCode = 0
        self.finishedNode = 0
        self.startTime = time.ctime()
        self.startTimeStamp = time.time()
        self.errornode = []
        self.threadPool = ThreadPool(controller.ThreadNum)
        self.graph = Graph()
        self.load_config()
        self.checkSomething()

    def load_config(self):
        if self.controller.ConfFile:
            with open(self.controller.ConfFile, 'r') as f:
                config = json.load(f)
                self.taskName = config['name']
        else:
            self.taskName = self.controller.TaskName
            KEY = self.controller.Key
            config = loadConfig(self.taskName, KEY)
        self.registParam(config['params'])
        self.name = config['name']
        self.desc = config['desc']
        self.plugins = config.get("plugins", [])
        self.rootNode = []
        for nodeInfo in config['nodes']:
            self.nodes.append(Node(self, nodeInfo))
        self.semaphore = Semaphore(max(0, 1 - len(self.nodes)))
        self.registPlugin()

    def registPlugin(self):
        self.pluginManager = PluginManager()
        for pName, kwargs in self.plugins:
            self.pluginManager.registPlugin(pName, kwargs)

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
        else:
            raise AnubisError("Invalid Param Type: " + type)

    def runNode(self, node):
        try:
            node.runNode()
        except Exception as e:
            self.errornode.append(node.id)
            self.exitCode = 1  # 异常码暂定1
            ErrorStack().add(e)
        self.semaphore.release()

    def prepareNode(self, node):
        if not node.preposition.acquire(False):
            self.submitNode(node)

    def submitNode(self, node):
        self.threadPool.submit(self.runNode, (node,))

    def run(self):
        try:
            self.pluginManager.beforeRun()
        except:
            return 1
        Log().log("@@@@@@@@@@@@@ %s 任务开始 @@@@@@@@@@@@@@@@@@" % self.taskName)

        for node in self.rootNode:
            self.submitNode(node)

        return self.finish()

    def finish(self):
        for i in range(len(self.nodes)):
            self.semaphore.acquire()
        self.endTime = time.ctime()
        if len(ErrorStack()) > 0:
            ErrorStack().logError()

        Log().log("""
################################
TaskName:  %s
TaskDesc:  %s
StartTime: %s
CostTime:  %.2f
FinishedStatus:   %d/%d
ErrorNode: %s
################################
""" % (self.taskName, self.desc, self.startTime, time.time() - self.startTimeStamp, self.finishedNode, len(self.nodes),
       " ".join(self.errornode)))
        try:
            self.pluginManager.afterRun()
        except:
            return 1
        return self.exitCode

    def checkSomething(self):
        hasCircle, circlePoint = self.graph.hasCircle()
        if hasCircle:
            raise AnubisError("节点关系中有环存在，请检查配置文件，成环节点[ %s ]" % ','.join(circlePoint))
