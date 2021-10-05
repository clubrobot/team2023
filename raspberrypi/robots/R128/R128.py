#!/usr/bin/python3
# -*- coding: utf-8 -*-

from robots.R128.setup_128 import *
from behaviours.robot_behaviour import RobotBehavior
from behaviours.avoidance_behaviour import AviodanceBehaviour
from robots.R128.actions.take_cup_action import TakeCup
import traceback
from math import pi

COLOR = RobotBehavior.BLUE_SIDE
PREPARATION = False


class R128(RobotBehavior):
    def __init__(self, manager, *args, timelimit=None, **kwargs):
        RobotBehavior.__init__(self, manager, *args,
                               timelimit=timelimit, **kwargs)

        self.avoidance_behaviour = AviodanceBehaviour(
            wheeledbase, roadmap, robot_beacon)

        self.wheeledbase = wheeledbase

        take1 = TakeCup(geogebra, 1)
        take2 = TakeCup(geogebra, 2)
        take3 = TakeCup(geogebra, 3)
        take4 = TakeCup(geogebra, 4)
        take5 = TakeCup(geogebra, 5)

        self.automate = [
            take5,
            take1,
            take2,
            take3,
            take4,
            take5,
            take1,
            take2,
            take3,
            take4,
            take5,
            take1,
            take2,
            take3,
            take4,
        ]

        self.automatestep = 0

    def make_decision(self):
        if(self.automatestep < len(self.automate)):
            action = self.automate[self.automatestep]
        else:
            return None, (self,), {}, (None, None)
            self.stop_event.set()

        return action.procedure, (self,), {}, (action.actionpoint + (action.orientation,), (action.actionpoint_precision, None))

    def goto_procedure(self, destination, thresholds=(None, None)):
        if self.avoidance_behaviour.move(destination, thresholds):
            self.automatestep += 1
            return True
        else:
            return False

    def set_side(self, side):
        pass

    def set_position(self):
        wheeledbase.set_position(*geogebra.get('StartBlue'), pi/2)

    def positioning(self):
        pass


if __name__ == '__main__':
    if PREPARATION:
        R128().start_preparation()
    else:
        robot = R128(manager, timelimit=100)
        robot.set_side(COLOR)
        init_robot()
        robot.set_position()
        input()
        robot.start()
