# IoT JumpWay Intel® Arduino/Genuino 101 Dev Kit LED Example

![IoT JumpWay Intel® Arduino/Genuino 101 Dev Kit LED Example Docs](../../images/Dev-Kit-LED/Arduino-101-Dev-Kit-LED.png)

## Introduction

Here you will find sample device scripts for connecting an Intel® Arduino/Genuino 101 and IoT Dev Kit to the IoT JumpWay using the Python MQTT Serial Library.

This tutorial helps you to set up an Arduino/Genuino 101 that allows control of an LED, and also an application that can control the LED via the IoT JumpWay.

## This project uses three applications:

1. A device application (Arduino) which communicates via serial with a Python Serial/MQTT application.
2. The Python Serial/MQTT application which communicates with the Arduino/Genuio 101 and the IoT JumpWay.
3. A Python MQTT application that sends commands to Arduino/Genuino 101 via the IoT JumpWay and the Python Serial/MQTT application.

## Python Versions

- 2.7 (Python Serial/MQTT application)
- 3.4 or above (Python commands application)

## Software requirements

1. [IoT JumpWay Python MQTT Serial Library](https://github.com/iotJumpway/IoT-JumpWay-Python-MQTT-Serial-Client "IoT JumpWay Python MQTT Serial Library")
2. Arduino/Genuino IDE
2. ArduinoJson

## Hardware Requirements

![IoT JumpWay Intel® Arduino/Genuino 101 Dev Kit LED Example Docs](../../images/Dev-Kit-LED/Arduino-101-Hardware.jpg)

1. Intel® Arduino/Genuino 101.
2. Grove starter kit for Intel® Arduino/Genuino 101.
3. 1 x LED.

## Before You Begin

If this is the first time you have used the IoT JumpWay in your IoT projects, you will require a developer account and some basics to be set up before you can start creating your IoT devices. Visit the following link and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications (About 5 minutes).

[IoT JumpWay Developer Program (BETA) Docs](https://github.com/iotJumpway/IoT-JumpWay-Docs/ "IoT JumpWay Developer Program (BETA) Docs")

## Adding The Arduino/Genuino Board To Arduino IDE

        - Tools -> Boards -> Boards Manager
        - Search for Curie, or Intel Curie
        - Right click on the right hand side of the Curie section and install the latest version

![IoT JumpWay Intel® Arduino/Genuino 101 Dev Kit LED Example Docs](../../images/Docs/Curie.jpg)

## Install Requirements On Your PC & Arduino/Genuino 101

1. For the Python Serial/MQTT application we will need the [IoT JumpWay Python MQTT Serial Library](https://github.com/iotJumpway/IoT-JumpWay-Python-MQTT-Serial-Client "IoT JumpWay Python MQTT Serial Library") installed on our PC/laptop/Mac. To Install the library, issue the following command on your chosen device:

    ```
        $ pip install iot_jumpway_mqtt_serial
    ```

2. Install the ArduinoJson library in the Arduino IDE:

    ```
        Sketch -> Include Library -> Manage Libraries
        Search for ArduinoJson
        Right click on the right hand side of the ArduinoJson section and install the latest version
    ```

![IoT JumpWay Intel® Arduino/Genuino 101 Dev Kit LED Example Docs](../../images/Docs/ArduinoJson.jpg)

## Setting Up Your Intel® Arduino/Genuino 101

![IoT JumpWay Intel® Arduino/Genuino 101 Dev Kit LED Example Docs](../../images/Dev-Kit-LED/Arduino-101-Setup.jpg)

First of all you need to connect up an LED to your Intel® Arduino/Genuino 101. To connect the LED you will need a Grove starter kit for Intel® Arduino/Genuino/Genuino 101.

1. Connect the Grove Starter Kit to your Intel® Arduino/Genuino 101.
2. Connect the LED to pin D5 of your Grove Starter Kit.

## Device Connection Credentials & Actuator Settings

- Follow the [IoT JumpWay Developer Program (BETA) Location Device Doc](https://github.com/iotJumpway/IoT-JumpWay-Docs/blob/master/4-Location-Devices.md "IoT JumpWay Developer Program (BETA) Location Device Doc") (About 1 minute) to set up your device, and the [IoT JumpWay Developer Program (BETA) Location Application Doc](https://github.com/iotJumpway/IoT-JumpWay-Docs/blob/master/5-Location-Applications.md "IoT JumpWay Developer Program (BETA) Location Application Doc") (About 1 minute) to set up your MQTT application, you will need the MQTT application to communicate with your serial application further on in the tutorial.

![IoT JumpWay  Intel® Arduino/Genuino 101 Dev Kit LED Example Docs](../../images/Dev-Kit-LED/Device-Creation.png)

- Download the [IoT JumpWay Python MQTT Serial Library Application](https://github.com/iotJumpway/IoT-JumpWay-Python-MQTT-Serial-Client/blob/master/application.py "IoT JumpWay Python MQTT Serial Library Application") and the [IoT JumpWay Python MQTT Serial Library Config File](https://github.com/iotJumpway/IoT-JumpWay-Python-MQTT-Serial-Client/blob/master/config.json "IoT JumpWay Python MQTT Serial Library Config File"), retrieve your connection credentials by following the link above, and update the config.json file with your new connection  credentials and actuator (LED) setting.

```
	"IoTJumpWaySettings": {
        "SystemLocation": 0,
        "SystemZone": 0,
        "SystemDeviceID": 0,
        "SystemDeviceName" : "Your Device Name",
        "SystemDeviceCom" : "Your Device Com Port"
    },
	"IoTJumpWayMQTTSettings": {
        "MQTTUsername": "Your Device MQTT Username",
        "MQTTPassword": "Your Device MQTT PASSWORD"
    }
```

- Open up the [Arduino/Genuino 101 Dev Kit LED Example](https://github.com/iotJumpway/IoT-JumpWay-Intel-Examples/blob/master/Intel-Arduino-101/Dev-Kit-LED/Dev-Kit-LED.ino "Arduino/Genuino 101 Dev Kit LED Example") in the Arduino IDE, and update the following line with your LED actuator ID retrieved from the steps above, then upload the sketch to your device:

    ```
        const int actuator1JumpWayID = 0;
    ```

## Execute The Python Program

As you have already uploaded your sketch, the program will now be running on your Arduino/Genuino 101. All that is left is to start the Python program with the following line:

    $ python NameOfYourSerialApplication.py

## Control Your Device With Your MQTT Application

Now it is time to set up your MQTT application mentioned in the steps above.

1. For this application you can use the application and config file from the [IoT JumpWay Intel® Edison Dev Kit LED Example](https://github.com/iotJumpway/IoT-JumpWay-Intel-Examples/tree/master/Intel-Edison/Dev-Kit-LED/Python "IoT JumpWay Intel® Edison Dev Kit LED Example").

2. Use the application information you received from steps above to fill out the details below:

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
            "username": "Your Device MQTT Username",
            "password": "Your Device MQTT Password",
            "applicationUsername": "Your Application MQTT Username",
            "applicationPassword": "Your Application MQTT Password"
        }
    ```

## Execute The Python Program

Now all you have to do is execute your MQTT application. This application sends a device command to turn on your LED through the IoT JumpWay to your serial application, which in turn, sends the command via serial to the relevant actuator on your Arduino/Genuino 101, in this case, your LED:

    $ python/python3 NameOfYourMQTTApplication.py

## Viewing Your Data

Each command sent to the device is stored in the [IoT JumpWay](https://iot.techbubbletechnologies.com/ "IoT JumpWay"). You will be able to access the data in the [IoT JumpWay Developers Area](https://iot.techbubbletechnologies.com/developers/dashboard/ "IoT JumpWay Developers Area"). Once you have logged into the Developers Area, visit the [IoT JumpWay Location Devices Page](https://iot.techbubbletechnologies.com/developers/location-devices "Location Devices page"), find your device and then visit the Commands Data page to view the data sent from your device.

![IoT JumpWay  Intel® Arduino/Genuino 101 Dev Kit LED Example Docs](../../images/Dev-Kit-LED/SensorData.png)

![IoT JumpWay  Intel® Arduino/Genuino 101 Dev Kit LED Example Docs](../../images/Dev-Kit-LED/WarningData.png)

## HACKSTER

For Hackster community members you can follow this project on the IoT JumpWay Hub:

[Follow This Project On Hackster](https://www.hackster.io/AdamMiltonBarker/intel-arduino-genuino-101-dev-kit-led-example-980afb "Follow This Project On Hackster")

## IoT JumpWay Intel® Arduino/Genuino 101 Examples Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel® Arduino/Genuino 101 Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Arduino/Genuino 101 Examples in your IoT projects.

## IoT JumpWay Intel® Arduino/Genuino 101 Examples Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/iotJumpway "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../images/main/Intel-Software-Innovator.jpg)