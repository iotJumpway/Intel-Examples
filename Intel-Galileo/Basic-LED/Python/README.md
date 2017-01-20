# IoT JumpWay Intel Galileo Gen 1 Basic LED Example

![IoT JumpWay Intel Galileo Gen 1 Basic LED Example Docs](../../../images/main/IoT-Jumpway.jpg)  

## Introduction

Here you will find sample device scripts for connecting Intel Galileo Gen 1 to the TechBubble Technologies IoT JumpWay using the Python MQTT Library. The codes allow you to set up a basic device that allows control of an LED. Once you understand how it works you are free to add as many actuators and sensors to your device and modify your code accordingly.

## Before You Begin

If this is the first time you have used the TechBubble IoT JumpWay in your IoT projects, you will require a developer account and some basics to be set up before you can start creating your IoT devices. Visit the following link and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications.

[TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/ "TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs")

## Python Versions

- 2.7
- 3

## Hardware requirements

1. Intel Galileo Gen 1.
2. 1 x LED.
3. 1 x 220 ohm Resistor
4. 2 x Jumper Wires
5. 1 x Breadboard

## Software requirements

1. TechBubbleIoTJumpWayMQTT  
2. JSon

## Preparing Your Intel Galileo Gen 1

To help secure your Intel Galileo Gen 1, follow the [Intel Galileo Security](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Galileo/DOCS/1-Security.md "Intel Galileo Security") guide.

## Install Requirements

    $ pip install --upgrade pip
    $ pip install -r requirements.txt

## Setting Up Your Raspberry Pi

First of all you need to connect up an LED to your Intel Galileo Gen 1. To connect the LED you will need a breadboard, a 220 ohm resistor, and two jumper wires. 

1. Place the LED on your breadboard.
2. Connect the short leg of the LED to pin 5 of your Intel Galileo Gen 1 using a jumper wire.
3. Connect one end of the resistor to the long leg of your LED.
4. Connect the other end of the resistor to the 3v output of the Intel Galileo Gen 1.

## Connection Credentials & Sensor Settings

- Follow the [TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc-](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/blob/master/4-Location-Devices.md "TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc") to set up your device. 

![IoT JumpWay Intel Galileo Gen 1 Basic LED Example Docs](../../../images/Basic-LED/Device-Creation.png)  

- Retrieve your connection credentials and update the config.json file with your new connection  credentials and sensor setting.

```
	"Sensors": {
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
		"SystemDeviceName" : "Your Device Name"
	}
```


```
	"IoTJumpWayMQTTSettings": {
		"host": "https://iot.techbubbletechnologies.com",
		"port": "8883",
		"username": "Your MQTT Username",
		"password": "Your MQTT Password"
	}
```


## Execute The Program

    $ python/python3 Basic-Led.py 

## IoT JumpWay Intel Galileo Examples Bugs/Issues

Please feel free to create issues for bugs and general issues you come accross whilst using the IoT JumpWay Intel Galileo Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel Galileo Examples in your IoT projects.