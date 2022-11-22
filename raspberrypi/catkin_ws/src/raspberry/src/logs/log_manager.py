#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from select import select
from time import time
from multiprocessing import Process, Pipe, Lock
from common.metaclass import Singleton

from logs.utils.types import *
from logs.utils.colors import *
from logs.utils.worker import *

class LogManager(metaclass=Singleton):
    """
    LogManager Singleton Purpose

    Usage:
        from logs.log_manager import *

        log = LogManager()
        log.start()

        logger = log.getlogger("WheeledBase", Logger.WRITE, DEBUG)
        logger2 = log.getlogger("Sensors", Logger.BOTH, DEBUG)

        logger(DEBUG, "hello")
        logger2(INFO, "World", x=1)

        sleep(2)
        log.stop()
    """
    #Worker Command
    INIT        = 0
    WRITE_LOG   = 1

    #Execution parameter
    SHOW    = 0
    WRITE   = 1
    BOTH    = 2

    def __init__(self):
        """
        Instanciate worker at the singleton creation
        """
        # Instantiate LogWorker
        self.worker = LogWorker()
        # Initial log time
        self.initial_time = time()

        # Lock
        self.lock = Lock()

    def initLogger(self, name, exec_param, level_disp):
        """
        Send Init command to the Worker Process on the specific logger proxy creation
        """
        if self._check_pid():
            self.__send(LogCommand(self.INIT, LogInit(name, exec_param, level_disp)))
        else:
            pass

    def writeLog(self, level, name, *args, **kwargs):
        """
        Send Write command to the Worker Process with the specific logger message
        """
        if self._check_pid():
            t = str("[{0:.3g}]".format(time() - self.initial_time))
            self.__send(LogCommand(self.WRITE_LOG, LogMsg(t, level, name, args, kwargs)))

    def reset_time(self):
        """
        Reset Time
        """
        if self._check_pid():
            self.initial_time = time()
        else:
            pass

    def getlogger(self, name, exec_param=SHOW, level_disp=CRITICAL):
        """
        Creating one Logger proxy running
            exec_param : SHOW, WRITE or BOTH
            level_disp : DEBUG, INFO, WARNING, ERROR, CRITICAL
        """
        if not self._check_pid():
            self.lock.acquire()
            print(colorise('---------------------------------------------------------------------------',color=Colors.RED))
            print(colorise('('+name+') WARNING : LogWorker is not running, no log will be saved !',color=Colors.RED,car_attr=Colors.BOLD))
            print(colorise('Try to Use :\n\r\tlog.start()',color=Colors.YELLOW))
            print(colorise('At the begginning of your app if you want to store logs',color=Colors.YELLOW))
            print(colorise('---------------------------------------------------------------------------',color=Colors.RED))
            self.lock.release()
        return Logger(self, name, exec_param, level_disp)

    def start(self):
        """
        Start Worker Process
        """
        try:
            self.worker.start()
        except:
            pass

    def stop(self):
        """
        Stop Worker Process
        """
        try:
            self.worker.terminate()
        except:
            pass

    def _check_pid(self):
        """
        Check For the existence of a unix pid. 
        """
        try:
            if self.worker.pid is not None:
                os.kill(self.worker.pid, 0)
            else:
                return False
        except OSError:
            return False
        else:
            return True

    # send pipe message
    def __send(self, obj):
        """
        Private send funtion
        """
        self.worker.pipe.child.send(obj)


class Logger:
    """
    Logger Purpose
    """
    #Execution parameter
    SHOW    = 0
    WRITE   = 1
    BOTH    = 2

    def __init__(self, parent, name, exec_param, level_disp):
        """
        Init the logger proxy
        """
        if not isinstance(parent, LogManager):
            raise RuntimeError("Logger needs to be created with LogManager Parent")
        self.parent = parent
        self.name = name

        self.exec_param = exec_param
        self.level_disp = level_disp

        self.parent.initLogger(self.name, self.exec_param, self.level_disp)

    def __call__(self, level , *args, **kwargs):
        """
        call write
        """
        self.write(level, *args, **kwargs)

    def write(self, level, *args, **kwargs):
        """
        send write command with desired message to the server
        """
        self.parent.writeLog(level, self.name, *args, **kwargs)

    def reset_time(self):
        """
        Reset Parent Time
        """
        self.parent.reset_time()

if __name__ == "__main__":
    def f(name):
        loggerf = LogManager().getlogger('f')
        for i in range(0,1000):
            loggerf(CRITICAL, 'hello', name)

    def g(name):
        loggerg = LogManager().getlogger('g')
        for i in range(0,1000):
            loggerg(CRITICAL, 'hello', name)

    LogManager().start()
    p = Process(target=f, args=('bob',))
    q = Process(target=g, args=('world',))
    p.start()
    q.start()
    p.join()
    q.join()

    input()
