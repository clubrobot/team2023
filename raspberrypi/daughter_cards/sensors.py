#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.serialutils import Deserializer
from daughter_cards.arduino import SecureArduino, TopicHandler, USHORT, BYTE
import time

UNUSED_SENSOR = 65535

# Instructions
GET_SENSOR1_OPCODE = 0x10
GET_SENSOR2_OPCODE = 0x11
GET_SENSOR3_OPCODE = 0x12
GET_SENSOR4_OPCODE = 0x13
GET_SENSOR5_OPCODE = 0x14
GET_SENSOR6_OPCODE = 0x15
GET_SENSOR7_OPCODE = 0x16
GET_SENSOR8_OPCODE = 0x17

CHECK_ERROR_OPCODE = 0X18

GET_ALL_TOPIC_OPCODE = 0x01


class Sensors(SecureArduino):
    TIMESTEP = 100
    MAX_DIST = 10000
    DEFAULT = {GET_SENSOR1_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR2_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR3_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR4_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR5_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR6_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR7_OPCODE: Deserializer(USHORT(MAX_DIST)),
               GET_SENSOR8_OPCODE: Deserializer(USHORT(MAX_DIST)), }

    def __init__(self, parent, uuid='SensorBoard'):
        SecureArduino.__init__(self, parent, uuid, default_result=self.DEFAULT)
        self.last_time = None

        try:
            self.addTopic(GET_ALL_TOPIC_OPCODE,
                      self.get_all_sensors_handler, "sensors", self.TIMESTEP)
        except:
            pass

        self.sensor1 = self.MAX_DIST
        self.sensor2 = self.MAX_DIST
        self.sensor3 = self.MAX_DIST
        self.sensor4 = self.MAX_DIST
        self.sensor5 = self.MAX_DIST
        self.sensor6 = self.MAX_DIST
        self.sensor7 = self.MAX_DIST
        self.sensor8 = self.MAX_DIST

    @TopicHandler(USHORT, USHORT, USHORT, USHORT, USHORT, USHORT, USHORT, USHORT)
    def get_all_sensors_handler(self, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8):
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.sensor3 = sensor3
        self.sensor4 = sensor4
        self.sensor5 = sensor5
        self.sensor6 = sensor6
        self.sensor7 = sensor7
        self.sensor8 = sensor8

    def get_all(self):
        return [self.sensor1, self.sensor2, self.sensor3, self.sensor4, self.sensor5, self.sensor6, self.sensor7, self.sensor8]

    def get_range_left_front(self):
        return self.sensor1, UNUSED_SENSOR

    def get_range_mid_left_front(self):
        return self.sensor2, UNUSED_SENSOR

    def get_range_mid_right_front(self):
        return self.sensor3, UNUSED_SENSOR

    def get_range_right_front(self):
        return self.sensor4, UNUSED_SENSOR

    def get_range_left_back(self):
        return self.sensor5, UNUSED_SENSOR

    def get_range_mid_left_back(self):
        return self.sensor6, UNUSED_SENSOR

    def get_range_mid_right_back(self):
        return self.sensor7, UNUSED_SENSOR

    def get_range_right_back(self):
        return self.sensor8, UNUSED_SENSOR

    def get_sensor1_range(self):
        return self.execute(GET_SENSOR1_OPCODE).read(USHORT) , UNUSED_SENSOR

    def get_sensor2_range(self):
        return self.execute(GET_SENSOR2_OPCODE).read(USHORT) , UNUSED_SENSOR

    def get_sensor3_range(self):
        return self.execute(GET_SENSOR3_OPCODE).read(USHORT) , UNUSED_SENSOR

    def get_sensor4_range(self):
        return self.execute(GET_SENSOR4_OPCODE).read(USHORT) , UNUSED_SENSOR

    def get_sensor5_range(self):
        return self.execute(GET_SENSOR5_OPCODE).read(USHORT) , UNUSED_SENSOR

    def get_sensor6_range(self):
        return self.execute(GET_SENSOR6_OPCODE).read(USHORT) , UNUSED_SENSOR

    def get_sensor7_range(self):
        return self.execute(GET_SENSOR7_OPCODE).read(USHORT) , UNUSED_SENSOR

    def get_sensor8_range(self):
        return self.execute(GET_SENSOR8_OPCODE).read(USHORT) , UNUSED_SENSOR

    def is_ready(self):
        try:
            return self.is_connected
        except:
            return False

    def check_errors(self):
        deser = self.execute(CHECK_ERROR_OPCODE)
        error = deser.read(BYTE)
        return error


if __name__ == "__main__":
    from setups.setup_serialtalks import *

    s = Sensors(manager, '/dev/tty.SLAB_USBtoUART')
