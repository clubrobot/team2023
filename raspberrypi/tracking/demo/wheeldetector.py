import numpy as np
import cv2
import cv2.aruco as aruco

def preProcessing(img):
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny=cv2.Canny(imgBlur,120,120)

    kernel=np.ones((5,5))
    imgDialation=cv2.dilate(imgCanny,kernel,iterations=2)
    imgErod=cv2.erode(imgDialation,kernel,iterations=1)
    return imgErod
"""This Method find markers 17 on the wheel and get is orientation
return 1 if the wheel face the south or 1 otherwise
return -1 if the wheel's marker is not detected.
"""
def getWheelOrientation():
    dictionary=cv2.aruco.Dictionary_get(aruco.DICT_4X4_250)

    cap=cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4, 480)
    cap.set(10,10)

    sucess,img=cap.read()

    parameters=aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10
    imgTree=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    markerids=[]
    markerCorners,markerids,rejectedCandidates=aruco.detectMarkers(imgTree,dictionary,parameters=parameters)
    if markerids is not None:
        for i in range(0,len(markerids)):
            if markerids[i][0]==17:
                aruco.drawDetectedMarkers(img, markerCorners)
                if (markerCorners[0][0][0][0] > markerCorners[0][0][2][0]):
                    return 1
                else:
                    return 0

    return -1


