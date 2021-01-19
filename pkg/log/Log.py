#!/usr/bin/env python
# encoding: utf-8

# @software: PyCharm
# @author: NightmareRevisited
# @file: Log.py
# @time: 2021/1/13 15:10
from pkg.classControl.Singleton import Singleton

try:
    from Queue import Queue
except ImportError:
    from queue import Queue
from threading import Thread, Semaphore
import sys
import time


class Log(Singleton):
    def __init__(self):
        self._stdoutQueue = Queue()
        self._logQueue = Queue()
        self._errorQueue = Queue()
        self._logHandler = []
        self._errorHandler = []
        self._prepare2Exit = False
        self._run()

    def log(self, *logData):
        logData = map(lambda x: str(x), logData)
        self._logQueue.put("\t".join(logData))

    def error(self, *erroLog):
        erroLog = map(lambda x: str(x), erroLog)
        self._errorQueue.put("\t".join(erroLog))

    def registLog(self, ioWriter):
        self._logHandler.append(ioWriter)

    def registErrorLog(self, ioWriter):
        self._errorHandler.append(ioWriter)

    def _run(self):
        def log():
            while True:
                logData = self._logQueue.get(block=True)
                self._stdoutQueue.put(logData)
                for ioWriter in self._logHandler:
                    ioWriter.write(logData + "\n")
                if self._prepare2Exit and self._logQueue.qsize() == 0:
                    self._logExitSema.release()
                    break

        self._logThread = Thread(target=log, name="LogThread")
        self._logThread.setDaemon(True)
        self._logThread.start()

        def error():
            while True:
                errorData = self._errorQueue.get(block=True)
                self._stdoutQueue.put(errorData)
                for ioWriter in self._errorHandler:
                    ioWriter.write(errorData + "\n")
                if self._prepare2Exit and self._errorQueue.qsize() == 0:
                    self._errorExitSema.release()
                    break

        self._errorThread = Thread(target=error, name="ErrorLogThread")
        self._errorThread.setDaemon(True)
        self._errorThread.start()

        def stdout():
            while True:
                output = self._stdoutQueue.get(block=True)
                sys.stdout.write("%s: %s \n" % (time.ctime(), output))

        self._stdoutThread = Thread(target=stdout, name="stdoutThread")
        self._stdoutThread.setDaemon(True)
        self._stdoutThread.start()

    def exit(self):
        self._prepare2Exit = True
        self._logExitSema = Semaphore(0)
        self._errorExitSema = Semaphore(0)
        self.log("Exit 0", time.ctime())
        self.error("Exit 0", time.ctime())
        self._logExitSema.acquire()
        self._errorExitSema.acquire()
