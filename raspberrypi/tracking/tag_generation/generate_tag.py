import numpy as np
import cv2
import cv2.aruco as aruco

MARKER_ID = 2

# Select type of aruco marker (size)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)

# Create an image from the marker
# second param is ID number
# last param is total image size
img = aruco.drawMarker(aruco_dict, MARKER_ID, 700)
cv2.imwrite("{}.jpg".format(MARKER_ID), img)
