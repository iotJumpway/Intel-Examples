
# TASS Movidius Example
## IoT Connected Computer Vision

![TASS Movidius Example](images/tass-movidius.jpg)

Acknowledgements: Uses code from Intel movidius/ncsdk ([movidius/ncsdk Github](https://github.com/movidius/ncsdk "movidius/ncsdk Github"))

## Introduction

TASS Movidius uses a pretrained Inception V3 model and an Intel® Movidius to carry out object and facial classification, both locally and on a live webcam stream. 

## Python Versions

- Tested in Python 3

## Software Requirements

- [Intel® NCSDK](https://github.com/movidius/ncsdk "Intel® NCSDK") 
- [IoT JumpWay MQTT Client](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Python-MQTT-Clients "IoT JumpWay MQTT Client") 

## Hardware Requirements

- Intel® Movidius

This tutorial can be used on a number of devices: 

- Laptop / PC running Ubuntu
- Intel® NUC running Ubuntu / Ubuntu LTS
- Raspberry Pi running Ubuntu LTS

## Install NCSDK

The first thing you will need to do once you have your operating system on your device is to install the NCSDK. For this you can follow the [official Github Repo README](https://github.com/movidius/ncsdk "official Github Repo README"). Once you have completed the instructions in the README and all is working correctly having run the examples, you can move to the next step in this tutorial. Some helpful advice here maybe to make sure that you use python3 if you run the run.py example as if you do not it may classify the image as a ringworm. 

## Cloning The Repo

You will need to clone this repository to a location on your development terminal. Navigate to the directory you would like to download it to and issue the following commands.

    $ git clone https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples.git
	
Once you have the repo, you will need to find the files in this folder located in [Intel-Movidius/TASS directory](# "Intel-Movidius/TASS directory")

