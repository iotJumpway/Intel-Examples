# Installation Of OpenCV On Intel® Edison

![IoT JumpWay Docs](../../images/Docs/Intel-Edison-Documentation.png)

## Introduction

The following information will help you install OpenCV on your Intel® Edison. This installation currently does not include the additional modules required for facial identification.

## Hardware Requirements

1. Intel® Edison.
2. 8 - 16 GB Card

## Guide

1. Before you can install OpenCV on your Intel® Edison, you need to setup your Edison to boot from an SD card. Use the following tutorial to accomplish this:

    [Booting Your Intel® Edison From An SD (Linux)](https://github.com/iotJumpway/IoT-JumpWay-Intel-Examples/blob/master/Intel-Edison/_DOCS/1-Booting-From-SD-Linux.md "Booting Your Intel® Edison From An SD (Linux)")

2. Execute the following:

    ```
        # echo "src/gz all http://repo.opkg.net/edison/repo/all

        src/gz edison http://repo.opkg.net/edison/repo/edison

        src/gz core2-32 http://repo.opkg.net/edison/repo/core2-32" >> /etc/opkg/base-feeds.conf
    ```

3. Update the packages on your Edison:

    ```
        # opkg update
    ```

4. Install the required packages for facial identification:

    ```
        # opkg install python-numpy opencv python-opencv
    ```

5. Install required packages for facial identification:

COMING SOON

## IoT JumpWay Intel® Edison Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel Examples in your IoT projects.

## IoT JumpWay Intel® Edison Examples Document Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/iotJumpway "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../images/main/Intel-Software-Innovator.jpg)