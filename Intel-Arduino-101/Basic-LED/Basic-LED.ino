/*
 
  Copyright (c) 2016 TechBubble Technologies and other Contributors.
  
  Contributors:  
  Adam Milton-Barker - TechBubble Technologies Limited
  
*/

#include <ArduinoJson.h>

String inputString = ""; 
const int actuator1 = 5;

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

      if(Actuator=="1"){
          
        if(Command=="TOGGLE"){
            
          digitalWrite(actuator1, HIGH);
          
          delay(2000);  
          
          digitalWrite(actuator1, LOW);
          
          delay(2000);  
            
          digitalWrite(actuator1, HIGH);
          
          delay(2000);  

          digitalWrite(actuator1, LOW);
          
        } else {
          
          if(CommandValue=="ON"){
            
            digitalWrite(actuator1, HIGH);
            
          }else{
            
            digitalWrite(actuator1, LOW);
            
          }
        
        }
        
      }
      inputString = "";
    }
  }
}

