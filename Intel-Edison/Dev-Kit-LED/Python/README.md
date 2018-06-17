# IoT JumpWay Intel® Edison Dev Kit LED Example

![IoT JumpWay Intel® Edison Dev Kit LED Example Docs](../../../images/Dev-Kit-LED/Intel-Edison-Dev-Kit-LED.png)

## Introduction

Want to take your first steps into the magical world of the Internet of Things, or want to find out how easy it is to use the IoT JumpWay as your secure IoT communication platform? This tutorial is for you an will hold your hand through setting up your first Intel® Edison project powered by the IoT JumpWay.

## What Will We Build?

This tutorial is a simple tutorial that will help you take your first steps to using the IoT JumpWay to connect your IoT devices and applications to the Internet of Things.

The tutorial will use IoT JumpWay Python MQTT Library for communication, an Intel® Edison and IoT Dev Kit with an added LED, and an application that can control the LED via the IoT JumpWay.

## Python Versions

- 2.7
- 3.4 or above

## Software requirements

1. [IoT JumpWay Python MQTT Client](https://github.com/iotJumpway/JumpWayMQTT "IoT JumpWay Python MQTT Client")

## Hardware Requirements

![IoT JumpWay Intel® Edison Dev Kit LED Example Docs](../../../images/Dev-Kit-LED/Edison-Hardware.jpg)

1. Intel® Edison.
2. Grove starter kit plus - Intel IoT Edition for Intel® Edison.
3. 1 x LED.

## Before You Begin

There are a few tutorials that you should follow before beginning, especially if it is the first time you have followed any of our Raspberry Pi tutorials or if it is the first time you have used the IoT JumpWay Developer Program. If this is the first time you have used the IoT JumpWay in your IoT projects, you will require a developer account and some basics to be set up before you can start creating your IoT devices. Visit the following [IoT JumpWay Developer Program Docs (5-10 minute read/setup)](https://github.com/iotJumpway/IoT-JumpWay-Docs/ "IoT JumpWay Developer Program Docs (5-10 minute read/setup)") and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications (About 5 minutes read).

- [Intel® Edison Security](https://github.com/iotJumpway/IoT-JumpWay-Intel-Examples/blob/master/Intel-Edison/DOCS/1-Security.md "Intel® Edison Security")

- [Intel® Edison Booting From SD (Linux)](https://github.com/iotJumpway/IoT-JumpWay-Intel-Examples/blob/master/Intel-Edison/_DOCS/1-Booting-From-SD-Linux.md "Intel® Edison Booting From SD (Linux)")

## Preparing Your Intel® Edison

To help secure your Intel® Edison, follow the [Intel® Edison Security](https://github.com/iotJumpway/IoT-JumpWay-Intel-Examples/blob/master/Intel-Edison/DOCS/1-Security.md "Intel® Edison Security") and the  [Intel® Edison Booting From SD (Linux)](https://github.com/iotJumpway/IoT-JumpWay-Intel-Examples/blob/master/Intel-Edison/_DOCS/1-Booting-From-SD-Linux.md "Intel® Edison Booting From SD (Linux)") guides.

## Cloning The Repo

You will need to clone this repository to a location on your Intel® Edison. Navigate to the directory you would like to download it to and issue the following commands.

    $ git clone https://github.com/iotJumpway/IoT-JumpWay-Intel-Examples.git

## Install Requirements

    $ cd IoT-JumpWay-Intel-Examples/Intel-Edison/Dev-Kit-LED/Python
    $ pip install --upgrade pip
    $ pip install -r requirements.txt

## Setting Up Your Intel® Edison

![IoT JumpWay Intel® Edison Dev Kit LED Example Docs](../../../images/Dev-Kit-LED/Edison-Blinking.jpg)

First of all you need to connect up an LED to your Intel® Edison. To connect the LED you will need an IoT Dev Kit.

1. Connect the IoT Dev Kit to your Intel® Edison.
2. Connect the LED to pin D5 of your IoT Dev Kit.

## Device / Application Connection Credentials & Sensor Settings

- Follow the [IoT JumpWay Developer Program (BETA) Location Device Doc](https://github.com/iotJumpway/IoT-JumpWay-Docs/blob/master/4-Location-Devices.md "IoT JumpWay Developer Program (BETA) Location Device Doc") to set up your device, and the [IoT JumpWay Developer Program (BETA) Location Application Doc](https://github.com/iotJumpway/IoT-JumpWay-Docs/blob/master/5-Location-Applications.md "IoT JumpWay Developer Program (BETA) Location Application Doc") to set up your application.

![IoT JumpWay Intel® Edison Basic LED Example Docs](../../../images/Docs/Device-Creation.png)

- Retrieve your connection credentials and update the config.json file with your new connection  credentials and actuator (LED) setting.

```
	"Actuators": {
		"LED": {
			"ID": 0,
			"PIN": 5
		}
	}
```

```
	"IoTJumpWaySettings": {
        "SystemLocation": 0,
        "SystemZone": 0,
        "SystemDeviceID": 0,
        "SystemDeviceName" : "Your Device Name",
        "SystemApplicationID": 0,
        "SystemApplicationName" : "Your Application Name"
	}
```

```
	"IoTJumpWayMQTTSettings": {
        "host": "https://iot.techbubbletechnologies.com",
        "port": "8883",
        "username": "Your Device MQTT Username",
        "password": "Your Device MQTT Password",
        "applicationUsername": "Your Application MQTT Username",
        "applicationPassword": "Your Application MQTT Password"
	}
```

## Execute The Programs

    $ sudo python/python3 Dev-Kit-Led-Device.py
    $ sudo python/python3 Dev-Kit-Led-Application.py

## Viewing Your Data

Each command sent to the device is stored in the [IoT JumpWay](https://iot.techbubbletechnologies.com/ "IoT JumpWay"). You will be able to access the data in the [IoT JumpWay Developers Area](https://iot.techbubbletechnologies.com/developers/dashboard/ "IoT JumpWay Developers Area"). Once you have logged into the Developers Area, visit the [IoT JumpWay Location Devices Page](https://iot.techbubbletechnologies.com/developers/location-devices "Location Devices page"), find your device and then visit the Commands Data page to view the data sent from your device.

![IoT JumpWay Intel® Edison Basic LED Example Docs](../../../images/Basic-LED/SensorData.png)

![IoT JumpWay Intel® Edison Basic LED Example Docs](../../../images/Basic-LED/WarningData.png)

## IoT JumpWay Intel® Edison Examples Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel® Edison Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Edison Examples in your IoT projects.

## IoT JumpWay Intel® Edison Examples Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/iotJumpway "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../../images/main/Intel-Software-Innovator.jpg)