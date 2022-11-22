import cv2
import os
from time import sleep
from tracking.libs.camera import *
print(cv2.__version__)

IMAGE_DIRECTORY = 'CalibrationPictures'

if __name__ == "__main__":

    try:
        os.mkdir(IMAGE_DIRECTORY)
    except OSError:
        pass

    os.chdir(IMAGE_DIRECTORY)

    N = int(input('Number of pictures ?\n'))

    Stop = False

    dispW = 1280
    dispH = 720
    flip = 0
    # Uncomment These next Two Line for Pi Camera
    camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(
        flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    cam = cv2.VideoCapture(camSet, cv2.CAP_GSTREAMER)

    for i in range(0, N):
        while not Stop:
            ret, frame = cam.read()
            cv2.imshow('nanoCam', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                break

        cv2.imwrite('Pic'+str(i)+'.jpg', frame)
        sleep(1)

    cam.release()
    cv2.destroyAllWindows()
