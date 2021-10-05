#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import the necessary packages
from imutils.video.webcamvideostream import WebcamVideoStream


class VideoStream:
    WEBCAM = 0
    PICAMERA = 1
    JETSONCAMERA = 2

    def __init__(self, src=0, camera=JETSONCAMERA, resolution=(1280, 720), framerate=21):
        # check to see if the picamera module should be used
        if camera == self.PICAMERA:
            # only import the picamera packages unless we are
            # explicity told to do so -- this helps remove the
            # requirement of `picamera[array]` from desktops or
            # laptops that still want to use the `imutils` package
            from imutils.video.pivideostream import PiVideoStream

            # initialize the picamera stream and allow the camera
            # sensor to warmup
            self.stream = PiVideoStream(
                resolution=resolution, framerate=framerate)
        elif camera == self.JETSONCAMERA:
            from .jetsonvideostream import JetsonVideoStream
            self.stream = JetsonVideoStream(
                resolution=resolution, framerate=framerate)

        # otherwise, we are using OpenCV so initialize the webcam
        # stream
        else:
            self.stream = WebcamVideoStream(src=src)

    def start(self):
        # start the threaded video stream
        return self.stream.start()

    def update(self):
        # grab the next frame from the stream
        self.stream.update()

    def read(self):
        # return the current frame
        return self.stream.read()

    def stop(self):
        # stop the thread and release any resources
        self.stream.stop()
