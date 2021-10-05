#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math

from common.serialtalks import BYTE, INT, LONG, FLOAT
from daughter_cards.arduino import Arduino

LED_ON_OPCODE = 0x11
LED_OFF_OPCODE = 0x12


class ButtonCard(Arduino):
    BUTTON_ID = 1
    RED_BUTTON = 3
    GREEN_BUTTON = 2
    BLUE_BUTTON = 1
    YELLOW_BUTTON = 4
    EMERGENCY = 5
    PLAY_MODE = 6
    DEV_MODE = 7
    TIRETTE = 8

    def __init__(self, parent, uuid='buttonCard'):
        Arduino.__init__(self, parent, uuid)
        self.functions = dict()
        self.bind(1, self._compute)

    def _compute(self, args):
        try:
            self.functions[args.read(BYTE)]()
        except KeyError:
            pass

    def affect(self, ID, function):
        self.functions[ID] = function

    def on(self, nb):
        self.send(LED_ON_OPCODE, BYTE(nb))

    def off(self, nb):
        self.send(LED_OFF_OPCODE, BYTE(nb))
