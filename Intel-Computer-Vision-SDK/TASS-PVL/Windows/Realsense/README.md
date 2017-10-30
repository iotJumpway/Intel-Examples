# IoT JumpWay Intel® Computer Vision SDK Windows TASS PVL RealSense Security System

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

8. [Virtual Studio 2017](https://www.visualstudio.com/downloads/ "Virtual Studio 2017")

## Hardware requirements

1. Windows PC with 6th Generation Intel® Core™ Processors with Intel® Iris® Pro Graphics and HD Graphics, In our example we are using an Intel® NUC NUC7i7BNH with Intel® OPtane Memory.

2. 1 x Realsense camera (Tested with F200 & R200)

## Before You Begin

There are a few tutorials that you should follow before beginning, especially if it is the first time you have used the TechBubble IoT JumpWay Developer Program. If you do not already have one, you will require a TechBubble IoT JumpWay Developer Program developer account, and some basics to be set up before you can start creating your IoT devices. Visit the following [IoT JumpWay Developer Program Docs (5-10 minute read/setup)](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/ "IoT JumpWay Developer Program Docs (5-10 minute read/setup)") and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications (About 5 minutes read).

## Preparing Your Windows Device

- [Install Intel® Computer Vision SDK](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Computer-Vision-SDK/TASS-PVL/Windows/_Docs/1-Installing-Intel-CV-SDK.md "Install Intel® Computer Vision SDK")

- [Install Intel® RealSense SDK](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Computer-Vision-SDK/TASS-PVL/Windows/_Docs/2-Installing-Intel-RealSense-SDK.md "Install Intel® RealSense SDK")

- [Install Microsoft Vcpkg](https://github.com/Microsoft/vcpkg "Install Microsoft Vcpkg"), Paho, Json

- [Install FFmpeg](http://ffmpeg.zeranoe.com/builds/ "Install FFmpeg")

- [Install Node JS](https://nodejs.org/en/download/ "Install Node JS")

- [Install Virtual Studio 2017](https://www.visualstudio.com/downloads/ "Install Virtual Studio 2017")

## IoT JumpWay Intel® Computer Vision SDK Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel® Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Examples in your IoT projects.

## IoT JumpWay Intel® Computer Vision SDK Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../../../images/main/Intel-Software-Innovator.jpg)