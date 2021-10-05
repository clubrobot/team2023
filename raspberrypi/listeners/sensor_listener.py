#!/usr/bin/env python3
# coding: utf-8

from threading import Thread, Event
from time import sleep
from math import hypot

from common.sync_flag_signal import Signal, Flag


class SensorListener(Thread):

    LEFT = 0
    MID_LEFT = 1
    MID_RIGHT = 3
    RIGHT = 4

    def __init__(self, left_getter, mid_left_getter, mid_right_getter, right_getter, timestep=0.1, threshold=220):
        Thread.__init__(self)
        self.daemon = True

        # Sensors list
        self.sensors_list = [self.LEFT,
                             self.MID_LEFT, self.MID_RIGHT, self.RIGHT]

        # Signals for each sensors
        self.__setattr__("signal"+str(self.LEFT), Signal())
        self.__setattr__("signal"+str(self.MID_LEFT), Signal())
        self.__setattr__("signal"+str(self.MID_RIGHT), Signal())
        self.__setattr__("signal"+str(self.RIGHT), Signal())

        # Sensors getter
        self.__setattr__("getter"+str(self.LEFT), left_getter)
        self.__setattr__("getter"+str(self.MID_LEFT), mid_left_getter)
        self.__setattr__("getter"+str(self.MID_RIGHT), mid_right_getter)
        self.__setattr__("getter"+str(self.RIGHT), right_getter)

        # Timestep
        self.timestep = timestep

        # Stopping event
        self.stop = Event()

        # Position threshold
        self.threshold = threshold

        # Atomatically start
        self.start()

    def bind(self, idx, func):
        self.__setattr__("flag"+str(idx), Flag(func))
        self.__getattribute__(
            "flag"+str(idx)).bind(self.__getattribute__("signal"+str(idx)))

    def _handle_sensor(self, idx):
        try:
            a, b = self.__getattribute__("getter"+str(idx))()
        except TimeoutError:
            pass

        if a < self.threshold or b < self.threshold:
            self.__getattribute__("signal"+str(idx)).ping()

    def run(self):
        while not self.stop.is_set():
            # Handle each sensors
            for sensor in self.sensors_list:
                self._handle_sensor(sensor)

            sleep(self.timestep)


if __name__ == "__main__":

    s = SensorListener(lambda: (1000, 1000), lambda: (500, 500),
                       lambda: (200, 200), lambda: (100, 100))
