########################################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
# Copyright 2017, Adam Milton-Barker, TechBubble Technologies, All rights reserved.
########################################################################################
# Module: TassTest.py
# Description: Tests a trained TASS computer vision model.
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