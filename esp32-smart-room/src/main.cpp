#include <Arduino.h>
#include "mqtt.h"

int count = 1;

void setup() {
  Serial.begin(9600);

  pinMode(LED_LIGHT, OUTPUT);
  pinMode(LED_AC, OUTPUT);
  pinMode(ALARM, OUTPUT);

  digitalWrite(LED_LIGHT, LOW);
  digitalWrite(LED_AC, LOW);

  WiFi.begin(WLAN_SSID, WLAN_PASS);

  Serial.print("Connecting WiFi..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println(" WiFi connected!");

  lightFeed.setCallback(lightCallback);
  acFeed.setCallback(acCallback);
  alarmFeed.setCallback(alarmCallback);
  
  MQTT_connect();
}

void loop() {
  MQTT_connect();

  if (count < 2) {
    mqtt.disconnect();
    count++;
  }

  mqtt.processPackets(1000);

}