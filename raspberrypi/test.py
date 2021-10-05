from common.xbeecom import *
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time

def aff(*args):
    print("balise: "+str(args[0]))
    return args[0]+1




balise = XBeeTalks("/dev/ttyUSB1")
robot = XBeeTalks("/dev/ttyUSB0")

balise.bind(0x20, aff)

balise.open()
robot.open()


time.sleep(1)

print("robot: "+str(robot.execute(balise.get_address(), 0x20, 1)))
