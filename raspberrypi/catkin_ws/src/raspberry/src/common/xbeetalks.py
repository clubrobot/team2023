#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This library is free software from Club robot Insa Rennes sources; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
"""

import pickle
import os, sys
import traceback
import warnings
import time
import random
import string

from threading import Thread, RLock, Event, current_thread
from queue import Queue, Empty

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
from digi.xbee.models.message import XBeeMessage
from digi.xbee.exception import XBeeException

BAUDRATE = 115200
MASTER_BYTE = b'R'
SLAVE_BYTE = b'A'




class AlreadyOpenedError(Exception): pass

class XBeeTalks:
    def __init__(self, port, baudrate=BAUDRATE):
        self.device = XBeeDevice(port, baudrate)
        
        self.instructions = dict()
        self.listener = XBeeListener(self)
        
        self.queues_dict = dict()
        self.queues_lock = RLock()
        
    def open(self):
        if(self.device.is_open()):
            raise AlreadyOpenedError("Device already in use")
        else:
            self.device.open()
        self.listener.start()
    
    def bind(self, opcode, instruction):
        if not opcode in self.instructions:
            self.instructions[opcode] = instruction
        else:
            raise KeyError('opcode {} is already bound to another instruction'.format(opcode))

    def get_address(self):
        return self.device.get_64bit_addr()

    def send(self, address, opcode, *args, **kwargs):
        retcode = random.randint(0, 0xFFFFFFFF)
        content = (opcode, retcode, args, kwargs)
        prefix = (MASTER_BYTE,)
        self.rawsend(address, pickle.dumps(prefix + content))
        return retcode

    def sendback(self, address, retcode, *args):
        content = (retcode, args)
        prefix = (SLAVE_BYTE,)
        self.rawsend(address, pickle.dumps(prefix + content))

    def get_queue(self, retcode):
        self.queues_lock.acquire()
        try:
            queue = self.queues_dict[retcode]
        except KeyError:
            queue = self.queues_dict[retcode] = Queue()
        finally:
            self.queues_lock.release()
        return queue

    def delete_queue(self, retcode):
        self.queues_lock.acquire()
        try:
            del self.queues_dict[retcode]
        finally:
            self.queues_lock.release()

    def reset_queues(self):
        self.queues_lock.acquire()
        self.queues_dict = dict()
        self.queues_lock.release()

    def process(self, sender, message):
        role = message[0]
        if (role == MASTER_BYTE):
            opcode, retcode, args, kwargs = message[1:]
            self.execinstruction(sender, opcode, retcode, *args, **kwargs)
        elif (role == SLAVE_BYTE):
            retcode, args = message[1:]
            queue = self.get_queue(retcode)
            queue.put(args)

    def execinstruction(self, sender, opcode, retcode, *args, **kwargs):
        try:
            # # Make sure that the authentification was well performed
            # if not self.is_authentificated:
                # raise AuthentificationError('you are not authentificated')
                # # AJOUT
                # self.parent.disconnect()

            # Get the function or method associated with the received opcode
            try:
                instruction = self.instructions[opcode]
            except KeyError:
                raise KeyError('opcode {} is not bound to any instruction'.format(opcode)) from None

            # Execute the instruction
            output = instruction(*args, **kwargs)

        except Exception:
            etype, value, tb = sys.exc_info()
            output = (etype, value, traceback.extract_tb(tb))

        # Send back the output
        self.sendback(sender, retcode, output)

    def poll(self, retcode, timeout=0):
        queue = self.get_queue(retcode)
        block = (timeout is None or timeout > 0)
        try:
            assert (current_thread() is not self.listener)
            output = queue.get(block, timeout)
        except Empty:
            if block:
                raise TimeoutError('timeout exceeded') from None
            else:
                return None
        if queue.qsize() == 0:
            self.delete_queue(retcode)
        if len(output) > 1:
            return output  # Return as a tuple
        else:
            return output[0]  # Return as a single variable

    def flush(self, retcode):
        while self.poll(retcode) is not None:
            pass

    def execute(self, address, opcode, *args, timeout=5, **kwargs):
        retcode = self.send(address, opcode, *args, **kwargs)
        output = self.poll(retcode, timeout=timeout)
        if isinstance(output, tuple) and isinstance(output[0], type) and issubclass(output[0], Exception):
            etype, value, tb = output
            output = ('{2}\n' +
                      '\nThe above exception was first raised by the distant TCPTalks instance:\n\n' +
                      'Distant traceback (most recent call last):\n' +
                      '{0}' +
                      '{1}: {2}''').format(''.join(traceback.format_list(tb)), etype.__name__, str(value))
            raise etype(output)
        else:
            return output

    def sleep_until_disconnected(self):
        if self.listener is not current_thread():
            self.listener.join()
        else:
            raise RuntimeError('cannot call the \'sleep_until_disconnected\' method from within the listening thread')

    def rawsend(self, adr, data):
        try:
            remote = RemoteXBeeDevice(self.device, adr)
            self.device.send_data_async(remote, data)
        except XBeeException:
            pass
            
class XBeeListener(Thread):
    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        self.stop = Event()
        self.daemon = True

    def run(self):
         while not self.stop.is_set():
            try:
                message = self.parent.device.read_data(1)
                data, buffer = loads(message.data)
                self.parent.process(message.remote_device.get_64bit_addr(), data)
            except:
                pass

def loads(rawbytes):
        a, b = 0, len(rawbytes)
        while (b - a > 1):
            i = (a + b) // 2
            try:
                output = pickle.loads(rawbytes[:i])
            except (EOFError, pickle.UnpicklingError, AttributeError):
                a = i
            else:
                b = i
        return pickle.loads(rawbytes[:b]), rawbytes[b:]
