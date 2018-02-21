# Computer Vision Controlled IoT Connected Robotic Arm

![Computer Vision Controlled IoT Connected Robotic Arm](Images/robotic-arm.jpg)

## Introduction

The Computer Vision Controlled IoT Connect Robotic Arm project is a collaboration between Intel Software Innovators, TechBubble Technologies & Saft7robotics. The project allows you to create a fully functioning IoT connected robotic arm that can be controlled by a computer vision neural neural network.

The project combines 3 main projects which are as follows:

- Saft7robotics: Arduino Powered Robotic Arm
- Adam Milton-Barker: InceptionFlow
- TechBubble Technologies: TASS AI

The project consists of three programs:

- Robotic Arm Program (Arduino)
- ESP8266 Communication Program (Arduino)
- InceptionFlow Computer Vision Program (Python)

# COMPETITION!!!

Want to win your very own robotic arm kit ? We are looking for the best project that utilizes the Computer Vision Controlled IoT Connected Robotic Arm project. To enter your project, you must:

- Star / Fork this repository.
- Like the [TechBubble Technologies](https://www.facebook.com/TechBubbleInfo "TechBubble Technologies") & [Saft7robotics](https://www.facebook.com/TechBubbleInfo "Saft7robotics") Facebook pages.
- Use all three of the programs that make up this tutorial.
- Add your full project idea including description / graphics / video to your project README file in your forked repository.
- Post the link to your README on the pinned post on the TechBubble Technologies Facebook page.

We are looking for the most innovative, crazy and out of this world projects, but would also like to see a real world use case. 

## BONUS

Use the IoT JumpWay for autonomous communication with other IoT devices connected to the IoT JumpWay for extra browny points ;) 

The competition is open until March 14th.

## ESP8266 Communication Program

The first step is to setup the ESP8266 Communication Program. You will find the [source code and tutorial](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/tree/master/Robotic-Arm/ESP8266 "source code and tutorial") in the [ESP8266 directory](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/tree/master/Robotic-Arm/ESP8266 "ESP8266 directory"). 

The ESP8266 Communication Program acts as a bridge between the Robotic Arm and the IoT JumpWay. The program listens for commands sent to the device and forwards them through to the arm via serial.

Follow the tutorial to get this part of the project set up. 

## Robotic Arm Core Program

The next step is to setup the Robotic Arm Core Program. You will find the [source code and tutorial](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/tree/master/Robotic-Arm/Arduino "source code and tutorial") in the [Arduino directory](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/tree/master/Robotic-Arm/Arduino "Arduino directory"). 

Follow the tutorial to get this part of the project set up.

## Computer Vision Program

The final step is to setup the Computer Vision Program. You will find the [source code and tutorial](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/tree/master/Robotic-Arm/Python "source code and tutorial") in the [Python directory](https://github.com/TechBubbleTechnologies/IoT-JumpWay-Intel-Examples/tree/master/Robotic-Arm/Python "Python directory"). 

The Computer Vision Program is based on Adam Milton-Barker's InceptionFlow and allows you train a neural network to detect faces or objects. In this tutorial, we train the neural network to be able to recognize up, down, left and right arrows, once the program detects an arrow, it will send the relevant command to the robotic arm.

Follow the tutorial to get this part of the project set up.     

## Bugs & Issues

Please feel free to create issues for bugs and general issues you come across whilst using this project. For issues with using the IoT JumpWay please visit the TechBubble GitHub repo.

## Contributors

- [Adam Milton-Barker, TechBubble Technologies Founder](https://github.com/AdamMiltonBarker "Adam Milton-Barker, TechBubble Technologies Founder")

![Adam Milton-Barker,  Intel Software Innovator](../images/main/Intel-Software-Innovator.jpg)   

- [Saft7Robotics](http://www.saft7robotics.com "Saft7Robotics")

![Saft7Robotics,  Intel Software Innovator](Images/Saft7Robotics.jpg)




