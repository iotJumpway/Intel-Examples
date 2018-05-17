
############################################################################################
# Title: OpenCV Helpers
# Description: Helper functions for OpenCV.
# Last Modified: 2018/02/21
############################################################################################

import os, json, cv2
import numpy as np
from datetime import datetime

class OpenCVHelpers():

    def __init__(self):

        pass

    def rect_to_bb(self, rect):
        # take a bounding predicted by dlib and convert it
        # to the format (x, y, w, h) as we would normally do
        # with OpenCV
        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y
    
        # return a tuple of (x, y, w, h)
        return (x, y, w, h)

    def shape_to_np(self, shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)
    
        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
    
        # return the list of (x, y)-coordinates
        return coords

    def whiten(self, source_image):
        source_mean = np.mean(source_image)
        source_standard_deviation = np.std(source_image)
        std_adjusted = np.maximum(source_standard_deviation, 1.0 / np.sqrt(source_image.size))
        whitened_image = np.multiply(np.subtract(source_image, source_mean), 1 / std_adjusted)
        return whitened_image

    def preprocess(self, src):
        # scale the image
        NETWORK_WIDTH = 160
        NETWORK_HEIGHT = 160
        preprocessed_image = cv2.resize(src, (NETWORK_WIDTH, NETWORK_HEIGHT))

        #convert to RGB
        preprocessed_image = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)

        #whiten
        preprocessed_image = self.whiten(preprocessed_image)

        # return the preprocessed image
        return preprocessed_image