# IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example

![IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example](../../../images/main/IoT-Jumpway.jpg)  

## Introduction

Here you will find sample device scripts for connecting Intel® Arduino/Genuino 101 and DFRobot LCD Keypad Shield to the TechBubble Technologies IoT JumpWay  using the Python MQTT Serial Library. The codes allow you to set up am intruder alarm system that is controlled by the DFRobot LCD Keypad Shield and the IoT JumpWay. Once you understand how it works you are free to add as many actuators and sensors to your device and modify your code accordingly.

This project uses three applications:

1. A device application (Arduino) which communicates via serial with a Python Serial/MQTT application.
2. The Python Serial/MQTT application which communicates with the Arduino/Genuio 101 / DFRobot LCD Keypad Shield, and the IoT JumpWay.
3. A python 

## Python Versions

- 2.7
- 3.4 or above

## Software requirements

1. iot_jumpway_mqtt_serial
2. Arduino/Genuino IDE

## Hardware Requirements

![IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example](../../../images/LCD-Intruder-System/DFRobot-LCD-Intruder-Hardware.jpg)

1. Intel® Arduino/Genuino 101.
2. DFRobot LCD Keypad Shield
3. 1 x DFRobot Digital PIR Sensor Module
4. 1 x DFRobot Digital Buzzer Module
5. 4 x male / female jumper wires
6. 2 x male / male jumper wires

## Before You Begin

If this is the first time you have used the TechBubble IoT JumpWay in your IoT projects, you will require a developer account and some basics to be set up before you can start creating your IoT devices. Visit the following link and check out the guides that take you through registration and setting up your Location Space, Zones, Devices and Applications.

[TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/ "TechBubble Technologies IoT JumpWay Developer Program (BETA) Docs")

## Adding The Arduino/Genuino Board To Arduino IDE

        - Tools -> Boards -> Boards Manager
        - Search for Curie, or Intel Curie
        - Right click on the right hand side of the Curie section and install the latest version

![IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example](../../../images/Docs/Curie.jpg)

## Install Requirements On Your PC

1. Install the iot_jumpway_mqtt_serial library:

    ```
        $ pip install iot_jumpway_mqtt_serial
    ```

## Setting Up Your Intel® Arduino/Genuino 101

![IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example](../../../images/LCD-Intruder-System/DFRobot-LCD-Intruder-Setup.jpg)

First of all you need to connect up your DFRobot LCD Keypad Shield to your Intel® Arduino/Genuino 101 and connect your DFRobot PIR Sensor Module & DFRobot Buzzer Module. Follow the next steps to accomplish this.

1. Place the shield on top of your Arduino as in the image above. 
2. Connect 3 or your male / female jumper wires to on end of your DFRobot PIR sensor wires.
3. Connect the green wire to D2 on the DFRobot LCD Keypad Shield, red to VCC and black to GND.
4. Connect your final male / female jumper wire to the green DFRobot buzzer wire, and the 2 male / male wires to the red and black wires of the buzzer.
5. Connect the green wire to D3 on the DFRobot LCD Keypad Shield, red to VCC and black to GND.

## Device Connection Credentials & Actuator Settings

- Follow the [TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Docs/blob/master/4-Location-Devices.md "TechBubble Technologies IoT JumpWay Developer Program (BETA) Location Device Doc") to set up your device. 

![IoT JumpWay  IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example Docs](../../../images/Basic-LED/Device-Creation.png)  

- Download the [TechBubble IoT JumpWay Python MQTT Serial Library Application](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Python-MQTT-Serial-Client/blob/master/application.py "TechBubble IoT JumpWay Python MQTT Serial Library Application") and the [TechBubble IoT JumpWay Python MQTT Serial Library Config File](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Python-MQTT-Serial-Client/blob/master/config.json "TechBubble IoT JumpWay Python MQTT Serial Library Config File"). Retrieve your connection credentials by following the link above, and update the config.json file with your new connection  credentials.

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

- Open up the [IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Arduino-101/3RD-PARTY-DFRobot/LCD-Intruder-System/LCD-Intruder-System.ino "IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example") and update the following lines with your DFRobot LCD Keypad Shield  & Module IDs retrieved from the steps above, then upload the sketch to your device:

    ```
        String JumpWaySensorType = "LCD Keypad";
        String JumpWaySensorID = "1";

        String JumpWaySensorType2 = "PIR Sensor";
        String JumpWaySensorID2 = "2";

        String JumpWaySensorType3 = "Buzzer";
        String JumpWaySensorID3 = "3";
    ```

- You may also need to alter the debounceWait variable if the buttons trigger multiple times.

    ```
        int debounceWait = 150;
    ```

## Execute The Python Program

As you have already uploaded your sketch, the program will now be running on your Arduino/Genuino 101. All that is left is to start the Python program with the following line:

    $ python NameOfYourSerialApplication.py 

## Autonomous Communication With Second Device

COMING SOON

## Viewing Your Data  

Each time you press a button, it will send data to the [TechBubble IoT JumpWay](https://iot.techbubbletechnologies.com/ "TechBubble IoT JumpWay"). You will be able to access the data in the [TechBubble IoT JumpWay Developers Area](https://iot.techbubbletechnologies.com/developers/dashboard/ "TechBubble IoT JumpWay Developers Area"). Once you have logged into the Developers Area, visit the [TechBubble IoT JumpWay Location Devices Page](https://iot.techbubbletechnologies.com/developers/location-devices "Location Devices page"), find your device and then visit the Sensor/Actuator page and the Warnings page to view the data sent from your device.

![IoT JumpWay  IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example Docs](../../../images/Basic-LED/SensorData.png)

![IoT JumpWay  IoT JumpWay Intel® Arduino/Genuino 101 DFRobot LCD Intruder System Example Docs](../../../images/Basic-LED/WarningData.png)

## IoT JumpWay Intel® Arduino/Genuino 101 Examples Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel® Arduino/Genuino 101 Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Arduino/Genuino 101 Examples in your IoT projects.

## IoT JumpWay Intel® Arduino/Genuino 101 Examples Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../../images/main/Intel-Software-Innovator.jpg)  