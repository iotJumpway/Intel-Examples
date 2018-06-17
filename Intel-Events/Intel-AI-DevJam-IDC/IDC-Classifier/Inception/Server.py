############################################################################################
# Title: Intel AI DevJam IDC Demo Classification Server
# Description: Serves an API for classification of both IDC & facial recognition images.
#
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
#   $ python3.5 Server.py IDC
#   $ python3.5 Server.py TASS
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
print("!! Welcome to Intel AI DevJam Classification Server, please wait while the program initiates !!")
print("")

import os, sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

print("-- Running on Python "+sys.version)

import time, csv, getopt, json, time, jsonpickle, cv2
import numpy as np

import JumpWayMQTT.Device as JWMQTTdevice
from tools.Helpers import Helpers
from tools.OpenCV import OpenCVHelpers as OpenCVHelpers
from tools.Facenet import FacenetHelpers

from datetime import datetime
from flask import Flask, request, Response
from mvnc import mvncapi as mvnc
from skimage.transform import resize

print("-- Imported Required Modules")

print("-- API Initiating ")
app = Flask(__name__)
print("-- API Intiated ")

class Server():

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

    def allocateGraph(self, graphfile, graphID):

        if graphID == "IDC":

            self.graph = self.movidius.AllocateGraph(graphfile)

        elif graphID == "TASS":

            self.fgraph = self.movidius.AllocateGraph(graphfile)

    def loadRequirements(self, graphID):

        if graphID == "IDC":

            self.reqsize = self._configs["ClassifierSettings"]["image_size"]

            with open(self._configs["ClassifierSettings"]["NetworkPath"] + self._configs["ClassifierSettings"]["InceptionGraph"], mode='rb') as f:

                self.graphfile = f.read()

            self.allocateGraph(self.graphfile,"IDC")
            print("-- Allocated IDC Graph OK")

            with open(self._configs["ClassifierSettings"]["NetworkPath"] + 'model/classes.txt', 'r') as f:

                for line in f:

                    cat = line.split('\n')[0]

                    if cat != 'classes':

                        self.categories.append(cat)

                f.close()

            print("-- IDC Categories Loaded OK:", len(self.categories))

        elif graphID == "TASS":

            with open(self._configs["ClassifierSettings"]["NetworkPath"] + self._configs["ClassifierSettings"]["Graph"], mode='rb') as f:

                self.fgraphfile = f.read()

            self.allocateGraph(self.fgraphfile,"TASS")
            print("-- Allocated TASS Graph OK")

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

Server = Server()
FacenetHelpers = FacenetHelpers()

