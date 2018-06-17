############################################################################################
# Title: Intel AI DevJam IDC Demo Classifier
# Description: Test classification of local IDC & facial recognition testing images.
# Acknowledgements: Uses code from Intel movidius/ncsdk (https://github.com/movidius/ncsdk)
# Last Modified: 2018-06-09
############################################################################################

############################################################################################
#
# CLASSIFIER MODE:
#
#   Classifier & IoT JumpWay configuration can be found in required/confs.json
#
# Example Usage:
#
#   $ python3.5 Classifier.py Inception
#   $ python3.5 Classifier.py Facenet
#
############################################################################################

############################################################################################
#
# The MIT License (MIT)
# 
# Intel AI DevJam IDC Demo Classifier
# Copyright (C) 2018 Adam Milton-Barker (AdamMiltonBarker.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
############################################################################################

print("")
print("")
print("!! Welcome to the Intel AI DevJam Classifier, please wait while the program initiates !!")
print("")

import os, sys

print("-- Running on Python "+sys.version)

import time,csv,getopt,json,time, cv2
import numpy as np

import JumpWayMQTT.Device as JWMQTTdevice
from tools.Helpers import Helpers
from tools.OpenCV import OpenCVHelpers as OpenCVHelpers
from tools.Facenet import FacenetHelpers

from datetime import datetime
from mvnc import mvncapi as mvnc
from skimage.transform import resize

print("-- Imported Required Modules")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["OMP_NUM_THREADS"] = "12"
os.environ["KMP_BLOCKTIME"] = "30"
os.environ["KMP_SETTINGS"] = "1"
os.environ["KMP_AFFINITY"]= "granularity=fine,verbose,compact,1,0"

print("-- Setup Environment Settings")

class Classifier():

    def __init__(self):

        self._configs = {}
        self.movidius = None
        self.jumpwayClient = None
        self.cameraStream = None
        self.imagePath = None

        self.mean = 128
        self.std = 1/128

        self.categories = []
        self.graphfile = None
        self.graph = None
        self.fgraphfile = None
        self.fgraph = None
        self.reqsize = None

        self.CheckDevices()
        self.Helpers = Helpers()
        self._configs = self.Helpers.loadConfigs()
        self.startMQTT()
        
        print("-- Classifier Initiated")

    def CheckDevices(self):

        #mvnc.SetGlobalOption(mvnc.GlobalOption.LOGLEVEL, 2)
        devices = mvnc.EnumerateDevices()
        if len(devices) == 0:
            print('!! WARNING! No Movidius Devices Found !!')
            quit()

        self.movidius = mvnc.Device(devices[0])
        self.movidius.OpenDevice()

        print("-- Movidius Connected")

    def allocateGraph(self,graphfile,graphID):

        if graphID == "IDC":

            self.graph = self.movidius.AllocateGraph(graphfile)

        elif graphID == "Facenet":

            self.fgraph = self.movidius.AllocateGraph(graphfile)

    def loadRequirements(self,graphID):

        if graphID == "IDC":

            self.reqsize = self._configs["ClassifierSettings"]["image_size"]

            with open(self._configs["ClassifierSettings"]["NetworkPath"] + self._configs["ClassifierSettings"]["InceptionGraph"], mode='rb') as f:

                self.graphfile = f.read()
                print("-- Allocated Inception V3 Graph OK")

            self.allocateGraph(self.graphfile,"IDC")

        elif graphID == "Facenet":

            with open(self._configs["ClassifierSettings"]["NetworkPath"] + self._configs["ClassifierSettings"]["Graph"], mode='rb') as f:

                self.fgraphfile = f.read()
                print("-- Allocated Facenet Graph OK")

            self.allocateGraph(self.fgraphfile,"Facenet")

        with open(self._configs["ClassifierSettings"]["NetworkPath"] + 'model/classes.txt', 'r') as f:

            for line in f:

                cat = line.split('\n')[0]

                if cat != 'classes':

                    self.categories.append(cat)

            f.close()

        print("-- IDC Categories Loaded OK:", len(self.categories))

    def startMQTT(self):

        try:

            self.jumpwayClient = JWMQTTdevice.DeviceConnection({
                "locationID": self._configs["IoTJumpWay"]["Location"],
                "zoneID": self._configs["IoTJumpWay"]["Zone"],
                "deviceId": self._configs["IoTJumpWay"]["Device"],
                "deviceName": self._configs["IoTJumpWay"]["DeviceName"],
                "username": self._configs["IoTJumpWayMQTT"]["MQTTUsername"],
                "password": self._configs["IoTJumpWayMQTT"]["MQTTPassword"]
            })

        except Exception as e:
            print(str(e))
            sys.exit()

        self.jumpwayClient.connectToDevice()

        print("-- IoT JumpWay Initiated")

Classifier = Classifier()
FacenetHelpers = FacenetHelpers()

