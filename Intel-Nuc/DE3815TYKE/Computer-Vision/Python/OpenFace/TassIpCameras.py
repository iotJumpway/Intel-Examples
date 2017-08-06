###############################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
###############################################################################
# Title: cameras.py
# OpenTass
# Description:
#   Manages local or IP cams.
# Last Modified: 8.3.2017
###############################################################################

import sys
import os
import time
import json
import threading

import cv2

class TassIpCameras(object):

    def __init__(self,camURL):

        print("LOADING "+camURL)

        self.ipCamFrame  = None
        self.ipCamEvent = threading.Event()
        self.ipCamEvent.set()

        self.video = cv2.VideoCapture(camURL)
        self.url = camURL

        if not self.video.isOpened():

            self.video.open()

            print("LOADED "+camURL)

        self.ipCamThread = threading.Thread(name='video_ipCam_thread',target=self.getIpCamFrame)
        self.ipCamThread.daemon = True
        self.ipCamThread.start()

    def readIpCamFrame(self):

        ipCam_blocker = self.ipCamEvent.wait()

        frame = self.ipCamFrame

        return frame

    def getIpCamFrame(self):

        while True:

            success, frame = self.video.read()
            self.ipCamEvent.clear

            if success:

                self.ipCamFrame  = frame
                self.ipCamEvent.set()