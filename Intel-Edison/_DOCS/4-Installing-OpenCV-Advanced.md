# Installation Of OpenCV On Intel® Edison

![TechBubble IoT JumpWay Docs](../../images/Docs/Intel-Edison-Documentation.png)  

## Introduction

The following information will help you install OpenCV on your Intel® Edison. This installation currently does not include the additional modules required for facial identification.

###THIS TUTORIAL IS NOT FULLY FUNCTIONING, PLEASE WAIT UNTIL THIS MESSAGE IS REMOVED BEFORE YOU ATTEMPT THIS INSTALLATION

## Hardware Requirements

1. Intel® Edison.
2. 8 - 16 GB Card

## Guide

1. Update apt-get:

    ```
    # opkg update
    # opkg upgrade
    ```

2. Install developer tools:

    ```
    # opkg install packagegroup-core-buildessential cmake git pkgconfig
    ```

3. Install image I/O packages:

    ```
    # opkg install libjpeg-dev libtiff-dev libjasper-dev libpng12-dev
    ```

4. Install GTK development library:

    ```
    # opkg install libgtk2.0-dev
    ```

5. Install video processing software:

    ```
    # opkg install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
    ```

6. Install gfortran:

    ```
    # opkg install gfortran
    ```

7. Install Atlas (This will take a while):

    ```
    # wget http://downloads.sourceforge.net/project/math-atlas/Stable/3.10.2/atlas3.10.2.tar.bz2
    # tar jxvf ./atlas3.10.2.tar.bz2
    # wget http://www.netlib.org/lapack/lapack-3.5.0.tgz
    # mkdir ./ATLAS/build
    # cd ./ATLAS/build
    # ../configure --prefix=/usr/local --with-netlib-lapack-tarfile=/home/root/lapack-3.5.0.tgz --nof77 -v 2
    # make build
    # make install
    ```


8. Install Python 2.7 development libraries:

    ```
    # 
    ```

9. Install Numpy:

    ```
    # pip install numpy
    ```

8. Checkout current OpenCV 3.1.0:

    ```
    # cd ~
    # git clone https://github.com/Itseez/opencv.git
    # cd opencv
    # git checkout 3.1.0
    ```

9. Checkout OpenCV Modules  3.1.0:

    ```
    # cd ~
    # git clone https://github.com/Itseez/opencv_contrib.git
    # cd opencv_contrib
    # git checkout 3.1.0
    ```

9. Setup the build:

    ```
    # cd ~/opencv
    # mkdir build
    # cd build
    # cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D BUILD_EXAMPLES=ON ..
    ```

10. Make and make install the build:

    ```
    # make -j4
    # sudo make install
    # sudo ldconfig
    ```


## IoT JumpWay Intel® Edison Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel Examples in your IoT projects.

## IoT JumpWay Intel® Edison Examples Document Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../images/main/Intel-Software-Innovator.jpg) 