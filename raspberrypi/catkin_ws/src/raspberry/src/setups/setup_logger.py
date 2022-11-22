#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logs.log_manager import *

LogManager().start()

setup_logger = LogManager().getlogger('Setup logger', level_disp=INFO)