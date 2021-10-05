#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setups.setup_logger import *
from common.components import Manager

manager = Manager.MANAGER_CREATED

if not manager:
    hostname = ""
    if hostname == "":
        setup_logger(INFO, "IP adress :  ")
        hostname = input()
        if len(hostname) == 0:
            hostname = "127.0.0.1"
        elif len(hostname.split(".")) == 1:
            hostname = "192.168.12." + hostname
        setup_logger(INFO, "Try reaching raspberry at IP " + hostname + "...")

    # Connect to the Raspberry Pi and the different modules
    manager = Manager(hostname)
    manager.connect(10)
