from setups.setup_wheeledbase import *
from beacons.robot_client import *

try:
    robot_beacon = RobotClient(2, wheeledbase.get_position,ip='127.0.0.1')
    robot_beacon.connect()
    robot_beacon.reset_ressources()
except TimeoutError:
    pass

wheeledbase.set_position(922, 1157, -1.57)

while True:
    wheeledbase.goto(900, 1730)
    wheeledbase.goto(442, 1992)
    wheeledbase.goto(1391, 2253)
