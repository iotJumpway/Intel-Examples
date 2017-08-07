########################################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
# Copyright 2017, Adam Milton-Barker, TechBubble Technologies, All rights reserved.
########################################################################################
# Module: TassClassifier.py
# Description: Detects & classifies faces in frames.
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

import time

import struct
import cv2
import dlib
import os
import fnmatch
import json
import pickle

import numpy as np
np.set_printoptions(precision=2)

from sklearn.mixture import GMM
import openface

from datetime import datetime
from scipy import spatial

from TassTools import TassTools

class TassClassifier():

    def __init__(self,model):

        self.TassTools = TassTools()

        self.model = model

        with open('config.json') as configs:

            self._configs = json.loads(configs.read())

        self.imgDim = self._configs["ClassifierSettings"]["imgDim"]
        self.threshold = self._configs["ClassifierSettings"]["threshold"]
        self.cuda = self._configs["ClassifierSettings"]["useCuda"]

        self.fileDir = os.path.dirname(os.path.abspath(__file__))
        self.modelsDir = self.fileDir+'/models'
        self.dlibModelDir = self.modelsDir+'/dlib'
        self.openfaceModelDir = self.modelsDir+'/openface'

        self.dlibFacePredictor = self.dlibModelDir+'/shape_predictor_68_face_landmarks.dat'
        self.networkModel = self.openfaceModelDir+'/nn4.small2.v1.t7'

        self.detector = dlib.get_frontal_face_detector()

        self.classifierModel = os.path.dirname(os.path.abspath(__file__)) + "/features/"+str(self.model)+"/classifier.pkl"

        self.faceCascade1 = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_FACES"])
        self.faceCascade2 = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_PROFILES"])
        self.faceCascade3 = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_FACES2"])
        self.faceCascade4 = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_FACES3"])
        self.faceCascade5 = cv2.CascadeClassifier( os.getcwd()+'/'+self._configs["ClassifierSettings"]["HAAR_PROFILES"])

        with open(self.classifierModel, 'r') as f:

            (self.le, self.clf) = pickle.load(f)

        self.align = openface.AlignDlib(self.dlibFacePredictor)
        self.net = openface.TorchNeuralNet(self.networkModel,imgDim=self.imgDim,cuda=self.cuda)

    def moveNotIdentified(self,frame):

        today = time.strftime("%Y-%m-%d-%H")

        if not os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/frames/'+today+'/notidentified/'):
            os.makedirs(os.path.dirname(os.path.abspath(__file__))+'/frames/'+today+'/notidentified/')

        fileName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.jpg'
        fileAddress=os.path.dirname(os.path.abspath(__file__))+'/frames/'+today+'/notidentified/'+fileName
        cv2.imwrite(fileAddress, frame)

    def moveIdentified(self,frame):

        today = time.strftime("%Y-%m-%d-%H")

        if not os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/frames/'+today+'/identified/'):
            os.makedirs(os.path.dirname(os.path.abspath(__file__))+'/frames/'+today+'/identified/')

        fileName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.jpg'
        fileAddress=os.path.dirname(os.path.abspath(__file__))+'/frames/'+today+'/identified/'+fileName
        cv2.imwrite(fileAddress, frame)

    def openCVDetect(self,frame):

        gray = self.TassTools.preProcess(frame)

        faces = self.faceCascade1.detectMultiScale(gray,
            scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
            minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if not len(faces):

            faces = self.faceCascade2.detectMultiScale(gray,
                scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                minSize=(30,30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

        if not len(faces):

            faces = self.faceCascade3.detectMultiScale(gray,
                scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                minSize=(30,30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

        if not len(faces):

            faces = self.faceCascade4.detectMultiScale(gray,
                scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                minSize=(30,30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

        if not len(faces):

            faces = self.faceCascade5.detectMultiScale(gray,
                scaleFactor=self._configs["ClassifierSettings"]["HAAR_SCALE_FACTOR"],
                minNeighbors=self._configs["ClassifierSettings"]["HAAR_MIN_NEIGHBORS"],
                minSize=(30,30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

        print( "OPENCV DETECTED " + str(len(faces)) + " FACES")

        if len(faces):

            newframe = frame.copy()

            today = time.strftime("%Y-%m-%d-%H")

            if not os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/frames/'+today+'/detected/'):
                os.makedirs(os.path.dirname(os.path.abspath(__file__))+'/frames/'+today+'/detected/')

            for (x, y, w, h) in faces:

                cv2.rectangle(newframe, (x, y), (x+w, y+h), (0, 255, 0), 2)

            fileName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.jpg'
            fileAddress=os.path.dirname(os.path.abspath(__file__))+'/frames/'+today+'/detected/'+fileName
            cv2.imwrite(fileAddress, newframe)

            return fileAddress, faces

        else:

            today = time.strftime("%Y-%m-%d-%H")

            if not os.path.exists(os.path.dirname(os.path.abspath('__file__'))+'/frames/'+today+'/notdetected/'):
                os.makedirs(os.path.dirname(os.path.abspath('__file__'))+'/frames/'+today+'/notdetected/')

            fileName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.jpg'
            fileAddress=os.path.dirname(os.path.abspath('__file__'))+'/frames/'+today+'/notdetected/'+fileName
            cv2.imwrite(fileAddress, frame)

            return None, None

    def dlibDetect(self,frame):

        grey = self.TassTools.preProcess(frame)
        faces = self.detector(grey, 1)

        print("DLIB DETECTED "+ str(len(faces))+" FACES")

        if len(faces):

            newframe = frame.copy()

            today = time.strftime("%Y-%m-%d-%H")

            if not os.path.exists(os.path.dirname(os.path.abspath('__file__'))+'/frames/'+today+'/detected/'):

                os.makedirs(os.path.dirname(os.path.abspath('__file__'))+'/frames/'+today+'/detected/')

            for face in faces:

                x,y,w,h = self.TassTools.convertRect(face)

                cv2.rectangle(newframe, (x, y), (x+w, y+h), (0, 255, 0), 2)

            fileName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.jpg'
            fileAddress=os.path.dirname(os.path.abspath('__file__'))+'/frames/'+today+'/detected/'+fileName
            cv2.imwrite(fileAddress, newframe)

            return fileAddress, faces

        else:

            today = time.strftime("%Y-%m-%d-%H")

            if not os.path.exists(os.path.dirname(os.path.abspath('__file__'))+'/frames/'+today+'/notdetected/'):

                os.makedirs(os.path.dirname(os.path.abspath('__file__'))+'/frames/'+today+'/notdetected/')

            fileName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.jpg'
            fileAddress=os.path.dirname(os.path.abspath('__file__'))+'/frames/'+today+'/notdetected/'+fileName
            cv2.imwrite(fileAddress, frame)

            return None, None

    def getRep(self, bgrImg):

        if bgrImg is None:

            raise Exception("Unable to load image/frame")

        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
        bb = self.align.getAllFaceBoundingBoxes(rgbImg)

        if bb is None:
            print "No Bounding Boxes Found"
            return None

        alignedFaces = []

        for box in bb:

            bl = (box.left(), box.bottom())
            tr = (box.right(), box.top())

            cv2.rectangle(
                bgrImg,
                bl,
                tr,
                color=(0, 255, 0),
                thickness=3
            )

            alignedFaces.append(
                self.align.align(
                    self.imgDim,
                    rgbImg,
                    box,
                    landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE
                )
            )

        if alignedFaces is None:

            print("Unable to align the frame")
            raise Exception("Unable to align the frame")

        reps = []

        for alignedFace in alignedFaces:

            reps.append(self.net.forward(alignedFace))

        return reps

    def classify(self, alignedFace, faces, cvOrDlib):

        if(cvOrDlib == "Dlib"):

            landmarks = self.align.findLandmarks(alignedFace, faces)

            if landmarks == None:

                print("LANDMARKS NOT FOUND")
                return None

            alignedFace = self.align.align(self.imgDim, alignedFace, faces,landmarks=landmarks,landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

        reps = self.getRep(alignedFace)
        people = []
        confidences = []

        for rep in reps:

            try:

                rep = rep.reshape(1, -1)
                predictions = self.clf.predict_proba(rep).ravel()
                maxI = np.argmax(predictions)
                people.append(self.le.inverse_transform(maxI))
                confidences.append(predictions[maxI]*100)

            except:

                print("No Face detected")

        return (people, confidences)

