from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase
from daughter_cards.actionneur import Actionneur
from tracking.libs.positionDetector import PositionDetector
from daughter_cards.sensors import Sensors
from setups.setup_serialtalks import *
from robots.team2022.team2022Robot import Bornibus

# Connect to the Raspberry Pi and the different modules
manager = Manager("10.0.0.4")
manager.connect(7)

bornibus = Bornibus(manager)
while(True):
    print(bornibus.avoidance_behaviour.sensors.get_range_left_back())

