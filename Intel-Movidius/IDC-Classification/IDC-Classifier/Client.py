############################################################################################
# Title: IDC Classification Client
# Description: Client for sending histology slides to the IDC Classification server.
# Acknowledgements: Uses code from Intel movidius/ncsdk (https://github.com/movidius/ncsdk)
# Last Modified: 2018-04-21
############################################################################################

############################################################################################
#
#    CLASSIFIER MODE:
#
#       Classifier & IoT JumpWay configuration can be found in data/confs.json
#
#    Example Usage:
#
#        $ python3.5 Client.py
#
############################################################################################

print("")
print("")
print("!! Welcome to IDC Classification Client, please wait while the program initiates !!")
print("")

import os, sys

print("-- Running on Python "+sys.version)
print("")

import requests, json, cv2, time

print("-- Imported Required Modules")

class Client():

    def __init__(self):

        self.addr = 'http://localhost:7455'
        self.apiUrl = self.addr + '/api/infer'
        self.positive = 'model/test/positive.png'
        self.negative = 'model/test/negative.png'
        self.content_type = 'image/jpeg'
        self.headers = {'content-type': self.content_type}

        print("-- IDC Classification Client Initiated")

    def sendImage(self, image):

        img = cv2.imread(image)
        _, img_encoded = cv2.imencode('.png', img)
        response = requests.post(self.apiUrl, data=img_encoded.tostring(), headers=self.headers)

        print(json.loads(response.text))

Client = Client()
Client.sendImage(Client.positive)
time.sleep(5)
Client.sendImage(Client.negative)
time.sleep(5)