#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math

from common.serialtalks import INT
from daughter_cards.arduino import Arduino

# Instructions

GET_POSITION_OPCODE = 0x10


class Tag(Arduino):

    def __init__(self, parent, uuid='tag'):
        Arduino.__init__(self, parent, uuid)

    def get_position(self, **kwargs):
        output = self.execute(GET_POSITION_OPCODE, **kwargs)
        x, y = output.read(INT, INT)
        return x, y
