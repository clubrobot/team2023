#!/usr/bin/env python3
#-*- coding: utf-8 -*-

class Action:
    """
        The purpose of this class is to define action object body
    """
    def procedure(self, robot):
        """
            The procedure method give the robot comportement to successfully acheive this action
        """
        raise RuntimeError("The 'procedure' method must be overriden")

if __name__ == "__main__":

    from math import pi

    class TakeCup(Action):
        def __init__(self, side):
            self.side = side
            self.action_point = (555, 666)# geogebra.get('Point name')
            self.orientation = pi
            self.actionpoint_precision = 10

        def procedure(self, robot):
            print(robot)


    take = TakeCup(0)

    print(take.side)
    print(take.action_point)
    print(take.orientation)