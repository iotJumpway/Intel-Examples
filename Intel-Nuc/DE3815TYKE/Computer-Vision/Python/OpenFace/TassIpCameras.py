###############################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
# Copyright 2017, Adam Milton-Barker, TechBubble Technologies, All rights reserved.
###############################################################################
# Title: cameras.py
# OpenTass
# Description: Manages local or IP cams.
# Acknowledgements: Uses code from openface (https://github.com/cmusatyalab/openface)
# Last Modified: 2017/08/06
#########################################################################################
# Licensed under the Apache License, Version 2.0 (the "License you may not use this
# file except in compliance with the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
########################################################################################

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