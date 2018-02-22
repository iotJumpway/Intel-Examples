
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

## Test Inception V3 Object Recognition

Now that everything is working, you can execute the following command which will start the program in Inception V3 object detection testing mode. To be in test mode you must edit the ClassifierSettings-MODE setting in data/confs.json to be InceptionTest.

```
python3 tass.py
```

If all went well, it should of taken about 0.3 seconds to identify each image, and out of the 11 images tested 10 were identified with a confidence higher than 50%, and the whole process should take around 4 or 5 seconds on an Intel® NUC. 

### Intel® NUC

```
- Loaded Test Image data/testing/images/512_InkjetPrinter.jpg

- DETECTION STARTED:  1519248012.519896
- Loaded Tensor
- DETECTION ENDED: 0.3664424419403076

TASS Detected Image ID 743 printer With A Confidence Of 0.97266

Published: 11
Published to Device Sensors Channel
Published To IoT JumpWay

*******************************************************************************
inception-v3 on NCS
*******************************************************************************
743 printer 0.97266
714 photocopier 0.024628
663 modem 0.00094414
733 Polaroid camera, Polaroid Land camera 0.00045657
746 projector 0.00042224
*******************************************************************************
```

```
TESTING ENDED
TESTED: 11
IDENTIFIED: 10
TESTING TIME: 4.594240665435791
```

## Test Yolo Object Recognition

You can execute the following command which will start the program in Yolo object detection testing mode. To be in Yolo object detection testing mode you must edit the ClassifierSettings-MODE setting in data/confs.json to be YoloTest.

```
python3 tass.py
```

If all went well, it should of taken about 0.7 seconds to identify the car and the bicycle. The TESTING TIME includes the time to publish the notification to the IoT JumpWay, the whole process should take around 1.4 seconds on an Intel® NUC. 

### Intel® NUC

```
- Loaded Test Image data/testing/yolo/dog.jpg

- DETECTION STARTED:  2018-02-22 02:00:50.509681
/usr/local/lib/python3.5/dist-packages/skimage/transform/_warps.py:84: UserWarning: The default mode, 'constant', will be changed to 'reflect' in skimage 0.15.
  warn("The default mode, 'constant', will be changed to 'reflect' in "
- Loaded Tensor
- DETECTION ENDED: 0.7135429382324219

- SAVED IMAGE/FRAME
- SAVED IMAGE/FRAME

TASS Detected  car With A Confidence Of 0.293343544006

Published: 2
Published to Device Sensors Channel
Published To IoT JumpWay


TASS Detected  bicycle With A Confidence Of 0.23780977726

Published: 3
Published to Device Sensors Channel
Published To IoT JumpWay


TESTING YOLO ENDED
TESTED: 1
IDENTIFIED: 2
TESTING TIME: 1.4020063877105713
```

## Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using this or any other Intel related IoT JumpWay issues. You may also use the issues area to ask for general help whilst using the IoT JumpWay in your IoT projects.

## Contributors

[![Adam Milton-Barker, Intel® Software Innovator](../../images/main/Intel-Software-Innovator.jpg)](https://github.com/AdamMiltonBarker)

 