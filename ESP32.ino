#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
#include <SoftwareSerial.h>
#include <ArduinoBLE.h>
#include <WiFi.h>

#define RX_PIN 16
#define TX_PIN 17

#define ENTERING 0
#define LEAVING 1
#define PUBLIC 0 // public room
#define RESTRICTED 1 // restricted room
#define WAITING_TIME 3 // time to wait for the door to close

// bluetooth settings
#define MAX_DEVICES 10
#define MIN_DISTANCE 60

SoftwareSerial board(TX_PIN, RX_PIN);

// utility functions
String getMacAddress();
String checkAuth(String mac_addr);
void openDoor(); 
void closeDoor();
void sendAlert(String mac_addr);
void sendAction(int action, String mac_addr);
void connectToWiFi();
void unlockSensors();
int post(StaticJsonDocument<400> request, String url);

// room settings
int room_type = RESTRICTED;
int room_id = 1;
bool door_open = false;

// wifi settings
const char * ssid = "";
const char * password = "";
String serverName = "/api/"; // <-----

void setup() {
  Serial.begin(115200);
  board.begin(9600);
  connectToWiFi();
  BLE.begin();
}

void loop() {
  String board_msg1 = "";
  String board_msg2 = "";

  bool presence_inside = false;
  bool presence_outside = false; 

  if (board.available()){
    board_msg1 = board.readString();

    if(board_msg1 == "inside"){
      presence_inside = true;
    }
    if(board_msg1 == "outside"){
      presence_outside = true;
    }
  }

  int action = 0;

  if(presence_inside != presence_outside){
    String mac_address = getMacAddress();

    action = (presence_outside) ? ENTERING : LEAVING;

    switch(room_type){

      case RESTRICTED:
        if(presence_outside){
          String auth = checkAuth(mac_address);

          if(auth == "false"){
            sendAlert(mac_address);
            unlockSensors();
            break;
          }
        }

      case PUBLIC:
        openDoor();
        delay(WAITING_TIME * 1000);

        if(board.available()){
          board_msg2 = board.readString();

          if(board_msg2 != board_msg1){
            sendAction(action, mac_address);
          }
        }

        closeDoor();
        unlockSensors();
        break;
    }
  }

  if (Serial.available())
    //Data coming from the serial monitor
    board.write(Serial.read());

}

String getMacAddress(){
  int device_rssi = 0;
  int min_rssi = 1000, i = 0;
  String closest_device = "none";

  BLE.scan();

  unsigned long start_time = millis();
  unsigned long end_time = start_time;

  while(i < MAX_DEVICES && (end_time - start_time) <= 5000){
    BLEDevice auth_device = BLE.available();

    if(auth_device.hasLocalName()){
      i++;
      device_rssi = auth_device.rssi() * -1;

      if(device_rssi < min_rssi){
        min_rssi = device_rssi;
        closest_device = auth_device.localName();
      }
    }

    end_time = millis();
  }

  if(closest_device == "none" || closest_device == ""){
    closest_device = "customer";
  }

  BLE.stopScan();

  Serial.println("Closest device: ");
  Serial.println(closest_device);
  Serial.print("\n");

  return closest_device;
}

String checkAuth(String mac_addr){

  StaticJsonDocument<400> request;
  request["device"] = mac_addr;
  request["room"] = room_id;

  int response = post(request, serverName + "openDoor");
  
  if(response == 200){
    return "true";  
  } else {
    return "false";
  }
}

void openDoor(){
  if(!door_open){
    Serial.print("Opening door\n");
    door_open = true; 
  }
}

void closeDoor(){
  if(door_open){
    Serial.print("Closing door\n");
    door_open = false;
  }
}

void sendAlert(String mac_addr){
  StaticJsonDocument<400> request;
  request["device"] = mac_addr;
  request["room"] = room_id;

  int response = post(request, serverName + "sendAlert");
}

void sendAction(int action, String mac_addr){
  StaticJsonDocument<400> request;
  request["device"] = mac_addr;
  request["room"] = room_id;
  request["event"] = action;

  int response = post(request, serverName + "addLog");
}

void connectToWiFi(){
  WiFi.begin(ssid, password);
  Serial.println("Connecting");

  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

int post(StaticJsonDocument<400> request, String url){
  if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;
      String requestBody;

      http.begin(client, url);
      http.addHeader("Content-Type", "application/json");

      serializeJson(request, requestBody);

      int httpResponseCode = http.POST(requestBody);

      http.end();

      return httpResponseCode;
    }
    else {
      Serial.println("WiFi Disconnected");
      return 0;
    }
}

void unlockSensors(){
    board.write("11\n");
}