from tracking.libs.posiitonDetector import *
import math

posdetect=positionDetector.PositionDetector()
posdetect.addMarker(17)
posdetect.init([0,0,0],math.radians(90),0)

while True:
    posdetect.update()
