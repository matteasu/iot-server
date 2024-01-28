#include <SoftwareSerial.h>

// WiFi module
#define WIFI_RX_PIN 3
#define WIFI_TX_PIN 2
// Presence sensor installed inside
#define TRIG_INSIDE 8
#define ECHO_INSIDE 9
// Presence sensor installed outside
#define TRIG_OUTSIDE 4
#define ECHO_OUTSIDE 5

#define OK_OUTSIDE 11
#define OK_INSIDE 10

#define MIN_DISTANCE 30 // minimum distance to trigger the door opening

SoftwareSerial wifi_module(WIFI_TX_PIN, WIFI_RX_PIN);

// utility functions
bool checkPresence(int trig, int echo);

// sensor locks
bool stop_inside = false;
bool stop_outside = false;

void setup() {
  // initialization of serial communication
  Serial.begin(9600); 
  wifi_module.begin(9600);

  // Setup of the sensor inside the room
  pinMode(TRIG_INSIDE, OUTPUT);
  pinMode(ECHO_INSIDE, INPUT);

  // setup of the sensor outside the room
  pinMode(TRIG_OUTSIDE, OUTPUT);
  pinMode(ECHO_OUTSIDE, INPUT);
}

void loop() {
  bool presence_inside = false; 
  bool presence_outside = false; 

  if(!stop_inside){
    presence_inside = checkPresence(TRIG_INSIDE, ECHO_INSIDE);
  }

  if(!stop_outside){
    presence_outside = checkPresence(TRIG_OUTSIDE, ECHO_OUTSIDE);
  }

  if(presence_inside){
    Serial.write("inside\n");
    wifi_module.write("inside");
    stop_inside = true;
  }

  if (presence_outside){
    Serial.write("outside\n");
    wifi_module.write("outside");
    stop_outside = true;
  }

  if(wifi_module.available()){
    int response = wifi_module.readString().toInt();
    
    if(response == OK_OUTSIDE){
      delay(2000);
      stop_inside = stop_outside = false;
      Serial.println("Resetting sensors...");
    }
  }
}

bool checkPresence(int trig, int echo){
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH);
  float distance = duration * 0.0343 / 2;

  return (distance < MIN_DISTANCE) ? true : false;
}