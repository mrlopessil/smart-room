#include "config.h"
#include <WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

extern Adafruit_MQTT_Client mqtt;

extern Adafruit_MQTT_Subscribe lightFeed;

extern Adafruit_MQTT_Subscribe acFeed;

extern Adafruit_MQTT_Subscribe alarmFeed;

void lightCallback(char *data, uint16_t len);

void acCallback(char *data, uint16_t len);

void alarmCallback(char *data, uint16_t len);

void MQTT_connect();

