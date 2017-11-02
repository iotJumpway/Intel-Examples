# IoT JumpWay Intel® Computer Vision SDK Windows Console TASS PVL Webcam Security System

![TechBubble IoT JumpWay Docs](../../images/Intel-Computer-Vision-Windows.png)

## Introduction

Here you will find a sample application for TASS PVL, a Computer Vision security system using Intel® Computer Vision SDK and an Intel® Edison connected to the Internet of Things via TechBubble Technologies IoT JumpWay.

Once you understand how it works you are free to modify the app accordingly.

## This project uses two applications:

1. A Windows Computer Vision application.
2. A Node JS application on an Intel® Edison that receives commands to activate LEDs and a buzzer when known or unknown faces are detected

## Software requirements

1. [TechBubble IoT JumpWay Node JS MQTT Client Library](https://github.com/TechBubbleTechnologies/IoT-JumpWay-NodeJS-MQTT-Client "TechBubble IoT JumpWay Node JS MQTT Client Library")

2. [TechBubble IoT JumpWay WebSocket MQTT Client](https://github.com/TechBubbleTechnologies/IoT-JumpWay-WebSockets-MQTT-Client "TechBubble IoT JumpWay WebSocket MQTT Client")

3. [Intel® Computer Vision SDK for Windows 10](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Computer-Vision-SDK/TASS-PVL/Windows/_Docs/1-Installing-Intel-CV-SDK.md "Intel® Computer Vision SDK for Windows 10")

4. [Microsoft Vcpkg](https://github.com/Microsoft/vcpkg "Microsoft Vcpkg"), Paho, Json

5. [Node JS](https://nodejs.org/en/download/ "Node JS")

6. [Visual Studio 2017](https://www.visualstudio.com/downloads/ "Visual Studio 2017")

## Hardware requirements

1. Windows PC with 6th Generation Intel® Core™ Processors with Intel® Iris® Pro Graphics and HD Graphics, In our example we are using an Intel® NUC NUC7i7BNH with Intel® OPtane Memory.

2. 1 x Intel® Edison

3. 1 x Webcam

## Before You Begin

There are a few tutorials that you should follow before beginning, especially if it is the first time you have used the TechBubble IoT JumpWay Developer Program. If you do not already have one, you will require a TechBubble IoT JumpWay Developer Program developer account, and some basics to be set up before you can start creating your IoT devices. Visit the following [IoT JumpWay Developer Program Docs (5-10 minute read/setup)](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/ "IoT JumpWay Developer Program Docs (5-10 minute read/setup)") and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications (About 5 minutes read).

## Preparing Your Windows Device

- [Install Intel® Computer Vision SDK](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Computer-Vision-SDK/TASS-PVL/Windows/_Docs/1-Installing-Intel-CV-SDK.md "Install Intel® Computer Vision SDK")

- [Install Microsoft Vcpkg](https://github.com/Microsoft/vcpkg "Install Microsoft Vcpkg"), Paho, Json

- [Install Visual Studio 2017](https://www.visualstudio.com/downloads/ "Install Visual Studio 2017")

- Install Paho MQTT

    ```
    C:\src\vcpkg> vcpkg install paho-mqtt:x64-windows
    ```

    Once installed, edit the MQTTAsync.h and MQTTClient.h files in C:\src\vcpkg\installed\x64-windows\include.

    Change:

    ```
    #if defined(WIN32) || defined(WIN64)
        #define DLLImport __declspec(dllimport)
        #define DLLExport __declspec(dllexport)
    #else
        #define DLLImport extern
        #define DLLExport  __attribute__ ((visibility ("default")))
    #endif
    ```

    To:

    ```
    #if defined(_WIN32) || defined(_WIN64)
        #define DLLImport __declspec(dllimport)
        #define DLLExport __declspec(dllexport)
    #else
        #define DLLImport extern
        #define DLLExport  __attribute__ ((visibility ("default")))
    #endif
    ```

- Install Nlohmann Json

    ```
    C:\src\vcpkg> vcpkg install nlohmann-json:x64-windows
    ```

- Plug In Your Webcam 

    Plug in your webcam and make sure that you have all of the relevant drivers installed for your machine to recognise the device.

## Cloning The Repo

You will need to clone this repository to a location on your Intel® Edison. Navigate to the directory you would like to download it to and issue the following command, or use the Windows GitHub GUI.

    C:\YourChosenLocation> git clone https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples.git

## IoT JumpWay Intel® Computer Vision SDK Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel® Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Examples in your IoT projects.

## IoT JumpWay Intel® Computer Vision SDK Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../../../../../../../images/main/Intel-Software-Innovator.jpg)