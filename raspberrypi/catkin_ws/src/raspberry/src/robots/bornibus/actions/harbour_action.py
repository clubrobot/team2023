#!/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep
from math import pi
import random

from behaviours.action.action import *
from behaviours.robot_behaviour import RobotBehavior
from logs.log_manager import *


class Harbour(Action):
    NORTH = 0
    SOUTH = 1
    def __init__(self, geo, color):

        self.logger = LogManager().getlogger(self.__class__.__name__, Logger.SHOW, INFO)
        self.color = color

        self.destination = random.randint(self.NORTH, self.SOUTH)

        if color == RobotBehavior.YELLOW_SIDE:
            north = 'NorthYellow'
            south = 'SouthYellow'
            self.orientation = pi
        else:
            north = 'NorthBlue'
            south = 'SouthBlue'
            self.orientation = -pi

        if self.destination == self.NORTH:
            self.actionpoint = geo.get(north)

            self.actionpoint_precision = 10
        else:
            self.actionpoint = geo.get(south)

            self.actionpoint_precision = 10

        self.logger(INFO, 'Final Harbour is : ', {
                    0: 'North', 1: 'South'}[self.destination])

    def procedure(self, robot):
        self.logger(INFO, 'Action is launch on', robot.__class__.__name__)
