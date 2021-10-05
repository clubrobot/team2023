#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setups.setup_logger import *

from daughter_cards.display import *
from managers.display_manager import *
from setups.setup_serialtalks import *

led1 = LEDMatrix(manager, 1)
led2 = LEDMatrix(manager, 2)
ssd = SevenSegments(manager)

display = DisplayPoints(ssd, led1, led2)
