#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setups.setup_robot_name import *
from setups.setup_wheeledbase import *
from beacons.robot_client import *

try:
    robot_beacon = RobotClient(
        ROBOT_ID, wheeledbase.get_position, ip='127.0.0.1')
    robot_beacon.connect()
    robot_beacon.reset_ressources()
except (TimeoutError, OSError):
    pass
