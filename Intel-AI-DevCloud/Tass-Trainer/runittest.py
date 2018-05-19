import json
import InceptionFlow
print("Imported Required Modules")

class TassColfaxTrainerInference():
    
    def __init__(self):
        
        self.InceptionFlow = InceptionFlow.InceptionFlow()
        print("Checking Inception V3 Model")
        
        self.InceptionFlow.checkModelDownload()
        print("Creating Inception V3 Graph")
        
        self.InceptionFlow.createInceptionGraph()
        print("TassColfaxTrainerInference Initiated")
        
    def InitiateTest(self):
        
        print("TassColfaxTrainerInference Testing Initiated")
        self.InceptionFlow.testModel()
        
TassColfaxTrainerInference = TassColfaxTrainerInference()
TassColfaxTrainerInference.InitiateTest()

