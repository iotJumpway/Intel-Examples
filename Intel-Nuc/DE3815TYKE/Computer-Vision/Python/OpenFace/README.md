# IoT JumpWay Intel® NUC DE3815TYKE OpenFace Computer Vision Example

![oT JumpWay Intel® NUC DE3815TYKE OpenFace Computer Vision Example](../../../../../images/NUC-DE3815TYKE/Computer-Vision/OpenFace/Intel-NUC-DE3815TYKE-CV.png)

## Introduction

Want to turn your Intel NUC DE3815TYKE into an Artificially Intelligent, IoT Connected CCTV Hub? This tutorial is for you!.

## What Will We Build?

The tutorial will use TechBubble Technologies IoT JumpWay Python MQTT Library for communication, an Intel® NUC DE3815TYKE 1 or more IP Cameras, an optional Realsense camera, and our own deep learning neural network based on the popular OpenFace facial recognition toolkit.

## Python Versions

- 2.7

## Software requirements

1. [TechBubble IoT JumpWay Python MQTT Client](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Python-MQTT-Clients "TechBubble IoT JumpWay Python MQTT Client")
1. [OpenFace](https://github.com/cmusatyalab/openface "OpenFace")

## Hardware requirements

1. Intel® NUC DE3815TYKE (Should work with other versions of Intel® NUC).
2. 1 or more IP cameras.  (Tested with 1)
3. 1 x Realsense camera (OPTIONAL) (Tested with F200 & R200)

## Before You Begin

There are a few tutorials that you should follow before beginning, especially if it is the first time you have used the TechBubble IoT JumpWay Developer Program. If you do not already have one, you will require a TechBubble IoT JumpWay Developer Program developer account, and some basics to be set up before you can start creating your IoT devices. Visit the following [IoT JumpWay Developer Program Docs (5-10 minute read/setup)](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/ "IoT JumpWay Developer Program Docs (5-10 minute read/setup)") and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications (About 5 minutes read).

## Preparing Your Intel® NUC DE3815TYKE

If you do not already have Ubuntu Server 16.04 LTS installed on your Intel® NUC DE3815TYKE, follow the [Installing Ubuntu Server 16.04 LTS on Intel® NUC DE3815TYKE](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Nuc/DE3815TYKE/_DOCS/1-Installing-Ubuntu-Server.md "Installing Ubuntu Server 16.04 LTS on Intel® NUC DE3815TYKE") guide.

## Cloning The Repo

You will need to clone this repository to a location on your Intel® NUC DE3815TYKE. Navigate to the directory you would like to download it to and issue the following commands.

    $ git clone https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples.git

## Install Requirements

    $ cd IoT-JumpWay-Intel-Examples/Intel-Nuc/DE3815TYKE/Computer-Vision/Python/OpenFace
    $ sudo apt install python-pip
    $ pip install --upgrade pip
    $ sudo pip install -r requirements.txt

## Install Remaining Required Software

1. Follow the [Installing OpenFace on Intel® NUC DE3815TYKE](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Nuc/DE3815TYKE/_DOCS/2-Installing-OpenFace.md "Installing OpenFace on Intel® NUC DE3815TYKE") guide.

2. Follow the [Installing Librealsense & Pyrealsense on Intel® NUC DE3815TYKE](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Nuc/DE3815TYKE/_DOCS/3-Installing-Librealsense.md "Installing Librealsense & Pyrealsense on Intel® NUC DE3815TYKE") guide. (OPTIONAL BUT REQUIRED IF USING REALSENSE CAMERA)

## IoT JumpWay Device / Application Connection Credentials & Settings

- Follow the [TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Application Doc](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/blob/master/5-Location-Applications.md "TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Application Doc") to set up your IoT JumpWay Location Application.

- Setup an IoT JumpWay Location Device for each IP camera you will be connecting to, and / or your Realsense camera. For this example, we only require the device ID for each camera, we will not be using the MQTT details for each camera as the application is capable of sending data on behalf of any device in its location. Follow the [TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/blob/master/4-Location-Devices.md "TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc") to set up your devices.

![IoT JumpWay Intel® Edison Basic LED Example Docs](../../../images/Docs/Device-Creation.png)

- Retrieve your connection credentials and update the config.json file with your new connection credentials and camera IDs, add a new entry to CameraList for each IP cam, and add your Realsense camera ID.

```
    "CameraList": [
        {
            "camID": "Your Camera ID from the IoT JumpWay here",
            "camURL": "URL to your IP camera here"
        }
    ],
    "RealsenseCam": {
        "camID": "Your Realsense Camera ID from the IoT JumpWay here"
    }
```

```
	"IoTJumpWaySettings": {
        "SystemLocation": 0,
        "SystemZone": 0,
        "SystemApplicationID": 0,
        "SystemApplicationName" : "Your Application Name"
	}
```

```
	"IoTJumpWayMQTTSettings": {
        "host": "https://iot.techbubbletechnologies.com",
        "port": "8883",
        "applicationUsername": "Your Application MQTT Username",
        "applicationPassword": "Your Application MQTT Password"
	}
```

## IoT JumpWay Intel® NUC DE3815TYKE Examples Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the Intel® NUC DE3815TYKE Docs. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Examples in your IoT projects.

## IoT JumpWay Intel® NUC DE3815TYKE Examples Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../../../../images/main/Intel-Software-Innovator.jpg)