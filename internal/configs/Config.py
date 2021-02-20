#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: ConfigManager.py
# @time: 2021/1/8 15:08

import os
import json
from internal.exception.AnubisError import AnubisError
import internal.consts as Const

DEFAULT_NAME = "default"
KEY_FILE_NAME = "KEY"

CONFIG_PATH = None


def getConfigPath():
    '''
    读取配置文件路径
    :return:
    '''
    cPath = os.path.split(os.path.realpath(__file__))[0]
    return os.path.join(cPath, "..", "..", Const.TASK_CUSTOM_BASE, Const.TASK_CUSTOM_CONFIG_BASE)


def getKey(taskName):
    # type: (str) -> str
    cPath = getConfigPath()
    keyFile = os.path.join(cPath, taskName, KEY_FILE_NAME)
    if not os.path.exists(keyFile):
        return Const.DEFAULT_KEY
    with open(keyFile, 'r') as f:
        return f.read()


def loadConfig(taskName, configName=DEFAULT_NAME):
    # type: (str, str) -> dict
    if configName == None:
        configName = DEFAULT_NAME
    cPath = getConfigPath()
    cFile = os.path.join(cPath, taskName, "%s.json" % configName)
    defaultFile = os.path.join(cPath, taskName, "%s.json" % DEFAULT_NAME)
    if not os.path.exists(cFile):
        if not os.path.exists(defaultFile):
            raise AnubisError("Job %s - %s config not found!" % (taskName, configName))
        cFile = defaultFile
    with open(cFile, 'r') as f:
        try:
            return json.load(f)
        except ValueError as e:
            raise AnubisError("Job %s - %s config json error!\nLocation: %s" % (taskName, cFile, e.message))
        except Exception as e:
            raise e
