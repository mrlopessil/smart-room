#include "mqtt.h"

WiFiClient client;

Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_PORT, AIO_USERNAME, AIO_KEY);

/************** FEEDS **************/
Adafruit_MQTT_Subscribe lightFeed =
  Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/light");

Adafruit_MQTT_Subscribe acFeed =
  Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/ac");

Adafruit_MQTT_Subscribe alarmFeed =
  Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/alarm");

/************** CALLBACK **************/
void lightCallback(char *data, uint16_t len) {
  Serial.print("LIGHT: ");
  Serial.println(data);

  if (strcmp(data, "ON") == 0) {
    digitalWrite(LED_LIGHT, HIGH);
  } else {
    digitalWrite(LED_LIGHT, LOW);
  }
}

void acCallback(char *data, uint16_t len) {
  Serial.print("AC: ");
  Serial.println(data);

  if (strcmp(data, "ON") == 0) {
    digitalWrite(LED_AC, HIGH);
  } else {
    digitalWrite(LED_AC, LOW);
  }
}

void alarmCallback(char *data, uint16_t len) {
  Serial.print("ALARM: ");
  Serial.println(data);

  if (strcmp(data, "ON") == 0) {
    tone(ALARM, 200);
  } else {
    tone(ALARM, 0);
  }
}

/************** MQTT CONNECT **************/
void MQTT_connect() {
  if (mqtt.connected()) {
    return;
  }

  int8_t ret;

  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    mqtt.disconnect();
    delay(5000);
  }

  Serial.println("MQTT connected!");

  delay(500);

  mqtt.subscribe(&lightFeed);
  mqtt.subscribe(&acFeed);
  mqtt.subscribe(&alarmFeed);
}