#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.parallel import Thread
import cv2


class JetsonVideoStream:
    def __init__(self, resolution=(1280,720), framerate=21, name="JetsonVideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(self.gstreamer_pipeline(
            display_width=resolution[0],
            display_height=resolution[1],
            framerate=framerate,
            flip_method=2), cv2.CAP_GSTREAMER)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def gstreamer_pipeline(self, capture_width=3280, capture_height=2464, display_width=1280, display_height=720, framerate=21, flip_method=2):
        return ('nvarguscamerasrc ! '
                'video/x-raw(memory:NVMM), '
                'width='+str(capture_width)+' , '
                'height='+str(capture_height)+' , '
                'format=NV12, '
                'framerate='+str(framerate)+'/1 ! '
                'nvvidconv flip-method='+str(flip_method)+' ! '
                'video/x-raw, width='+str(display_width) + ', '
                'height='+str(display_height)+' , '
                'format=BGRx ! '
                'videoconvert ! '
                'video/x-raw , '
                'format=BGR ! '
                'appsink')
