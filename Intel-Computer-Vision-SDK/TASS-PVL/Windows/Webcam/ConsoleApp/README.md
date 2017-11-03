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

3. 1x Grove starter kit plus - Intel IoT Edition for Intel® Edison

4. 1 x Blue LED (Grove)

5. 1 x Red LED (Grove)

6. 1 x Buzzer (Grove)

7. 1 x Webcam

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

## IoT JumpWay Device Connection Credentials & Settings

- Follow the [TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Application Doc](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/blob/master/5-Location-Applications.md "TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Application Doc") to set up your IoT JumpWay Location Application.

- Setup an IoT JumpWay Location Device for TASS PVL, ensuring you set up you camera node,as you will need the ID of the camera for the project to work. Once your create your device, make sure you note the MQTT username and password, the device ID and device name exactly, you will also need the zone and location ID. You will need to edit your device and add the rules that will allow it to communicate autonomously with the Intel Edison, but for now, these are the only steps that need doing at this point.

Follow the [TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/blob/master/4-Location-Devices.md "TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc") to set up your devices.

![IoT JumpWay Device Creation Docs](../../../../../images/Docs/Device-Creation.jpg)

- Locate and update the following code in TASS-PVL-Windows-Console, and replace with your device settings.

```
    int IntelliLanLocation = 0;
    int IntelliLanZone = 0;
    int IntelliLanDevice = 0;
    int IntelliLanSensor = 0;
    std::string IntelliLanDeviceN = "YourIoTJumpWayDeviceNameHere";
    std::string IntelliLanDeviceU = "YourIoTJumpWayDeviceUsernameHere";
    std::string IntelliLanDeviceP = "YourIoTJumpWayDevicePasswordHere";
```

- You may also need to edit this value, this allows the application to connect to your webcam, generally the value is either 1 or 0, in my case it is 1 which is the default setting in the provided application. If you receive an error on startup that the application cannot connect to your camera, you will need to modify this setting and ensure that you have installed all the required drivers for your camera.

```
    int camera = 1;
```

## Additional Include Directories & Library Directories

If you installed the Intel® Computer Vision SDK to any directory other than the default (C:\Intel\CV SDK\) you will need to update the Additional Include Directories & Library Directories settings to reflect your installed location. 

![Additional Include Directories](../../../../images/CPP-Additional-Include-Directories)

![Additional Library Directories](../../../../images/Linker-Additional-Library-Directories.PNG)

## Setting Up Your Intel® Edison

![IoT JumpWay Intel® Edison Dev Kit IoT Alarm](../../../../images/Edsion-Hardware-Setup.jpg)

The next step is to set up your Intel® Edison so that TASS PVL can communicate with it via the IoT JumpWay. For this, we already created a tutorial, the IoT JumpWay Intel® Edison Dev Kit IoT Alarm, that will guide you through this process. The only difference is that you do not need to set up the Python commands application, as in this project, TASS PVL will replace the Python commands application, to save time, please only follow the steps for the Intel® Edison device Node JS application. 

You will find the tutorial on the following link: 

[IoT JumpWay Intel® Edison Dev Kit IoT Alarm](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/tree/master/Intel-Edison/Dev-Kit-IoT-Alarm/NodeJS "IoT JumpWay Intel® Edison Dev Kit IoT Alarm")

Once you have completed that tutorial and have your device setup, return he to complete the final integration steps.

## IoT JumpWay Intel® Computer Vision SDK Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel® Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Examples in your IoT projects.

## IoT JumpWay Intel® Computer Vision SDK Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../../../../../../../images/main/Intel-Software-Innovator.jpg)