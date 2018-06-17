############################################################################################
# Title: IoT JumpWay Helpers
# Description: Helper functions for IoT JumpWay programs.
# Last Modified: 2018-06-09
############################################################################################

import os, json, cv2
from datetime import datetime

class Helpers():

    def __init__(self):

        pass

    def loadConfigs(self):

        with open("required/confs.json") as configs:

            _configs = json.loads(configs.read())

        return _configs

    def saveImage(self,networkPath,frame):

        timeDirectory =  networkPath + "data/captures/"+datetime.now().strftime('%Y-%m-%d')+'/'+datetime.now().strftime('%H')

        if not os.path.exists(timeDirectory):
            os.makedirs(timeDirectory)

        currentImage=timeDirectory+'/'+datetime.now().strftime('%M-%S')+'.jpg'
        print(currentImage)
        print("")

        cv2.imwrite(currentImage, frame)

        return currentImage