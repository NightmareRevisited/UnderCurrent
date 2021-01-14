#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: __init__.py
# @time: 2021/1/13 16:51
import os
import sys


def runCommand(cmd, ignore=False):
    if sys.platform == "win32":
        return runWindowsCommand(cmd, ignore)
    else:
        return runLinuxCommand(cmd, ignore)


def runWindowsCommand(cmd, ignore):
    execute = os.popen(cmd, "r")
    output = execute.read()
    status = execute.close()
    status = status if status else 0
    if ignore:
        status = 0
    return output, status


def runLinuxCommand(cmd, ignore):
    pipe = os.popen('{ ' + cmd + '; } 2>&1', 'r')
    text = pipe.read()
    sts = pipe.close()
    if sts is None: sts = 0
    if text[-1:] == '\n': text = text[:-1]
    if ignore:
        sts = 0
    return text, sts
