########################################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
########################################################################################
# Module: TassTest.py
# Description: Tests a trained TASS computer vision model.
# Acknowledgements: Uses code from openface (https://github.com/cmusatyalab/openface)
# Last Modified: 8.3.2017
########################################################################################

import os
import cv2
import time

from TassTools import TassTools
from TassClassifier import TassClassifier

TassTools = TassTools()
TassClassifier = TassClassifier(1)

for file in os.listdir("testing/"):

    newPayload = cv2.imread("testing/"+file)
    persons, confidences = TassClassifier.classify(newPayload," ","CV")
    print "SHOULD BE: " + os.path.splitext(os.path.basename("testing/"+file))[0]
    print "DETECTED: "+ str(persons[0]) + " With Confidence: " + str(confidences[0])
    if str(persons[0]) == "unknown":
        print("Intruder")
    else:
        print(str(persons[0]) + " " + str(confidences[0]))
    print("")

    time.sleep(5)