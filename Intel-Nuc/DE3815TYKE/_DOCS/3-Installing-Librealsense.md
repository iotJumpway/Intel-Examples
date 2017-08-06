# Installing Librealsense & Pyrealsense on Intel® NUC DE3815TYKE

![TechBubble IoT JumpWay Docs](../../../images/Docs/Intel-NUC-Documentation.png)

## Introduction

The following information will help you install Librealsense & Pyrealsense on the Intel® Nuc DE3815TYKE.

## Install Librealsense

    $ sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade

    $ sudo apt-get install libusb-1.0-0-dev pkg-config

    $ sudo apt-get install libglfw3-dev

    $ git clone https://github.com/IntelRealSense/librealsense.git

    $ cd librealsense

    $ mkdir build && cd build

    $ cmake ../

    $ make && sudo make install

## Install Pyrealsense

    $ sudo pip install pycparser

    $ sudo pip install cython

    $ sudo sudo pip install pyrealsense

## IoT JumpWay Intel® NUC DE3815TYKE Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel® Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Examples in your IoT projects.

## IoT JumpWay Intel® NUC DE3815TYKE Examples Document Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel® Software Innovator](../../../images/main/Intel-Software-Innovator.jpg)







