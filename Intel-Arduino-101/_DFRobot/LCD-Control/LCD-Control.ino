/*
 
  Copyright (c) 2016 TechBubble Technologies and other Contributors.
  
  Contributors:  
  Adam Milton-Barker - TechBubble Technologies Limited
  For this project you will need to use the TechBubble IoT JumpWay Python MQTT Serial Library:
  https://github.com/TechBubbleTechnologies/IoT-JumpWay-Python-MQTT-Serial-Client
  
*/

#include <LiquidCrystal.h>

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
 
void loop(){

   lcd.setCursor(0,1);             
   lcd_key = read_LCD_buttons();
   
   String jsonString = "";
   
   switch (lcd_key){   
       
       case btnUP:{
             lcd.print("COMMAND 1"); 
             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"1\"}";
             delay(debounceWait);
             Serial.println(jsonString);
             break;
             
       }
       
       case btnDOWN:{
        
             lcd.print("COMMAND 2"); 
             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"2\"}";
             delay(debounceWait);
             Serial.println(jsonString);
             break;
             
       }
       case btnLEFT:{
        
             lcd.print("COMMAND 3");  
             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"3\"}";
             delay(debounceWait);
             Serial.println(jsonString);
             break;
             
       }     

       case btnRIGHT:{          
             
            lcd.print("COMMAND 4"); 
             jsonString = "{\"Sensor\":\""+JumpWaySensorType+"\",\"SensorID\":\""+JumpWaySensorID+"\",\"SensorValue\": \"4\"}";
             delay(debounceWait);
             Serial.println(jsonString);
            break;
       }  

       case btnNONE:{          
             
            lcd.print("         "); 
            break;
       }
       
       delay(5000);
       
   }
}