# Installation Of Linux Motion On Intel® Edison

![TechBubble IoT JumpWay Docs](../../images/Docs/Intel-Edison-Documentation.png)   

## Introduction

The following information will help you install Linux Motion on your Intel® Edison.

PLEASE NOTE: 

- This is a basic tutorial that will result in an insecure stream, in project tutorials where we use Linux Motion, we will take you through creating a secure stream. 
- This tutorial does provide instructions on using the password feature of Linux Motion, please use a secure username and password. 
- Motion will store images on your Edison, if you do not keep on top of them your diskspace will quickly fill up. 

## Hardware Requirements

1. Intel® Edison.
2. 8 - 16 GB Card

## Guide

1. Before you can install Linux Motion on your Intel® Edison, you may want to setup your Edison to boot from an SD card. Use the following tutorial to accomplish this:

    [Booting Your Intel® Edison From An SD (Linux)](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/blob/master/Intel-Edison/_DOCS/1-Booting-From-SD-Linux.md "Booting Your Intel® Edison From An SD (Linux)")

2. Update your packages:

    ```
        # opkg update
        # opkg upgrade
    ```

2. Execute the following to create a user group and user for Motion:

    ```
        # groupadd -r motion
        # useradd -r -m -s /bin/true -g motion -G video motion
    ```

3. Create the directory required for the daemon to run:

    ```
        # mkdir /var/run/motion/
    ```

4. Execute the following command to rename the required config file to the correct name:  

    ```
        # mv /etc/motion-dist.conf /etc/motion.conf
    ```

5. Open the configuration file: 

    ```
        # nano /etc/motion.conf
    ```
    
6. Turn off the feature that only allows streams to be accessed on local host:

    ```
        webcam_localhost = off
    ```

7. If you want to change the port that the webcam is streamed to change the following value. It is a good idea to change the port so that it does not use the default port.

    ```
        webcam_localhost = off
    ```

8. Check Linux Motion is working, execute the following command and then navigate to YOUR_INTEL_EDISON_IP:8081 

    ```
        webcam_port YOUR_PORT_NUMBER
    ```

9. In my case I am using a camera that is 1280 x 780, motion may not work if you do not have the correct resolution set for your camera, to modify the dimensions find and edit the following in the config file:

    ```
        width 640 
        height 380
    ```

10. If you want to change the quality of the images and video stream, change the following line:

    ```
        quality 90
        webcam_quality 90
    ```

11. We want our stream to be as fast possible, in order to do so, find and modify the following line, I use 30 as my camera is 30 fps:

    ```
        framerate 2
        webcam_maxrate 1
    ```

12. If you want to be able to see where it picks up motion on the stream, set the following to on:

    ```
        locate off
    ```

13. If you want to change the location that the images and videos are saved, change the following location:

    ```
        target_dir /usr/local/apache2/htdocs/cam1
    ```

13. At the time of writing this, the daemon controls did not work, if you want to stop motion do the following:

    ```
        # top
    ```

    Find the PID for motion.

    ```
        CTRL C to exit top
    ```

    ```
        # kill PID_FOR_MOTION
    ```

## IoT JumpWay Intel® Edison Examples Document Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../images/main/Intel-Software-Innovator.jpg)  