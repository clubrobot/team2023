#!/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep
from math import pi

from behaviours.action.action import *
from logs.log_manager import *

class TakeCup(Action):
    def __init__(self, geo, idx):

        self.logger = LogManager().getlogger(self.__class__.__name__, Logger.SHOW, INFO)

        self.idx = idx
        self.actionpoint = geo.get('Cup'+str(self.idx))
        self.orientation = pi
        self.actionpoint_precision = 10

    def procedure(self, robot):
        self.logger(INFO, 'Action is launch on', robot.__class__.__name__)
        self.logger(INFO, 'Taking Cup number ', self.idx)

        robot.wheeledbase.turnonthespot(pi)
        robot.wheeledbase.wait()
        sleep(3)