def main(argv):

    if argv[0] == "Facenet":

        Classifier.loadRequirements(argv[0])

        humanStart = datetime.now()
        clockStart = time.time()

        print("-- FACENET TEST MODE STARTING ")
        print("-- STARTED: ", humanStart)

        validDir    = Classifier._configs["ClassifierSettings"]["NetworkPath"] + Classifier._configs["ClassifierSettings"]["ValidPath"]
        testingDir  = Classifier._configs["ClassifierSettings"]["NetworkPath"] + Classifier._configs["ClassifierSettings"]["TestingPath"]

        files = 0
        identified = 0

        for test in os.listdir(testingDir):
            
                if test.endswith('.jpg') or test.endswith('.jpeg') or test.endswith('.png') or test.endswith('.gif'):
                    #print(testingDir+test)

                    test_output = FacenetHelpers.infer(cv2.imread(testingDir+test), Classifier.fgraph)
                    files = files + 1

                    for valid in os.listdir(validDir):

                            if valid.endswith('.jpg') or valid.endswith('.jpeg') or valid.endswith('.png') or valid.endswith('.gif'):

                                valid_output = FacenetHelpers.infer(cv2.imread(validDir+valid), Classifier.fgraph)

                                if (FacenetHelpers.match(valid_output, test_output)):
                                    identified = identified + 1
                                    print("-- MATCH "+test)

                                    Classifier.jumpwayClient.publishToDeviceChannel(
                                        "Warnings",
                                        {
                                            "WarningType":"CCTV",
                                            "WarningOrigin": Classifier._configs["Cameras"][0]["ID"],
                                            "WarningValue": "RECOGNISED",
                                            "WarningMessage":test.rsplit( ".", 1 )[ 0 ]+" Detected"
                                        }
                                    )
                                    break
                                else:
                                    
                                    print("-- NO MATCH")

                                    Classifier.jumpwayClient.publishToDeviceChannel(
                                        "Warnings",
                                        {
                                            "WarningType":"CCTV",
                                            "WarningOrigin": Classifier._configs["Cameras"][0]["ID"],
                                            "WarningValue": "INTRUDER",
                                            "WarningMessage":"INTRUDER"
                                        }
                                    )

        humanEnd = datetime.now()
        clockEnd = time.time()

        print("")
        print("-- FACENET TEST MODE ENDING")
        print("-- ENDED: ", humanEnd)
        print("-- TESTED: ", files)
        print("-- IDENTIFIED: ", identified)
        print("-- TIME(secs): {0}".format(clockEnd - clockStart))
        print("")
        print("!! SHUTTING DOWN !!")
        print("")

        Classifier.fgraph.DeallocateGraph()
        Classifier.movidius.CloseDevice()

    elif argv[0] == "Inception":

        Classifier.loadRequirements("IDC")

        humanStart = datetime.now()
        clockStart = time.time()

        print("-- INCEPTION V3 TEST MODE STARTED: : ", humanStart)

        rootdir= Classifier._configs["ClassifierSettings"]["NetworkPath"] + Classifier._configs["ClassifierSettings"]["InceptionImagePath"]

        files = 0
        identified = 0

        for file in os.listdir(rootdir):

            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png') or file.endswith('.gif'):

                files = files + 1
                fileName = rootdir+file

                print("-- Loaded Test Image", fileName)
                img = cv2.imread(fileName).astype(np.float32)

                dx,dy,dz= img.shape
                delta=float(abs(dy-dx))

                if dx > dy:

                    img=img[int(0.5*delta):dx-int(0.5*delta),0:dy]

                else:

                    img=img[0:dx,int(0.5*delta):dy-int(0.5*delta)]

                img = cv2.resize(img, (Classifier.reqsize, Classifier.reqsize))
                img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

                for i in range(3):

                    img[:,:,i] = (img[:,:,i] - Classifier.mean) * Classifier.std

                detectionStart = datetime.now()
                detectionClockStart = time.time()

                print("-- DETECTION STARTING ")
                print("-- STARTED: : ", detectionStart)

                Classifier.graph.LoadTensor(img.astype(np.float16), 'user object')
                output, userobj = Classifier.graph.GetResult()

                top_inds = output.argsort()[::-1][:5]

                detectionEnd = datetime.now()
                detectionClockEnd = time.time()

                print("-- DETECTION ENDING")
                print("-- ENDED: ", detectionEnd)
                print("-- TIME: {0}".format(detectionClockEnd - detectionClockStart))

                if output[top_inds[0]] > Classifier._configs["ClassifierSettings"]["InceptionThreshold"] and Classifier.categories[top_inds[0]] == "1":

                    identified = identified + 1

                    print("")
                    print("!! TASS Identified IDC with a confidence of", str(output[top_inds[0]]))
                    print("")

                    Classifier.jumpwayClient.publishToDeviceChannel(
                            "Warnings",
                            {
                                "WarningType":"CCTV",
                                "WarningOrigin": Classifier._configs["Cameras"][0]["ID"],
                                "WarningValue": "RECOGNISED",
                                "WarningMessage":"IDC Detected"
                            }
                        )

                    print("")

                else:

                    print("")
                    print("!! TASS Did Not Identify IDC")
                    print("")

                    Classifier.jumpwayClient.publishToDeviceChannel(
                        "Warnings",
                        {
                            "WarningType":"CCTV",
                            "WarningOrigin": Classifier._configs["Cameras"][0]["ID"],
                            "WarningValue": "NOT RECOGNISED",
                            "WarningMessage":"IDC Not Detected"
                        }
                    )

                    print("")

                Classifier.jumpwayClient.publishToDeviceChannel(
                    "Sensors",
                    {
                        "Sensor":"CCTV",
                        "SensorID": Classifier._configs["Cameras"][0]["ID"],
                        "SensorValue":"IDC: " + Classifier.categories[top_inds[0]] + " (Confidence: " + str(output[top_inds[0]]) + ")"
                    }
                )

        humanEnd = datetime.now()
        clockEnd = time.time()

        print("")
        print("-- INCEPTION V3 TEST MODE ENDING")
        print("-- ENDED: ", humanEnd)
        print("-- TESTED: ", files)
        print("-- IDENTIFIED: ", identified)
        print("-- TIME(secs): {0}".format(clockEnd - clockStart))
        print("")

        print("!! SHUTTING DOWN !!")
        print("")

        Classifier.graph.DeallocateGraph()
        Classifier.movidius.CloseDevice()

    else:

        print("**ERROR** Check Your Commandline Arguments")
        print("")

if __name__ == "__main__":

	main(sys.argv[1:])