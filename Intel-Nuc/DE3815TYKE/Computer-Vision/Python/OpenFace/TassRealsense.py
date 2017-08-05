########################################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
########################################################################################
# Module: TassRealsense.py
# Description: Processes frames from a Realsense camera.
# Acknowledgements: Uses code from pyrealsense (https://github.com/toinsson/pyrealsense)
# Last Modified: 8.3.2017
########################################################################################

import logging
logging.basicConfig(level=logging.INFO)

import cv2
import pyrealsense as pyrs

from TassTools import TassTools
from TassClassifier import TassClassifier

class TassRealsense():

    def __init__(self):

        self.TassTools = TassTools()
        self.TassClassifier = TassClassifier(1)

        realsenseDevice = 0
        framesPerSecond = 30

        serv = pyrs.Service()
        realsense = serv.Device(device_id = realsenseDevice, streams = [pyrs.stream.ColorStream(fps = framesPerSecond)])

        self.processFrame(realsense)

    def processFrame(self,realsense):

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

                        print "Unable To Classify Frame "

                for i, c in enumerate(confidences):

                    if persons[i] == "unknown":

                        print "Unknown Person Detected With Confidence " + str(c)

                    elif persons[i] != "":

                        print str(persons[i])+" Detected With Confidence " + str(c)

            else:

                dlframe = cv2.flip(frame, 1)
                currentImage,detected = self.TassClassifier.dlibDetect(dlframe)

                if detected is not  None:

                    for face in detected:

                        persons, confidences = self.TassClassifier.classify(dlframe,face,"Dlib")

                        if len(confidences):

                            print "P: " + str(persons) + " C: " + str(confidences)

                        else:

                            print "Unable To Classify Frame "

                    for i, c in enumerate(confidences):

                        if persons[i] == "unknown":

                            print "Unknown Person Detected With Confidence " + str(c)

                        elif persons[i] != "":

                            print str(persons[i])+" Detected With Confidence " + str(c)

TassRealsense = TassRealsense()