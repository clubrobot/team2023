import imp
from common.components import Manager
from daughter_cards.wheeledbase import WheeledBase
from tracking.libs.positionDetector import PositionDetector
from daughter_cards.sensors import Sensors
# Connect to the Raspberry Pi and the different modules
manager = Manager("10.0.0.10")
manager.connect(10)


# Connect wheeledbase

wb = WheeledBase(manager)

sensors =Sensors(manager)# '/dev/tty.SLAB_USBtoUART'

while(True):
	wb
#	print(sensors.get_sensor3_range())
#	print(sensors.sensor1)
	
#LEFTCODEWHEEL_RADIUS_VALUE              = 21.90460280828869
#RIGHTCODEWHEEL_RADIUS_VALUE         = 22.017182927267537
#ODOMETRY_AXLETRACK_VALUE            = 357.5722465739272
# verifier les moteurs sans assver (vrif les sens de marche) open loop velocities
# verifier les codeuses et leur sens
# Faire la metrologie et l'enregistrer
# calibrer l'odométrie (verif la precision)
# calib asservisseement
