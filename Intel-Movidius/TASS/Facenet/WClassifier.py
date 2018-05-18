############################################################################################
# Title: TASS Movidius Facenet WebCam Classifier
# Description: Connects to a local webcam or stream for realtime face recognition.
# Acknowledgements: Uses code from Intel movidius/ncsdk (https://github.com/movidius/ncsdk)
# Last Modified: 2018-05-16
############################################################################################

############################################################################################
#
#    CLASSIFIER MODE:
#
#       Classifier & IoT JumpWay configuration can be found in required/confs.json
#
#    Example Usage:
#
#        $ python3.5 Classifier.py
#
############################################################################################

print("")
print("")
print("!! Welcome to TASS Movidius Facenet WebCam Classifier, please wait while the program initiates !!")
print("")

import os, sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

print("-- Running on Python "+sys.version)
print("")

import time,csv,getopt,json, time, cv2, dlib, imutils, urllib.request, threading 
import numpy as np

import JumpWayMQTT.Device as JWMQTTdevice
from tools.Helpers import Helpers
from tools.OpenCV import OpenCVHelpers as OpenCVHelpers
from tools.Facenet import FacenetHelpers as FacenetHelpers
 
from mvnc import mvncapi as mvnc
from imutils import face_utils
from skimage.transform import resize

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver  import ThreadingMixIn
from io import BytesIO
from PIL import Image
from datetime import datetime

capture=None

class Classifier():

    def __init__(self):

        self._configs = {}
        self.movidius = None
        self.jumpwayClient = None
        self.OpenCVCapture = None

        self.graphfile = None
        self.graph = None

        self.CheckDevices()
        self.Helpers = Helpers()
        self.OpenCVHelpers = OpenCVHelpers()
        self.FacenetHelpers = FacenetHelpers()
        self._configs = self.Helpers.loadConfigs()
        self.loadRequirements()
        self.startMQTT()

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self._configs["ClassifierSettings"]["Dlib"])

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

    def loadRequirements(self):

        with open(self._configs["ClassifierSettings"]["NetworkPath"] + self._configs["ClassifierSettings"]["Graph"], mode='rb') as f:

            self.graphfile = f.read()

        self.allocateGraph(self.graphfile)

        print("-- Allocated Graph OK")

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

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					while( capture.isOpened() ) :
						rc, frame = capture.read()
						if not rc:
							continue
							
						cv2.imwrite("currentRaw.jpg",frame)

						gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
						rects = Classifier.detector(gray, 1)

						for (i, rect) in enumerate(rects):
							# determine the facial landmarks for the face region, then
							# convert the facial landmark (x, y)-coordinates to a NumPy
							# array
							shape = Classifier.predictor(gray, rect)
							shape = face_utils.shape_to_np(shape)

							# convert dlib's rectangle to a OpenCV-style bounding box
							# [i.e., (x, y, w, h)], then draw the face bounding box
							(x, y, w, h) = face_utils.rect_to_bb(rect)
							cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

							# loop over the (x, y)-coordinates for the facial landmarks
							# and draw them on the image
							for (x, y) in shape:
								cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
								
							cv2.imwrite("currentProcessed.jpg",frame)
							print("-- Saved frame ")
							print("")

							validDir = Classifier._configs["ClassifierSettings"]["NetworkPath"] + Classifier._configs["ClassifierSettings"]["ValidPath"]

							output = FacenetHelpers.infer(frame, Classifier.graph)

							for valid in os.listdir(validDir):

									if valid.endswith('.jpg') or valid.endswith('.jpeg') or valid.endswith('.png') or valid.endswith('.gif'):

										valid_output = FacenetHelpers.infer(cv2.imread(validDir+valid), Classifier.graph)

										if (FacenetHelpers.match(valid_output, output)):
											print("-- MATCH ")
											print("")

											Classifier.jumpwayClient.publishToDeviceChannel(
												"Warnings",
												{
													"WarningType":"CCTV",
													"WarningOrigin": Classifier._configs["Cameras"][0]["ID"],
													"WarningValue": "RECOGNISED",
													"WarningMessage":valid.rsplit( ".", 1 )[ 0 ]+" Detected"
												}
											)
											break
										else:
											print("-- NO MATCH")
											print("")

											Classifier.jumpwayClient.publishToDeviceChannel(
												"Warnings",
												{
													"WarningType":"CCTV",
													"WarningOrigin": Classifier._configs["Cameras"][0]["ID"],
													"WarningValue": "INTRUDER",
													"WarningMessage":"INTRUDER"
												}
											)
									else:
										print("-- NO VALID ID")
										print("")
							
						imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
						imgRGB = cv2.flip(imgRGB, 1)
						jpg = Image.fromarray(imgRGB)
						tmpFile = BytesIO()
						jpg.save(tmpFile,'JPEG')
						self.wfile.write("--jpgboundary".encode())
						self.send_header('Content-type','image/jpeg')
						self.send_header('Content-length',str(tmpFile.getbuffer().nbytes))
						self.end_headers()
						self.wfile.write( tmpFile.getvalue() )
						time.sleep(0.05)
					
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>'.encode())
			self.wfile.write('<img src="'+Classifier._configs["Cameras"][0]["Stream"]+':'+Classifier._configs["Cameras"][0]["StreamPort"]+'/cam.mjpg"/>'.encode())
			self.wfile.write('</body></html>'.encode())
			return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def main():
	global capture
	global Classifier
	global FacenetHelpers
	Classifier = Classifier()
	FacenetHelpers = FacenetHelpers()

	try:
		
		capture = cv2.VideoCapture(Classifier._configs["Cameras"][0]["URL"])
		capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
		capture.set(cv2.CAP_PROP_SATURATION,0.2)

	except Exception as e:
		print("-- FAILED TO CONNECT TO WEBCAM")
		print(str(e))
		sys.exit()

	global img
	try:
		server = ThreadedHTTPServer(('192.168.1.44', 8080), CamHandler)
		print("server started")
		server.serve_forever()
	except KeyboardInterrupt:
		capture.release()
		server.socket.close()

if __name__ == '__main__':
	main()