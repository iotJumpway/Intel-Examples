/*

  Copyright (c) 2014 Adam Milton-Barker.

  Contributors:
  Adam Milton-Barker

  For this project you will need to use the IoT JumpWay Python MQTT Serial Library:
  https://github.com/iotJumpway/IoT-JumpWay-Python-MQTT-Serial-Client

*/

#include <LiquidCrystal.h>
#include <ArduinoJson.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

int lcd_key     = 0;
int adc_key_in  = 0;

#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5

String JumpWaySensorType = "LCD Keypad";
String JumpWaySensorID = "1";

String JumpWaySensorType2 = "PIR Sensor";
String JumpWaySensorID2 = "2";

String JumpWaySensorType3 = "Buzzer";
String JumpWaySensorID3 = "3";

byte DFRobotMotionPin = 2;
byte DFRobotBuzzerPin = 3;

String jsonString = "";
String inputString = "";

int debounceWait = 150;
int armedStatus = 0;

int read_LCD_buttons(){

    adc_key_in = analogRead(0);

    if (adc_key_in > 1000) return btnNONE;
    if (adc_key_in < 50)   return btnRIGHT;
    if (adc_key_in < 350)  return btnUP;
    if (adc_key_in < 650)  return btnDOWN;
    if (adc_key_in < 950)  return btnLEFT;

    return btnNONE;
}

void start_alarm(){

    digitalWrite(DFRobotBuzzerPin, HIGH);
    delay(1);

}

void stop_alarm(){

    digitalWrite(DFRobotBuzzerPin, LOW);
    delay(1);

}

void incoming(){

  while (Serial.available()) {

    char inChar = (char)Serial.read();

    inputString += inChar;

    if (inChar == '\n') {

      StaticJsonBuffer<200> jsonBuffer;
      JsonObject& root = jsonBuffer.parseObject(inputString);

      String Actuator = root["ActuatorID"];
      String Command = root["Command"];
      int CommandValue = root["CommandValue"];

      if(Command=="TOGGLE"){

          commands(CommandValue);

      }

    }
    inputString = "";
  }

}

void commands(int button){

   switch (button){

       case 1:{

             lcd.setCursor(0,1);
             lcd.print("ARMED    ");
             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"ARMED\"}";
             delay(debounceWait);
             armedStatus = 1;
             Serial.println(jsonString);
             break;

       }

       case 2:{

             lcd.setCursor(0,1);
             lcd.print("NOT ARMED");

             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"NOT ARMED\"}";
             delay(debounceWait);
             armedStatus = 0;
             Serial.println(jsonString);

             break;

       }
       case 3:{

             lcd.setCursor(0,1);
             lcd.print("ALARM ON");

             start_alarm();

             jsonString = "{\"Sensor\":\""+JumpWaySensorType3+"\",\"SensorID\":\""+JumpWaySensorID3+"\",\"SensorValue\": \"ALARM ON\"}";
             delay(debounceWait);
             Serial.println(jsonString);

             break;

       }

       case 4:{

             lcd.setCursor(0,1);
             lcd.print("ALARM OFF");

             stop_alarm();

             jsonString = "{\"Sensor\":\""+JumpWaySensorType3+"\",\"SensorID\":\""+JumpWaySensorID3+"\",\"SensorValue\": \"ALARM OFF\"}";
             delay(debounceWait);
             Serial.println(jsonString);

            break;

       }

   }

}

void setup(){

   pinMode(DFRobotMotionPin,INPUT);
   pinMode(DFRobotBuzzerPin, OUTPUT);

   start_alarm();
   stop_alarm();

   Serial.begin(9600);

   lcd.begin(16, 2);
   lcd.setCursor(0,0);
   lcd.print("ONLINE");

}

void loop(){

   String jsonString = "";

   lcd_key = read_LCD_buttons();

   if(armedStatus == 1){

     lcd.setCursor(0,1);
     lcd.print("ARMED    ");
     byte state = digitalRead(DFRobotMotionPin);

     if(state == 1){

        lcd.setCursor(0,1);
        lcd.print("INTRUDER!");

        jsonString = "{\"Sensor\":\""+JumpWaySensorType2+"\",\"SensorID\":\""+JumpWaySensorID2+"\",\"SensorValue\": \"MOTION\"}";
        Serial.println(jsonString);

        start_alarm();

        jsonString = "{\"Sensor\":\""+JumpWaySensorType3+"\",\"SensorID\":\""+JumpWaySensorID3+"\",\"SensorValue\": \"ALARM ON\"}";
        Serial.println(jsonString);

        jsonString = "{\"WarningType\":\""+JumpWaySensorType2+"\",\"WarningOrigin\":\""+JumpWaySensorID2+"\",\"WarningValue\": \"MOTION\",\"WarningMessage\": \"Motion has been detected\"}";
        Serial.println(jsonString);

     } else if(state == 0){

        lcd.setCursor(0,1);
        lcd.print("ARMED    ");

        jsonString = "{\"Sensor\":\""+JumpWaySensorType2+"\",\"SensorID\":\""+JumpWaySensorID2+"\",\"SensorValue\": \"OK\"}";
        Serial.println(jsonString);

        stop_alarm();

        jsonString = "{\"Sensor\":\""+JumpWaySensorType3+"\",\"SensorID\":\""+JumpWaySensorID3+"\",\"SensorValue\": \"ALARM OFF\"}";
        Serial.println(jsonString);

     }

   } else {

      lcd.setCursor(0,1);
      lcd.print("NOT ARMED");

   }

   switch (lcd_key){

       case btnUP:{

             commands(1);
             break;

       }
       case btnDOWN:{

             commands(2);
             break;

       }
       case btnLEFT:{

             commands(3);
             break;

       }
       case btnRIGHT:{

             commands(4);
             break;

       }
       case btnNONE:{

            lcd.setCursor(0,1);
            lcd.print("         ");
            break;

       }

       delay(5000);

   }
}