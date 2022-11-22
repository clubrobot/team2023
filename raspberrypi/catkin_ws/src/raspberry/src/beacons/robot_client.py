#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import sys

from beacons.global_sync import *

_BEACON_PORT = 25568

BORNIBUS_ID = 1
R128_ID = 2

class RobotClient(ClientGS):
    """Inherit from GlobalSync client and run on the robots in order to give our pos to the other

    Args:
        ClientGS (class): GlobalSync client
    """
    def __init__(self, ID, my_pos_getter, ip="192.168.12.1", port=_BEACON_PORT):
        """Init the client

        Args:
            ID (int): my robot id
            my_pos_getter (function): my position getter (ex : wheeledbase.get_position())
            ip (str, optional): server ip. Defaults to "192.168.12.1".
            port (int, optional): server port. Defaults to _BEACON_PORT.
        """
        ClientGS.__init__(self, ID, ip=ip, port=port)
        self.logger = LogManager().getlogger("RobotClient", Logger.SHOW, level_disp=INFO)

        self.my_pos_getter = my_pos_getter

    def _get_my_pos(self):
        """Return my pos from the wheeledbase

        Returns:
            [type]: [description]
        """
        return self.my_pos_getter()