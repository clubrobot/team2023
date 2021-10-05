#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from select import select
from time import asctime
from multiprocessing import Process, Pipe, Lock
from common.metaclass import Singleton

from logs.utils.types import *
from logs.utils.colors import *


class LogWorker(Process):
    """
    The main purpose of LogWorker is to store and display all the logs recieved from loggers proxy
    It run on an other process to avoid parent process speed reduction.
    """
    # Worker Command
    INIT = 0
    WRITE_LOG = 1

    # Execution parameter
    SHOW = 0
    WRITE = 1
    BOTH = 2

    def __init__(self):
        """
        Init
        """
        Process.__init__(self)

        # Terminate with the main process.
        self.daemon = True

        # Communication pipe.
        self.pipe = PipeType(*Pipe())

        # Lock
        self.lock = Lock()

        # Dict that contain all loggers proxy context.
        self.context = dict()

        # file to store all logs
        self.commonLogFile = None
        self.commonLogFileName = None

        # Folder name
        self.folder = '{}-{}-{}'.format(*asctime().split(" ")[1:4])

    def run(self):
        """
        Process
        """
        # infinite loop
        while True:
            # get the message
            msg = self.__recv()

            # called at logger creation
            if msg is not None and msg.command == self.INIT:
                self.__init(msg)

            # called at each logger write cmd
            elif msg is not None and msg.command == self.WRITE_LOG:
                self.__write(msg)

    def __init(self, msg):
        """
        Called when INIT command is received, it create logger context on the worker
        """
        # if logger doesn't exist
        if not msg.args.name in self.context:
            # create it and store the context
            self.__createContext(msg)

            # if write parameter is set, create file
            if msg.args.exec_param > 0:
                self.__createFolder(self.context[msg.args.name]["folder"])

                self.context[msg.args.name]["file"] = self.__createFile(
                    self.context[msg.args.name]["filename"])

                self.commonLogFile = self.__createFile(self.commonLogFileName)

            else:
                self.context[msg.args.name]["file"] = None

    def __write(self, msg):
        """
        Called when WRITE_LOG command is received, it display and store message on files
        """
        # if logger exist
        if msg.args.name in self.context:
            # if disaly is set

            # if exec_param equals 0 (print only) or 2 (both manner)
            if self.context[msg.args.name]["exec_param"] % 2 == 0:
                # check the desired diplaylog severity
                if msg.args.level.value >= self.context[msg.args.name]["level_disp"]:
                    # show the message
                    self.__showMsg(msg)

            # if write on file is set 1 (write only) or 2 (both manner)
            if self.context[msg.args.name]["exec_param"] > 0:
                # write specific logs
                self.__writeFile(self.context[msg.args.name]["file"], msg)
                self.__writeFile(self.commonLogFile, msg)

    def __showMsg(self, msg):
        """
        Display logs with colorisation on terminal
        """
        print(self.__formatTime(msg.args.time),
              self.__formatName(msg.args.name),
              self.__formatLevel(msg.args.level),
              ':',
              *msg.args.args)

        for key, content in msg.args.kwargs.items():
            print("  •", key, ":", content)

    def __writeFile(self, f, msg):
        """
        Write logs on specific file
        """
        if f is not None:
            f.write(msg.args.time)
            f.write('('+msg.args.name+')')
            f.write(msg.args.level.name)
            f.write(" : ")
            for arg in msg.args.args:
                f.write(" {}".format(str(arg)))

            for key, content in msg.args.kwargs.items():
                f.write("\n\t{} : ".format(str(key))+str(content))

            f.write("\n")
            f.flush()

    def __formatTime(self, time):
        """
        Format time with colorisation
        """
        return colorise(time, car_attr=Colors.BOLD)

    def __formatLevel(self, level):
        """
        Format level with colorisation
        """
        return colorise(level.name, color=level.color)

    def __formatName(self, name):
        """
        Format name with colorisation
        """
        name = '('+name+')'
        return colorise(name, color=Colors.GREY, car_attr=Colors.BOLD)

    def __createContext(self, msg):
        """
        Creating specific logger context
        """
        self.context[msg.args.name] = dict()
        self.context[msg.args.name]["folder"] = self.folder
        self.context[msg.args.name]["filename"] = self.folder + \
            '/'+msg.args.name+'.log'
        self.context[msg.args.name]["exec_param"] = msg.args.exec_param
        self.context[msg.args.name]["level_disp"] = msg.args.level_disp.value

        self.commonLogFileName = self.folder + '/all.log'

    def __createFolder(self, name):
        """
        Creating Folder if doesn't exist
        """
        if not os.path.exists(name):
            try:
                os.mkdir(name)
            except OSError:
                print("Creation of the directory %s failed" % name)

    def __createFile(self, name):
        """
        Creating or open file
        """
        return open(name, "a", newline='\n', encoding="utf-8")

    def __recv(self):
        """
        Blocking recieve that permit to avoid some Pipe polling limitation
        """
        try:
            if select([self.pipe.parent], [], [], None)[0]:
                return self.pipe.parent.recv()
            else:
                return None
        except:
            return None
