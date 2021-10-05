#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.serialtalks import BYTE, FLOAT
from common.serialutils import Deserializer
from daughter_cards.arduino import SecureArduino

CSA_GET_CUP_COLOR_ESTIMATE_OPCODE = 0X10
# Optional operations.
CSA_GET_RGB_OPCODE = 0X11
CSA_SET_INTEGRATION_TIME_OPCODE = 0X12
CSA_SET_GAIN_OPCODE = 0X13
CSA_ENABLE_OPCODE = 0X14
CSA_DISABLE_OPCODE = 0X15
CSA_LEDS_ON_OPCODE = 0X16
CSA_LEDS_OFF_OPCODE = 0X17
CSA_SET_CUP_COLOR_ESTIMATE_SAMPLE_SIZE_OPCODE = 0X18
CSA_RESET = 0x19


class ColorSensorArray(SecureArduino):
    INTEGRATION_TIME_2_4MS = 0
    INTEGRATION_TIME_24MS = 1
    INTEGRATION_TIME_50MS = 2
    INTEGRATION_TIME_101MS = 3
    INTEGRATION_TIME_154MS = 4
    INTEGRATION_TIME_700MS = 5
    GAIN_1X = 0
    GAIN_4X = 1
    GAIN_16X = 2
    GAIN_60X = 3
    CUP_COLOR_ESTIMATE_RED = 0
    CUP_COLOR_ESTIMATE_GREEN = 1
    CUP_COLOR_ESTIMATE_ERROR = 2

    DEFAULT = {
        CSA_GET_CUP_COLOR_ESTIMATE_OPCODE: Deserializer(BYTE(CUP_COLOR_ESTIMATE_ERROR)),
        CSA_GET_RGB_OPCODE: Deserializer(FLOAT(255) + FLOAT(255) + FLOAT(255))
    }

    def __init__(self, parent, uuid='ColorSensors'):
        SecureArduino.__init__(self, parent, uuid, self.DEFAULT)

    def get_cup_color_estimate(self, channel: int) -> int:
        return self.execute(CSA_GET_CUP_COLOR_ESTIMATE_OPCODE, BYTE(channel)).read(BYTE)

    def get_rgb(self, channel: int) -> (float, float, float):
        return self.execute(CSA_GET_RGB_OPCODE, BYTE(channel)).read(FLOAT, FLOAT, FLOAT)

    def set_integration_time(self, channel: int, it: int):
        self.send(CSA_SET_INTEGRATION_TIME_OPCODE, BYTE(channel), BYTE(it))

    def set_gain(self, channel: int, gain: int):
        self.send(CSA_SET_GAIN_OPCODE, BYTE(channel), BYTE(gain))

    def enable(self, channel: int):
        self.send(CSA_ENABLE_OPCODE, BYTE(channel))

    def disable(self, channel: int):
        self.send(CSA_DISABLE_OPCODE, BYTE(channel))

    def leds_on(self):
        self.send(CSA_LEDS_ON_OPCODE)

    def leds_off(self):
        self.send(CSA_LEDS_OFF_OPCODE)

    def reset(self):
        self.send(CSA_RESET)
