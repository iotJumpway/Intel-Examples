###############################################################################
# Title: TASS Movidius Core
# Description: Test classification of a local image or classifies live webcam stream.
# Acknowledgements: Uses code from Intel movidius/ncsdk (https://github.com/movidius/ncsdk)
# Last Modified: 2018/02/21
########################################################################################
        
print('')
print("Welcome to TASS Movidius, please wait while the program initiates...")
print('')

from mvnc import mvncapi as mvnc
import sys
import numpy
import cv2
import json
import techbubbleiotjumpwaymqtt.device as iotJumpway 

print("- Imported Required Modules")

class TassMovidius():
    
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

        with open("data/confs.json") as configs:

            self._configs = json.loads(configs.read())
            
        self.imagePath = self._configs["ClassifierSettings"]["ImagePath"]+self._configs["ClassifierSettings"]["Image"]
        
        self.CheckDevices()
        self.LoadModelRequirements()
        self.AllocateGraph()
        self.startMQTT()
        
        print("")
        print("-- TassMovidius Initiated")
        
        if self._configs["ClassifierSettings"]["MODE"] == "LIVE":
            
            print("-- YOU ARE IN LIVE MODE, EDIT data/confs.json TO CHANGE MODE TO TEST --")
            print("")
            self.startStream()
        
        else:
            
            print("-- YOU ARE IN TEST MODE, EDIT data/confs.json TO CHANGE MODE TO LIVE --")
            print("")
        
    def CheckDevices(self):
        
        #mvnc.SetGlobalOption(mvnc.GlobalOption.LOGLEVEL, 2)
        devices = mvnc.EnumerateDevices()
        if len(devices) == 0:
            print('WARNING! No Movidius Devices Found')
            quit()

        self.movidius = mvnc.Device(devices[0])
        self.movidius.OpenDevice()
        
        print("- Movidius Connected")
        
    def LoadModelRequirements(self):
        
        with open(self._configs["ClassifierSettings"]["NetworkPath"] + self._configs["ClassifierSettings"]["Graph"], mode='rb') as f:
            
            self.graphfile = f.read()
        
        print("- Graph Loaded OK")
            
        with open(self._configs["ClassifierSettings"]["NetworkPath"] + 'categories.txt', 'r') as f:
            
            for line in f:
                
                cat = line.split('\n')[0]
                
                if cat != 'classes':
                    
                    self.categories.append(cat)
                    
            f.close()
        
            print("- Categories Loaded OK:", len(self.categories))
        
        with open(self._configs["ClassifierSettings"]["NetworkPath"] + 'inputsize.txt', 'r') as f:
            
            self.reqsize = int(f.readline().split('\n')[0])
        
        print("- Image Size Loaded OK", self.reqsize)
            
    def AllocateGraph(self):

        self.graph = self.movidius.AllocateGraph(self.graphfile)
        
        print("- Allocated Graph OK")
            
    def startMQTT(self):

        try:

            self.jumpwayClient = iotJumpway.JumpWayPythonMQTTDeviceConnection({
                "locationID": self._configs["IoTJumpWay"]["Location"],
                "zoneID": self._configs["IoTJumpWay"]["Zone"],
                "deviceId": self._configs["IoTJumpWay"]["Device"],
                "deviceName": self._configs["IoTJumpWayDevice"]["Name"],
                "username": self._configs["IoTJumpWayMQTT"]["Username"],
                "password": self._configs["IoTJumpWayMQTT"]["Password"]
            })

        except Exception as e:
            print(str(e))
            sys.exit()

        self.jumpwayClient.connectToDevice()
        
        print("- IoT JumpWay Initiated")
            
    def startStream(self):
        
        self.cameraStream = cv2.VideoCapture(self._configs["Cameras"][0]["URL"])
        
        print("- Camera Stream Initiated")
        
TassMovidius = TassMovidius()

while True:
    
    if TassMovidius._configs["ClassifierSettings"]["MODE"] == "Test":

        print("TEST MODE")
        print('')
        
        img = cv2.imread(TassMovidius.imagePath).astype(numpy.float32)
        print("- Loaded Test Image", TassMovidius.imagePath)
        
        dx,dy,dz= img.shape
        delta=float(abs(dy-dx))
        
        if dx > dy: 
            
            img=img[int(0.5*delta):dx-int(0.5*delta),0:dy]
            
        else:
            
            img=img[0:dx,int(0.5*delta):dy-int(0.5*delta)]
            
        img = cv2.resize(img, (TassMovidius.reqsize, TassMovidius.reqsize))
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        for i in range(3):
            
            img[:,:,i] = (img[:,:,i] - TassMovidius.mean) * TassMovidius.std

        TassMovidius.graph.LoadTensor(img.astype(numpy.float16), 'user object')
        print('- Loaded Tensor')
        output, userobj = TassMovidius.graph.GetResult()

        top_inds = output.argsort()[::-1][:5]

        print('')
        print(''.join(['*' for i in range(79)]))
        print('inception-v3 on NCS')
        print(''.join(['*' for i in range(79)]))
        
        for i in range(5):
            
            print(top_inds[i], TassMovidius.categories[top_inds[i]], output[top_inds[i]])

        print(''.join(['*' for i in range(79)]))
        
        print('')
        print("TASS Detected Image ID", top_inds[0], TassMovidius.categories[top_inds[0]], "With A Confidence Of", output[top_inds[0]])
        print('')
        
        if output[top_inds[0]] > TassMovidius._configs["ClassifierSettings"]["TestThreshold"]:

            TassMovidius.jumpwayClient.publishToDeviceChannel(
                    "Sensors",
                    {
                        "Sensor":"CCTV",
                        "SensorID": TassMovidius._configs["Cameras"][0]["ID"],
                        "SensorValue":"OBJECT: " + TassMovidius.categories[top_inds[0]] + " (Confidence: " + str(output[top_inds[0]]) + ")"
                    }
                )
            
            print('Published To IoT JumpWay')
            print('')
        
        TassMovidius.graph.DeallocateGraph()
        TassMovidius.movidius.CloseDevice()
        
        print("TEST MODE ENDED")
        print("Good Bye")
        print('')
        
        sys.exit()
        
    else:
    
        print("LIVE MODE")
        print('')
        
        pass
                
print("SHUTTING DOWN")
print("")

TassMovidius.graph.DeallocateGraph()
TassMovidius.movidius.CloseDevice()
TassMovidius.jumpwayClient.disconnectFromDevice()
        
if TassMovidius._configs["ClassifierSettings"]["MODE"] == "LIVE":
    
    TassMovidius.cameraStream.release()