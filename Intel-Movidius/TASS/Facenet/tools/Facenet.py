############################################################################################
# Title: Facenet Helpers
# Description: Helper functions for Facenet.
# Last Modified: 2018/02/21
############################################################################################

import os, json, cv2
import numpy as np
from datetime import datetime

from tools.OpenCV import OpenCVHelpers as OpenCVHelpers

class FacenetHelpers():
    
    def __init__(self):
        
        self.OpenCVHelpers = OpenCVHelpers()
        
    def infer(self, image_to_classify, facenet_graph):
        
        # get a resized version of the image that is the dimensions
        # SSD Mobile net expects
        resized_image = self.preprocess(image_to_classify)

        #cv2.imshow("preprocessed", resized_image)

        # ***************************************************************
        # Send the image to the NCS
        # ***************************************************************
        facenet_graph.LoadTensor(resized_image.astype(np.float16), None)

        # ***************************************************************
        # Get the result from the NCS
        # ***************************************************************
        output, userobj = facenet_graph.GetResult()

        #print("Total results: " + str(len(output)))
        #print(output)

        return output

    def match(self, face1_output, face2_output):
        if (len(face1_output) != len(face2_output)):
            print('-- Length mismatch in match')
            return False
        total_diff = 0
        for output_index in range(0, len(face1_output)):
            this_diff = np.square(face1_output[output_index] - face2_output[output_index])
            total_diff += this_diff
        print('-- Total Difference is: ' + str(total_diff))

        if (total_diff < 1.3):
            # the total difference between the two is under the threshold so
            # the faces match.
            return True

    # create a preprocessed image from the source image that matches the
    # network expectations and return it
    def preprocess(self, src):
        # scale the image
        NETWORK_WIDTH = 160
        NETWORK_HEIGHT = 160
        preprocessed_image = cv2.resize(src, (NETWORK_WIDTH, NETWORK_HEIGHT))

        #convert to RGB
        preprocessed_image = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)

        #whiten
        preprocessed_image = self.OpenCVHelpers.whiten(preprocessed_image)

        # return the preprocessed image
        return preprocessed_image