@app.route('/api/TASS/infer', methods=['POST'])
def TASSinference():
    
    Server.CheckDevices()
    Server.loadRequirements("TASS")

    humanStart = datetime.now()
    clockStart = time.time()

    print("-- FACENET LIVE INFERENCE STARTED: ", humanStart)

    r = request
    nparr = np.fromstring(r.data, np.uint8)

    print("-- Loading Face")
    fileName = "data/captured/TASS/"+str(clockStart)+'.png'
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    cv2.imwrite(fileName,img)
    img = cv2.imread(fileName).astype(np.float32)
    print("-- Loaded Sample")

    validDir    = Server._configs["ClassifierSettings"]["NetworkPath"] + Server._configs["ClassifierSettings"]["ValidPath"]
    testingDir  = Server._configs["ClassifierSettings"]["NetworkPath"] + Server._configs["ClassifierSettings"]["TestingPath"]

    files = 0
    identified = 0

    test_output = FacenetHelpers.infer(img, Server.fgraph)
    files = files + 1

    for valid in os.listdir(validDir):

        if valid.endswith('.jpg') or valid.endswith('.jpeg') or valid.endswith('.png') or valid.endswith('.gif'):

            valid_output = FacenetHelpers.infer(cv2.imread(validDir+valid), Server.fgraph)
            known, confidence = FacenetHelpers.match(valid_output, test_output)
            if (known=="True"):
                identified = identified + 1
                print("-- MATCH "+valid)
                break

    if identified:

        Server.jumpwayClient.publishToDeviceChannel(
            "Warnings",
            {
                "WarningType":"CCTV",
                "WarningOrigin": Server._configs["Cameras"][0]["ID"],
                "WarningValue": "RECOGNISED",
                "WarningMessage":valid + " Detected With Confidence " + str(confidence)
            }
        )

    else:

        Server.jumpwayClient.publishToDeviceChannel(
            "Warnings",
            {
                "WarningType":"CCTV",
                "WarningOrigin": Server._configs["Cameras"][0]["ID"],
                "WarningValue": "INTRUDER",
                "WarningMessage": " Intruder Detected With Confidence " + str(confidence)
            }
        )

    humanEnd = datetime.now()
    clockEnd = time.time()

    Server.fgraph.DeallocateGraph()
    Server.movidius.CloseDevice()

    print("")
    print("-- FACENET LIVE INFERENCE ENDED: ", humanEnd)
    print("-- TESTED: ", 1)
    print("-- IDENTIFIED: ", identified)
    print("-- TIME(secs): {0}".format(clockEnd - clockStart))
    print("")

    if identified:

        validPerson = os.path.splitext(valid)[0]

        message = validPerson +" Detected With Confidence " + str(confidence)
        person = validPerson

    else:

        message = "Intruder Detected With Confidence " + str(confidence)
        person = "Intruder"

    response = {
        'Response': 'OK',
        'Results': identified,
        'Person': person,
        'Confidence': confidence,
        'ResponseMessage': message
    }

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/IDC/infer', methods=['POST'])
def IDCinference():
        
    Server.CheckDevices()
    Server.loadRequirements("IDC")

    humanStart = datetime.now()
    clockStart = time.time()

    print("-- INCEPTION V3 IDC INFERENCE STARTED: ", humanStart)
    print("")

    r = request
    nparr = np.fromstring(r.data, np.uint8)

    print("-- Loading Sample")
    fileName = "data/captured/IDC/"+str(clockStart)+'.png'
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    cv2.imwrite(fileName,img)
    img = cv2.imread(fileName).astype(np.float32)
    print("-- Loaded Sample")

    dx,dy,dz= img.shape
    delta=float(abs(dy-dx))

    if dx > dy:

        img=img[int(0.5*delta):dx-int(0.5*delta),0:dy]

    else:

        img=img[0:dx,int(0.5*delta):dy-int(0.5*delta)]

    img = cv2.resize(img, (Server.reqsize, Server.reqsize))
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    for i in range(3):

        img[:,:,i] = (img[:,:,i] - Server.mean) * Server.std

    detectionStart = datetime.now()
    detectionClockStart = time.time()

    print("-- IDC DETECTION STARTED: : ", detectionStart)
    print("")

    Server.graph.LoadTensor(img.astype(np.float16), 'user object')
    output, userobj = Server.graph.GetResult()

    top_inds = output.argsort()[::-1][:5]

    detectionEnd = datetime.now()
    detectionClockEnd = time.time()

    identified = 0

    print("-- IDC DETECTION ENDED: ", detectionEnd)
    print("-- TIME: {0}".format(detectionClockEnd - detectionClockStart))

    print("OUTPUT: " + str(output[top_inds[0]]))
    print("THRESHOLD: " + str(Server._configs["ClassifierSettings"]["InceptionThreshold"]))
    print("")

    if output[top_inds[0]] > Server._configs["ClassifierSettings"]["InceptionThreshold"] and Server.categories[top_inds[0]] == "1":
        identified = identified + 1

        print("!! TASS Identified IDC with a confidence of", str(output[top_inds[0]]))

        Server.jumpwayClient.publishToDeviceChannel(
                "Warnings",
                {
                    "WarningType":"CCTV",
                    "WarningOrigin": Server._configs["Cameras"][0]["ID"],
                    "WarningValue": "RECOGNISED",
                    "WarningMessage":"IDC Detected With Confidence " + str(output[top_inds[0]])
                }
            )

        print("")

    else:

        print("!! TASS Did Not Identify IDC")

        Server.jumpwayClient.publishToDeviceChannel(
                "Warnings",
                {
                    "WarningType":"CCTV",
                    "WarningOrigin": Server._configs["Cameras"][0]["ID"],
                    "WarningValue": "NOT RECOGNISED",
                    "WarningMessage":"IDC Not Detected With Confidence " + str(output[top_inds[0]])
                }
            )


    Server.jumpwayClient.publishToDeviceChannel(
            "Sensors",
            {
                "Sensor":"CCTV",
                "SensorID": Server._configs["Cameras"][0]["ID"],
                "SensorValue":"IDC: " + Server.categories[top_inds[0]] + " (Confidence: " + str(output[top_inds[0]]) + ")"
            }
        )

    #print(top_inds)
    #print(Server.categories)

    Server.graph.DeallocateGraph()
    Server.movidius.CloseDevice()

    humanEnd = datetime.now()
    clockEnd = time.time()

    print("")
    print("-- INCEPTION V3 LIVE INFERENCE ENDING")
    print("-- ENDED: ", humanEnd)
    print("-- TESTED: ", 1)
    print("-- IDENTIFIED: ", identified)
    print("-- TIME(secs): {0}".format(clockEnd - clockStart))
    print("")

    if identified:

        message = "IDC Detected With Confidence " + str(output[top_inds[0]])

    else:

        message = "IDC Not Detected With Confidence " + str(output[top_inds[0]])

    response = {
        'Response': 'OK',
        'Results': identified,
        'Confidence': str(output[top_inds[0]]),
        'ResponseMessage': message
    }

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == "__main__":
        
    app.run(host=Server._configs["Cameras"][0]["Stream"], port=Server._configs["Cameras"][0]["StreamPort"])
