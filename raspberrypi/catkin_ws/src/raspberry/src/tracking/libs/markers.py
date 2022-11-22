import numpy as np
import cv2
import cv2.aruco as aruco

class Marker:
    """
        The purpose of this class is to define a marker
    """

    def __init__(self, identifier, size, dictionnary=aruco.DICT_4X4_100):
        """
            Init with aruco tag ID, its size in mm
        """
        self.identifier = identifier
        self.size = size  # mm
        self.dictionnary = dictionnary

class MarkerList:
    def __init__(self, ids, size, dictionnary=aruco.DICT_4X4_100):
        self.markers = list()
        self.size = len(ids)

        for i in range(0, self.size):
            self.markers.append(Marker(ids[i], size, dictionnary))

class ReferenceMarker(Marker):
    def __init__(self, identifier, size, pos, rotAngle=None, dictionnary=aruco.DICT_4X4_100):
        """
            Init reference marker
        """
        Marker.__init__(self, identifier, size, dictionnary)
        self.pos = pos
        if rotAngle is None:
            self.matrix = np.float32([[1, 0, 0, self.pos.x],
                                      [0, 1, 0, self.pos.y],
                                      [0, 0, 1, self.pos.z],
                                      [0, 0, 0, 1]])
        else:
            th = np.radians(rotAngle)
            self.matrix = np.float32([[np.cos(th),  -np.sin(th), 0, self.pos.x],
                                      [np.sin(th), np.cos(th), 0, self.pos.y],
                                      [0, 0, 1, self.pos.z],
                                      [0, 0, 0, 1]])
