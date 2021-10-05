#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logs.utils.colors import Colors
from collections import namedtuple

"""
Pipe tuple that contain the two pipe sockets
"""
PipeType    = namedtuple('PipeType', ['parent', 'child'])
LogCommand  = namedtuple('LogCommand', ['command', 'args'])
LogLevel    = namedtuple('LogLevel', ['value', 'name', 'color'])
LogMsg      = namedtuple('LogMsg', ['time', 'level', 'name', 'args', 'kwargs'])
LogInit     = namedtuple('LogInit', ['name', 'exec_param', 'level_disp'])

"""
Logs Levels
"""
# Le programme complet est en train de partir en couille.
CRITICAL    = LogLevel(50, '[CRITICAL]', Colors.RED2)
# Une opération a foirée.
ERROR       = LogLevel(40, '[ERROR]', Colors.RED)
# Pour avertir que quelque chose mérite l’attention.
WARNING     = LogLevel(30, '[WARNING]', Colors.YELLOW)
# Pour informer de la marche du programme.
INFO        = LogLevel(20, '[INFO]', Colors.GREEN)
# Pour dumper des information quand vous débuggez.
DEBUG       = LogLevel(10, '[DEBUG]', Colors.BLUE)