# Expanding The Available Disk Space On Intel® Galileo Gen 1

![IoT JumpWay Docs](../../images/main/IoT-Jumpway.jpg)

## Introduction

The following information will help you utilize the full amount of available space in your Intel® Galileo Gen 1.

## Expanding The Disk Space

To expand the disk space available you need to have an external Linux machine with Gparted installed. Once installed follow the next steps to maximize your disk space.

1. Insert your SD card with pre installed Yocto image into your external Linux device.

2. Open Gparted:

    ```
        $ sudo gparted
    ```

3. Select the SD card in the top right of the Gparted GUI.

4. Right click on the partion that is 1GB.

5. Select Move / Resize

6. Increase the New Size setting until the free space is empty.

7. Click resize and click the green check box at the top, then click apply when prompted and wait for the process to finish.

8. Plug the SD card back into the Galileo and boot up.

9. Run the following command:

    ```
        # df -h
    ```

10. you should see an output similar to the following, where /dev/root matches the size of your SD card.

    ```
        # df -h
        Filesystem      Size  Used Avail Use% Mounted on
        /dev/root       7.2G  783M  6.1G  12% /
        devtmpfs        117M     0  117M   0% /dev
        tmpfs           117M     0  117M   0% /dev/shm
        tmpfs           117M  4.4M  112M   4% /run
        tmpfs           117M     0  117M   0% /sys/fs/cgroup
        tmpfs           117M  8.0K  117M   1% /tmp
        tmpfs           117M   12K  117M   1% /var/volatile
        /dev/mmcblk0p1   50M   16M   34M  33% /media/card
    ```

## IoT JumpWay Intel® Galileo Examples Document Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/iotJumpway "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../images/main/Intel-Software-Innovator.jpg)



