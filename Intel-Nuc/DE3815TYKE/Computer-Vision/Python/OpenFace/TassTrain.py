########################################################################################
# Author: Adam Milton-Barker
# Contact: adammiltonbarker@eu.techbubbletechnologies.com
########################################################################################
# Module: TassTrain.py
# Description: Trains a TASS computer vision model.
# Acknowledgements: Uses code from openface (https://github.com/cmusatyalab/openface)
# Last Modified: 8.3.2017
########################################################################################

import time

start = time.time()

import sys
import os
import time
import json

from multiprocessing import Process

import cv2
import dlib
import pickle
import shutil
import random

from operator import itemgetter

import numpy as np
np.set_printoptions(precision=2)
import pandas as pd

import openface
import openface.helper
from openface.data import iterImgs

from sklearn.pipeline import Pipeline
from sklearn.lda import LDA
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.mixture import GMM
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

from datetime import datetime

class TassTrain():

    def __init__(self):

        self._configs = {}

        with open('config.json') as configs:

            self._configs = json.loads(configs.read())

        self.fileDir = os.path.dirname(os.path.abspath(__file__))
        self.modelDir = self.fileDir+'/models'
        self.dlibModelDir = self.modelDir+'/dlib'
        self.openfaceModelDir = self.modelDir+'/openface'

        self.dlibFacePredictor = self.dlibModelDir+'/shape_predictor_68_face_landmarks.dat'
        self.networkModel = self.openfaceModelDir+'/nn4.small2.v1.t7'

        self.imgDim = self._configs["ClassifierSettings"]["imgDim"]
        self.ldaDim = self._configs["ClassifierSettings"]["ldaDim"]
        self.threshold = self._configs["ClassifierSettings"]["threshold"]
        self.cuda = self._configs["ClassifierSettings"]["useCuda"]

        self.align = openface.AlignDlib(self.dlibFacePredictor)
        self.net = openface.TorchNeuralNet(self.networkModel,imgDim=self.imgDim,cuda=self.cuda)
        self.landmarks = 'outerEyesAndNose'
        self.skipMulti = 1
        self.fallbackLfw = ''

    def train(self,workDir,classifier = 'LinearSvm'):

        print("Loading embeddings.")

        fname = "{}/labels.csv".format(workDir)

        labels = pd.read_csv(fname, header=None).as_matrix()[:, 1]
        labels = map(itemgetter(1),
                    map(os.path.split,
                        map(os.path.dirname, labels)))

        fname = "{}/reps.csv".format(workDir)

        embeddings = pd.read_csv(fname, header=None).as_matrix()

        le = LabelEncoder().fit(labels)
        labelsNum = le.transform(labels)
        nClasses = len(le.classes_)

        print("Training for {} classes.".format(nClasses))

        if classifier == 'LinearSvm':

            clf = SVC(C=1, kernel='linear', probability=True)

        elif classifier == 'GMM':

            clf = GMM(n_components=nClasses)

        elif classifier == 'RadialSvm':

            clf = SVC(C=1, kernel='rbf', probability=True, gamma=2)

        elif classifier == 'DecisionTree':

            clf = DecisionTreeClassifier(max_depth=20)

        elif classifier == 'GaussianNB':

            clf = GaussianNB()

        elif classifier == 'DBN':

            from nolearn.dbn import DBN

            clf = DBN([embeddings.shape[1], 500, labelsNum[-1:][0] + 1],
                    learn_rates=0.3,
                    learn_rate_decays=0.9,
                    epochs=300,
                    verbose=1)

        if self.ldaDim > 0:

            clf_final = clf
            clf = Pipeline([('lda', LDA(n_components=self.ldaDim)),
                            ('clf', clf_final)])

        clf.fit(embeddings, labelsNum)

        fName = "{}/classifier.pkl".format(workDir)

        print("Saving classifier to '{}'".format(fName))

        with open(fName, 'w') as f:

            pickle.dump((le, clf), f)

    def alignWithDlib(self,inputDir,outputDir):

        openface.helper.mkdirP(outputDir)
        imgs = list(iterImgs(inputDir))
        random.shuffle(imgs)

        landmarkMap = {
            'outerEyesAndNose': openface.AlignDlib.OUTER_EYES_AND_NOSE,
            'innerEyesAndBottomLip': openface.AlignDlib.INNER_EYES_AND_BOTTOM_LIP
        }

        if self.landmarks not in landmarkMap:

            raise Exception("Landmarks unrecognized: {}".format(self.landmarks))

        landmarkIndices = landmarkMap[self.landmarks]
        align = openface.AlignDlib(self.dlibFacePredictor)
        nFallbacks = 0

        for imgObject in imgs:

            print("=== {} ===".format(imgObject.path))
            outDir = os.path.join(outputDir, imgObject.cls)
            openface.helper.mkdirP(outDir)
            outputPrefix = os.path.join(outDir, imgObject.name)
            imgName = outputPrefix + ".png"

            if os.path.isfile(imgName):

                pass

            else:

                rgb = imgObject.getRGB()

                if rgb is None:

                    print("  + Unable to load.")

                    outRgb = None

                else:

                    outRgb = align.align(self.imgDim, rgb,
                                        landmarkIndices=landmarkIndices,
                                        skipMulti=self.skipMulti)

                    if outRgb is None:

                        print("  + Unable to align.")

                if self.fallbackLfw and outRgb is None:

                    nFallbacks += 1

                    deepFunneled = "{}/{}.jpg".format(os.path.join(
                            self.fallbackLfw,
                            imgObject.cls),
                        imgObject.name)
                    shutil.copy(deepFunneled, "{}/{}.jpg".format(os.path.join(
                            outputDir,
                            imgObject.cls),
                        imgObject.name))

                if outRgb is not None:

                    outBgr = cv2.cvtColor(outRgb, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(imgName, outBgr)

        if self.fallbackLfw:

            print('nFallbacks:', nFallbacks)

    def initiatePreproces(self,model):

        trainingPath=os.path.dirname(os.path.abspath(__file__)) + "/training/"+str(model)
        trainedPath=os.path.dirname(os.path.abspath(__file__)) + "/trained/"+str(model)
        featurePath=os.path.dirname(os.path.abspath(__file__)) + "/features/"+str(model)

        process = 1

        for n in range(7):

            process = process + 1
            p = Process(target=self.alignWithDlib, args=(trainingPath,trainedPath))
            p.start()
            p.join()
            print("Finished Process "+str(process))

        print("Finished Preprocessing Training Images For Model "+str(model))

        os.system(os.path.dirname(os.path.abspath(__file__)) + "/batch-represent/main.lua -outDir " + featurePath + " -data  " + trainedPath)

        print("Finished Generating Features For Model "+str(model))

        self.train(featurePath)

        print("Finished Training Model For Model "+str(model))

TassTrain = TassTrain()
TassTrain.initiatePreproces(1)