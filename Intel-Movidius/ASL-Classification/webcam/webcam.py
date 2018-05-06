############################################################################################
# Title: ASL Classifier Webam
# Description: Sends frames of a webcam to the node js server via sockets.
# Last Modified: 2018-05-05
############################################################################################

############################################################################################
#
#    Configuration:
#
#       Update your socket server configuration in ../required/confs.json 
#
############################################################################################

print("")
print("")
print("!! Welcome to the ASL Classifier Webcam, please wait while the program initiates !!")
print("")

import os, sys, cv2, logging, json

print("-- Running on Python "+sys.version)
print("")

from PIL import Image
from datetime import datetime
from datetime import timedelta
from socketIO_client import SocketIO

print("-- Imported Required Modules")
print("")

logging.basicConfig(level=logging.DEBUG)

print("-- Setup Logging")

class Webcam():
    
    def __init__(self):
        
        self.confs = {}
        self.nextCapture = datetime.now()
        
        with open('../required/confs.json') as confs:
            
            self.confs = json.loads(confs.read())
            
        try:
            
            self.OpenCVCapture = cv2.VideoCapture(self.confs["Cameras"][0]["URL"])
            self.socketIO = SocketIO(self.confs["Cameras"][0]["SocketIP"],self.confs["Cameras"][0]["SocketPort"])
            print("-- Connected to "+self.confs["Cameras"][0]["Name"])
            
        except Exception as e:
            print("!! FAILED TO CONNECT TO WEBCAM !!")
            print(str(e))
            sys.exit()

        print("")
        print("-- ASL Classifier Webcam Initiated")
        print("")

Webcam = Webcam()

while True:
    
    if Webcam.nextCapture <= datetime.now():
        
        Webcam.nextCapture = Webcam.nextCapture + timedelta(seconds=0.3) 
        ret, img = Webcam.OpenCVCapture.read()
        if not ret: continue

        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (20,450)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2

        cv2.putText(img,'ASL Classifier', 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)

        cv2.imwrite('../server/public/images/img.png', img)
        Webcam.socketIO.emit('newFrame')
