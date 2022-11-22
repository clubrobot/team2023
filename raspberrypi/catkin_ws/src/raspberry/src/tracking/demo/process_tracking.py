from time import sleep
import glob

from logs.log_manager import *
from tracking.libs.camera import *
from tracking.libs.manager import *
from tracking.libs.utils import *
from tracking.libs.markers import *

if __name__ == "__main__":
    # Start logger
    LogManager().start()

    #                     id| size | Coords(x,y,z)  |    flip aroud Z
    ref = ReferenceMarker(42, 0.02, Point(0.125, 0.150, 0.0), 90)

    markerList = MarkerList([1, 2, 3, 4, 5], 0.02)

    man = TrackingManager()
    man.start()

    while not man.setup(ref, camera=VideoStream.WEBCAM, mode=man.MODE_WHEATHERVANE, debug=True):
        pass

    man.startTracking()

    while True:
        print(man.getWheatherVaneOrientation())
        sleep(1)

    man.stopTracking()

    input()
