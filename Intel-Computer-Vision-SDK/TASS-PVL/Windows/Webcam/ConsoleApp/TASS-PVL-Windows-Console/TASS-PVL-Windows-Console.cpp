/*
* Copyright 2016 Intel Corporation.
*
* The source code, information and material ("Material") contained herein is
* owned by Intel Corporation or its suppliers or licensors, and title to such
* Material remains with Intel Corporation or its suppliers or licensors. The
* Material contains proprietary information of Intel or its suppliers and
* licensors. The Material is protected by worldwide copyright laws and treaty
* provisions. No part of the Material may be used, copied, reproduced,
* modified, published, uploaded, posted, transmitted, distributed or disclosed
* in any way without Intel's prior express written permission. No license under
* any patent, copyright or other intellectual property rights in the Material
* is granted to or conferred upon you, either expressly, by implication,
* inducement, estoppel or otherwise. Any license under such intellectual
* property rights must be express and approved by Intel in writing.
*
* Unless otherwise agreed by Intel in writing, you may not remove or alter this
* notice or any other notice embedded in Materials by Intel or Intel's
* suppliers or licensors in any way.
*/

/*
* TASS-PVL WINDOWS WEBCAM CONSOLE APP
*
* Developed by Adam Milton-Barker
* TechBubble Technologies 
* https://eu.techbubbletechnologies.com
*
* IoT Connectivity Powered By TechBubble IoT JumpWay
* https://iot.techbubbletechnologies.com
*
*/

#include "stdafx.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <iostream>
#include <fstream>
#include <sstream>
#include <time.h>

#include <iostream>
#include <fstream>
#include <sstream>

#include "opencv2/core.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/pvl.hpp"

#include "MQTTAsync.h"
#include "nlohmann/json.hpp"

using namespace cv;
using namespace std;
using namespace cv::pvl;
using json = nlohmann::json;

#define QOS         1
#define TIMEOUT     10000L

std::string IntelliLanMQTT = "ssl://iot.techbubbletechnologies.com:8883";
int IntelliLanLocation = 0;
int IntelliLanZone = 0;
int IntelliLanDevice = 0;
int IntelliLanSensor = 0;
std::string IntelliLanDeviceN = "YourIoTJumpWayDeviceNameHere";
std::string IntelliLanDeviceU = "YourIoTJumpWayDeviceUsernameHere";
std::string IntelliLanDeviceP = "YourIoTJumpWayDevicePasswordHere";

std::string knownDB = "known.xml";

int timeBetweenAPICalls = 0.5 * 60;
time_t lastTimeOfKnownAPICall = time(NULL);
time_t lastTimeOfUnknownAPICall = time(NULL);

int camera = 1;
int disc_finished = 0;
int subscribed = 0;
int finished = 0;
bool bRegist = false;
bool readScreen = false;
int userFaceID = 0;

volatile MQTTAsync_token deliveredtoken;

void processFrames();

bool displayAndNotify(
	MQTTAsync client,
	Mat& img,
	const std::vector<Face>& faces,
	const std::vector<int>& personIDs,
	const std::vector<int>& confidence,
	double elapsed
);

void drawSmile(
	cv::Mat& image,
	std::vector<cv::pvl::Face>& results
);

void publishToDeviceSensors(
	MQTTAsync client,
	int person,
	int confidence
);

void publishToDeviceWarnings(
	MQTTAsync client,
	int person,
	int confidence,
	std::string value
);

std::vector<std::string> explode(const std::string &delimiter, const std::string &str)
{
	std::vector<std::string> arr;

	int strleng = str.length();
	int delleng = delimiter.length();
	if (delleng == 0)
		return arr;

	int i = 0;
	int k = 0;
	while (i<strleng)
	{
		int j = 0;
		while (i + j<strleng && j<delleng && str[i + j] == delimiter[j])
			j++;
		if (j == delleng)
		{
			arr.push_back(str.substr(k, i - k));
			i += delleng;
			k = i;
		}
		else
		{
			i++;
		}
	}
	arr.push_back(str.substr(k, i - k));
	return arr;
}

void onSubscribe(void* context, MQTTAsync_successData* response)
{
	printf("Subscribe succeeded\n");
	subscribed = 1;
}

