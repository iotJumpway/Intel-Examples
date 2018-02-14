/*
ANDROID BLUETOOTH ROBOTICS ABR1

 ROBOT CONTROL
 
 6 SERVO OUTPUTS
 6 DIGITAL OUTPUTS
 
 SAFT7ROBOTICS.COM
 ROBOT EDUKASI INDONESIA
 
 YOU CAN USING ANDROID BLUETOOTH ROBOTICS ABR1 FOR EASY CONNECTION
 PLEASE VISIT www.saft7robotics.com/abr1
 
 -----------------------
 WIRING CONNECTIONS:
 SERVOS:
 SERVO 1 : DIGITAL PWM 3
 SERVO 2 : DIGITAL PWM 5
 SERVO 3 : DIGITAL PWM 6
 SERVO 4 : DIGITAL PWM 9
 SERVO 5 : DIGITAL PWM 10
 SERVO 6 : DIGITAL PWM 11
 
 LED/OTHERS:
 OUTPUT 1 : DIGITAL 2
 OUTPUT 2 : DIGITAL 4
 OUTPUT 3 : DIGITAL 7
 OUTPUT 4 : DIGITAL 8
 OUTPUT 5 : DIGITAL 12
 OUTPUT 6 : DIGITAL 13
 
 INPUT FOR SERVOS : 5-6VOLT DC
 
 Receive text from bluetooth to control output:
 
 Button 1 ON  : Digital 2  : 6600
 Button 1 OFF : Digital 2  : 6650
 Button 2 ON  : Digital 4  : 6700
 Button 2 OFF : Digital 4  : 6750
 Button 3 ON  : Digital 7  : 6800
 Button 3 OFF : Digital 7  : 6850
 Button 4 ON  : Digital 8  : 6900
 Button 4 OFF : Digital 8  : 6950
 Button 5 ON  : Digital 12  : 7000
 Button 5 OFF : Digital 12  : 7050
 Button 6 ON  : Digital 13  : 7100
 Button 6 OFF : Digital 13  : 7150
 
 --------------
 Designed & Coded by Firmansyah Saftari, May 2016
 www.saft7.com
 
 */

#include <SoftwareSerial.h>
#include <Servo.h> 
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 20, 4); // 0x27 or 0x3F
Servo myservo1, myservo2, myservo3, myservo4, myservo5, myservo6;
int bluetoothTx = 0;
int bluetoothRx = 1;
int servo1;
int servo2;
int servo3;
int servo4;
int servo5;
int servo6;
int out1 = 2;
int out2 = 4;
int out3 = 7;
int out4 = 8;
int out5 = 12;
int out6 = 13;
int idata ;
SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);
void setup()
{
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);

  myservo1.attach(3);
  myservo2.attach(5);
  myservo3.attach(6);
  myservo4.attach(9);
  myservo5.attach(10);
  myservo6.attach(11);

  pinMode(out1, OUTPUT);
  pinMode(out2, OUTPUT);
  pinMode(out3, OUTPUT);
  pinMode(out4, OUTPUT);
  pinMode(out5, OUTPUT);
  pinMode(out6, OUTPUT); 
  Serial.begin(9600);
  bluetooth.begin(9600);
}

void loop()
{
  while (bluetooth.available()) { 
    delay(10);
    //-------------------------------receiving data from bluetooth
    unsigned int servopos = bluetooth.read();
    unsigned int servopos1 = bluetooth.read();
    unsigned int idata = (servopos1 *256) + servopos; 

    //----------------------------------------- servo out
    //  SERVO 1
    if (idata >= 1000 && idata < 1180) {
      servo1 = idata - 1000;
      myservo1.write(servo1);
      Serial.println(servo1);
      lcd.print(servo1);
    }
    //  SERVO 2
    else if (idata >= 2000 && idata < 2180) {
      servo2 = idata - 2000;
      myservo2.write(servo2);
      Serial.println(servo2);   
      lcd.print(servo2);   
    }
    //  SERVO 3
    else if (idata >= 3000 && idata < 3180) {
      servo3 = idata - 3000;
      myservo3.write(servo3);
      lcd.print(servo3);
      Serial.println(servo3);  
      lcd.print(servo3);
    }
    //  SERVO 4
    else if (idata >= 4000 && idata < 4180) {
      servo4 = idata - 4000;
      myservo4.write(servo4);
      lcd.print(servo4);
      Serial.println(servo4);  
      lcd.print(servo4);
    }
    //  SERVO 5
    else if (idata >= 5000 && idata < 5180) {
      servo5 = idata - 5000;
      myservo5.write(servo5);
      Serial.println(servo5);  
      lcd.print(servo5);
    }
    //  SERVO 6
    else if (idata >= 6000 && idata < 6180) {
      servo6 = idata - 6000;
      myservo6.write(servo6);
      Serial.println(servo6);  
      lcd.print(servo6);
    }     

    //------------------------------digital output

    //  OUTPUT 1 - ON
    else if (idata == 6600) {
      digitalWrite(out1,HIGH);
      Serial.println("1 ON");
      lcd.print("1 ON");
    }

    //  OUTPUT 1 - OFF
    else if (idata == 6650) {
      digitalWrite(out1,LOW);
      Serial.println("1 OFF");
      lcd.print("1 OFF");
    }

    //  OUTPUT 2 - ON
    else if (idata == 6700) {
      digitalWrite(out2,HIGH);
      Serial.println("2 ON");
      lcd.print("2 ON");
    }

    //  OUTPUT 2 - OFF
    else if (idata == 6750) {
      digitalWrite(out2,LOW);
      Serial.println("2 OFF");
      lcd.print("2 OFF");
    }

    //  OUTPUT 3 - ON
    else if (idata == 6800) {
      digitalWrite(out3,HIGH);
      lcd.print("3 ON");
      lcd.print("3 ON");
    }

    //  OUTPUT 3 - OFF
    else if (idata == 6850) {
      digitalWrite(out3,LOW);
      Serial.println("3 OFF");
      lcd.print("3 OFF");
    }

    //  OUTPUT 4 - ON
    else if (idata == 6900) {
      digitalWrite(out4,HIGH);
      Serial.println("4 ON");
      lcd.print("4 ON");
    }

    //  OUTPUT 4 OFF
    else if (idata == 6950) {
      digitalWrite(out4,LOW);
      Serial.println("4 OFF");
      lcd.print("4 OFF");
    }

    //  OUTPUT 5 - ON
    else if (idata == 7000) {
      digitalWrite(out5,HIGH);
      Serial.println("5 ON");
      lcd.print("5 ON");
    }

    //  OUTPUT 5 - OFF
    else if (idata == 7050) {
      digitalWrite(out5,LOW);
      Serial.println("5 OFF");
      lcd.print("5 OFF");
    }

    //  OUTPUT 6 - ON
    else if (idata == 7100) {
      digitalWrite(out6,HIGH);
      Serial.println("6 ON");
      lcd.print("6 ON");
    }

    //  OUTPUT 6 - OFF
    else if (idata == 7150) {
      digitalWrite(out6,LOW);
      Serial.println("6 OFF");
      lcd.print("6 OFF");
    }
  }
}
