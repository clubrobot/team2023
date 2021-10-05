#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
import numpy as np
import cv2
import cv2.aruco as aruco

from threading import Thread, Event, Lock

from logs.log_manager import *
from tracking.libs.utils import *
from tracking.libs.display import *
from tracking.libs.markers import *

ORIENTATION_NONE = 0
ORIENTATION_NORTH = 1
ORIENTATION_SOUTH = 2

class TrackingCore(Thread):
    """
        This class purpose is to track robots positions on a map

        (3000,3000) +---------------------------------------+ x
                    |                                       |
                    |                     ref: id 42        |
                    |        (1250, 1500)+                  |
                    |                                       |
                    |                                       |
                    |                                       |
                y   +---------------------------------------+ (0,0)
                                        ^
                                        Camera

        This class try to find markers in a given list and extract its positions.

        It only find two marker, one for robot A and one for Robot B.

        The robots marker attributon is given by Z distance from the reference marker plan

            * Robot A marker : Robot height + min balise height -> 430 mm + 50 mm
            * Robot B marker : Robot height + max balise height -> 430 mm + 80 mm

    """
    MODE_TRACKING = 0
    MODE_WHEATHERVANE = 1

    def __init__(self, camera, refMarker, mode = MODE_TRACKING, debug=False, dictionnary=aruco.DICT_4X4_100, exec_param=Logger.SHOW, log_level=INFO):
        """
            Init all Tracker Components
        """
        Thread.__init__(self)

        self.deamon = True

        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        try:
            # File storage in OpenCV
            cv_file = cv2.FileStorage(
                "../calibration.yaml", cv2.FILE_STORAGE_READ)

            self.camera_matrix = cv_file.getNode("camera_matrix").mat()
            self.dist_matrix = cv_file.getNode("dist_coeff").mat()

            # release file
            cv_file.release()
        except:
            self.logger(
                ERROR, 'No calibration file found, try to run calibration script before')
            sleep(0.2)
            sys.exit(1)

        # Get aruco dict
        self.dict = aruco.Dictionary_get(dictionnary)

        # Get detection parameters
        self.parameters = aruco.DetectorParameters_create()
        self.parameters.adaptiveThreshConstant = 10

        self.camera = camera
        self.refMarker = refMarker
        self.mode = mode
        self.debug = debug

        self.calibrationMatrix = None

        self.stop = Event()
        self.stop.clear()

        self.calibrated = Event()
        self.calibrated.clear()

        self.lock = Lock()

        self.currentFrame = None

        self.pos = list([(-1000, -1000) , (-1000, -1000)])
        self.wheatherVaneOrientation = ORIENTATION_NONE

        self.logger(INFO, 'Tracker Initialisation Success !')

    def terminate(self):
        """
            Terminate Thread
        """
        self.stop.set()
        self.join()

    def get_current_frame(self):
        return self.currentFrame

    def getPos(self):
        self.lock.acquire()
        pos = self.pos
        self.lock.release()
        return pos

    def getWheatherVaneOrientation(self):
        self.lock.acquire()
        orientation = self.wheatherVaneOrientation
        self.lock.release()
        return orientation

    def is_calibrated(self):
        """
            Get Calibration Flag
        """
        return self.calibrated.is_set()

    def recalibrate(self):
        """
            Clear calibration flag to attempt new calibration
        """
        self.calibrated.clear()

    def run(self):
        """
            Compute method to print estimated position for each tag
        """
        while not self.stop.is_set():
            if self.mode == self.MODE_TRACKING:
                if not self.is_calibrated():
                    if self.calibrate():
                        self.logger(INFO, 'Calibration Done')
                        self.calibrated.set()
                    else:
                        self.logger(INFO, 'Waiting for calibration')
                        sleep(1)
                else:
                    self.compute()
            elif self.mode == self.MODE_WHEATHERVANE:
                self.compute()

        self.camera.stop()

    def calibrate(self):
        """
            Calibrate method to get calibration matrix from camera
        """
        # Get frames
        frame, gray = self._getFrame()

        # Detect Markers
        corners, ids, _ = aruco.detectMarkers(
            gray, self.dict, parameters=self.parameters)

        index = self._getMarkerIndex(ids, self.refMarker.identifier)

        if index is not None:
            self.calibrationMatrix = self._getCalibrationMatrix(corners, index)

            if self.debug:
                aruco.drawDetectedMarkers(frame, corners)
                self._updateCurrentFrame(frame)

            if self.calibrationMatrix is not None:
                return True
        else:
            if self.debug:
                self._updateCurrentFrame(frame)
            return False

    def compute(self):
        # Get frame
        frame, gray = self._getFrame()
        # Detect Markers
        corners, ids, _ = aruco.detectMarkers(gray, self.dict, parameters=self.parameters)

        if np.all(ids != None):
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                corners, self.refMarker.size, self.camera_matrix, self.dist_matrix)

            if self.debug:
                aruco.drawDetectedMarkers(frame, corners)

            for i in range(0, ids.size):
                if self.mode == self.MODE_TRACKING:
                    if ids[i] != self.refMarker.identifier:
                        self.pos[0] = self._getPointMilimeters(rvec[i], tvec[i])[:2]
                elif self.mode == self.MODE_WHEATHERVANE:
                    if ids[i] == self.refMarker.identifier:
                        self._ComputeWheatherVaneOrientation(rvec[i], tvec[i])

        if self.debug:
            self._updateCurrentFrame(frame)

    def _ComputeWheatherVaneOrientation(self, rvec, tvec):
        """
            Internal method to get milimeters pos from rvec and tvec.
            1. Get rotation matrix from Rvec by rodrigues func:
                R = Rodrigues(rvec)
            2. Create vetor
                Vec =   | 0 |
                        | 1 |
                        | 0 |
            3. get orientation vecter
                orVec = R * Vec
            4. get real orientation
                if(orVec[1] > 0)
                    SOUTH
                else
                    NORTH
        """
        R = np.float32(cv2.Rodrigues(rvec)[0])
        vec = np.float32([0, 1, 1]).reshape(3, 1)
        orVec = np.matmul(R, vec)
        if(orVec[1] > 0):
            # SOUTH
            self.lock.acquire()
            self.wheatherVaneOrientation = ORIENTATION_SOUTH
            self.lock.release()
        else:
            # NORTH
            self.lock.acquire()
            self.wheatherVaneOrientation = ORIENTATION_NORTH
            self.lock.release()

    def _getPointMilimeters(self, rvec, tvec):
        """
            Internal method to get milimeters pos from rvec and tvec.

            1. Get rotation matrix from Rvec by rodrigues func:

                R = Rodrigues(rvec)

            2. Compose 4x4 matrix with R and Tvec:

                                    | Rxx  Rxy  Rxz tvecx |
                Rmarker = |R|t| =   | Ryx  Ryy  Ryz tvecy |
                                    | Rzx  Rzy  Rzz tvecz |
                                    |  0    0    0    1   |

            3. Project coordinates of detected marker:

                | x |                                 | 0 |
                | y |   = ((Rref * Rcal) * Rmarker) * | 0 |
                | z |                                 | 0 |
                | 1 |                                 | 1 |

                Note: marker coordinates is always Zero on marker world

            4. Convert point to millimeters, round it and return it
        """
        try:
            R = np.float32(cv2.Rodrigues(rvec)[0])
            t = np.float32(tvec[0]).reshape(3, 1)

            Rmarker = np.concatenate((R, t), axis=1)
            Rmarker = np.vstack([Rmarker, np.float32([0, 0, 0, 1])])

            point = (np.matmul(np.matmul(self.refMarker.matrix,
                                         self.calibrationMatrix), Rmarker)).dot([0, 0, 0, 1])

            return round(point[0]*1000), round(point[1]*1000), round(point[2]*1000)
        except:
            return None

    def _getMarkerIndex(self, idList, requestId):
        """
            Internal method to get marker index on ids list
        """
        try:
            return np.where(idList == np.array(requestId))[0][0]
        except:
            return None

    def _getFrame(self):
        """
            Internal method to get camera frame.
            It retrun color and gray frame
        """
        frame = self.camera.read(width=800)
        return (frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    def _updateCurrentFrame(self, frame):
        self.lock.acquire()
        self.currentFrame = frame.copy()
        self.lock.release()

    def _getCalibrationMatrix(self, corners, index):
        """
            Internal method to retreive map calibration matrix from reference marker on map.

            1. Get rotation matrix from Rvec by rodrigues func:

                R = Rodrigues(rvec)

            2. Compose 4x4 Calibration matrix with R and Tvec:

                                | Rxx  Rxy  Rxz tvecx |
                Rcal  = |R|t| = | Ryx  Ryy  Ryz tvecy |
                                | Rzx  Rzy  Rzz tvecz |
                                |  0    0    0    1   |
            3. And invert it:

                Rcal = inv(Rcal)

            Return None if error occur
        """
        try:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                corners[index], self.refMarker.size, self.camera_matrix, self.dist_matrix)

            R = np.float32(cv2.Rodrigues(rvec)[0])
            t = np.float32(tvec[0][0]).reshape(3, 1)

            Rcal = np.concatenate((R, t), axis=1)
            Rcal = np.vstack([Rcal, np.float32([0, 0, 0, 1])])

            return np.linalg.inv(Rcal)
        except:
            return None
