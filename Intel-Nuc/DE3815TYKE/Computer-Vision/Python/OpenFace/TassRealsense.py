########################################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
# Copyright 2017, Adam Milton-Barker, TechBubble Technologies, All rights reserved.
########################################################################################
# Module: TassRealsense.py
# Description: Processes frames from a Realsense camera.
# Acknowledgements: Uses code from pyrealsense (https://github.com/toinsson/pyrealsense)
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


import logging
logging.basicConfig(level=logging.INFO)

import cv2
import pyrealsense as pyrs
import sys
import json

from TassTools import TassTools
from TassClassifier import TassClassifier

from techbubbleiotjumpwaymqtt.application import JumpWayPythonMQTTApplicationConnection

class TassRealsense():

    def __init__(self):

        self.JumpWayMQTTClient = ""

        self.TassTools = TassTools()
        self.TassClassifier = TassClassifier(1)

        self._configs = {}

        with open('config.json') as configs:

            self._configs = json.loads(configs.read())

        framesPerSecond = 30

        serv = pyrs.Service()
        realsense = serv.Device(device_id = self._configs["RealsenseCam"]["localCamID"], streams = [pyrs.stream.ColorStream(fps = framesPerSecond)])

        self.startMQTT()
        self.processFrame(realsense,self._configs["RealsenseCam"]["camID"],self._configs["RealsenseCam"]["camZone"],self._configs["RealsenseCam"]["camSensorID"])

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

    def processFrame(self,realsense,realsenseID,realsenseZone,realsenseSensor):

        realsense.apply_ivcam_preset(0)

        while True:

            realsense.wait_for_frames()

            frame = self.TassTools.resize(cv2.cvtColor(realsense.color, cv2.COLOR_RGB2BGR))
            currentImage,detected = self.TassClassifier.openCVDetect(frame)

            if detected is not  None:

                for face in detected:

                    persons, confidences = self.TassClassifier.classify(frame,face,"CV")

                    if len(confidences):

                        print "P: " + str(persons) + " C: " + str(confidences)

                    else:

                        self.TassClassifier.moveNotIdentified(frame)

                        print "Unable To Classify Frame "

                for i, c in enumerate(confidences):

                    if persons[i] == "unknown":

                        self.JumpWayMQTTClient.publishToDeviceChannel(
                            "Sensors",
                            realsenseZone,
                            realsenseID,
                            {
                                "Sensor":"CCTV",
                                "Sensors": realsenseSensor,
                                "SensorValue":"Intruder"
                            }
                        )

                        self.JumpWayMQTTClient.publishToDeviceChannel(
                            "Warnings",
                            realsenseZone,
                            realsenseID,
                            {
                                "WarningType":"CCTV",
                                "WarningOrigin": realsenseSensor,
                                "WarningValue":"Intruder",
                                "WarningMessage":"An intruder has been detected"
                            }
                        )

                        self.TassClassifier.moveNotIdentified(frame)

                        print "Unknown Person Detected With Confidence " + str(c)

                    elif persons[i] != "":

                        self.JumpWayMQTTClient.publishToDeviceChannel(
                            "Sensors",
                            realsenseZone,
                            realsenseID,
                            {
                                "Sensor":"CCTV",
                                "Sensors": realsenseSensor,
                                "SensorValue":persons[i]
                            }
                        )

                        self.JumpWayMQTTClient.publishToDeviceChannel(
                            "Warnings",
                            realsenseZone,
                            realsenseID,
                            {
                                "WarningType":"CCTV",
                                "WarningOrigin": realsenseSensor,
                                "WarningValue":persons[i],
                                "WarningMessage":"User " + str(persons[i]) + " detected with confidence: " + str(c)
                            }
                        )

                        self.TassClassifier.moveIdentified(frame)

                        print str(persons[i])+" Detected With Confidence " + str(c)

            else:

                #dlframe = cv2.flip(frame, 1)
                currentImage,detected = self.TassClassifier.dlibDetect(frame)

                if detected is not  None:

                    for face in detected:

                        persons, confidences = self.TassClassifier.classify(frame,face,"CV")

                        if len(confidences):

                            print "P: " + str(persons) + " C: " + str(confidences)

                        else:

                            self.TassClassifier.moveNotIdentified(frame)

                            print "Unable To Classify Frame "

                    for i, c in enumerate(confidences):

                        if persons[i] == "unknown":

                            self.JumpWayMQTTClient.publishToDeviceChannel(
                                "Sensors",
                                realsenseZone,
                                realsenseID,
                                {
                                    "Sensor":"CCTV",
                                    "Sensors": realsenseSensor,
                                    "SensorValue":"Intruder"
                                }
                            )

                            self.JumpWayMQTTClient.publishToDeviceChannel(
                                "Warnings",
                                realsenseZone,
                                realsenseID,
                                {
                                    "WarningType":"CCTV",
                                    "WarningOrigin": realsenseSensor,
                                    "WarningValue":"Intruder",
                                    "WarningMessage":"An intruder has been detected"
                                }
                            )

                            self.TassClassifier.moveNotIdentified(frame)

                            print "Unknown Person Detected With Confidence " + str(c)

                        elif persons[i] != "":

                            self.JumpWayMQTTClient.publishToDeviceChannel(
                                "Sensors",
                                realsenseZone,
                                realsenseID,
                                {
                                    "Sensor":"CCTV",
                                    "Sensors": realsenseSensor,
                                    "SensorValue":persons[i]
                                }
                            )

                            self.JumpWayMQTTClient.publishToDeviceChannel(
                                "Warnings",
                                realsenseZone,
                                realsenseID,
                                {
                                    "WarningType":"CCTV",
                                    "WarningOrigin": realsenseSensor,
                                    "WarningValue":persons[i],
                                    "WarningMessage":"User " + str(persons[i]) + " detected with confidence: " + str(c)
                                }
                            )

                            self.TassClassifier.moveIdentified(frame)

                            print str(persons[i])+" Detected With Confidence " + str(c)

TassRealsense = TassRealsense()