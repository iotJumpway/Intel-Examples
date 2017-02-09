/*
 
  Copyright (c) 2016 TechBubble Technologies and other Contributors.
  
  Contributors:  
  Adam Milton-Barker - TechBubble Technologies Limited

  For this project you will need to use the TechBubble IoT JumpWay Python MQTT Serial Library:

  https://github.com/TechBubbleTechnologies/IoT-JumpWay-Python-MQTT-Serial-Client
  
*/

#include <ArduinoJson.h>

String inputString = ""; 
const int actuator1Pin = 5;
const int actuator1JumpWayID = 0;

void setup() {
  
  Serial.begin(9600); 
  Serial.println("Ready"); 
  
}

void loop() {
  
  while (Serial.available()) {
    
    char inChar = (char)Serial.read();
    
    inputString += inChar;
    
    if (inChar == '\n') {
      
      StaticJsonBuffer<200> jsonBuffer;
      JsonObject& root = jsonBuffer.parseObject(inputString);
      
      String Actuator = root["ActuatorID"];
      String Command = root["Command"];
      String CommandValue = root["CommandValue"];

      if(Actuator==actuator1JumpWayID){
          
        if(Command=="TOGGLE"){
            
          digitalWrite(actuator1Pin, HIGH);
          
          delay(2000);  
          
          digitalWrite(actuator1Pin, LOW);
          
          delay(2000);  
            
          digitalWrite(actuator1Pin, HIGH);
          
          delay(2000);  

          digitalWrite(actuator1Pin, LOW);
          
        } else {
          
          if(CommandValue=="ON"){
            
            digitalWrite(actuator1Pin, HIGH);
            
          }else{
            
            digitalWrite(actuator1Pin, LOW);
            
          }
        
        }
        
      }
      inputString = "";
    }
  }
}

