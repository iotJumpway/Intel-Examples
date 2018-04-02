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

String jsonString = "";
String inputString = "";

int debounceWait = 150;

int read_LCD_buttons(){

    adc_key_in = analogRead(0);

    if (adc_key_in > 1000) return btnNONE;
    if (adc_key_in < 50)   return btnRIGHT;
    if (adc_key_in < 350)  return btnUP;
    if (adc_key_in < 650)  return btnDOWN;
    if (adc_key_in < 950)  return btnLEFT;

    return btnNONE;
}

void setup(){

   Serial.begin(9600);
   lcd.begin(16, 2);
   lcd.setCursor(0,0);
   lcd.print("ONLINE");

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

             lcd.print("COMMAND 1");
             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"1\"}";
             delay(debounceWait);
             Serial.println(jsonString);
             break;

       }

       case 2:{

             lcd.print("COMMAND 2");
             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"2\"}";
             delay(debounceWait);
             Serial.println(jsonString);
             break;

       }
       case 3:{

             lcd.print("COMMAND 3");
             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"3\"}";
             delay(debounceWait);
             Serial.println(jsonString);
             break;

       }

       case 4:{

             lcd.print("COMMAND 4");
             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"4\"}";
             delay(debounceWait);
             Serial.println(jsonString);
            break;

       }

   }

}

void loop(){

   lcd.setCursor(0,1);
   lcd_key = read_LCD_buttons();

   jsonString = "";

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

            lcd.print("         ");
            break;
       }

       delay(5000);

   }
}