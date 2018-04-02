# Installing Python 3.6 (And Most Others) On Your Intel® Edison

![IoT JumpWay Docs](../../images/Docs/Intel-Edison-Documentation.png)

## PLEASE NOTE:

MRAA will not work with Python 3 or above

## Introduction

The following information will help you install Python 3.6 on your Intel® Edison.

## Installing Python 3.6

To install Python 3.6 on your Intel® Edison, follow the steps below:

1. Move to the home directory:

    ```
        cd ~
    ```

2. Download the source:

    ```
        wget --no-check-certificate https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
    ```

3. Unpack the source:

    ```
        tar -xvf Python-3.6.0.tgz
    ```

4. Move into the Python directory, configure and make. You have to just wait for the make to finish as there is no output, be patient:

    ```
        cd Python-3.6.0/
        ./configure --with-pydebug
        make -s -j4
    ```

5. Next issue the following command, thanks to Gerard Vidal, for working this out

    ```
        sudo make install
    ```

6. Now check that Python 3.6 is being used:

    ```
        # python
    ```

7. You should see the following output:

    ```
        Python 3.6.0 (default, Feb  1 2017, 05:35:57)
        [GCC 4.9.1] on linux
        Type "help", "copyright", "credits" or "license" for more information.
    ```

8. Now you can clean up some space by deleting the downloaded. DO NOT delete the Python-3.6.0 directory, if you do you will have to start again with this tutorial as Python will no longer work.

    ```
        # rm -rf Python-3.6.0.tgz
    ```

## Installing Pip 3

Pip 3 will be installed with this method

## IoT JumpWay Intel® Edison Examples Document Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/iotJumpway "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../images/main/Intel-Software-Innovator.jpg)







