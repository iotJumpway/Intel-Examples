# *****************************************************************************
# Colfax Tax Trainer
# Copyright (c) 2018 Adam Milton-Barker - AdamMiltonBarker.com
# Based on Google's Tensorflow Imagenet Inception V3
# *****************************************************************************

import json
import InceptionFlow

print("Imported Required Modules")

class TassColfaxTrainer():
    
    def __init__(self):
        
        self.InceptionFlow = InceptionFlow.InceptionFlow()
            
        print("TassColfaxTrainer Initiated")
        
    def InitiateTraining(self):
        
        print("TassColfaxTrainer Training Initiated")
        self.InceptionFlow.trainModel()
        
TassColfaxTrainer = TassColfaxTrainer()
TassColfaxTrainer.InitiateTraining()    

