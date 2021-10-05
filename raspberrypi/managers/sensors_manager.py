#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from threading import Thread, Event, Lock
import math
from common.sync_flag_signal import Signal
from common.automaton import *

class Sensor:
    HILL_ZONE = ((300, 1490), (200, 2800))
    SCALE_ZONE = ((1150, 1600), (1200, 1800))
    START_ZONE = ((0, 0), (0, 0))

    def __init__(self, wheeledbase, name, dist, pos, angle, connexion_flag):
        self.dist = dist
        self.pos = pos
        self.angle = angle
        self.enabled = True
        self.name = name
        self.wheeledbase = wheeledbase
        self.is_connected = connexion_flag

    def set_side(self, side):
        if side == Automaton.YELLOW:
            self.START_ZONE = ((0, 1200), (0, 500))
            self.SCALE_ZONE = ((1150, 1600), (1480, 1800))
        else:
            self.START_ZONE = ((0, 1200), (2500, 3000))
            self.SCALE_ZONE = ((1150, 1600), (1200, 1520))

    def disable(self):
        self.enabled = False

    def obstacle(self, threshold):
        dist = self.dist()
        if dist > threshold:
            return False
        wheeledbase_pos = self.wheeledbase.get_position_latch()

        x = wheeledbase_pos[0] + self.pos[0]*math.cos(wheeledbase_pos[2]) - self.pos[1]*math.sin(wheeledbase_pos[2]) \
            + math.cos(self.angle+wheeledbase_pos[2])*dist
        y = wheeledbase_pos[1] + self.pos[0]*math.sin(wheeledbase_pos[2]) + self.pos[1]*math.cos(wheeledbase_pos[2]) \
            + math.sin(self.angle+wheeledbase_pos[2])*dist

        # zone pente
        if x < Sensor.HILL_ZONE[0][0] or x > Sensor.HILL_ZONE[0][1] or \
           y < Sensor.HILL_ZONE[1][0] or y > Sensor.HILL_ZONE[1][1]:
            return False

        # zone balance
        if Sensor.SCALE_ZONE[0][0] < x < Sensor.SCALE_ZONE[0][1] and \
           Sensor.SCALE_ZONE[1][0] < y < Sensor.SCALE_ZONE[1][1]:
            return False

        if Sensor.START_ZONE[0][0] < x < Sensor.START_ZONE[0][1] and \
           Sensor.START_ZONE[1][0] < y < Sensor.START_ZONE[1][1]:
            return False

        return True


class SensorsManager(Thread):
    SENSORS_FREQ = 0.2

    def __init__(self, wheeledbase, sensors_front, sensors_back, sensors_lat, threshold=300):
        Thread.__init__(self)
        self.daemon = False

        wheeledbase_pos = wheeledbase
        self.max_linvel = wheeledbase_pos.max_linvel.get()
        self.max_angvel = wheeledbase_pos.max_angvel.get()

        self.sensors_front = sensors_front
        self.sensors_back = sensors_back
        self.sensors_lat = sensors_lat

        self.front_disable = Event()
        self.back_disable = Event()

        self.threshold = threshold
        self.lock = Lock()

        self.stopped = False
        self.stop_thread = Event()

    def set_thresold(self, thresold):
        self.lock.acquire()
        self.threshold = thresold
        self.lock.release()

    def stop(self):
        self.stop_thread.set()
