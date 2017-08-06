# Installing OpenFace on Intel® NUC DE3815TYKE

![TechBubble IoT JumpWay Docs](../../../images/Docs/Intel-NUC-Documentation.png)

## Introduction

The following information will help you install OpenFace on the Intel® Nuc DE3815TYKE.

## OpenFace Prerequisites

    $ sudo apt install git

    $ git clone https://github.com/cmusatyalab/openface.git  --recursive

## Install OpenCV 2.4.11

    $ sudo apt-get install build-essential

    $ sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev

    $ sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

    $ wget https://github.com/Itseez/opencv/archive/2.4.11.zip

    $ sudo apt install unzip

    $ unzip 2.4.11.zip

    $ cd ~/opencv-2.4.11 && mkdir release && cd release

    $ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..

    $ make

    $ sudo make install

## Install DLib

    $ sudo apt-get install libopenblas-dev liblapack-dev

    $ sudo apt-get install libboost-all-dev

    $ mkdir -p ~/src && cd ~/src

    $ wget https://github.com/davisking/dlib/releases/download/v18.16/dlib-18.16.tar.bz2

    $ tar xf dlib-18.16.tar.bz2

    $ cd dlib-18.16/python_examples

    $ mkdir build && cd build

    $ cmake ../../tools/python

    $ cmake --build . --config Release

    $  sudo cp dlib.so /usr/local/lib/python2.7/dist-packages

## Install Torch

    $ git clone https://github.com/torch/distro.git ~/torch --recursive

    $ cd ~/torch; bash install-deps;

    $ ./install.sh

    $ source ~/.bashrc

    $ for NAME in dpnn nn optim optnet csvigo cutorch cunn fblualib torchx tds; do luarocks install $NAME; done

## OpenFace Installation

    $ cd ~/openface

    $ sudo python2 setup.py install

## IoT JumpWay Intel® NUC DE3815TYKE Bugs/Issues

Please feel free to create issues for bugs and general issues you come across whilst using the IoT JumpWay Intel® Examples. You may also use the issues area to ask for general help whilst using the IoT JumpWay Intel® Examples in your IoT projects.

## IoT JumpWay Intel® NUC DE3815TYKE Examples Document Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel® Software Innovator](../../../images/main/Intel-Software-Innovator.jpg)