void onSubscribeFailure(void* context, MQTTAsync_failureData* response)
{
	printf("Subscribe failed, rc %d\n", response ? response->code : 0);
	finished = 1;
}

int msgarrvd(void *context, char *topicName, int topicLen, MQTTAsync_message *message)
{
	printf("Message Arrived", message);
	return 1;
}

void onDisconnect(void* context, MQTTAsync_successData* response)
{
	printf("Successful disconnection from TechBubble IoT JumpWay\n");
	finished = 1;
}

void onSend(void* context, MQTTAsync_successData* response)
{
	MQTTAsync client = (MQTTAsync)context;
	MQTTAsync_disconnectOptions opts = MQTTAsync_disconnectOptions_initializer;
	int rc;

	printf("Message with token value %d delivery confirmed\n", response->token);

}

void onConnectFailure(void* context, MQTTAsync_failureData* response)
{
	printf("Connect to TechBubble IoT JumpWay failed, rc %d\n", response ? response->code : 0);
	finished = 1;
}

void onConnect(void* context, MQTTAsync_successData* response)
{
	MQTTAsync client = (MQTTAsync)context;
	MQTTAsync_responseOptions opts = MQTTAsync_responseOptions_initializer;
	MQTTAsync_message pubmsg = MQTTAsync_message_initializer;
	int rc;

	printf("Connected to TechBubble IoT JumpWay\n");

	opts.onSuccess = onSend;
	opts.context = client;

	pubmsg.payload = "ONLINE";
	pubmsg.payloadlen = strlen("ONLINE");
	pubmsg.qos = QOS;
	pubmsg.retained = 0;
	deliveredtoken = 0;

	std::stringstream IntelliLanDeviceStatusTopicS;
	IntelliLanDeviceStatusTopicS << IntelliLanLocation << "/Devices/" << IntelliLanZone << "/" << IntelliLanDevice << "/Status";
	std::string IntelliLanDeviceStatusTopic = IntelliLanDeviceStatusTopicS.str();

	std::stringstream IntelliLanDeviceCommandsTopicS;
	IntelliLanDeviceCommandsTopicS << IntelliLanLocation << "/Devices/" << IntelliLanZone << "/" << IntelliLanDevice << "/Commands";
	std::string IntelliLanDeviceCommandsTopic = IntelliLanDeviceCommandsTopicS.str();

	if ((rc = MQTTAsync_sendMessage(client, IntelliLanDeviceStatusTopic.c_str(), &pubmsg, &opts)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to start sendMessage, return code %d\n", rc);
		exit(EXIT_FAILURE);
	}

	if ((rc = MQTTAsync_subscribe(client, IntelliLanDeviceCommandsTopic.c_str(), QOS, &opts)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to start subscribe, return code %d\n", rc);
		exit(EXIT_FAILURE);
	}
}

void connlost(void *context, char *cause)
{
	int rc;
	MQTTAsync client = (MQTTAsync)context;
	MQTTAsync_connectOptions conn_opts = MQTTAsync_connectOptions_initializer;
	MQTTAsync_SSLOptions ssl_opts = MQTTAsync_SSLOptions_initializer;
	MQTTAsync_willOptions will_opts = MQTTAsync_willOptions_initializer;

	std::stringstream IntelliLanDeviceStatusTopicS;
	IntelliLanDeviceStatusTopicS << IntelliLanLocation << "/Devices/" << IntelliLanZone << "/" << IntelliLanDevice << "/Status";
	std::string IntelliLanDeviceStatusTopic = IntelliLanDeviceStatusTopicS.str();

	MQTTAsync_create(&client, IntelliLanMQTT.c_str(), IntelliLanDeviceN.c_str(), MQTTCLIENT_PERSISTENCE_NONE, NULL);
	MQTTAsync_setCallbacks(client, NULL, connlost, msgarrvd, NULL);

	conn_opts.keepAliveInterval = 20;
	conn_opts.cleansession = 1;
	conn_opts.onSuccess = onConnect;
	conn_opts.onFailure = onConnectFailure;
	conn_opts.context = client;
	conn_opts.username = IntelliLanDeviceU.c_str();
	conn_opts.password = IntelliLanDeviceP.c_str();
	conn_opts.will = &will_opts;
	will_opts.topicName = IntelliLanDeviceStatusTopic.c_str();
	will_opts.message = "OFFLINE";
	conn_opts.ssl = &ssl_opts;
	ssl_opts.enableServerCertAuth = 0;
	ssl_opts.trustStore = "ca.pem";
	ssl_opts.enabledCipherSuites = "TLSv1";

	if ((rc = MQTTAsync_connect(client, &conn_opts)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to start connect, return code %d\n", rc);
		finished = 1;
	}
}


int main(int argc, char* argv[])
{
	processFrames();
	return 1;
}

void processFrames()
{
	const char* WINDOW_NAME = "TASS PVL Windows Console App";

	Ptr<FaceDetector> pvlFD;
	Ptr<FaceRecognizer> pvlFR;

	Mat imgIn;
	Mat imgGray;

	VideoCapture capture; 
	
	capture.open(camera);

	if (!capture.isOpened())
	{
		cerr << "Error: fail to capture video." << endl;
		return;
	}

	pvlFR = FaceRecognizer::create();
	if (pvlFR.empty())
	{
		cerr << "Error: fail to create PVL face recognizer" << endl;
		return;
	}

	pvlFD = FaceDetector::create();
	if (pvlFD.empty())
	{
		cerr << "Error: fail to create PVL face detector" << endl;
		return;
	}

	capture >> imgIn;
	if (imgIn.empty())
	{
		cerr << "Error: no input image" << endl;
		return;
	}

	cvtColor(imgIn, imgGray, COLOR_BGR2GRAY);
	if (imgGray.empty())
	{
		cerr << "Error: get gray image()" << endl;
		return;
	}

	int keyDelay = 1;

	namedWindow(WINDOW_NAME, WINDOW_AUTOSIZE);

	bool bTracking = true;

	pvlFD->setTrackingModeEnabled(bTracking);
	pvlFR->setTrackingModeEnabled(bTracking);

	std::vector<Face> faces;
	std::vector<Face> validFaces;
	std::vector<int>  personIDs;
	std::vector<int>  confidence;

	int64 startTick = getTickCount();

	try
	{
		bTracking = pvlFR->isTrackingModeEnabled();
		pvlFR = Algorithm::load<FaceRecognizer>(knownDB);
		pvlFR->setTrackingModeEnabled(bTracking);
	}
	catch (...)
	{

	}

	int rc;
	MQTTAsync client;
	MQTTAsync_connectOptions conn_opts = MQTTAsync_connectOptions_initializer;
	MQTTAsync_SSLOptions ssl_opts = MQTTAsync_SSLOptions_initializer;
	MQTTAsync_willOptions will_opts = MQTTAsync_willOptions_initializer;

	std::stringstream IntelliLanDeviceStatusTopicS;
	IntelliLanDeviceStatusTopicS << IntelliLanLocation << "/Devices/" << IntelliLanZone << "/" << IntelliLanDevice << "/Status";
	std::string IntelliLanDeviceStatusTopic = IntelliLanDeviceStatusTopicS.str();

	MQTTAsync_create(&client, IntelliLanMQTT.c_str(), IntelliLanDeviceN.c_str(), MQTTCLIENT_PERSISTENCE_NONE, NULL);
	MQTTAsync_setCallbacks(client, NULL, connlost, msgarrvd, NULL);

	conn_opts.keepAliveInterval = 20;
	conn_opts.cleansession = 1;
	conn_opts.onSuccess = onConnect;
	conn_opts.onFailure = onConnectFailure;
	conn_opts.context = client;
	conn_opts.username = IntelliLanDeviceU.c_str();
	conn_opts.password = IntelliLanDeviceP.c_str();
	conn_opts.will = &will_opts;
	will_opts.topicName = IntelliLanDeviceStatusTopic.c_str();
	will_opts.message = "OFFLINE";
	conn_opts.ssl = &ssl_opts;
	ssl_opts.enableServerCertAuth = 0;
	ssl_opts.trustStore = "ca.pem";
	ssl_opts.enabledCipherSuites = "TLSv1";

	if ((rc = MQTTAsync_connect(client, &conn_opts)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to start connect, return code %d\n", rc);
	}


	for (;;)
	{

		faces.clear();
		personIDs.clear();
		confidence.clear();

		pvlFD->detectFaceRect(imgGray, faces);

		if (faces.size() > 0)
		{
			validFaces.clear();
			int validFaceCount = 0;

			if (bTracking)
			{
				validFaceCount = MIN(static_cast<int>(faces.size()), pvlFR->getMaxFacesInTracking());
			}
			else
			{
				validFaceCount = faces.size();
			}

			for (int i = 0; i < validFaceCount; i++)
			{
				validFaces.push_back(faces[i]);
			}

			pvlFR->recognize(imgGray, validFaces, personIDs, confidence);

			for (uint i = 0; i < faces.size(); ++i)
			{
				pvlFD->detectEye(imgGray, faces[i]);
				pvlFD->detectMouth(imgGray, faces[i]);
				pvlFD->detectBlink(imgGray, faces[i]);
				pvlFD->detectSmile(imgGray, faces[i]);
			}
			for (uint i = 0; i < faces.size(); ++i)
			{
				const Face& face = faces[i];
				Rect faceRect = face.get<Rect>(Face::FACE_RECT);
				Point leftEyePos = face.get<Point>(Face::LEFT_EYE_POS);
				Point rightEyePos = face.get<Point>(Face::RIGHT_EYE_POS);
				Point mouthPos = face.get<Point>(Face::MOUTH_POS);
				bool closingLeft = face.get<bool>(Face::CLOSING_LEFT_EYE);
				bool closingRight = face.get<bool>(Face::CLOSING_RIGHT_EYE);
				bool smiling = face.get<bool>(Face::SMILING);
			}

			if (bRegist)
			{
				bRegist = false;

				for (uint i = 0; i < personIDs.size(); i++)
				{
					if (personIDs[i] == FACE_RECOGNIZER_UNKNOWN_PERSON_ID)
					{
						int personID = pvlFR->createNewPersonID();
						pvlFR->registerFace(imgGray, validFaces[i], personID, true);
						pvlFR->save(knownDB);
						userFaceID = 0;
					}
				}

				if (!bTracking)
				{
					pvlFR->recognize(imgGray, validFaces, personIDs, confidence);
				}
			}
		}

		double elasped = static_cast<double>(getTickCount() - startTick) / getTickFrequency();
		startTick = getTickCount();

		displayAndNotify(client, imgIn, faces, personIDs, confidence, elasped);
		drawSmile(imgIn, faces);
		imshow(WINDOW_NAME, imgIn);

		char key = static_cast<char>(waitKey(keyDelay));
		if (key == 'q' || key == 'Q')
		{
			std::cout << "Quit." << std::endl;
			break;
		}
		else if (key == 'r' || key == 'R')
		{
			bRegist = true;
		}
		else if (key == 's' || key == 'S')
		{
			std::cout << "Save. " << knownDB << std::endl;
			pvlFR->save(knownDB);
		}

		capture >> imgIn;
		if (imgIn.empty()) { break; }
		cvtColor(imgIn, imgGray, COLOR_BGR2GRAY);
	}

	destroyWindow(WINDOW_NAME);

}


static void roundedRectangle(Mat& src, const Point& topLeft, const Point& bottomRight,
	const Scalar lineColor, const int thickness, const int lineType, const int cornerRadius)
{

	Point p1 = topLeft;
	Point p2 = Point(bottomRight.x, topLeft.y);
	Point p3 = bottomRight;
	Point p4 = Point(topLeft.x, bottomRight.y);

	line(src, Point(p1.x + cornerRadius, p1.y), Point(p2.x - cornerRadius, p2.y), lineColor, thickness, lineType);
	line(src, Point(p2.x, p2.y + cornerRadius), Point(p3.x, p3.y - cornerRadius), lineColor, thickness, lineType);
	line(src, Point(p4.x + cornerRadius, p4.y), Point(p3.x - cornerRadius, p3.y), lineColor, thickness, lineType);
	line(src, Point(p1.x, p1.y + cornerRadius), Point(p4.x, p4.y - cornerRadius), lineColor, thickness, lineType);

	ellipse(src, p1 + Point(cornerRadius, cornerRadius), Size(cornerRadius, cornerRadius), 180.0, 0, 90, lineColor, thickness, lineType);
	ellipse(src, p2 + Point(-cornerRadius, cornerRadius), Size(cornerRadius, cornerRadius), 270.0, 0, 90, lineColor, thickness, lineType);
	ellipse(src, p3 + Point(-cornerRadius, -cornerRadius), Size(cornerRadius, cornerRadius), 0.0, 0, 90, lineColor, thickness, lineType);
	ellipse(src, p4 + Point(cornerRadius, -cornerRadius), Size(cornerRadius, cornerRadius), 90.0, 0, 90, lineColor, thickness, lineType);
}


static void putTextCenter(InputOutputArray img, const String& text, Point& point, int fontFace,
	double fontScale, Scalar color, int thickness = 1, int lineType = LINE_8)
{
	int baseline;
	Size textSize = getTextSize(text, fontFace, fontScale, thickness, &baseline);

	Point center = point;
	center.x -= (textSize.width / 2);
	putText(img, text, center, fontFace, fontScale, color, thickness, lineType);
}

void drawSmile(cv::Mat& image, std::vector<cv::pvl::Face>& results)
{
	for (uint i = 0; i < results.size(); i++)
	{
		cv::pvl::Face& r = results[i];
		cv::Rect faceRect = r.get<cv::Rect>(cv::pvl::Face::FACE_RECT);

		int x = faceRect.x + 5;
		int y = faceRect.y + faceRect.height + 15;

		std::stringstream smile(std::ios_base::app | std::ios_base::out);
		smile << r.get<int>(cv::pvl::Face::SMILE_SCORE);

		if (r.get<int>(cv::pvl::Face::SMILE_SCORE) >= 35)
		{
			cv::putText(image, "HAPPY", cv::Point(x, y + 10), cv::FONT_HERSHEY_PLAIN, 2, cv::Scalar(0, 0, 255.0));
		}

	}
}

void publishToDeviceSensors(
	MQTTAsync client,
	int person,
	int confidence
)
{
	MQTTAsync_responseOptions opts = MQTTAsync_responseOptions_initializer;
	MQTTAsync_message pubmsg = MQTTAsync_message_initializer;
	int rc;

	opts.onSuccess = onSend;
	opts.context = client;

	std::stringstream IntelliLanDeviceDataS;
	IntelliLanDeviceDataS << "{ \"Sensor\": \"CCTV\",  \"SensorID\": " << IntelliLanSensor << ", \"SensorValue\": " << person << " }";
	std::string IntelliLanDeviceData = IntelliLanDeviceDataS.str();
	std::cout << IntelliLanDeviceData << std::endl;

	pubmsg.payload = (char*)IntelliLanDeviceData.c_str();
	pubmsg.payloadlen = IntelliLanDeviceData.size();
	pubmsg.qos = QOS;
	pubmsg.retained = 0;
	deliveredtoken = 0;

	std::stringstream IntelliLanDeviceSensorsTopicS;
	IntelliLanDeviceSensorsTopicS << IntelliLanLocation << "/Devices/" << IntelliLanZone << "/" << IntelliLanDevice << "/Sensors";
	std::string IntelliLanDeviceSensorsTopic = IntelliLanDeviceSensorsTopicS.str();
	std::cout << IntelliLanDeviceSensorsTopic;

	if ((rc = MQTTAsync_sendMessage(client, IntelliLanDeviceSensorsTopic.c_str(), &pubmsg, &opts)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to start sendMessage, return code %d\n", rc);
		exit(EXIT_FAILURE);
	}

}

void publishToDeviceWarnings(
	MQTTAsync client,
	int person,
	int confidence,
	std::string value 
)
{
	MQTTAsync_responseOptions opts = MQTTAsync_responseOptions_initializer;
	MQTTAsync_message pubmsg = MQTTAsync_message_initializer;
	int rc;

	std::stringstream IntelliLanDeviceDataS;
	IntelliLanDeviceDataS << "{ \"WarningType\": \"CCTV\",  \"WarningOrigin\": " << IntelliLanSensor << ", \"WarningValue\": \"" << value << "\", \"WarningMessage\": " << person << " }";
	std::string IntelliLanDeviceData = IntelliLanDeviceDataS.str();
	std::cout << IntelliLanDeviceData << std::endl;

	pubmsg.payload = (char*)IntelliLanDeviceData.c_str();
	pubmsg.payloadlen = IntelliLanDeviceData.size();

	opts.onSuccess = onSend;
	opts.context = client;

	pubmsg.qos = QOS;
	pubmsg.retained = 0;
	deliveredtoken = 0;

	std::stringstream IntelliLanDeviceSensorsTopicS;
	IntelliLanDeviceSensorsTopicS << IntelliLanLocation << "/Devices/" << IntelliLanZone << "/" << IntelliLanDevice << "/Warnings";
	std::string IntelliLanDeviceSensorsTopic = IntelliLanDeviceSensorsTopicS.str();
	std::cout << IntelliLanDeviceSensorsTopic;

	if ((rc = MQTTAsync_sendMessage(client, IntelliLanDeviceSensorsTopic.c_str(), &pubmsg, &opts)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to start sendMessage, return code %d\n", rc);
		exit(EXIT_FAILURE);
	}

}

bool displayAndNotify(MQTTAsync client, Mat& img, const std::vector<Face>& faces, const std::vector<int>& personIDs, const std::vector<int>& confidence, double elapsed)
{
	const int FONT = FONT_HERSHEY_PLAIN;
	const Scalar GREEN = Scalar(0, 255, 0, 255);
	const Scalar BLUE = Scalar(255, 0, 0, 255);

	Point pointLT, pointRB;
	String string;

	for (uint i = 0; i < faces.size(); i++)
	{
		const Face& face = faces[i];
		Rect faceRect = face.get<Rect>(Face::FACE_RECT);

		pointLT.x = faceRect.x;
		pointLT.y = faceRect.y;
		pointRB.x = faceRect.x + faceRect.width;
		pointRB.y = faceRect.y + faceRect.height;

		roundedRectangle(img, pointLT, pointRB, GREEN, 1, 8, 5);


		if (i < personIDs.size())
		{
			string.clear();

			if (personIDs[i] > 0)
			{
				string = format("Person:%d(%d)", personIDs[i], confidence[i]);
				if (time(NULL) - lastTimeOfKnownAPICall >= timeBetweenAPICalls) {
					publishToDeviceSensors(client, personIDs[i], confidence[i]);
					publishToDeviceWarnings(client, personIDs[i], confidence[i], "Recognised");
					lastTimeOfKnownAPICall = time(NULL);
				}
			}
			else if (personIDs[i] == FACE_RECOGNIZER_UNKNOWN_PERSON_ID)
			{
				string = "UNKNOWN";
				if (time(NULL) - lastTimeOfUnknownAPICall >= timeBetweenAPICalls) {
					publishToDeviceSensors(client, 0, 0);
					publishToDeviceWarnings(client, 0, 0, "Not Recognised");
					lastTimeOfUnknownAPICall = time(NULL);
				}
			}
			else
			{
				//do nothing
			}

			pointLT.x += faceRect.width / 2;
			pointLT.y -= 2;
			putTextCenter(img, string, pointLT, FONT, 1.2, GREEN, 2);
		}
	}

	pointLT.x = 2;
	pointLT.y = 16;
	string = "(Q)Quit";
	putText(img, string, pointLT, FONT, 1, BLUE, 1, 8);

	pointLT.y += 16;
	string = "(R)Register current unknown faces";
	putText(img, string, pointLT, FONT, 1, BLUE, 1, 8);

	pointLT.y += 16;
	string = "(L)load faces from xml";
	putText(img, string, pointLT, FONT, 1, BLUE, 1, 8);

	pointLT.y += 16;
	string = "(S)save faces into xml";
	putText(img, string, pointLT, FONT, 1, BLUE, 1, 8);

	const int FPS_MEASURE_INTERVAL = 30;
	static int fpsInterval = 0;
	static double fpsSum = 0;
	static double fps = 0;

	fpsSum += elapsed;

	if (fpsInterval++ == FPS_MEASURE_INTERVAL)
	{
		fps = 1.f / fpsSum * FPS_MEASURE_INTERVAL;

		fpsInterval = 0;
		fpsSum = 0;
	}

	pointLT.y = img.size().height - 7;
	string = format("fps:%.1f", fps);
	putText(img, string, pointLT, FONT, 1.2, BLUE, 2, 8);

	return true;
}