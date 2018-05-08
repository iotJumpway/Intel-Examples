############################################################################################
# Title: ASL Classification Classifier
# Description: Test classification of local testing images.
# Acknowledgements: Uses code from Intel movidius/ncsdk (https://github.com/movidius/ncsdk)
# Last Modified: 2018-05-06
############################################################################################

############################################################################################
#
#    CLASSIFIER MODE:
#
#       Classifier & IoT JumpWay configuration can be found in ../required/confs.json
#
#    Example Usage:
#
#        $ python3.5 Classifier.py InceptionTest
#
############################################################################################

print("")
print("")
print("!! Welcome to the ASL Classification Classifier, please wait while the program initiates !!")
print("")

import os, sys

print("-- Running on Python "+sys.version)
print("")

import time,csv,getopt,json,time, cv2

import numpy as np
import JumpWayMQTT.Device as JWMQTTdevice

from mvnc import mvncapi as mvnc
from tools.Helpers import Helpers
from datetime import datetime
from skimage.transform import resize

print("-- Imported Required Modules")
print("")

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
        self.reqsize = None

        self.extensions = [
            ".jpg",
            ".png"
        ]

        self.CheckDevices()
        self.Helpers = Helpers()
        self._configs = self.Helpers.loadConfigs()
        self.startMQTT()

        print("")
        print("-- Classifier Initiated")
        print("")

    def CheckDevices(self):

        #mvnc.SetGlobalOption(mvnc.GlobalOption.LOGLEVEL, 2)
        devices = mvnc.EnumerateDevices()
        if len(devices) == 0:
            print('!! WARNING! No Movidius Devices Found !!')
            quit()

        self.movidius = mvnc.Device(devices[0])
        self.movidius.OpenDevice()

        print("-- Movidius Connected")

    def allocateGraph(self,graphfile):

        self.graph = self.movidius.AllocateGraph(graphfile)

    def loadInceptionRequirements(self):

        self.reqsize = self._configs["ClassifierSettings"]["image_size"]

        with open(self._configs["ClassifierSettings"]["NetworkPath"] + self._configs["ClassifierSettings"]["InceptionGraph"], mode='rb') as f:

            self.graphfile = f.read()

        self.allocateGraph(self.graphfile)

        print("-- Allocated Graph OK")

        with open(self._configs["ClassifierSettings"]["NetworkPath"] + 'model/classes.txt', 'r') as f:

            for line in f:

                cat = line.split('\n')[0]

                if cat != 'classes':

                    self.categories.append(cat)

            f.close()

        print("-- Categories Loaded OK:", len(self.categories))

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

def main(argv):

    if argv[0] == "InceptionTest":

        humanStart = datetime.now()
        clockStart = time.time()

        print("-- INCEPTION V3 TEST MODE STARTING ")
        print("-- STARTED: : ", humanStart)
        print("")

        Classifier.loadInceptionRequirements()

        rootdir= Classifier._configs["ClassifierSettings"]["NetworkPath"] + Classifier._configs["ClassifierSettings"]["InceptionImagePath"]

        files = 0
        identified = 0
        correct = 0
        incorrect = []

        map_characters = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'del', 27: 'nothing', 28: 'space'}

        for file in os.listdir(rootdir):

            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png') or file.endswith('.gif'):

                files = files + 1
                fileName = rootdir+file

                print("")
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

                print("-- DETECTION STARTED: ", detectionStart)

                Classifier.graph.LoadTensor(img.astype(np.float16), 'user object')
                output, userobj = Classifier.graph.GetResult()

                top_inds = output.argsort()[::-1][:5]

                detectionEnd = datetime.now()
                detectionClockEnd = time.time()

                print("-- DETECTION ENDED: ", detectionEnd)
                print("-- DETECTION TIME: {0}".format(detectionClockEnd - detectionClockStart))

                if output[top_inds[0]] > Classifier._configs["ClassifierSettings"]["InceptionThreshold"]:

                    identified = identified + 1

                    if map_characters[top_inds[0]]+".jpg" == file:

                        isRight = "CORRECTLY"
                        correct = correct + 1

                    else:
                        
                        isRight = "INCORRECTLY"
                        incorrect.append(currentDir+"/"+file)

                    print("-- "+isRight+" DETECTED: "+map_characters[top_inds[0]])
                    print("")

                #print(top_inds)
                #print(Classifier.categories)

                print("".join(['*' for i in range(79)]))
                print('inception-v3 on NCS')
                print("".join(['*' for i in range(79)]))

                for i in range(2):

                    print(top_inds[i], Classifier.categories[top_inds[i]], output[top_inds[i]])

                print("".join(['*' for i in range(79)]))

        humanEnd = datetime.now()
        clockEnd = time.time()

        print("")
        print("-- INCEPTION V3 TEST MODE ENDING")
        print("-- ENDED: ", humanEnd)
        print("-- TIME(secs): {0}".format(clockEnd - clockStart))
        print("-- TESTED: ", files)
        print("-- IDENTIFIED: ", identified)
        print("-- CORRECT: ", correct)
        print("-- INCORRECT: ")
        print(json.dumps(incorrect, sort_keys=True, indent=4))
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