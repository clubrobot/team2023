#!/usr/bin/env python3
# coding: utf-8

from threading import Thread, Event
from time import sleep
from math import hypot

from common.sync_flag_signal import Signal, Flag
from common.tcptalks import NotConnectedError


class PositionListener(Thread):
    BROTHER = 0
    OPPONENTA = 1
    OPPONENTB = 2

    def __init__(self, brother_getter, opponents_getter, timestep=0.5, threshold=10):
        Thread.__init__(self)
        self.daemon = True

        # Robots list
        self.robots_list = [self.BROTHER, self.OPPONENTA, self.OPPONENTB]

        # Signals for each robots
        self.__setattr__("signal"+str(self.BROTHER), Signal())
        self.__setattr__("signal"+str(self.OPPONENTA), Signal())
        self.__setattr__("signal"+str(self.OPPONENTB), Signal())

        # Brother and opponents getter
        self.__setattr__("getter"+str(self.BROTHER), brother_getter)
        self.__setattr__("getter"+str(self.OPPONENTA),
                         lambda: opponents_getter()[0])
        self.__setattr__("getter"+str(self.OPPONENTB),
                         lambda: opponents_getter()[1])

        self.__setattr__("position"+str(self.BROTHER), (-1000, -1000))
        self.__setattr__("position"+str(self.OPPONENTA), (-1000, -1000))
        self.__setattr__("position"+str(self.OPPONENTB), (-1000, -1000))

        # Timestep
        self.timestep = timestep

        # Stopping event
        self.stop = Event()

        # Position threshold
        self.threshold = threshold

        # Position error
        self.error = 0

        self.pos = (-1000, -1000)

        # Atomatically start
        self.start()

    def bind(self, idx, func):
        self.__setattr__("flag"+str(idx), Flag(func))
        self.__getattribute__(
            "flag"+str(idx)).bind(self.__getattribute__("signal"+str(idx)))

    def get_position(self, idx):
        return self.__getattribute__("position"+str(idx))

    def _handle_position(self, idx):
        try:
            self.pos = self.__getattribute__("getter"+str(idx))()
        except:
            pass

        x, y = self.pos[:2]
        if (hypot(y - self.__getattribute__("position"+str(idx))[1], x - self.__getattribute__("position"+str(idx))[0]) + self.error) > self.threshold:
            self.__getattribute__("signal"+str(idx)).ping()

            self.error = 0
        else:
            self.error += hypot(y - self.__getattribute__("position"+str(idx))
                                [1], x - self.__getattribute__("position"+str(idx))[0])

        self.__setattr__("position"+str(idx), (x, y))

    def run(self):
        while not self.stop.is_set():
            # handle brother pos
            for robot in self.robots_list:
                try:
                    self._handle_position(robot)
                except NotConnectedError:
                    pass

            sleep(self.timestep)


if __name__ == "__main__":

    p = PositionListener(lambda: (-1000, -1000),
                         lambda: [(-2000, -1000), (-3000, -1000)])
