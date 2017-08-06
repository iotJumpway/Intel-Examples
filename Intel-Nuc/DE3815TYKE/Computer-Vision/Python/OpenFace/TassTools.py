########################################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
# Copyright 2017, Adam Milton-Barker, TechBubble Technologies, All rights reserved.
########################################################################################
# Module: TassTools.py
# Description: Tool functions.
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

import cv2

class TassTools():

    def __init__(self):

        pass

    def preProcess(self,image):

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl1 = clahe.apply( cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

        return cl1

    def resize(self,frame):

        r = 640.0 / frame.shape[1]
        dim = (640, int(frame.shape[0] * r))
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

        return resized

    def convertRect(self,rect):

        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y

        return (x, y, w, h)
