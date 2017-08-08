###############################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
# Copyright 2017, Adam Milton-Barker, TechBubble Technologies, All rights reserved.
###############################################################################
# Title: TassCore.py
# Description: Loops through all cameras and processes each frame.
# Acknowledgements: Uses code from openface (https://github.com/cmusatyalab/openface)
# Last Modified: 2017/08/06
########################################################################################
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

from TassTools import TassTools
from TassClassifier import TassClassifier
import TassIpCameras as TassIpCameras

from techbubbleiotjumpwaymqtt.application import JumpWayPythonMQTTApplicationConnection

import cv2
import dlib
import numpy as np

from datetime import datetime

class TassCore():

    def __init__(self):

        self.TassTools = TassTools()
        self.TassClassifier = TassClassifier(1)

        self._configs = {}

        with open("config.json") as configs:

            self._configs = json.loads(configs.read())

        self.startMQTT()

        for i, camera in enumerate(self._configs["CameraList"]):

            camThread = threading.Thread(
                name="camera_thread_" + str(i),
                target=self.processFrame,
                args=(TassIpCameras.TassIpCameras(
                    camera["camURL"]),
                    camera["camID"],
                    camera["camSensorID"],
                    camera["camZone"],
                )
            )

            camThread.start()

    def startMQTT(self):

        try:

            self.JumpWayMQTTClient = JumpWayPythonMQTTApplicationConnection({
				"locationID": self._configs["IoTJumpWayMQTTSettings"]["SystemLocation"],
				"applicationID": self._configs["IoTJumpWayMQTTSettings"]["SystemApplicationID"],
				"applicationName": self._configs["IoTJumpWayMQTTSettings"]["SystemApplicationName"],
				"username": self._configs["IoTJumpWayMQTTSettings"]["applicationUsername"],
				"password": self._configs["IoTJumpWayMQTTSettings"]["applicationPassword"]
			})

        except Exception as e:
            print(str(e))
            sys.exit()

        self.JumpWayMQTTClient.connectToApplication()

    def processFrame(self,camera,camID,camSensorID,camZone):

        while True:

            frame =  camera.readIpCamFrame()

            if frame is  None:

                continue

            frame = self.TassTools.resize(frame)
            currentImage,detected = self.TassClassifier.openCVDetect(frame)

            if detected is not  None:

                currentImage = cv2.imread(currentImage)
                persons, confidences = self.TassClassifier.classify(currentImage," ","CV")

                if len(confidences):

                    print "P: " + str(persons) + " C: " + str(confidences)

                else:

                    self.TassClassifier.moveNotIdentified(frame)

                    print "Unable To Classify Frame "

                for i, c in enumerate(confidences):

                    if persons[i] == "unknown":

                        self.JumpWayMQTTClient.publishToDeviceChannel(
                            "Sensors",
                            camZone,
                            camID,
                            {
                                "Sensor":"CCTV",
                                "SensorID": camSensorID,
                                "SensorValue":"Intruder"
                            }
                        )

                        self.JumpWayMQTTClient.publishToDeviceChannel(
                            "Warnings",
                            camZone,
                            camID,
                            {
                                "WarningType":"CCTV",
                                "WarningOrigin": camSensorID,
                                "WarningValue":"Intruder",
                                "WarningMessage":"An intruder has been detected"
                            }
                        )

                        self.TassClassifier.moveNotIdentified(frame)

                        print "Unknown Person Detected With Confidence " + str(c)

                    elif persons[i] != "":

                        self.JumpWayMQTTClient.publishToDeviceChannel(
                            "Sensors",
                            camZone,
                            camID,
                            {
                                "Sensor":"CCTV",
                                "SensorID": camSensorID,
                                "SensorValue":persons[i]
                            }
                        )

                        self.JumpWayMQTTClient.publishToDeviceChannel(
                            "Warnings",
                            camZone,
                            camID,
                            {
                                "WarningType":"CCTV",
                                "WarningOrigin": camSensorID,
                                "WarningValue":persons[i],
                                "WarningMessage":"User " + str(persons[i]) + " detected with confidence: " + str(c)
                            }
                        )

                        self.TassClassifier.moveIdentified(frame)

                        print str(persons[i])+" Detected With Confidence " + str(c)

            else:

                dlframe = cv2.flip(frame, 1)
                currentImage,detected = self.TassClassifier.dlibDetect(dlframe)

                if detected is not  None:

                    for face in detected:

                        persons, confidences = self.TassClassifier.classify(dlframe,face,"CV")

                        if len(confidences):

                            print "P: " + str(persons) + " C: " + str(confidences)

                        else:

                            self.TassClassifier.moveNotIdentified(frame)

                            print "Unable To Classify Frame "

                    for i, c in enumerate(confidences):

                        if persons[i] == "unknown":

                            self.JumpWayMQTTClient.publishToDeviceChannel(
                                "Sensors",
                                camZone,
                                camID,
                                {
                                    "Sensor":"CCTV",
                                    "SensorID": camSensorID,
                                    "SensorValue":"Intruder"
                                }
                            )

                            self.JumpWayMQTTClient.publishToDeviceChannel(
                                "Warnings",
                                camZone,
                                camID,
                                {
                                    "WarningType":"CCTV",
                                    "WarningOrigin": camSensorID,
                                    "WarningValue":"Intruder",
                                    "WarningMessage":"An intruder has been detected"
                                }
                            )

                            self.TassClassifier.moveNotIdentified(frame)

                            print "Unknown Person Detected With Confidence " + str(c)

                        elif persons[i] != "":

                            self.JumpWayMQTTClient.publishToDeviceChannel(
                                "Sensors",
                                camZone,
                                camID,
                                {
                                    "Sensor":"CCTV",
                                    "SensorID": camSensorID,
                                    "SensorValue":persons[i]
                                }
                            )

                            self.JumpWayMQTTClient.publishToDeviceChannel(
                                "Warnings",
                                camZone,
                                camID,
                                {
                                    "WarningType":"CCTV",
                                    "WarningOrigin": camSensorID,
                                    "WarningValue":persons[i],
                                    "WarningMessage":"User " + str(persons[i]) + " detected with confidence: " + str(c)
                                }
                            )

                            self.TassClassifier.moveIdentified(frame)

                            print str(persons[i])+" Detected With Confidence " + str(c)

TassCore = TassCore()