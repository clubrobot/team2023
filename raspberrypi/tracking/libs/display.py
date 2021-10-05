import sys
import numpy as np
import cv2
import cv2.aruco as aruco

from time import sleep


class ArucoDisplay():
    def __init__(self, wait=1):
        self.wait = wait

    def show(self, frame):
        if frame is not None:
            cv2.imshow('frame', frame)
            if cv2.waitKey(self.wait) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                sleep(0.5)
                sys.exit(0)

    def stop(self):
        cv2.destroyAllWindows()
        sleep(0.5)
        sys.exit(0)
