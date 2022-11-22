#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arduino classes including SerialTalks and SerialTopic.
"""
from common.serialtalks import *
from common.components import *

_MANAGE_OPCODE = 0X07
_SUBSCRIBE     = 0X0
_UNSUBSCRIBE   = 0X1

def TopicHandler(*args):
    """
    Decorator for auto deserialization purpose.

    args: sorted Deserializer list for extract args from received packet.

    return: 
        decorator for encapsulating function with deserialization.

    example :
        from common.serialtalks import FLOAT

        @TopicHandler(FLOAT, FLOAT)
        def topicHandler(x, y):
            return x, y
    """
    def producedDecorator(fct):
        def cap_fct(self, data):
            if(len(args)>1):
                return fct(self, *data.read(*args))
            else :
                return fct(self,  data.read(*args))
        return cap_fct
    return producedDecorator

class Arduino(SerialTalksProxy):
    """
    Arduino class including serialtalks proxy and serialtopic gesture.
    """
    def __init__(self, server, uuid):
        SerialTalksProxy.__init__(self, server, uuid)

    def addTopic(self, topic_code, handler, name, timestep):
        """
        Add topic handler to a specific topic_code.
        This function will create both enable and disable function according to the topic name.

        args:
            topic_code : The serial topic code.
            handler : A handler function. This function must have only one arg (if no decorator arduino.TopicHandler).
            name : The topic name in order to create enable and disable function
            timestep : Topic timestep to use on embedded device.
        """
        name = name[0].upper() + name.lower()[1:]

        if  (not self.__dict__.get("subscribe"+name, None) is None ) or (not self.__dict__.get("unsubscribe"+name, None) is None):
            raise RuntimeError("Unable to create subscriber method")

        def sub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_SUBSCRIBE), BYTE(topic_code), LONG(timestep))
            return bool(output.read(BYTE))

        def usub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_UNSUBSCRIBE),  BYTE(topic_code))
            return bool(output.read(BYTE))

        self.__setattr__("subscribe"+name, sub)
        self.__setattr__("unsubscribe"+name, usub)

        self.bind(topic_code, handler)

class SecureArduino(SecureSerialTalksProxy):
    """
    Arduino class including serialtalks proxy and serialtopic gesture with default func result.
    """
    def __init__(self, server, uuid, default_result):
        SecureSerialTalksProxy.__init__(self, server, uuid, default_result)

    def addTopic(self, topic_code, handler, name, timestep):
        """
        Add topic handler to a specific topic_code.
        This function will create both enable and disable function according to the topic name.

        args:
            topic_code : The serial topic code.
            handler : A handler function. This function must have only one arg (if no decorator arduino.TopicHandler).
            name : The topic name in order to create enable and disable function
            timestep : Topic timestep to use on embedded device.
        """
        name = name[0].upper() + name.lower()[1:]

        if  (not self.__dict__.get("subscribe"+name, None) is None ) or (not self.__dict__.get("unsubscribe"+name, None) is None):
            raise RuntimeError("Unable to create subscriber method")

        def sub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_SUBSCRIBE), BYTE(topic_code), LONG(timestep))
            return bool(output.read(BYTE))

        def usub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_UNSUBSCRIBE),  BYTE(topic_code))
            return bool(output.read(BYTE))

        self.__setattr__("subscribe"+name, sub)
        self.__setattr__("unsubscribe"+name, usub)

        self.bind(topic_code, handler)

class ArduinoLocal(SerialTalks):
    """
    Arduino class including serialtalks proxy and serialtopic gesture with default func result.
    """
    def __init__(self, port):
        SerialTalks.__init__(self, port)

    def addTopic(self, topic_code, handler, name, timestep):
        """
        Add topic handler to a specific topic_code.
        This function will create both enable and disable function according to the topic name.

        args:
            topic_code : The serial topic code.
            handler : A handler function. This function must have only one arg (if no decorator arduino.TopicHandler).
            name : The topic name in order to create enable and disable function
            timestep : Topic timestep to use on embedded device.
        """
        name = name[0].upper() + name.lower()[1:]

        if  (not self.__dict__.get("subscribe"+name, None) is None ) or (not self.__dict__.get("unsubscribe"+name, None) is None):
            raise RuntimeError("Unable to create subscriber method")

        def sub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_SUBSCRIBE), BYTE(topic_code), LONG(timestep))
            return bool(output.read(BYTE))

        def usub():
            output = self.execute(
                _MANAGE_OPCODE, BYTE(_UNSUBSCRIBE),  BYTE(topic_code))   
            return bool(output.read(BYTE))

        self.__setattr__("subscribe"+name, sub)
        self.__setattr__("unsubscribe"+name, usub)

        self.bind(topic_code, handler)


