# Installing Python 3.6 On Your Intel® Edison

![TechBubble IoT JumpWay Docs](../../images/Docs/Intel-Edison-Documentation.png)  

## WARNING

This tutorial will replace the existing Python 2.7 with Python 3.6. 

## Introduction

The following information will help you install Python 3 on your Intel® Edison.

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

5. Next remove the link for Python 2.7 and add one for Python 3.6

    ```
        rm /usr/bin/python
        ln -s /home/root/Python-3.6.0/python /usr/bin/python
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

WORKING ON THIS, TO BE UPDATED
    
## IoT JumpWay Intel® Edison Examples Document Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../../images/main/Intel-Software-Innovator.jpg)  







