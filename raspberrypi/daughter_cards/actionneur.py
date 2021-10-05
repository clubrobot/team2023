#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.serialutils import Deserializer
from daughter_cards.arduino import Arduino, INT, BYTE
import time

# Instructions
MOVE_ELEVATOR_OPCODE = 0x10
GET_ELEVATOR_POSITION_OPCODE = 0x11
MOVE_CLAMP_OPCODE = 0x12
SET_CLAMP_POSITION_OPCODE = 0x13
MOVE_WINDSOCK_ARM_OPCODE = 0x14
SET_WINDSOCK_ARM_POSITION_OPCODE = 0x15
MOVE_FLAG_OPCODE = 0x16
RAISE_FLAG_OPCODE = 0x17
LOWER_FLAG_OPCODE = 0x18
GET_FLAG_POSITION_OPCODE = 0x19
CALIBRATE_ELEVATOR_OPCODE = 0x20
CALIBRATE_FLAG_OPCODE = 0x21


class Actionneur(Arduino):

    # def __init__(self, uuid='/dev/arduino/Actionneur'):
    def __init__(self, parent, uuid='/dev/arduino/Actionneur'):
        Arduino.__init__(self, parent, uuid)

    def move_elevator(self, id, height):
        self.send(MOVE_ELEVATOR_OPCODE, BYTE(id), BYTE(height))

    def get_elevator_position(self, id):
        pos_elevator = self.execute(GET_ELEVATOR_POSITION_OPCODE, BYTE(id))
        return pos_elevator.read(BYTE)

    def move_clamp(self, id, state):
        self.send(MOVE_CLAMP_OPCODE, BYTE(id), BYTE(state))

    def set_clamp_position(self, id, position):
        self.send(SET_CLAMP_POSITION_OPCODE, BYTE(id), BYTE(position))

    def move_windsock_arm(self, state):
        self.send(MOVE_WINDSOCK_ARM_OPCODE, BYTE(state))

    def set_windsock_arm_position(self, position):
        self.send(SET_WINDSOCK_ARM_POSITION_OPCODE, BYTE(position))

    def move_flag(self, height):
        self.send(MOVE_FLAG_OPCODE, BYTE(height))

    def raise_flag(self):
        self.send(RAISE_FLAG_OPCODE)

    def lower_flag(self):
        self.send(LOWER_FLAG_OPCODE)

    def get_flag_position(self):
        pos_flag = self.execute(GET_FLAG_POSITION_OPCODE)
        return pos_flag.read(BYTE)

    def calibrate_elevator(self, id):
        self.send(CALIBRATE_ELEVATOR_OPCODE, BYTE(id))

    def calibrate_flag(self):
        self.send(CALIBRATE_FLAG_OPCODE)


if __name__ == "__main__":
    from setups.setup_serialtalks import *

    s = Actionneur(manager)
    s.connect()
