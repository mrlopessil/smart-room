from Adafruit_IO import MQTTClient
from python.config import AIO_USERNAME, AIO_KEY, FEED_LIGHT, FEED_AC, FEED_INTRUDER, FEED_LAST_PERSON, FEED_ALARM

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.connect()
client.loop_background()

def last_seen(stream):
    client.publish(FEED_LAST_PERSON, stream)

def invader(stream):
    client.publish(FEED_INTRUDER, stream)

def alarm_on():
    client.publish(FEED_ALARM, "ON")

def ac_on():
    client.publish(FEED_AC, "ON")

def light_on():
    client.publish(FEED_LIGHT, "ON")

def alarm_off():
    client.publish(FEED_ALARM, "OFF")

def ac_off():
    client.publish(FEED_AC, "OFF")

def light_off():
    client.publish(FEED_LIGHT, "OFF")
