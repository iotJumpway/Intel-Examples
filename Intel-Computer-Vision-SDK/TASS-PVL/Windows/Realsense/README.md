# IoT JumpWay Intel® Computer Vision SDK Windows TASS PVL Security System

![TechBubble IoT JumpWay Docs](../images/Intel-Computer-Vision-Windows.png)

## Introduction

Here you will find a sample application for TASS PVL, a Computer Vision security system using Intel® Computer Vision SDK and an Intel® Edison connected to the Internet of Things via TechBubble Technologies IoT JumpWay.

Once you understand how it works you are free to modify the app accordingly.

## This project uses four applications:

1. A device application (Node JS) which communicates with the IoT via the TechBubble Technologies IoT JumpWay.
2. A Windows Computer Vision application that sends commands to the device to toggle the state of the LEDs and buzzer when known or unknown faces are detected.
3. A Python Flask webserver displaying the real time stream from your camera and allowing you to train known people via the TechBubble IoT JumpWay WebSockets Client.
4. A Node JS application that streams the camera feed via sockets.

## Software requirements

1. [TechBubble IoT JumpWay Node JS MQTT Client Library](https://github.com/TechBubbleTechnologies/IoT-JumpWay-NodeJS-MQTT-Client "TechBubble IoT JumpWay Node JS MQTT Client Library")

2. [TechBubble IoT JumpWay WebSocket MQTT Client](https://github.com/TechBubbleTechnologies/IoT-JumpWay-WebSockets-MQTT-Client "TechBubble IoT JumpWay WebSocket MQTT Client")

3. [Intel® Computer Vision SDK for Windows 10](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Computer-Vision-SDK/TASS-PVL/Windows/_Docs/1-Installing-Intel-CV-SDK.md "Intel® Computer Vision SDK for Windows 10")

4. [Intel® RealSense SDK for Windows 10](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Computer-Vision-SDK/TASS-PVL/Windows/_Docs/2-Installing-Intel-RealSense-SDK.md "Intel® RealSense SDK for Windows 10")

5. [Microsoft Vcpkg](https://github.com/Microsoft/vcpkg "Microsoft Vcpkg"), Paho, Json

6. [FFmpeg](http://ffmpeg.zeranoe.com/builds/ "FFmpeg")

7. [Node JS](https://nodejs.org/en/download/ "Node JS")

## IoT JumpWay Intel® Computer Vision SDK Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel® Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Examples in your IoT projects.

## IoT JumpWay Intel® Computer Vision SDK Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../../../images/main/Intel-Software-Innovator.jpg)