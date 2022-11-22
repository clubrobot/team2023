#!/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep
from math import pi

from behaviours.action.action import *
from behaviours.robot_behaviour import RobotBehavior
from logs.log_manager import *


class PushCupAction(Action):
    def __init__(self, geo, color, idx):

        self.logger = LogManager().getlogger(self.__class__.__name__, Logger.SHOW, INFO)

        self.color = color
        self.idx = idx

        if self.color == RobotBehavior.YELLOW_SIDE:
            self.actionpoint = geo.get('PushYellow'+str(self.idx))
            if self.idx == 1 or self.idx == 2:
                self.orientation = pi/2
            else:
                self.orientation = pi
        else:
            self.actionpoint = geo.get('PushBlue'+str(self.idx))
            if self.idx == 1 or self.idx == 2:
                self.orientation = -pi/2
            else:
                self.orientation = pi

        self.actionpoint_precision = 10

    def procedure(self, robot):
        self.logger(INFO, 'Action is launch on', robot.__class__.__name__)
        self.logger(INFO, 'Go to Push action '+str(self.idx))

        robot.wheeledbase.turnonthespot(self.orientation)
        robot.wheeledbase.wait()

        x_in, y_in, theta_in = robot.wheeledbase.get_position()

        if self.color == RobotBehavior.YELLOW_SIDE:
            if self.idx == 1 or self.idx == 2:
                x_sp, y_sp, theta_sp = x_in, y_in + 250, theta_in
            else:
                x_sp, y_sp, theta_sp = x_in + 250, y_in, theta_in
        else:
            if self.idx == 1 or self.idx == 2:
                x_sp, y_sp, theta_sp = x_in, y_in - 250, theta_in
            else:
                x_sp, y_sp, theta_sp = x_in + 250, y_in, theta_in

        # # Deploy arm
        # sleep(1)

        robot.wheeledbase.goto(x_sp, y_sp, theta_sp)
        robot.wheeledbase.wait()

        robot.wheeledbase.goto(x_in, y_in, theta_in)
        robot.wheeledbase.wait()

        # UnDeploy arm
        # sleep(1)
