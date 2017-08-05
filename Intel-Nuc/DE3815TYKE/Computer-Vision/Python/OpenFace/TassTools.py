########################################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
########################################################################################
# Module: TassTools.py
# Description: Tool functions.
# Acknowledgements: Uses code from openface (https://github.com/cmusatyalab/openface)
# Last Modified: 8.3.2017
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
