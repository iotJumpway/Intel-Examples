# Booting Your Edison From An SD (Linux)

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

Once on the page scroll towards the bottom in the software section and click on the link to download the latest Yocto Poky Image, once downloaded, unpack the contents to ~/Downloads/edison.

## Mount & Move Files To The SD Card

1. Next you need to move into the previously created edison folder:

    ```
        $ cd ~/Downloads/edison
    ```

2. Then enter the following command to create the Rootfs directory:

    ```
        $ mkdir Rootfs
    ```

3. Then mount the edison image to the Rootfs directory:

    ```
        $ sudo mount ./edison-image-edison.ext4 Rootfs
    ```

4. Finally copy the files to your SD card, replacing YOUR_SD_CARD with the name of your mounted SD card.

    ```
        $ sudo cp -a Rootfs/* /media/YOUR_SD_CARD/
    ```

## Setting Up Your Edison To Use The SD Card

Now you need to take your SD card and plug it into the Edison, run the following command to find the name of the SD:

    ```
        $ dmesg |tail -n 10
    ```

You should see an output similar to the one below:

    ```
        [53400.186825] mmc1: new high speed SDHC card at address 1234
        [53400.187781] mmcblk1: mmc1:1234 SA08G 7.28 GiB
        [53400.189731]  mmcblk1: p1
        [53412.585076] EXT4-fs (mmcblk1p1): recovery complete
        [53412.589107] EXT4-fs (mmcblk1p1): mounted filesystem with ordered data mode. O
    ```

This tells us that the SD card is “/dev/mmcblk1” and the partition we’ve created is "/dev/mmcblk1p1".





