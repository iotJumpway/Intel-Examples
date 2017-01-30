# Booting Your Edison From An SD

![TechBubble IoT JumpWay Docs](../../images/main/IoT-Jumpway.jpg)  

## Introduction

The following information will help you set up your SD card and use it to boot the Edison, for this tutorial we recommend an 8 - 16gb SD.

## Formatting Your SD card

First of all you need to format your SD card, for this section of the guide we will be using a Linux computer running Ubuntu and the GParted software. 

1. Open up a terminal and install GParted if it is not already installed. 

    ```
        $ sudo apt install gparted
    ```

2. Insert your SD card into your computer and open GParted.

    ```
        $ sudo gparted
    ```

3. Select the SD card by clicking on the dropdown menu in the top right of the GParted GUI.

4. Delete the partitions from your SD card by right clicking on them and selecting delete.

5. Create a new Primary Partition by right clicking, selecting new and filling out the information, make sure you have  EXT4 selected as the filesystem.

6. When you have filled out the options, click Add and wait for the process to complete. 

## Download The Latest Yocto

The next step is to download the latest Yocto image for your Edison, to do this visit the following link:

[Intel® Edison Module Downloads](https://software.intel.com/en-us/iot/hardware/edison/downloads "Intel® Edison Module Downloads")

Once on the page scroll towards the bottom in the software section and click on the link to download the latest Yocto Poky Image.

