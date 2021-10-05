#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import sys

from beacons.global_sync import *

_BEACON_PORT = 25568
_EYE_ID = 3

try:
    from tracking.libs.manager import *
    from tracking.libs.utils import *
    from tracking.libs.markers import *

    _WHEATHERVANE_MARKER_ID          = 17
    _WHEATHERVANE_MARKER_SIZE        = 0.06 # meters
    _WHEATHERVANE_MARKER_COORDINATES = Point(0, 0, 0) # (x, y, z) meters
    _WHEATHERVANE_MARKER_Z_ROTATION  = 0 # Degrees

except:
    pass


class EyeClient(ClientGS):
    def __init__(self, ip="192.168.12.1", port=_BEACON_PORT):
        ClientGS.__init__(self, _EYE_ID , ip=ip, port=port)
        self.logger = LogManager().getlogger("EyeClient", Logger.SHOW, level_disp=INFO)

        self.tracking = None

        try:
            #                     id| size | Coords(x,y,z)  |    flip aroud Z
            self.reference = ReferenceMarker(_WHEATHERVANE_MARKER_ID, _WHEATHERVANE_MARKER_SIZE, _WHEATHERVANE_MARKER_COORDINATES , _WHEATHERVANE_MARKER_Z_ROTATION)

            self.tracking = TrackingManager()
            self.tracking.start()

        except:
            self.logger(WARNING, "You should probably check your opencv package first")
            self.logger(WARNING, "Tracking can't work in this configuration")
            self.logger(WARNING, "But all others components works fine ! :)")

        self.logger(INFO, "Eye Client succefully initialised")

    def init_tracking(self, camera=VideoStream.PICAMERA):
        if self.tracking is not None:
            while not self.tracking.setup(self.reference, camera=camera, mode=self.tracking.MODE_WHEATHERVANE):
                pass

            self.tracking.startTracking()

    def _get_my_final_orientation(self):
        if self.tracking is not None:
            return self.tracking.getWheatherVaneOrientation()
        else:
            return ORIENTATION_NONE
