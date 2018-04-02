/*
  Robotic Arm ESP8266 Communication Program
  Copyright (c) 2018 Adam Milton-Barker - AdamMiltonBarker.com
  Based on Paho MQTT
  Uses IoT JumpWay MQTT Client
*/

WiFiClientSecure espClient;
PubSubClient client(espClient);

const char* mqtt_server = "iot.techbubbletechnologies.com";
int  mqttPort = 8883;

const char* ssid = "YourSSID";
const char* password = "YourWiFiPassword";

String locationID = "YourLocationID";
String zoneID = "YourZoneID";
String deviceID = "YourDeviceID";
char deviceName[] = "YourDeviceName";
char mqttUsername[]   = "YourDeviceMQTTUsername";
char mqttPassword[]  = "YourDeviceMQTTPassword";

void setupWiFi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected!");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  String readString = "";
  for (int i = 0; i < length; i++) {
    readString += (char)payload[i];
  }
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(readString);
  String CommandValue = root["CommandValue"];
  Serial.println(CommandValue);
}

void subscribeToDeviceCommands(){
  String commandTopic = locationID+"/Devices/"+zoneID+"/"+deviceID+"/Commands";
  commandTopic.toCharArray(charBuf, 50);
  client.subscribe(charBuf);
}

void publishToDeviceStatus(const char* data){
  String statusTopic = locationID+"/Devices/"+zoneID+"/"+deviceID+"/Status";
  statusTopic.toCharArray(charBuf, 50);
  client.publish(charBuf,data);
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting connection to IoT JumpWay...");
    if (client.connect(deviceName, mqttUsername, mqttPassword)) {
      Serial.println("Connected to IoT JumpWay!");
      publishToDeviceStatus("ONLINE");
      subscribeToDeviceCommands();
    } else {
      Serial.print("Failed to connect to IoT JumpWay, rc=");
      Serial.print(client.state());
      Serial.println("... trying again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setupWiFi();
  client.setServer(mqtt_server,mqttPort);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
