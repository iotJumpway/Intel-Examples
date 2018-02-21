
# TASS Movidius Example: IoT Connected Computer Vision

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

## Install IoT JumpWay MQTT Client

Next install the IoT JumpWay MQTT Client. For this you can execute the following command:

```
pip3 install techbubbleiotjumpwaymqtt 
```

## Cloning The Repo

You will need to clone this repository to a location on your development terminal. Navigate to the directory you would like to download it to and issue the following commands.

    $ git clone https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples.git
	
Once you have the repo, you will need to find the files in this folder located in [Intel-Movidius/TASS directory](https://github.com/AdamMiltonBarker/IoT-JumpWay-Intel-Examples/tree/master/Intel-Movidius/TASS "Intel-Movidius/TASS directory"). You will need to navigate to this directory in your terminal also, once you are there, execute the following command:

```
make all
```

This will run ncprofile, nccompile and run:

1. Downloads the TensorFlow checkpoint file.
2. Runs the conversion/save python script to generate network.meta file.
3. Profiles, Compiles and Checks the network using the Neural Compute SDK.
4. Runs tass.py

## Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using this or any other Intel related IoT JumpWay issues. You may also use the issues area to ask for general help whilst using the IoT JumpWay in your IoT projects.

## Contributors

[![Adam Milton-Barker, Intel® Software Innovator](../../images/main/Intel-Software-Innovator.jpg)](https://github.com/AdamMiltonBarker)

 